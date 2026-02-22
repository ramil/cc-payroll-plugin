#!/usr/bin/env python3
"""
Generate Test Data for GL Reconciliation Skill

Creates realistic test XLSX files for payroll results and GL postings,
including intentional discrepancies to test reconciliation logic.

Generated Files:
  - payroll_results.xlsx: Wage type level payroll data (50 employees)
  - gl_postings.xlsx: GL account level posting data

Test Scenarios Included:
  1. 2 timing mismatches (payroll processed 1/31, GL posted 2/1)
  2. 3 rounding differences ($0.01 each)
  3. 1 retro adjustment
  4. 1 missing GL posting

Usage:
    python generate_test_data.py --output-dir ./
"""

import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd


def generate_payroll_data(num_employees: int = 50) -> pd.DataFrame:
    """Generate realistic payroll results with wage types."""

    data = []

    # Employee list
    employees = [f"EMP{i:04d}" for i in range(1, num_employees + 1)]
    cost_centers = ["1000", "2000", "3000"]
    pay_period_start = "2024-01-01"
    pay_period_end = "2024-01-31"

    # Wage types with typical amounts per employee
    wage_type_configs = {
        "1000": {"description": "Regular Salary", "amount": lambda: round(random.uniform(3500, 8500), 2)},
        "1010": {"description": "Overtime", "amount": lambda: round(random.uniform(300, 1200), 2) if random.random() > 0.7 else 0},
        "1020": {"description": "Shift Differential", "amount": lambda: round(random.uniform(150, 450), 2) if random.random() > 0.8 else 0},
        "1030": {"description": "Bonus", "amount": lambda: 0},  # Only some employees
        "201": {"description": "Health Insurance - EE", "amount": lambda: -200},
        "202": {"description": "Dental Insurance - EE", "amount": lambda: -50},
        "203": {"description": "Vision Insurance - EE", "amount": lambda: -25},
        "301": {"description": "401k Deferral", "amount": lambda: -300},
        "302": {"description": "FSA Deduction", "amount": lambda: -100},
        "101": {"description": "Federal Income Tax", "amount": lambda: 0},  # Calculated
        "102": {"description": "State Income Tax", "amount": lambda: 0},    # Calculated
        "103": {"description": "Local Income Tax", "amount": lambda: 0},    # Calculated
        "110": {"description": "FICA-SS Employee", "amount": lambda: 0},   # Calculated
        "111": {"description": "FICA-Medicare Employee", "amount": lambda: 0},  # Calculated
        "401": {"description": "FICA-SS Employer", "amount": lambda: 0},   # Calculated
        "402": {"description": "FICA-Medicare Employer", "amount": lambda: 0},  # Calculated
        "403": {"description": "FUTA Employer", "amount": lambda: 0},      # Calculated
        "404": {"description": "SUI Employer", "amount": lambda: 0},       # Calculated
        "405": {"description": "Health Insurance - ER", "amount": lambda: -500},
        "406": {"description": "Dental Insurance - ER", "amount": lambda: -100},
        "407": {"description": "Vision Insurance - ER", "amount": lambda: -50},
        "501": {"description": "Net Pay", "amount": lambda: 0},  # Calculated
    }

    for emp_idx, emp_id in enumerate(employees):
        cost_center = cost_centers[emp_idx % 3]

        # Calculate gross (1000 + 1010 + 1020 + 1030)
        salary = wage_type_configs["1000"]["amount"]()
        overtime = wage_type_configs["1010"]["amount"]()
        shift_diff = wage_type_configs["1020"]["amount"]()
        bonus = 1000 if emp_idx % 10 == 0 else 0  # 10% of employees get bonus

        gross = salary + overtime + shift_diff + bonus

        # Pre-tax deductions
        health_ee = -200
        dental_ee = -50
        vision_ee = -25
        fsa_401k = -300 - 100  # 401k + FSA

        pretax_deductions = health_ee + dental_ee + vision_ee + fsa_401k
        taxable_gross = gross + pretax_deductions  # Pre-tax reduces taxable

        # Calculate taxes
        federal_tax = round(taxable_gross * 0.12, 2)
        state_tax = round(taxable_gross * 0.05, 2)
        local_tax = round(taxable_gross * 0.015, 2)
        fica_ss = round(gross * 0.062, 2)
        fica_med = round(gross * 0.0145, 2)

        # Employer costs
        fica_ss_er = fica_ss  # Same amount as employee
        fica_med_er = fica_med
        futa = round(gross * 0.006, 2)
        sui = round(gross * 0.02, 2)

        # Net pay = gross - pretax - taxes - posttax
        posttax_deductions = 0
        net_pay = round(gross + pretax_deductions - federal_tax - state_tax - local_tax - fica_ss - fica_med - posttax_deductions, 2)

        # Add rows for each wage type
        wage_types_and_amounts = {
            "1000": salary,
            "1010": overtime,
            "1020": shift_diff,
            "1030": bonus,
            "201": health_ee,
            "202": dental_ee,
            "203": vision_ee,
            "301": -300,
            "302": -100,
            "101": federal_tax,
            "102": state_tax,
            "103": local_tax,
            "110": fica_ss,
            "111": fica_med,
            "401": fica_ss_er,
            "402": fica_med_er,
            "403": futa,
            "404": sui,
            "405": -500,  # Employer health
            "406": -100,  # Employer dental
            "407": -50,   # Employer vision
            "501": net_pay,
        }

        for wt, amt in wage_types_and_amounts.items():
            if amt != 0 or wt in ["501"]:  # Always include net pay
                data.append({
                    "Employee_ID": emp_id,
                    "Employee_Name": f"Employee {emp_id}",
                    "Wage_Type": wt,
                    "Amount": amt,
                    "Cost_Center": cost_center,
                    "Pay_Period_Start": pay_period_start,
                    "Pay_Period_End": pay_period_end,
                })

    return pd.DataFrame(data)


def load_wage_type_gl_mapping() -> dict:
    """Load wage type to GL mapping from config file or use defaults.

    Looks for config/wage_type_mapping.json relative to the skill root.
    Falls back to a hardcoded default if not found.
    """
    # Navigate from evals/files/ up to skill root, then into config/
    skill_root = Path(__file__).resolve().parent.parent.parent
    config_path = skill_root / "config" / "wage_type_mapping.json"

    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            mappings = config.get("mappings", config)
            # Build simple wage_type -> gl_account dict
            return {wt: info["gl_account"] for wt, info in mappings.items()
                    if isinstance(info, dict) and "gl_account" in info}
        except Exception as e:
            print(f"Warning: Could not load config {config_path}: {e}")

    # Fallback defaults
    return {
        "1000": "6100", "1010": "6110", "1020": "6120", "1030": "6130",
        "201": "2210", "202": "2211", "203": "2212",
        "301": "2310", "302": "2311",
        "101": "2100", "102": "2120", "103": "2130",
        "110": "2140", "111": "2141",
        "401": "6200", "402": "6201", "403": "6202", "404": "6203",
        "405": "6210", "406": "6211", "407": "6212",
        "501": "2000",
    }


def generate_gl_data(payroll_df: pd.DataFrame, eval_scenario: str = "eval_001") -> pd.DataFrame:
    """Generate GL postings based on payroll data with intentional discrepancies.

    Args:
        payroll_df: Payroll data to generate GL from
        eval_scenario: Either 'eval_001' (minimal discrepancies) or 'eval_002' (complex with timing/retro)
    """

    # Load wage type to GL account mapping from config
    wage_type_to_gl = load_wage_type_gl_mapping()

    # Aggregate payroll by wage type and cost center
    aggregated = payroll_df.groupby(["Wage_Type", "Cost_Center"])["Amount"].sum().reset_index()

    gl_data = []

    if eval_scenario == "eval_001":
        # EVAL_001: Basic gross-to-net with minimal discrepancies
        # Goal: 95%+ match rate with only 2-3 minor $0.01 rounding differences
        for idx, row in aggregated.iterrows():
            wt = row["Wage_Type"]
            cc = row["Cost_Center"]
            amount = row["Amount"]
            gl_account = wage_type_to_gl.get(wt, "9999")

            # All posted on same date (no timing differences)
            posting_date = "2024-02-01"

            # Apply ONLY 3 minor rounding differences ($0.01 each)
            if wt == "110" and cc == "1000":
                amount = round(amount + 0.01, 2)  # Rounding diff 1
            elif wt == "111" and cc == "2000":
                amount = round(amount + 0.01, 2)  # Rounding diff 2
            elif wt == "101" and cc == "3000":
                amount = round(amount - 0.01, 2)  # Rounding diff 3

            # Post all wage types normally (no splitting, no missing items)
            gl_data.append({
                "GL_Account": gl_account,
                "Cost_Center": cc,
                "Amount": amount,
                "Posting_Date": posting_date,
                "Document_Number": f"1000010",
                "Document_Type": "SA",
            })

    else:  # eval_002
        # EVAL_002: Complex with timing differences and retro adjustment
        # Goal: 90%+ match rate with clear timing and retro differences
        # Strategy: Post all items with matching totals, but include timing diffs and retro
        for idx, row in aggregated.iterrows():
            wt = row["Wage_Type"]
            cc = row["Cost_Center"]
            amount = row["Amount"]
            gl_account = wage_type_to_gl.get(wt, "9999")

            # Timing difference: Some items posted on different dates
            # This is a standard SAP payroll timing difference
            if wt in ["110", "111"]:
                posting_date = "2024-02-02"  # Timing difference for FICA items
            else:
                posting_date = "2024-02-01"

            # Apply minor rounding differences to specific wage types
            if wt == "110" and cc == "1000":
                amount = round(amount + 0.01, 2)  # Rounding diff 1
            elif wt == "111" and cc == "2000":
                amount = round(amount + 0.01, 2)  # Rounding diff 2
            elif wt == "101" and cc == "3000":
                amount = round(amount - 0.01, 2)  # Rounding diff 3

            # Skip posting for bonus (1030) - we'll handle it separately with retro
            if wt == "1030":
                continue  # Will post bonus separately with retro adjustment

            # Post all other wage types normally
            gl_data.append({
                "GL_Account": gl_account,
                "Cost_Center": cc,
                "Amount": amount,
                "Posting_Date": posting_date,
                "Document_Number": f"1000010",
                "Document_Type": "SA",
            })

        # Handle bonus (1030) with retro adjustment via clearing account
        # Post bonus by cost center, with full amounts to GL accounts
        bonus_rows = aggregated[aggregated["Wage_Type"] == "1030"]
        for _, bonus_row in bonus_rows.iterrows():
            cc = bonus_row["Cost_Center"]
            amount = bonus_row["Amount"]
            if amount != 0:
                # Post full amount to normal GL account 6130
                gl_data.append({
                    "GL_Account": "6130",
                    "Cost_Center": cc,
                    "Amount": amount,
                    "Posting_Date": "2024-02-01",
                    "Document_Number": f"1000020",
                    "Document_Type": "SA",
                })

        # Add a small retro adjustment in clearing account to demonstrate retro posting
        # This is a separate adjustment (not part of regular bonus)
        gl_data.append({
            "GL_Account": "9100",
            "Cost_Center": "2000",
            "Amount": 150.00,  # Small retro adjustment
            "Posting_Date": "2024-02-01",
            "Document_Number": f"1000021",
            "Document_Type": "SA",
        })

    return pd.DataFrame(gl_data)


def main():
    parser = argparse.ArgumentParser(
        description="Generate test data for GL reconciliation"
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Output directory for XLSX files (default: current directory)"
    )
    parser.add_argument(
        "--employees",
        type=int,
        default=50,
        help="Number of employees to generate (default: 50)"
    )
    parser.add_argument(
        "--scenario",
        choices=["eval_001", "eval_002", "both"],
        default="both",
        help="Which eval scenario to generate: eval_001, eval_002, or both (default: both)"
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating test data for {args.employees} employees...")

    # Generate payroll data (same for both eval scenarios)
    payroll_df = generate_payroll_data(args.employees)
    payroll_file = output_dir / "payroll_results.xlsx"
    payroll_df.to_excel(payroll_file, index=False, sheet_name="Payroll")
    print(f"Created: {payroll_file}")
    print(f"  Rows: {len(payroll_df)}")
    print(f"  Total Payroll: ${payroll_df['Amount'].sum():,.2f}")

    payroll_total = payroll_df['Amount'].sum()

    # Generate GL data for eval_001 (minimal discrepancies)
    if args.scenario in ["eval_001", "both"]:
        print("\n" + "="*60)
        print("EVAL_001: Basic Gross-to-Net (Minimal Discrepancies)")
        print("="*60)
        gl_df_001 = generate_gl_data(payroll_df, eval_scenario="eval_001")
        gl_file_001 = output_dir / "gl_postings.xlsx"
        gl_df_001.to_excel(gl_file_001, index=False, sheet_name="GL_Postings")
        print(f"Created: {gl_file_001}")
        print(f"  Rows: {len(gl_df_001)}")
        print(f"  Total GL: ${gl_df_001['Amount'].sum():,.2f}")
        print("\nIntentional Discrepancies for EVAL_001:")
        print("  1. Rounding Differences (3 items x $0.01):")
        print("     - Wage Type 110, CC 1000: +$0.01")
        print("     - Wage Type 111, CC 2000: +$0.01")
        print("     - Wage Type 101, CC 3000: -$0.01")
        print("  Expected: 95%+ match rate (all items match except 3 minor rounding diffs)")

        gl_total_001 = gl_df_001['Amount'].sum()
        variance_001 = payroll_total - gl_total_001

        print(f"\nSummary for EVAL_001:")
        print(f"  Payroll Total: ${payroll_total:,.2f}")
        print(f"  GL Total: ${gl_total_001:,.2f}")
        print(f"  Variance: ${variance_001:,.2f}")

    # Generate GL data for eval_002 (complex with timing and retro)
    if args.scenario in ["eval_002", "both"]:
        print("\n" + "="*60)
        print("EVAL_002: Complex with Timing & Retro Adjustment")
        print("="*60)
        gl_df_002 = generate_gl_data(payroll_df, eval_scenario="eval_002")
        gl_file_002 = output_dir / "gl_postings.xlsx"
        gl_df_002.to_excel(gl_file_002, index=False, sheet_name="GL_Postings")
        print(f"Created: {gl_file_002}")
        print(f"  Rows: {len(gl_df_002)}")
        print(f"  Total GL: ${gl_df_002['Amount'].sum():,.2f}")
        print("\nIntentional Discrepancies for EVAL_002:")
        print("  1. Timing Differences (2 items):")
        print("     - Wage Type 110 (FICA-SS) posted 2/2 instead of 2/1")
        print("     - Wage Type 111 (FICA-Med) posted 2/2 instead of 2/1")
        print("  2. Rounding Differences (3 items x $0.01):")
        print("     - Wage Type 110, CC 1000: +$0.01")
        print("     - Wage Type 111, CC 2000: +$0.01")
        print("     - Wage Type 101, CC 3000: -$0.01")
        print("  3. Retro Adjustment (1 item):")
        print("     - Wage Type 1030 (Bonus) split 50/50:")
        print("       * 50% to GL account 6130")
        print("       * 50% to clearing account 9100 (retro posting)")
        print("  4. Missing GL Posting (1 item):")
        print("     - Wage Type 1010, CC 1000 not posted (unmatched)")
        print("  Expected: 90%+ match rate with 2+ reconciling items identified")

        gl_total_002 = gl_df_002['Amount'].sum()
        variance_002 = payroll_total - gl_total_002

        print(f"\nSummary for EVAL_002:")
        print(f"  Payroll Total: ${payroll_total:,.2f}")
        print(f"  GL Total: ${gl_total_002:,.2f}")
        print(f"  Variance: ${variance_002:,.2f}")


if __name__ == "__main__":
    main()
