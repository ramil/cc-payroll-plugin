#!/usr/bin/env python3
"""
Payroll-to-GL Reconciliation Script

Reconciles SAP payroll results against GL postings, identifying matched items,
unmatched items, and reconciling items. Supports multiple reconciliation types:
gross-to-net, employer costs, tax liabilities, and cost center allocation.

Usage:
    python reconcile_payroll_gl.py payroll.xlsx gl.xlsx --recon-type all --tolerance 0.01
    python reconcile_payroll_gl.py payroll.xlsx gl.xlsx --recon-type gross_to_net --output recon.json
    python reconcile_payroll_gl.py payroll.xlsx gl.xlsx --wage-type-config /path/to/mapping.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import pandas as pd


# Default US Payroll Wage Type to GL Account Mapping
# Used as fallback when no config file is found
DEFAULT_WAGE_TYPE_GL_MAPPING = {
    # Gross Salary/Wages
    "1000": {"description": "Regular Salary", "gl_account": "6100", "category": "gross", "type": "income"},
    "1010": {"description": "Overtime", "gl_account": "6110", "category": "gross", "type": "income"},
    "1020": {"description": "Shift Differential", "gl_account": "6120", "category": "gross", "type": "income"},
    "1030": {"description": "Bonus", "gl_account": "6130", "category": "gross", "type": "income"},

    # Pre-Tax Deductions
    "201": {"description": "Health Insurance - Employee", "gl_account": "2210", "category": "deduction_pretax", "type": "liability"},
    "202": {"description": "Dental Insurance - Employee", "gl_account": "2211", "category": "deduction_pretax", "type": "liability"},
    "203": {"description": "Vision Insurance - Employee", "gl_account": "2212", "category": "deduction_pretax", "type": "liability"},
    "301": {"description": "401k Deferral", "gl_account": "2310", "category": "deduction_pretax", "type": "liability"},
    "302": {"description": "FSA Deduction", "gl_account": "2311", "category": "deduction_pretax", "type": "liability"},
    "303": {"description": "HSA Deduction", "gl_account": "2312", "category": "deduction_pretax", "type": "liability"},

    # Taxes Withheld
    "101": {"description": "Federal Income Tax Withholding", "gl_account": "2100", "category": "tax_withholding", "type": "liability"},
    "102": {"description": "State Income Tax Withholding", "gl_account": "2120", "category": "tax_withholding", "type": "liability"},
    "103": {"description": "Local Income Tax Withholding", "gl_account": "2130", "category": "tax_withholding", "type": "liability"},
    "110": {"description": "FICA-SS Employee Withholding", "gl_account": "2140", "category": "tax_withholding", "type": "liability"},
    "111": {"description": "FICA-Medicare Employee Withholding", "gl_account": "2141", "category": "tax_withholding", "type": "liability"},

    # Employer Taxes & Benefits
    "401": {"description": "FICA-SS Employer", "gl_account": "6200", "category": "employer_tax", "type": "expense"},
    "402": {"description": "FICA-Medicare Employer", "gl_account": "6201", "category": "employer_tax", "type": "expense"},
    "403": {"description": "FUTA Employer", "gl_account": "6202", "category": "employer_tax", "type": "expense"},
    "404": {"description": "SUI Employer", "gl_account": "6203", "category": "employer_tax", "type": "expense"},
    "405": {"description": "Health Insurance - Employer", "gl_account": "6210", "category": "benefit_cost", "type": "expense"},
    "406": {"description": "Dental Insurance - Employer", "gl_account": "6211", "category": "benefit_cost", "type": "expense"},
    "407": {"description": "Vision Insurance - Employer", "gl_account": "6212", "category": "benefit_cost", "type": "expense"},

    # Net Pay
    "501": {"description": "Net Pay", "gl_account": "2000", "category": "net_pay", "type": "liability"},
}


def load_wage_type_mapping(config_path: Optional[str] = None) -> Dict:
    """
    Load wage type to GL account mapping from config file or embedded defaults.

    Resolution order:
      1. Explicit config_path (from --wage-type-config CLI argument)
      2. config/wage_type_mapping.json relative to the skill root
      3. Embedded DEFAULT_WAGE_TYPE_GL_MAPPING

    Args:
        config_path: Optional explicit path to a JSON config file

    Returns:
        Dictionary mapping wage type codes to GL account info
    """
    # 1. Try explicit path from CLI argument
    if config_path:
        p = Path(config_path)
        if not p.exists():
            print(f"Error: Config file not found: {config_path}", file=sys.stderr)
            sys.exit(1)
        return _load_config_file(p)

    # 2. Try default config location (config/ relative to skill root)
    #    Script is in scripts/, config is in config/ (sibling directory)
    skill_root = Path(__file__).resolve().parent.parent
    default_config = skill_root / "config" / "wage_type_mapping.json"
    if default_config.exists():
        return _load_config_file(default_config)

    # 3. Fall back to embedded defaults
    print("  Mapping source: embedded defaults (no config file found)")
    return DEFAULT_WAGE_TYPE_GL_MAPPING.copy()


def _load_config_file(config_path: Path) -> Dict:
    """Load and validate a wage type mapping config file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid JSON in {config_path}: {e}", file=sys.stderr)
        print("  Falling back to embedded defaults", file=sys.stderr)
        return DEFAULT_WAGE_TYPE_GL_MAPPING.copy()
    except Exception as e:
        print(f"Warning: Could not read {config_path}: {e}", file=sys.stderr)
        print("  Falling back to embedded defaults", file=sys.stderr)
        return DEFAULT_WAGE_TYPE_GL_MAPPING.copy()

    # Extract mappings (support both flat dict and nested {"mappings": {...}} format)
    if "mappings" in config:
        mappings = config["mappings"]
    else:
        # Filter out _meta keys and treat the rest as mappings
        mappings = {k: v for k, v in config.items() if not k.startswith("_")}

    # Validate entries
    valid_categories = {"gross", "deduction_pretax", "deduction_posttax", "tax_withholding",
                        "employer_tax", "benefit_cost", "net_pay"}
    valid_types = {"income", "expense", "liability"}
    required_fields = {"description", "gl_account", "category", "type"}

    warnings = []
    for wt, info in mappings.items():
        if not isinstance(info, dict):
            warnings.append(f"  Wage type {wt}: expected dict, got {type(info).__name__}")
            continue
        missing = required_fields - set(info.keys())
        if missing:
            warnings.append(f"  Wage type {wt}: missing fields: {', '.join(missing)}")
        if info.get("category") and info["category"] not in valid_categories:
            warnings.append(f"  Wage type {wt}: unknown category '{info['category']}'")
        if info.get("type") and info["type"] not in valid_types:
            warnings.append(f"  Wage type {wt}: unknown type '{info['type']}'")

    if warnings:
        print(f"Mapping validation warnings ({config_path}):", file=sys.stderr)
        for w in warnings:
            print(w, file=sys.stderr)

    print(f"  Mapping source: {config_path} ({len(mappings)} wage types)")
    return mappings


def find_column(df: pd.DataFrame, possible_names: List[str], data_type: str = "unknown") -> Optional[str]:
    """
    Find a column in dataframe by matching against possible column names.
    Case-insensitive, handles variations in spacing and underscores.

    Args:
        df: pandas DataFrame to search
        possible_names: List of possible column names to match
        data_type: Description of what we're looking for (for error messages)

    Returns:
        Column name if found, None otherwise
    """
    df_cols = [col.strip().lower().replace(" ", "_").replace("-", "_") for col in df.columns]

    for possible in possible_names:
        normalized = possible.lower().replace(" ", "_").replace("-", "_")
        if normalized in df_cols:
            original_col = df.columns[df_cols.index(normalized)]
            return original_col

    return None


def load_and_validate_data(payroll_path: str, gl_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load and validate payroll and GL data files."""
    try:
        payroll_df = pd.read_excel(payroll_path)
        gl_df = pd.read_excel(gl_path)
    except Exception as e:
        print(f"Error loading Excel files: {e}", file=sys.stderr)
        sys.exit(1)

    if payroll_df.empty:
        print("Error: Payroll file is empty", file=sys.stderr)
        sys.exit(1)

    if gl_df.empty:
        print("Error: GL file is empty", file=sys.stderr)
        sys.exit(1)

    return payroll_df, gl_df


def extract_payroll_data(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Extract and normalize payroll data by wage type.
    Returns dictionary keyed by wage type with aggregated amounts.
    """
    wage_type_col = find_column(df, ["wage_type", "WT", "wage type", "wt_code"])
    amount_col = find_column(df, ["amount", "amt", "value", "gross", "total"])
    cost_center_col = find_column(df, ["cost_center", "KOSTL", "cost centre", "cc"])
    emp_col = find_column(df, ["employee_id", "emp_id", "personnel_no", "employee"])

    if not wage_type_col or not amount_col:
        print("Error: Could not find wage type or amount columns", file=sys.stderr)
        sys.exit(1)

    # Normalize data
    result = {
        "by_wage_type": {},
        "by_employee": {},
        "raw": df.copy()
    }

    for idx, row in df.iterrows():
        wt = str(row[wage_type_col]).strip()
        amt = float(row[amount_col]) if pd.notna(row[amount_col]) else 0.0
        cc = str(row[cost_center_col]).strip() if cost_center_col and pd.notna(row[cost_center_col]) else "UNKNOWN"
        emp = str(row[emp_col]).strip() if emp_col and pd.notna(row[emp_col]) else "UNKNOWN"

        # Aggregate by wage type
        if wt not in result["by_wage_type"]:
            result["by_wage_type"][wt] = {
                "total": 0.0,
                "by_cost_center": {},
                "count": 0,
                "details": []
            }

        result["by_wage_type"][wt]["total"] += amt
        result["by_wage_type"][wt]["count"] += 1
        result["by_wage_type"][wt]["details"].append({
            "employee": emp,
            "amount": amt,
            "cost_center": cc
        })

        if cc not in result["by_wage_type"][wt]["by_cost_center"]:
            result["by_wage_type"][wt]["by_cost_center"][cc] = 0.0
        result["by_wage_type"][wt]["by_cost_center"][cc] += amt

        # Aggregate by employee
        if emp not in result["by_employee"]:
            result["by_employee"][emp] = {
                "total": 0.0,
                "wage_types": {}
            }
        result["by_employee"][emp]["total"] += amt
        if wt not in result["by_employee"][emp]["wage_types"]:
            result["by_employee"][emp]["wage_types"][wt] = 0.0
        result["by_employee"][emp]["wage_types"][wt] += amt

    return result


def extract_gl_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Extract and normalize GL data by account and cost center.
    """
    gl_account_col = find_column(df, ["gl_account", "account", "acct", "account_number"])
    amount_col = find_column(df, ["amount", "amt", "value", "debit", "credit"])
    cost_center_col = find_column(df, ["cost_center", "KOSTL", "cost centre", "cc"])
    posting_date_col = find_column(df, ["posting_date", "posting date", "BUDAT", "date"])
    doc_col = find_column(df, ["document", "document_no", "doc_no", "doc_number"])

    if not gl_account_col or not amount_col:
        print("Error: Could not find GL account or amount columns", file=sys.stderr)
        sys.exit(1)

    result = {
        "by_account": {},
        "by_cost_center": {},
        "raw": df.copy()
    }

    for idx, row in df.iterrows():
        account = str(row[gl_account_col]).strip()
        amt = float(row[amount_col]) if pd.notna(row[amount_col]) else 0.0
        cc = str(row[cost_center_col]).strip() if cost_center_col and pd.notna(row[cost_center_col]) else "UNKNOWN"
        posting_date = str(row[posting_date_col]) if posting_date_col and pd.notna(row[posting_date_col]) else "UNKNOWN"
        doc = str(row[doc_col]).strip() if doc_col and pd.notna(row[doc_col]) else "UNKNOWN"

        # Aggregate by GL account
        if account not in result["by_account"]:
            result["by_account"][account] = {
                "total": 0.0,
                "by_cost_center": {},
                "count": 0,
                "details": []
            }

        result["by_account"][account]["total"] += amt
        result["by_account"][account]["count"] += 1
        result["by_account"][account]["details"].append({
            "amount": amt,
            "cost_center": cc,
            "posting_date": posting_date,
            "document": doc
        })

        if cc not in result["by_account"][account]["by_cost_center"]:
            result["by_account"][account]["by_cost_center"][cc] = 0.0
        result["by_account"][account]["by_cost_center"][cc] += amt

        # Aggregate by cost center
        if cc not in result["by_cost_center"]:
            result["by_cost_center"][cc] = {
                "total": 0.0,
                "by_account": {}
            }
        result["by_cost_center"][cc]["total"] += amt
        if account not in result["by_cost_center"][cc]["by_account"]:
            result["by_cost_center"][cc]["by_account"][account] = 0.0
        result["by_cost_center"][cc]["by_account"][account] += amt

    return result


def reconcile_gross_to_net(payroll_data: Dict, gl_data: Dict, tolerance: float,
                           wage_type_mapping: Dict = None) -> Dict[str, Any]:
    """
    Reconcile gross-to-net calculation.
    Validates: Gross - Deductions = Net Pay in GL
    """
    if wage_type_mapping is None:
        wage_type_mapping = DEFAULT_WAGE_TYPE_GL_MAPPING
    result = {
        "matched": [],
        "unmatched": [],
        "reconciling_items": [],
        "walkdown": {
            "total_gross": 0.0,
            "total_deductions": 0.0,
            "total_net": 0.0,
            "gl_net_pay": 0.0
        }
    }

    payroll_by_wt = payroll_data["by_wage_type"]

    # Calculate totals from payroll
    gross_wts = ["1000", "1010", "1020", "1030"]
    result["walkdown"]["total_gross"] = sum(
        payroll_by_wt.get(wt, {}).get("total", 0.0) for wt in gross_wts
    )

    deduction_wts = list(set(payroll_by_wt.keys()) - set(gross_wts) - set(["501"]))
    result["walkdown"]["total_deductions"] = sum(
        payroll_by_wt.get(wt, {}).get("total", 0.0) for wt in deduction_wts
    )

    if "501" in payroll_by_wt:
        result["walkdown"]["total_net"] = payroll_by_wt["501"]["total"]
    else:
        result["walkdown"]["total_net"] = result["walkdown"]["total_gross"] - result["walkdown"]["total_deductions"]

    # Get GL net pay posting
    gl_by_account = gl_data["by_account"]
    net_pay_gl_account = "2000"
    if net_pay_gl_account in gl_by_account:
        result["walkdown"]["gl_net_pay"] = gl_by_account[net_pay_gl_account]["total"]

    # Check if they match
    variance = abs(result["walkdown"]["total_net"] - result["walkdown"]["gl_net_pay"])
    if variance <= tolerance:
        result["matched"].append({
            "type": "net_pay",
            "payroll_amount": result["walkdown"]["total_net"],
            "gl_amount": result["walkdown"]["gl_net_pay"],
            "variance": variance,
            "gl_account": net_pay_gl_account
        })
    else:
        result["unmatched"].append({
            "type": "net_pay",
            "payroll_amount": result["walkdown"]["total_net"],
            "gl_amount": result["walkdown"]["gl_net_pay"],
            "variance": variance,
            "reason": "Net pay variance exceeds tolerance"
        })

    # Check individual gross components
    for wt in gross_wts:
        if wt in payroll_by_wt:
            wt_info = wage_type_mapping.get(wt, {})
            gl_account = wt_info.get("gl_account")
            payroll_amt = payroll_by_wt[wt]["total"]

            if gl_account and gl_account in gl_by_account:
                gl_amt = gl_by_account[gl_account]["total"]
                variance = abs(payroll_amt - gl_amt)

                if variance <= tolerance:
                    result["matched"].append({
                        "wage_type": wt,
                        "description": wt_info.get("description", ""),
                        "payroll_amount": payroll_amt,
                        "gl_account": gl_account,
                        "gl_amount": gl_amt,
                        "variance": variance
                    })
                else:
                    result["unmatched"].append({
                        "source": "payroll",
                        "wage_type": wt,
                        "description": wt_info.get("description", ""),
                        "payroll_amount": payroll_amt,
                        "gl_account": gl_account,
                        "gl_amount": gl_amt,
                        "variance": variance
                    })

    return result


def reconcile_employer_costs(payroll_data: Dict, gl_data: Dict, tolerance: float,
                            wage_type_mapping: Dict = None) -> Dict[str, Any]:
    """Reconcile employer-paid costs and taxes."""
    if wage_type_mapping is None:
        wage_type_mapping = DEFAULT_WAGE_TYPE_GL_MAPPING
    result = {
        "matched": [],
        "unmatched": [],
        "reconciling_items": [],
        "by_cost_type": {}
    }

    payroll_by_wt = payroll_data["by_wage_type"]
    gl_by_account = gl_data["by_account"]

    employer_cost_wts = {
        "401": "FICA-SS",
        "402": "FICA-Med",
        "403": "FUTA",
        "404": "SUI",
        "405": "Health Ins",
        "406": "Dental Ins",
        "407": "Vision Ins"
    }

    for wt, cost_type in employer_cost_wts.items():
        if wt not in payroll_by_wt:
            continue

        wt_info = wage_type_mapping.get(wt, {})
        gl_account = wt_info.get("gl_account")
        payroll_amt = payroll_by_wt[wt]["total"]

        result["by_cost_type"][cost_type] = {
            "payroll_amount": payroll_amt,
            "gl_account": gl_account,
            "gl_amount": 0.0,
            "variance": 0.0,
            "matched": False
        }

        if gl_account and gl_account in gl_by_account:
            gl_amt = gl_by_account[gl_account]["total"]
            variance = abs(payroll_amt - gl_amt)
            result["by_cost_type"][cost_type]["gl_amount"] = gl_amt
            result["by_cost_type"][cost_type]["variance"] = variance

            if variance <= tolerance:
                result["matched"].append({
                    "wage_type": wt,
                    "cost_type": cost_type,
                    "payroll_amount": payroll_amt,
                    "gl_account": gl_account,
                    "gl_amount": gl_amt,
                    "variance": variance
                })
                result["by_cost_type"][cost_type]["matched"] = True
            else:
                result["unmatched"].append({
                    "wage_type": wt,
                    "cost_type": cost_type,
                    "payroll_amount": payroll_amt,
                    "gl_account": gl_account,
                    "gl_amount": gl_amt,
                    "variance": variance
                })

    return result


def reconcile_tax_liabilities(payroll_data: Dict, gl_data: Dict, tolerance: float) -> Dict[str, Any]:
    """Reconcile tax withholding liabilities."""
    result = {
        "matched": [],
        "unmatched": [],
        "reconciling_items": [],
        "by_jurisdiction": {}
    }

    payroll_by_wt = payroll_data["by_wage_type"]
    gl_by_account = gl_data["by_account"]

    tax_withholding_map = {
        "101": ("Federal", "2100"),
        "102": ("State", "2120"),
        "103": ("Local", "2130"),
        "110": ("FICA-SS", "2140"),
        "111": ("FICA-Med", "2141")
    }

    for wt, (jurisdiction, gl_account) in tax_withholding_map.items():
        if wt not in payroll_by_wt:
            continue

        payroll_amt = payroll_by_wt[wt]["total"]

        result["by_jurisdiction"][jurisdiction] = {
            "wage_type": wt,
            "payroll_amount": payroll_amt,
            "gl_account": gl_account,
            "gl_amount": 0.0,
            "variance": 0.0,
            "matched": False
        }

        if gl_account in gl_by_account:
            gl_amt = gl_by_account[gl_account]["total"]
            variance = abs(payroll_amt - gl_amt)
            result["by_jurisdiction"][jurisdiction]["gl_amount"] = gl_amt
            result["by_jurisdiction"][jurisdiction]["variance"] = variance

            if variance <= tolerance:
                result["matched"].append({
                    "wage_type": wt,
                    "jurisdiction": jurisdiction,
                    "payroll_amount": payroll_amt,
                    "gl_account": gl_account,
                    "gl_amount": gl_amt,
                    "variance": variance
                })
                result["by_jurisdiction"][jurisdiction]["matched"] = True
            else:
                result["unmatched"].append({
                    "wage_type": wt,
                    "jurisdiction": jurisdiction,
                    "payroll_amount": payroll_amt,
                    "gl_account": gl_account,
                    "gl_amount": gl_amt,
                    "variance": variance
                })

    return result


def reconcile_cost_center_allocation(payroll_data: Dict, gl_data: Dict, tolerance: float) -> Dict[str, Any]:
    """Reconcile payroll allocation by cost center to GL cost center postings."""
    result = {
        "matched": [],
        "unmatched": [],
        "reconciling_items": [],
        "by_cost_center": {}
    }

    payroll_by_cc = {}
    for wt, wt_data in payroll_data["by_wage_type"].items():
        for cc, amt in wt_data.get("by_cost_center", {}).items():
            if cc not in payroll_by_cc:
                payroll_by_cc[cc] = 0.0
            payroll_by_cc[cc] += amt

    gl_by_cc = gl_data.get("by_cost_center", {})

    all_cost_centers = set(list(payroll_by_cc.keys()) + list(gl_by_cc.keys()))

    for cc in all_cost_centers:
        payroll_amt = payroll_by_cc.get(cc, 0.0)
        gl_amt = gl_by_cc.get(cc, {}).get("total", 0.0)
        variance = abs(payroll_amt - gl_amt)

        result["by_cost_center"][cc] = {
            "payroll_amount": payroll_amt,
            "gl_amount": gl_amt,
            "variance": variance,
            "matched": variance <= tolerance
        }

        if variance <= tolerance:
            result["matched"].append({
                "cost_center": cc,
                "payroll_amount": payroll_amt,
                "gl_amount": gl_amt,
                "variance": variance
            })
        else:
            result["unmatched"].append({
                "cost_center": cc,
                "payroll_amount": payroll_amt,
                "gl_amount": gl_amt,
                "variance": variance
            })

    return result


def identify_reconciling_items(payroll_data: Dict, gl_data: Dict,
                               wage_type_mapping: Dict = None) -> List[Dict[str, Any]]:
    """
    Identify and classify reconciling items.
    Checks for: timing differences, rounding, retro adjustments, etc.
    """
    if wage_type_mapping is None:
        wage_type_mapping = DEFAULT_WAGE_TYPE_GL_MAPPING
    reconciling_items = []

    # Check for timing differences (posting dates don't match payroll period)
    gl_details = []
    for account, account_data in gl_data["by_account"].items():
        for detail in account_data.get("details", []):
            gl_details.append(detail)

    if gl_details:
        posting_dates = [d.get("posting_date", "UNKNOWN") for d in gl_details]
        posting_dates = list(set(posting_dates))

        if len(posting_dates) > 1:
            reconciling_items.append({
                "type": "timing",
                "description": f"Multiple GL posting dates detected: {', '.join(posting_dates)}",
                "resolution_steps": [
                    "Verify GL posting date configuration",
                    "Check payroll period vs GL period cutoff rules",
                    "Identify which postings belong to next period"
                ]
            })

    # Check for rounding differences
    payroll_by_wt = payroll_data["by_wage_type"]
    gl_by_account = gl_data["by_account"]

    rounding_diffs = []
    for wt, wt_info in wage_type_mapping.items():
        if wt in payroll_by_wt and wt_info.get("gl_account") in gl_by_account:
            payroll_amt = payroll_by_wt[wt]["total"]
            gl_amt = gl_by_account[wt_info.get("gl_account")]["total"]
            variance = abs(payroll_amt - gl_amt)

            if 0 < variance < 0.01:
                rounding_diffs.append({
                    "wage_type": wt,
                    "variance": variance
                })

    if rounding_diffs:
        reconciling_items.append({
            "type": "rounding",
            "description": f"Rounding differences identified in {len(rounding_diffs)} accounts (all < $0.01)",
            "affected_items": rounding_diffs,
            "resolution_steps": [
                "Verify aggregation level (employee vs GL posting)",
                "Check if GL consolidation rules apply",
                "Acceptable if total < $0.01"
            ]
        })

    return reconciling_items


def main():
    parser = argparse.ArgumentParser(
        description="Reconcile SAP payroll results to GL postings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python reconcile_payroll_gl.py payroll.xlsx gl.xlsx --recon-type all
  python reconcile_payroll_gl.py payroll.xlsx gl.xlsx --recon-type gross_to_net --tolerance 0.01
  python reconcile_payroll_gl.py payroll.xlsx gl.xlsx --output recon_results.json
        """
    )

    parser.add_argument("payroll_file", help="Path to payroll results XLSX file")
    parser.add_argument("gl_file", help="Path to GL postings XLSX file")
    parser.add_argument(
        "--recon-type",
        choices=["all", "gross_to_net", "employer_costs", "tax_liabilities", "cost_center_allocation"],
        default="all",
        help="Reconciliation type(s) to perform (default: all)"
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.01,
        help="Variance tolerance for matching (default: 0.01)"
    )
    parser.add_argument(
        "--output",
        default="reconciliation_results.json",
        help="Output JSON file (default: reconciliation_results.json)"
    )
    parser.add_argument(
        "--wage-type-config",
        default=None,
        help="Path to wage type GL mapping JSON config file (default: uses config/wage_type_mapping.json or embedded defaults)"
    )

    args = parser.parse_args()

    # Load wage type mapping
    print("Loading wage type mapping...")
    wage_type_mapping = load_wage_type_mapping(args.wage_type_config)

    # Load data
    payroll_df, gl_df = load_and_validate_data(args.payroll_file, args.gl_file)

    # Extract data
    payroll_data = extract_payroll_data(payroll_df)
    gl_data = extract_gl_data(gl_df)

    # Perform reconciliations
    reconciliation_results = {}

    if args.recon_type in ["all", "gross_to_net"]:
        reconciliation_results["gross_to_net"] = reconcile_gross_to_net(
            payroll_data, gl_data, args.tolerance, wage_type_mapping)

    if args.recon_type in ["all", "employer_costs"]:
        reconciliation_results["employer_costs"] = reconcile_employer_costs(
            payroll_data, gl_data, args.tolerance, wage_type_mapping)

    if args.recon_type in ["all", "tax_liabilities"]:
        reconciliation_results["tax_liabilities"] = reconcile_tax_liabilities(payroll_data, gl_data, args.tolerance)

    if args.recon_type in ["all", "cost_center_allocation"]:
        reconciliation_results["cost_center_allocation"] = reconcile_cost_center_allocation(payroll_data, gl_data, args.tolerance)

    # Identify reconciling items
    reconciling_items = identify_reconciling_items(payroll_data, gl_data, wage_type_mapping)

    # Aggregate summary
    total_payroll = payroll_data["by_wage_type"].values()
    total_payroll_amount = sum(wt["total"] for wt in total_payroll)

    total_gl_amount = sum(account["total"] for account in gl_data["by_account"].values())

    total_matched = sum(
        len(results.get("matched", []))
        for results in reconciliation_results.values()
    )
    total_unmatched = sum(
        len(results.get("unmatched", []))
        for results in reconciliation_results.values()
    )

    match_rate = (total_matched / (total_matched + total_unmatched) * 100) if (total_matched + total_unmatched) > 0 else 0

    output = {
        "reconciliation_summary": {
            "total_payroll_amount": round(total_payroll_amount, 2),
            "total_gl_amount": round(total_gl_amount, 2),
            "total_variance": round(abs(total_payroll_amount - total_gl_amount), 2),
            "matched_count": total_matched,
            "unmatched_count": total_unmatched,
            "reconciling_items_count": len(reconciling_items),
            "match_rate_percent": round(match_rate, 1)
        },
        "reconciliation_results": reconciliation_results,
        "reconciling_items": reconciling_items
    }

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Reconciliation complete. Results written to {output_path}")
    print(f"Match Rate: {match_rate:.1f}%")
    print(f"Total Variance: ${abs(total_payroll_amount - total_gl_amount):.2f}")


if __name__ == "__main__":
    main()
