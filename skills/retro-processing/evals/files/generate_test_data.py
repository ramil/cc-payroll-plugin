#!/usr/bin/env python3
"""
Generate test data for retro-processing skill evaluation.

Creates current_results.xlsx and prior_results.xlsx with deliberate retro scenarios.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd


def generate_employee_data(emp_id: str, emp_name: str, cost_center: str, department: str,
                          payroll_area: str, is_current: bool, scenario: str = 'none', ee_status: int = 0) -> List[Dict[str, Any]]:
    """
    Generate wage type data for an employee.

    Args:
        emp_id: Employee ID
        emp_name: Employee name
        cost_center: Cost center code
        department: Department name
        payroll_area: Payroll area code
        is_current: If True, generate post-retro data; if False, generate pre-retro data
        scenario: Scenario type (none, salary_increase, org_reassignment, tax_correction,
                 benefit_change, terminated_with_retro, new_hire_retro)
        ee_status: Employee status (0=Active, 3=Withdrawn/Terminated)

    Returns:
        List of wage type records
    """
    records = []

    # Base salary
    if scenario == 'salary_increase' and is_current:
        base_salary = 5416.67  # 5% increase
    else:
        base_salary = 5000.00

    # Federal tax (approximately 12.5% of base)
    fed_tax = round(base_salary * 0.125, 2)

    # State tax (approximately 5% of base)
    state_tax = round(base_salary * 0.05, 2)

    # FICA (approximately 7.65% - employee portion)
    fica = round(base_salary * 0.0765, 2)

    # Health insurance deduction
    if scenario == 'benefit_change' and is_current:
        health_ins = 300.00  # Increased from 250
    else:
        health_ins = 250.00

    # Retirement deduction
    retirement = 200.00

    # Cost center allocation (for org_reassignment scenario)
    if scenario == 'org_reassignment' and is_current:
        cc = '5200'  # New cost center
    else:
        cc = cost_center

    # Wage types
    base_wt = [
        {'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Wage_Type': '/100',
         'Wage_Type_Description': 'Base Salary', 'Amount': base_salary,
         'Cost_Center': cc, 'Department': department, 'Payroll_Area': payroll_area, 'Period': '202401', 'EE_Status': ee_status},

        {'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Wage_Type': '/103',
         'Wage_Type_Description': 'Federal Tax Withheld', 'Amount': -fed_tax,
         'Cost_Center': cc, 'Department': department, 'Payroll_Area': payroll_area, 'Period': '202401', 'EE_Status': ee_status},

        {'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Wage_Type': '/104',
         'Wage_Type_Description': 'State Tax Withheld', 'Amount': -state_tax,
         'Cost_Center': cc, 'Department': department, 'Payroll_Area': payroll_area, 'Period': '202401', 'EE_Status': ee_status},

        {'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Wage_Type': '/105',
         'Wage_Type_Description': 'FICA Withheld', 'Amount': -fica,
         'Cost_Center': cc, 'Department': department, 'Payroll_Area': payroll_area, 'Period': '202401', 'EE_Status': ee_status},

        {'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Wage_Type': '/200',
         'Wage_Type_Description': 'Health Insurance Deduction', 'Amount': -health_ins,
         'Cost_Center': cc, 'Department': department, 'Payroll_Area': payroll_area, 'Period': '202401', 'EE_Status': ee_status},

        {'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Wage_Type': '/201',
         'Wage_Type_Description': 'Retirement Deduction', 'Amount': -retirement,
         'Cost_Center': cc, 'Department': department, 'Payroll_Area': payroll_area, 'Period': '202401', 'EE_Status': ee_status},
    ]

    # Add tax correction for tax_correction scenario
    if scenario == 'tax_correction' and is_current:
        # Increase federal tax due to filing status change
        additional_tax = round(base_salary * 0.05, 2)  # Additional 5%
        base_wt[1]['Amount'] = -fed_tax - additional_tax  # Update /103

    # Net pay (/560)
    gross = base_salary
    deductions = health_ins + retirement
    taxes = fed_tax + state_tax + fica
    net_pay = round(gross - deductions - taxes, 2)

    base_wt.append({
        'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Wage_Type': '/560',
        'Wage_Type_Description': 'Net Pay', 'Amount': net_pay,
        'Cost_Center': cc, 'Department': department, 'Payroll_Area': payroll_area, 'Period': '202401', 'EE_Status': ee_status
    })

    # Add /551 (retro difference) for current results if applicable
    if is_current and scenario in ['salary_increase', 'benefit_change', 'tax_correction']:
        retro_diff = round(base_salary - 5000, 2)
        if retro_diff != 0:
            base_wt.append({
                'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Wage_Type': '/551',
                'Wage_Type_Description': 'Retroactive Adjustment', 'Amount': retro_diff,
                'Cost_Center': cc, 'Department': department, 'Payroll_Area': payroll_area, 'Period': '202401', 'EE_Status': ee_status
            })

    return base_wt


def generate_test_data():
    """Generate test data files."""
    current_records = []
    prior_records = []

    # Scenario 1: 5 employees with salary increases
    for i in range(1, 6):
        emp_id = f'E{i:03d}'
        emp_name = f'Employee {i}'
        cc = '4100'
        dept = 'Engineering'
        pa = '01'

        prior_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, False, 'none'))
        current_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, True, 'salary_increase'))

    # Scenario 2: 3 employees with cost center reassignments
    for i in range(6, 9):
        emp_id = f'E{i:03d}'
        emp_name = f'Employee {i}'
        cc = '4200'
        dept = 'Sales'
        pa = '01'

        prior_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, False, 'none'))
        current_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, True, 'org_reassignment'))

    # Scenario 3: 2 employees with tax corrections
    for i in range(9, 11):
        emp_id = f'E{i:03d}'
        emp_name = f'Employee {i}'
        cc = '4300'
        dept = 'Finance'
        pa = '01'

        prior_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, False, 'none'))
        current_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, True, 'tax_correction'))

    # Scenario 4: 1 employee with benefit enrollment change
    emp_id = 'E011'
    emp_name = 'Employee 11'
    cc = '4100'
    dept = 'Engineering'
    pa = '01'
    prior_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, False, 'none'))
    current_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, True, 'benefit_change'))

    # Scenario 5: 1 terminated employee with final pay adjustment
    emp_id = 'E012'
    emp_name = 'Employee 12'
    cc = '4400'
    dept = 'HR'
    pa = '01'
    # Prior: Include records for terminated employee
    prior_recs = generate_employee_data(emp_id, emp_name, cc, dept, pa, False, 'none', ee_status=3)
    # Add vacation payout
    prior_recs.append({
        'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Wage_Type': '/110',
        'Wage_Type_Description': 'Vacation Payout', 'Amount': 3000.00,
        'Cost_Center': cc, 'Department': dept, 'Payroll_Area': pa, 'Period': '202401'
    })
    prior_records.extend(prior_recs)

    # Current: Retro adjustment to final pay
    current_recs = generate_employee_data(emp_id, emp_name, cc, dept, pa, True, 'none', ee_status=3)
    # Vacation payout with retro adjustment
    current_recs.append({
        'Employee_ID': emp_id, 'Employee_Name': emp_name, 'Wage_Type': '/110',
        'Wage_Type_Description': 'Vacation Payout', 'Amount': 3250.00,  # Increased due to retro
        'Cost_Center': cc, 'Department': dept, 'Payroll_Area': pa, 'Period': '202401'
    })
    current_records.extend(current_recs)

    # Scenario 6: 1 new hire with backdated start
    emp_id = 'E013'
    emp_name = 'Employee 13'
    cc = '4500'
    dept = 'Operations'
    pa = '01'
    # Prior: No records (new hire)
    # Current: Start date was backdated to Dec 2023
    current_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, True, 'none'))

    # Scenario 7: 37 employees with no retro changes
    for i in range(14, 51):
        emp_id = f'E{i:03d}'
        emp_name = f'Employee {i}'
        cc = f'41{(i % 10):02d}'  # Cycle through cost centers
        departments = ['Engineering', 'Sales', 'Finance', 'HR', 'Operations']
        dept = departments[i % len(departments)]
        pa = '01'

        prior_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, False, 'none'))
        current_records.extend(generate_employee_data(emp_id, emp_name, cc, dept, pa, True, 'none'))

    # Create DataFrames
    prior_df = pd.DataFrame(prior_records)
    current_df = pd.DataFrame(current_records)

    # Sort for consistency
    prior_df = prior_df.sort_values(['Employee_ID', 'Wage_Type']).reset_index(drop=True)
    current_df = current_df.sort_values(['Employee_ID', 'Wage_Type']).reset_index(drop=True)

    # Write to Excel
    output_dir = Path(__file__).parent

    prior_file = output_dir / 'prior_results.xlsx'
    current_file = output_dir / 'current_results.xlsx'

    print(f"Generating test data...")
    print(f"  Prior results: {len(prior_df)} rows")
    print(f"  Current results: {len(current_df)} rows")

    prior_df.to_excel(prior_file, index=False, sheet_name='Payroll Results')
    current_df.to_excel(current_file, index=False, sheet_name='Payroll Results')

    print(f"\nTest data files created:")
    print(f"  {prior_file}")
    print(f"  {current_file}")

    # Print summary
    print(f"\nTest scenarios:")
    print(f"  Salary increase (5 employees): E001-E005")
    print(f"  Org reassignment (3 employees): E006-E008")
    print(f"  Tax correction (2 employees): E009-E010")
    print(f"  Benefit change (1 employee): E011")
    print(f"  Terminated employee (1 employee): E012")
    print(f"  New hire retro (1 employee): E013")
    print(f"  No retro changes (37 employees): E014-E050")

    return 0


if __name__ == '__main__':
    sys.exit(generate_test_data())
