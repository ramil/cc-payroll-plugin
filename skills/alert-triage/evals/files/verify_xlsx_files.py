#!/usr/bin/env python3
"""
Comprehensive XLSX file verification script.
Checks structure, data ranges, and field validity across payroll test files.
"""

import pandas as pd
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class XLSXVerifier:
    def __init__(self):
        self.results = {}
        self.overall_status = True

    def verify_file(self, file_path: str, checks: Dict) -> bool:
        """Verify a single XLSX file with specified checks."""
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"\n✗ FAIL: {file_path.name} - FILE NOT FOUND")
            self.results[file_path.name] = {"status": "FAIL", "reason": "File not found"}
            self.overall_status = False
            return False

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            print(f"\n✗ FAIL: {file_path.name} - Cannot read file: {e}")
            self.results[file_path.name] = {"status": "FAIL", "reason": f"Read error: {e}"}
            self.overall_status = False
            return False

        print(f"\n{'='*70}")
        print(f"File: {file_path.name}")
        print(f"{'='*70}")
        print(f"Rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")

        file_status = True
        failed_checks = []

        # Run each check
        for check_name, check_func in checks.items():
            try:
                result, message = check_func(df)
                status_icon = "✓" if result else "✗"
                print(f"{status_icon} {check_name}: {message}")
                if not result:
                    file_status = False
                    failed_checks.append(check_name)
            except Exception as e:
                print(f"✗ {check_name}: ERROR - {e}")
                file_status = False
                failed_checks.append(f"{check_name} (error)")

        # Summary for this file
        status_str = "PASS" if file_status else "FAIL"
        print(f"\nResult: {status_str}")
        self.results[file_path.name] = {
            "status": status_str,
            "failed_checks": failed_checks if failed_checks else "None"
        }

        if not file_status:
            self.overall_status = False

        return file_status

    # ============ COMMON CHECKS ============
    @staticmethod
    def check_rows(expected_min: int = 1):
        """Check minimum number of rows."""
        def check(df):
            if len(df) >= expected_min:
                return True, f"{len(df)} rows found (>= {expected_min})"
            return False, f"Only {len(df)} rows found, expected >= {expected_min}"
        return check

    @staticmethod
    def check_column_exists(column_name: str):
        """Check if a column exists."""
        def check(df):
            if column_name in df.columns:
                return True, f"Column '{column_name}' exists"
            return False, f"Column '{column_name}' missing"
        return check

    @staticmethod
    def check_columns_exist(column_names: List[str]):
        """Check if multiple columns exist."""
        def check(df):
            missing = [col for col in column_names if col not in df.columns]
            if not missing:
                return True, f"All columns exist: {column_names}"
            return False, f"Missing columns: {missing}"
        return check

    @staticmethod
    def check_salary_range(column: str, min_val: float, max_val: float):
        """Check if salary values are within realistic range."""
        def check(df):
            if column not in df.columns:
                return False, f"Column '{column}' not found"
            valid_data = df[column].dropna()
            if len(valid_data) == 0:
                return False, f"Column '{column}' has no valid values"
            out_of_range = valid_data[(valid_data < min_val) | (valid_data > max_val)]
            if len(out_of_range) == 0:
                return True, f"All {len(valid_data)} values in range ${min_val:,.0f}-${max_val:,.0f}"
            return False, f"{len(out_of_range)} values out of range. Min: ${valid_data.min():,.0f}, Max: ${valid_data.max():,.0f}"
        return check

    @staticmethod
    def check_no_negative_values(column: str):
        """Check that a column has no negative values."""
        def check(df):
            if column not in df.columns:
                return False, f"Column '{column}' not found"
            valid_data = df[column].dropna()
            negatives = valid_data[valid_data < 0]
            if len(negatives) == 0:
                return True, f"No negative values in '{column}'"
            return False, f"{len(negatives)} negative values found in '{column}'"
        return check

    @staticmethod
    def check_column_values_include(column: str, required_values: List):
        """Check that column includes all required values."""
        def check(df):
            if column not in df.columns:
                return False, f"Column '{column}' not found"
            unique_vals = df[column].unique()
            missing = [v for v in required_values if v not in unique_vals]
            if not missing:
                return True, f"Column '{column}' includes all values {required_values}"
            return False, f"Column '{column}' missing values: {missing}. Has: {list(unique_vals)[:5]}"
        return check

    @staticmethod
    def check_column_values_in_set(column: str, valid_values: set):
        """Check that all values in column are in the valid set."""
        def check(df):
            if column not in df.columns:
                return False, f"Column '{column}' not found"
            unique_vals = set(df[column].dropna().unique())
            invalid = unique_vals - valid_values
            if not invalid:
                return True, f"All values in '{column}' are valid: {valid_values}"
            return False, f"Invalid values in '{column}': {invalid}"
        return check

    @staticmethod
    def check_specific_row_value(ee_id_col: str, ee_id: str, col_name: str, expected_value):
        """Check a specific row's column value."""
        def check(df):
            if ee_id_col not in df.columns:
                return False, f"Column '{ee_id_col}' not found"
            if col_name not in df.columns:
                return False, f"Column '{col_name}' not found"
            row = df[df[ee_id_col] == ee_id]
            if len(row) == 0:
                return False, f"No record found with {ee_id_col}='{ee_id}'"
            actual_value = row[col_name].iloc[0]
            if actual_value == expected_value:
                return True, f"Record {ee_id} has {col_name}={expected_value}"
            return False, f"Record {ee_id} has {col_name}={actual_value}, expected {expected_value}"
        return check

    @staticmethod
    def check_alert_count_and_statuses(total_expected: int = 50):
        """Check alert file has correct count and status distribution (5-column format)."""
        def check(df):
            if len(df) != total_expected:
                return False, f"Expected {total_expected} alerts, found {len(df)}"

            # Check for Status column
            if 'Status' not in df.columns:
                return False, "Column 'Status' not found"

            # Check for Validation Rule column
            if 'Validation Rule' not in df.columns:
                return False, "Column 'Validation Rule' not found"

            status_counts = df['Status'].value_counts()
            valid_statuses = {"Open", "Solution Applied", "Resolved", "Forwarded"}
            actual_statuses = set(df['Status'].dropna().unique())
            invalid = actual_statuses - valid_statuses

            if invalid:
                return False, f"Invalid statuses found: {invalid}"

            # Check that we have a mix of statuses
            has_open = 'Open' in status_counts
            has_other = len(status_counts) > 1

            if has_open and has_other:
                msg = f"{total_expected} alerts with status distribution: "
                msg += ", ".join([f"{k}={v}" for k, v in status_counts.items()])
                return True, msg
            return False, f"Incomplete status distribution: {dict(status_counts)}"
        return check

    def print_summary(self):
        """Print final summary."""
        print(f"\n{'='*70}")
        print("VERIFICATION SUMMARY")
        print(f"{'='*70}")

        passed = sum(1 for r in self.results.values() if r["status"] == "PASS")
        failed = sum(1 for r in self.results.values() if r["status"] == "FAIL")

        for filename, result in self.results.items():
            status_icon = "✓" if result["status"] == "PASS" else "✗"
            print(f"{status_icon} {filename}: {result['status']}")
            if result['status'] == 'FAIL' and result['failed_checks'] != "None":
                print(f"  Failed checks: {result['failed_checks']}")

        print(f"\nTotal: {passed} PASS, {failed} FAIL")
        print(f"Overall Status: {'PASS' if self.overall_status else 'FAIL'}")
        print(f"{'='*70}\n")

        return self.overall_status


def main():
    verifier = XLSXVerifier()

    # Define verification checks for each file
    files_to_check = {
        "/sessions/intelligent-affectionate-mayer/mnt/cc-payroll-plugin/1.0.0/skills/compliance-audit/evals/files/payroll_data.xlsx": {
            "Row count": verifier.check_rows(5),
            "Has Employee_ID": verifier.check_column_exists("Employee_ID"),
            "Has Monthly_Salary": verifier.check_column_exists("Monthly_Salary"),
            "Has Gross_Pay": verifier.check_column_exists("Gross_Pay"),
            "Has EE_Status": verifier.check_column_exists("EE_Status"),
            "Monthly_Salary in range": verifier.check_salary_range("Monthly_Salary", 3000, 18000),
            "No negative Gross_Pay": verifier.check_no_negative_values("Gross_Pay"),
            "EE_Status has values 0 and 3": verifier.check_column_values_include("EE_Status", [0, 3]),
        },

        "/sessions/intelligent-affectionate-mayer/mnt/cc-payroll-plugin/1.0.0/skills/variance-analyzer/evals/files/payroll_current.xlsx": {
            "Row count": verifier.check_rows(5),
            "Has Employee_ID": verifier.check_column_exists("Employee_ID"),
            "Has Amount": verifier.check_column_exists("Amount"),
            "Has EE_Status": verifier.check_column_exists("EE_Status"),
            "Amount includes realistic wage entries": verifier.check_salary_range("Amount", 0, 8000),
        },

        "/sessions/intelligent-affectionate-mayer/mnt/cc-payroll-plugin/1.0.0/skills/retro-processing/evals/files/current_results.xlsx": {
            "Row count": verifier.check_rows(5),
            "Has Employee_ID": verifier.check_column_exists("Employee_ID"),
            "Has EE_Status": verifier.check_column_exists("EE_Status"),
            "Employee_ID values found": verifier.check_rows(10),
        },

        "/sessions/intelligent-affectionate-mayer/mnt/cc-payroll-plugin/1.0.0/skills/gl-reconciliation/evals/files/payroll_results.xlsx": {
            "Row count": verifier.check_rows(5),
            "Has Amount": verifier.check_column_exists("Amount"),
            "Has Employee_ID": verifier.check_column_exists("Employee_ID"),
            "Amounts are reasonable": verifier.check_salary_range("Amount", -1000, 10000),
        },

        "/sessions/intelligent-affectionate-mayer/mnt/cc-payroll-plugin/1.0.0/skills/payroll-reporting/evals/files/payroll_summary.xlsx": {
            "Row count": verifier.check_rows(5),
            "Has Employee_ID": verifier.check_column_exists("Employee_ID"),
            "Has EE_Status": verifier.check_column_exists("EE_Status"),
            "Has Pay_Area": verifier.check_column_exists("Pay_Area"),
            "Pay_Area uses valid codes": verifier.check_column_values_in_set("Pay_Area", {"US01", "US02", "US03"}),
        },

        "/sessions/intelligent-affectionate-mayer/mnt/cc-payroll-plugin/1.0.0/skills/alert-triage/evals/files/pcc_alerts_export.xlsx": {
            "Has 50 alerts with valid statuses": verifier.check_alert_count_and_statuses(50),
            "Has Validation Rule column": verifier.check_column_exists("Validation Rule"),
            "Has Employee Name column": verifier.check_column_exists("Employee Name"),
            "Has Personnel Number column": verifier.check_column_exists("Personnel Number"),
            "Has Status column": verifier.check_column_exists("Status"),
        },
    }

    # Run verifications
    for file_path, checks in files_to_check.items():
        verifier.verify_file(file_path, checks)

    # Print summary
    overall_pass = verifier.print_summary()

    # Exit with appropriate code
    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
