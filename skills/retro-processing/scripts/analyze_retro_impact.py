#!/usr/bin/env python3
"""
Analyze retroactive payroll adjustment impact by comparing current and prior payroll results.

Identifies affected employees, calculates wage type changes, estimates GL impact, and assesses risk.
"""

import sys
import json
import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

import pandas as pd


# Standard column name variations for flexible matching
EMPLOYEE_ID_COLS = ['Employee_ID', 'EmpID', 'EMPID', 'EmployeeID', 'Emp_ID', 'ID']
EMPLOYEE_NAME_COLS = ['Employee_Name', 'EmpName', 'EMPNAME', 'EmployeeName', 'Emp_Name', 'Name']
WAGE_TYPE_COLS = ['Wage_Type', 'WageType', 'WAGETYPE', 'Wage_Code', 'Code']
WAGE_DESC_COLS = ['Wage_Type_Description', 'Description', 'WageTypeDescription', 'Desc']
AMOUNT_COLS = ['Amount', 'Value', 'Wage_Amount', 'Amt']
COST_CENTER_COLS = ['Cost_Center', 'CostCenter', 'COSTCENTER', 'Cost_Ctr', 'CC']
DEPARTMENT_COLS = ['Department', 'Dept', 'DEPT', 'Department_Name', 'Dept_Name']
PAYROLL_AREA_COLS = ['Payroll_Area', 'PA', 'PayrollArea', 'PAYAREA']
PERIOD_COLS = ['Period', 'PERIOD', 'Month', 'Payroll_Period']

# GL account mapping (simplified; actual mapping would be more complex)
GL_MAPPING = {
    '/100': ('4100', 'Base Salary'),
    '/101': ('4100', 'Salary Supplement'),
    '/102': ('4110', 'Hourly Wages'),
    '/103': ('2100', 'Federal Tax Withheld'),
    '/104': ('2110', 'State Tax Withheld'),
    '/105': ('2120', 'Local Tax Withheld'),
    '/200': ('2200', 'Health Insurance Deduction'),
    '/201': ('2210', 'Retirement Deduction'),
    '/551': ('5100', 'Retroactive Adjustment'),
    '/552': ('5110', 'Subsequent Adjustment'),
    '/553': ('5120', 'Retro Change from Last'),
    '/560': ('4200', 'Payment Amount'),
    '/562': ('5130', 'Retro Tax Adjustment'),
}


def find_column(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
    """Find column in DataFrame matching any of possible names (case-insensitive)."""
    df_cols_lower = {col.lower(): col for col in df.columns}
    for name in possible_names:
        if name.lower() in df_cols_lower:
            return df_cols_lower[name.lower()]
    return None


def normalize_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Normalize DataFrame column names to standard names. Returns normalized df and mapping."""
    mapping = {}

    # Map each column type
    col_types = [
        (EMPLOYEE_ID_COLS, 'Employee_ID'),
        (EMPLOYEE_NAME_COLS, 'Employee_Name'),
        (WAGE_TYPE_COLS, 'Wage_Type'),
        (WAGE_DESC_COLS, 'Wage_Type_Description'),
        (AMOUNT_COLS, 'Amount'),
        (COST_CENTER_COLS, 'Cost_Center'),
        (DEPARTMENT_COLS, 'Department'),
        (PAYROLL_AREA_COLS, 'Payroll_Area'),
        (PERIOD_COLS, 'Period'),
    ]

    rename_dict = {}
    for possible_names, standard_name in col_types:
        found_col = find_column(df, possible_names)
        if found_col:
            if found_col != standard_name:
                rename_dict[found_col] = standard_name
            mapping[standard_name] = found_col

    df_normalized = df.rename(columns=rename_dict)
    return df_normalized, mapping


def load_payroll_data(file_path: str) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Load and normalize payroll XLSX file."""
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading {file_path}: {e}")

    if df.empty:
        raise ValueError(f"File is empty: {file_path}")

    df_normalized, mapping = normalize_dataframe(df)

    # Ensure required columns exist
    if 'Employee_ID' not in df_normalized.columns:
        raise ValueError("Could not find Employee_ID column")
    if 'Wage_Type' not in df_normalized.columns:
        raise ValueError("Could not find Wage_Type column")
    if 'Amount' not in df_normalized.columns:
        raise ValueError("Could not find Amount column")

    return df_normalized, mapping


def classify_retro_type(wage_type_deltas: Dict[str, float]) -> str:
    """Classify retro type based on which wage types changed."""
    wage_types_changed = set(wage_type_deltas.keys())

    # Pay rate change: /100, /101, /102 affected
    if any(wt in wage_types_changed for wt in ['/100', '/101', '/102']):
        return 'Pay Rate Change'

    # Tax correction: /103, /104, /105, /562 affected
    if any(wt in wage_types_changed for wt in ['/103', '/104', '/105', '/562']):
        return 'Tax Correction'

    # Benefit change: /200 series affected
    if any(wt.startswith('/20') for wt in wage_types_changed):
        return 'Benefit Change'

    # Retro adjustments: /551, /552, /553 present
    if any(wt in wage_types_changed for wt in ['/551', '/552', '/553']):
        return 'System Adjustment'

    # Default to general adjustment
    return 'General Adjustment'


def assess_risk_level(retro_delta: float, threshold_low: float = 500.0,
                      threshold_medium: float = 2000.0, threshold_high: float = 5000.0) -> str:
    """Classify risk level based on retro amount."""
    abs_delta = abs(retro_delta)
    if abs_delta < threshold_low:
        return 'Low'
    elif abs_delta < threshold_medium:
        return 'Medium'
    elif abs_delta < threshold_high:
        return 'High'
    else:
        return 'Critical'


def detect_edge_cases(employee_id: str, current_emp: pd.DataFrame,
                      prior_emp: pd.DataFrame, wage_type_deltas: Dict[str, float]) -> List[str]:
    """Detect potential edge cases for employee."""
    edge_cases = []

    # Check for year boundary crossing
    if 'Period' in current_emp.columns and 'Period' in prior_emp.columns:
        current_periods = current_emp['Period'].unique()
        prior_periods = prior_emp['Period'].unique()
        if len(current_periods) > 0 and len(prior_periods) > 0:
            try:
                current_min = min(current_periods)
                current_max = max(current_periods)
                prior_min = min(prior_periods)
                prior_max = max(prior_periods)

                # Check if spanning calendar year
                if str(current_min)[:4] != str(current_max)[:4]:
                    edge_cases.append('Year-Boundary Crossing')
            except (ValueError, TypeError):
                pass

    # Check for missing wage types
    current_wts = set(current_emp['Wage_Type'].unique()) if not current_emp.empty else set()
    prior_wts = set(prior_emp['Wage_Type'].unique()) if not prior_emp.empty else set()
    missing_in_current = prior_wts - current_wts
    if missing_in_current:
        edge_cases.append(f'Missing wage types in current: {", ".join(sorted(missing_in_current))}')

    # Check for terminated employee indicator (no prior data after certain date)
    if len(prior_emp) == 0 and len(current_emp) > 0:
        edge_cases.append('No Prior Period Data (Possible New Hire Retro)')

    # High-value retro
    total_delta = sum(abs(v.get('delta', 0)) if isinstance(v, dict) else abs(v)
                     for v in wage_type_deltas.values())
    if total_delta > 5000:
        edge_cases.append('High-Value Retro (>$5000)')

    return edge_cases


def analyze_retro_impact(current_file: str, prior_file: str,
                         risk_thresholds: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """
    Analyze retroactive payroll impact.

    Args:
        current_file: XLSX file with post-retro payroll results
        prior_file: XLSX file with pre-retro payroll results
        risk_thresholds: Optional dict with keys 'low', 'medium', 'high' for risk levels

    Returns:
        Dictionary with impact analysis results
    """
    # Set default risk thresholds
    thresholds = {'low': 500.0, 'medium': 2000.0, 'high': 5000.0}
    if risk_thresholds:
        thresholds.update(risk_thresholds)

    # Load data
    print(f"Loading payroll data...")
    current_df, current_mapping = load_payroll_data(current_file)
    prior_df, prior_mapping = load_payroll_data(prior_file)

    print(f"Current: {len(current_df)} rows, Prior: {len(prior_df)} rows")

    # Group by employee
    current_by_emp = {emp_id: group for emp_id, group
                      in current_df.groupby('Employee_ID')}
    prior_by_emp = {emp_id: group for emp_id, group
                    in prior_df.groupby('Employee_ID')}

    affected_employees = []
    retro_by_type = defaultdict(int)
    retro_by_risk = defaultdict(int)
    retro_by_cost_center = defaultdict(float)
    retro_by_dept = defaultdict(float)
    total_retro_amount = 0.0
    gl_accounts_affected = set()
    edge_case_warnings = []

    # Process each employee
    all_employees = set(current_by_emp.keys()) | set(prior_by_emp.keys())
    print(f"Processing {len(all_employees)} unique employees...")

    for emp_id in sorted(all_employees):
        current_emp = current_by_emp.get(emp_id, pd.DataFrame())
        prior_emp = prior_by_emp.get(emp_id, pd.DataFrame())

        # Build wage type maps
        current_map = {}
        if not current_emp.empty:
            for _, row in current_emp.iterrows():
                wt = row['Wage_Type']
                current_map[wt] = current_map.get(wt, 0) + row['Amount']

        prior_map = {}
        if not prior_emp.empty:
            for _, row in prior_emp.iterrows():
                wt = row['Wage_Type']
                prior_map[wt] = prior_map.get(wt, 0) + row['Amount']

        # Calculate deltas
        all_wts = set(current_map.keys()) | set(prior_map.keys())
        wage_type_changes = {}
        total_delta = 0.0

        for wt in sorted(all_wts):
            current_amt = current_map.get(wt, 0.0)
            prior_amt = prior_map.get(wt, 0.0)
            delta = current_amt - prior_amt

            if abs(delta) > 0.01:  # Ignore rounding
                wage_type_changes[wt] = {
                    'prior': round(prior_amt, 2),
                    'current': round(current_amt, 2),
                    'delta': round(delta, 2)
                }
                total_delta += delta

                # Track GL accounts
                if wt in GL_MAPPING:
                    gl_accounts_affected.add(GL_MAPPING[wt][0])

        # Only include if there are changes
        if wage_type_changes:
            # Get employee name if available
            emp_name = 'Unknown'
            if not current_emp.empty and 'Employee_Name' in current_emp.columns:
                emp_name = current_emp['Employee_Name'].iloc[0]
            elif not prior_emp.empty and 'Employee_Name' in prior_emp.columns:
                emp_name = prior_emp['Employee_Name'].iloc[0]

            # Get cost center and department
            cost_center = 'Unknown'
            department = 'Unknown'
            if not current_emp.empty:
                if 'Cost_Center' in current_emp.columns:
                    cc = current_emp['Cost_Center'].iloc[0]
                    if pd.notna(cc):
                        cost_center = str(cc)
                if 'Department' in current_emp.columns:
                    dept = current_emp['Department'].iloc[0]
                    if pd.notna(dept):
                        department = str(dept)

            # Classify retro type
            retro_type = classify_retro_type(wage_type_changes)

            # Assess risk
            risk_level = assess_risk_level(total_delta, thresholds['low'],
                                          thresholds['medium'], thresholds['high'])

            # Detect edge cases
            edge_cases = detect_edge_cases(emp_id, current_emp, prior_emp, wage_type_changes)

            affected_employees.append({
                'employee_id': emp_id,
                'employee_name': emp_name,
                'total_retro_delta': round(total_delta, 2),
                'retro_type': retro_type,
                'risk_level': risk_level,
                'wage_type_changes': wage_type_changes,
                'cost_center': cost_center,
                'department': department,
                'edge_cases': edge_cases
            })

            # Aggregate
            retro_by_type[retro_type] += 1
            retro_by_risk[risk_level] += 1
            total_retro_amount += total_delta

            if cost_center != 'Unknown':
                retro_by_cost_center[cost_center] += total_delta
            if department != 'Unknown':
                retro_by_dept[department] += total_delta

            # Collect edge case warnings
            if edge_cases:
                edge_case_warnings.extend([
                    f"{emp_id}: {ec}" for ec in edge_cases
                ])

    # Build result
    result = {
        'affected_employees': affected_employees,
        'retro_summary': {
            'total_employees_affected': len(affected_employees),
            'total_retro_amount': round(total_retro_amount, 2),
            'by_retro_type': dict(retro_by_type),
            'by_risk_level': dict(retro_by_risk),
        },
        'gl_impact': {
            'estimated_accounts_affected': sorted(list(gl_accounts_affected)),
            'total_difference_amount': round(total_retro_amount, 2),
            'by_cost_center': {k: round(v, 2) for k, v in sorted(retro_by_cost_center.items())},
            'by_department': {k: round(v, 2) for k, v in sorted(retro_by_dept.items())},
        },
        'edge_case_warnings': sorted(list(set(edge_case_warnings)))
    }

    return result


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Analyze retroactive payroll adjustment impact'
    )
    parser.add_argument('current', help='XLSX file with post-retro payroll results')
    parser.add_argument('prior', help='XLSX file with pre-retro payroll results')
    parser.add_argument('--output', '-o', default='retro_analysis.json',
                       help='Output JSON file (default: retro_analysis.json)')
    parser.add_argument('--risk-low', type=float, default=500.0,
                       help='Risk threshold for Low level (default: 500)')
    parser.add_argument('--risk-medium', type=float, default=2000.0,
                       help='Risk threshold for Medium level (default: 2000)')
    parser.add_argument('--risk-high', type=float, default=5000.0,
                       help='Risk threshold for High level (default: 5000)')

    args = parser.parse_args()

    try:
        print(f"Analyzing retro impact: {args.current} vs {args.prior}")
        thresholds = {
            'low': args.risk_low,
            'medium': args.risk_medium,
            'high': args.risk_high
        }
        result = analyze_retro_impact(args.current, args.prior, thresholds)

        # Write output
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"\nAnalysis complete:")
        print(f"  Affected employees: {result['retro_summary']['total_employees_affected']}")
        print(f"  Total retro amount: ${result['retro_summary']['total_retro_amount']:,.2f}")
        print(f"  GL accounts affected: {len(result['gl_impact']['estimated_accounts_affected'])}")
        print(f"  Edge case warnings: {len(result['edge_case_warnings'])}")
        print(f"\nOutput written to: {output_path.resolve()}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
