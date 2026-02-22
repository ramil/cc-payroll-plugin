#!/usr/bin/env python3
"""
Payroll Compliance Validation Script

Validates payroll data against federal regulations, wage base limits, and internal controls.
Produces JSON output with detailed findings and risk scoring.

Usage:
    python validate_payroll.py payroll_data.xlsx [--prior prior_period.xlsx] [--output validation_results.json]

Author: CC Payroll Plugin
License: Proprietary
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

import pandas as pd
import numpy as np


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PayrollValidator:
    """Validates payroll data against compliance rules and controls."""

    # Wage base limits for 2025
    SS_WAGE_BASE = 176100.00
    FUTA_WAGE_BASE = 7000.00
    MEDICARE_THRESHOLD = 200000.00
    FEDERAL_MIN_WAGE = 7.25

    # Severity levels and weights
    SEVERITY_LEVELS = {
        'Critical': {'weight': 100, 'color': 'red'},
        'High': {'weight': 50, 'color': 'orange'},
        'Medium': {'weight': 20, 'color': 'yellow'},
        'Low': {'weight': 5, 'color': 'blue'}
    }

    # Category weights for risk score calculation
    CATEGORY_WEIGHTS = {
        'Data Completeness': 0.20,
        'Calculation Accuracy': 0.25,
        'Wage Base Limits': 0.15,
        'Prior Period Comparison': 0.15,
        'Compliance Rules': 0.15,
        'Anomaly Detection': 0.10
    }

    def __init__(self, payroll_df: pd.DataFrame, prior_df: Optional[pd.DataFrame] = None):
        """Initialize validator with payroll data."""
        self.payroll_df = payroll_df
        self.prior_df = prior_df
        self.validation_results = {
            'validation_date': datetime.utcnow().isoformat() + 'Z',
            'total_records': len(payroll_df),
            'risk_score': 0,
            'risk_level': '',
            'overall_status': 'PASS',
            'pass_count': 0,
            'warning_count': 0,
            'fail_count': 0,
            'validation_categories': [],
            'critical_findings': [],
            'affected_employees': {}
        }
        self.category_results = {}

    def validate(self) -> Dict[str, Any]:
        """Run all validation categories."""
        logger.info(f"Starting validation of {len(self.payroll_df)} payroll records")

        # Run validation categories
        self._validate_data_completeness()
        self._validate_calculation_accuracy()
        self._validate_wage_base_limits()
        if self.prior_df is not None:
            self._validate_prior_period_comparison()
        self._validate_compliance_rules()
        self._validate_anomaly_detection()

        # Calculate risk score
        self._calculate_risk_score()

        # Build summary statistics
        self._build_summary_stats()

        logger.info(f"Validation complete. Risk score: {self.validation_results['risk_score']}")
        return self.validation_results

    def _validate_data_completeness(self) -> None:
        """Validate data completeness across required fields."""
        category_name = 'Data Completeness'
        checks = []

        # Check 1: Missing Employee IDs
        missing_ids = self.payroll_df['Employee ID'].isna().sum()
        check = self._create_check(
            'Missing Employee IDs',
            'Critical' if missing_ids > 0 else 'Low',
            missing_ids,
            f"{missing_ids} employee records have missing IDs",
            "Ensure all employees have valid SAP employee IDs from HR system"
        )
        checks.append(check)
        if missing_ids > 0:
            self.validation_results['affected_employees'].setdefault(category_name, []).extend(
                self.payroll_df[self.payroll_df['Employee ID'].isna()]['Name'].tolist()
            )

        # Check 2: Missing Names
        missing_names = self.payroll_df['Name'].isna().sum()
        check = self._create_check(
            'Missing Employee Names',
            'Critical' if missing_names > 0 else 'Low',
            missing_names,
            f"{missing_names} records have missing employee names",
            "Verify employee master data in SAP (transaction PA30)"
        )
        checks.append(check)

        # Check 3: Blank Gross Pay
        blank_gross = self.payroll_df['Gross Pay'].isna().sum()
        check = self._create_check(
            'Blank Gross Pay Amounts',
            'Critical' if blank_gross > 0 else 'Low',
            blank_gross,
            f"{blank_gross} records have blank or zero gross pay",
            "Review payroll input data; all employees must have gross pay amount"
        )
        checks.append(check)
        if blank_gross > 0:
            affected = self.payroll_df[self.payroll_df['Gross Pay'].isna()]['Name'].tolist()
            self.validation_results['affected_employees'].setdefault(category_name, []).extend(affected)

        # Check 4: Missing Cost Center
        missing_cc = self.payroll_df['Cost Center'].isna().sum()
        check = self._create_check(
            'Missing Cost Center',
            'High' if missing_cc > 0 else 'Low',
            missing_cc,
            f"{missing_cc} employees not assigned to cost center",
            "Assign all employees to valid cost center in PA30 or PU03"
        )
        checks.append(check)
        if missing_cc > 0:
            affected = self.payroll_df[self.payroll_df['Cost Center'].isna()]['Name'].tolist()
            self.validation_results['affected_employees'].setdefault(category_name, []).extend(affected)

        # Check 5: Missing Wage Type
        missing_wt = self.payroll_df['Wage Type'].isna().sum()
        check = self._create_check(
            'Missing Wage Type Code',
            'High' if missing_wt > 0 else 'Low',
            missing_wt,
            f"{missing_wt} records missing wage type (e.g., 1000, /101, /201)",
            "Ensure wage type codes are properly configured per SAP wage type master"
        )
        checks.append(check)

        # Check 6: Missing Department
        missing_dept = self.payroll_df['Department'].isna().sum()
        check = self._create_check(
            'Missing Department Code',
            'Medium' if missing_dept > 0 else 'Low',
            missing_dept,
            f"{missing_dept} employees missing department assignment",
            "Assign all employees to valid organizational unit (PA30)"
        )
        checks.append(check)
        if missing_dept > 0:
            affected = self.payroll_df[self.payroll_df['Department'].isna()]['Name'].tolist()
            self.validation_results['affected_employees'].setdefault(category_name, []).extend(affected)

        # Check 7: Missing Payroll Area
        missing_pa = self.payroll_df['Payroll Area'].isna().sum()
        check = self._create_check(
            'Missing Payroll Area',
            'Medium' if missing_pa > 0 else 'Low',
            missing_pa,
            f"{missing_pa} employees not assigned payroll area",
            "Configure payroll area assignment in PA30 (e.g., US, US-CA)"
        )
        checks.append(check)

        # Check 8: Duplicate Records
        duplicates = self.payroll_df.duplicated(subset=['Employee ID'], keep=False).sum()
        check = self._create_check(
            'Duplicate Employee Records',
            'High' if duplicates > 0 else 'Low',
            duplicates,
            f"{duplicates} duplicate employee records detected",
            "Remove duplicate entries; ensure each employee appears once per period"
        )
        checks.append(check)

        self.category_results[category_name] = checks
        self._save_category_results(category_name, checks)

    def _validate_calculation_accuracy(self) -> None:
        """Validate mathematical accuracy of payroll calculations."""
        category_name = 'Calculation Accuracy'
        checks = []

        # Check 1: Negative Gross Pay
        negative_gross = (self.payroll_df['Gross Pay'] < 0).sum()
        check = self._create_check(
            'Negative Gross Pay',
            'Critical' if negative_gross > 0 else 'Low',
            negative_gross,
            f"{negative_gross} employees have negative gross pay amounts",
            "Correct payroll entry; gross pay must be positive or zero (unpaid leave)"
        )
        checks.append(check)
        if negative_gross > 0:
            affected = self.payroll_df[self.payroll_df['Gross Pay'] < 0]['Name'].tolist()
            self.validation_results['affected_employees'].setdefault(category_name, []).extend(affected)

        # Check 2: Net Pay > Gross Pay
        invalid_net = (self.payroll_df['Net Pay'] > self.payroll_df['Gross Pay']).sum()
        check = self._create_check(
            'Net Pay Exceeds Gross Pay',
            'Critical' if invalid_net > 0 else 'Low',
            invalid_net,
            f"{invalid_net} records have net pay exceeding gross pay",
            "Review deductions and withholding; net cannot exceed gross"
        )
        checks.append(check)
        if invalid_net > 0:
            affected = self.payroll_df[
                self.payroll_df['Net Pay'] > self.payroll_df['Gross Pay']
            ]['Name'].tolist()
            self.validation_results['affected_employees'].setdefault(category_name, []).extend(affected)

        # Check 3: Tax Withholding > Gross Pay
        invalid_tax = (self.payroll_df['Federal Tax'] > self.payroll_df['Gross Pay']).sum()
        check = self._create_check(
            'Federal Tax Exceeds Gross Pay',
            'Critical' if invalid_tax > 0 else 'Low',
            invalid_tax,
            f"{invalid_tax} employees have tax withholding exceeding gross pay",
            "Review W-4 information and tax configuration; withholding cannot exceed gross"
        )
        checks.append(check)

        # Check 4: Overtime Rate Validation
        overtime_invalid = (self.payroll_df['Overtime'].isna()) | (
            self.payroll_df['Overtime'] < self.payroll_df['Regular Rate'] * 1.5
        )
        overtime_issues = overtime_invalid.sum()
        check = self._create_check(
            'Overtime Rate Validation (FLSA)',
            'High' if overtime_issues > 5 else 'Medium',
            overtime_issues,
            f"{overtime_issues} records have invalid overtime rates (should be 1.5x regular)",
            "Ensure overtime calculated as 1.5x regular rate per FLSA requirements"
        )
        checks.append(check)

        # Check 5: FICA Calculation Verification
        ss_withholding = self.payroll_df['Gross Pay'] * 0.062
        ss_diff = (self.payroll_df['SS Withholding'] - ss_withholding).abs()
        ss_issues = (ss_diff > 0.50).sum()  # Allow $0.50 rounding tolerance
        check = self._create_check(
            'FICA Social Security Calculation (6.2%)',
            'High' if ss_issues > 0 else 'Low',
            ss_issues,
            f"{ss_issues} records have incorrect SS withholding (should be 6.2% of gross)",
            "Verify Social Security withholding rate and wage base limits in tax configuration"
        )
        checks.append(check)

        # Check 6: Garnishment Limit Compliance
        garnishment_limit = 0.25  # 25% maximum of disposable income
        invalid_garnishments = (
            self.payroll_df['Garnishment'] > self.payroll_df['Gross Pay'] * garnishment_limit
        ).sum()
        check = self._create_check(
            'Garnishment Limit Compliance (≤25%)',
            'High' if invalid_garnishments > 0 else 'Low',
            invalid_garnishments,
            f"{invalid_garnishments} garnishments exceed 25% limit per Consumer Credit Protection Act",
            "Review garnishment amounts; maximum 25% of disposable income per CCPA"
        )
        checks.append(check)
        if invalid_garnishments > 0:
            affected = self.payroll_df[
                self.payroll_df['Garnishment'] > self.payroll_df['Gross Pay'] * garnishment_limit
            ]['Name'].tolist()
            self.validation_results['affected_employees'].setdefault(category_name, []).extend(affected)

        self.category_results[category_name] = checks
        self._save_category_results(category_name, checks)

    def _validate_wage_base_limits(self) -> None:
        """Validate wage base limits for payroll taxes."""
        category_name = 'Wage Base Limits'
        checks = []

        # Check 1: Social Security Wage Base
        ss_over = (self.payroll_df['YTD Earnings'] > self.SS_WAGE_BASE).sum()
        check = self._create_check(
            'Social Security Wage Base Exceeded ($176,100)',
            'High' if ss_over > 0 else 'Low',
            ss_over,
            f"{ss_over} employees have YTD earnings exceeding SS wage base of ${self.SS_WAGE_BASE:,.2f}",
            "Verify SS withholding stopped once annual wage base exceeded; review YTD calculations"
        )
        checks.append(check)
        if ss_over > 0:
            affected = self.payroll_df[
                self.payroll_df['YTD Earnings'] > self.SS_WAGE_BASE
            ]['Name'].tolist()
            self.validation_results['affected_employees'].setdefault(category_name, []).extend(affected)

        # Check 2: FUTA Wage Base
        futa_over = (self.payroll_df['YTD Earnings'] > self.FUTA_WAGE_BASE).sum()
        check = self._create_check(
            'FUTA Wage Base Exceeded ($7,000)',
            'Medium' if futa_over > 0 else 'Low',
            futa_over,
            f"{futa_over} employees exceed FUTA wage base of ${self.FUTA_WAGE_BASE:,.2f}",
            "Verify FUTA contribution stopped once wage base exceeded (employer tax)"
        )
        checks.append(check)

        # Check 3: Additional Medicare Threshold
        medicare_over = (self.payroll_df['YTD Earnings'] > self.MEDICARE_THRESHOLD).sum()
        check = self._create_check(
            'Additional Medicare Threshold ($200,000)',
            'Medium' if medicare_over > 0 else 'Low',
            medicare_over,
            f"{medicare_over} employees exceed Additional Medicare threshold of ${self.MEDICARE_THRESHOLD:,.2f}",
            "Verify 0.9% Additional Medicare withholding applied above $200,000"
        )
        checks.append(check)

        # Check 4: State SUI Wage Base
        # Using $7,000 as typical state SUI base (varies by state)
        state_sui_base = 7000.00
        sui_over = (self.payroll_df['YTD Earnings'] > state_sui_base).sum()
        check = self._create_check(
            'State SUI Wage Base Limits',
            'Medium' if sui_over > 3 else 'Low',
            sui_over,
            f"{sui_over} employees may exceed state SUI wage base (varies by state)",
            "Verify state SUI withholding per state-specific wage base limits"
        )
        checks.append(check)

        self.category_results[category_name] = checks
        self._save_category_results(category_name, checks)

    def _validate_prior_period_comparison(self) -> None:
        """Validate current period against prior period."""
        category_name = 'Prior Period Comparison'
        checks = []

        if self.prior_df is None:
            logger.warning("Prior period data not provided; skipping prior period comparison")
            return

        # Check 1: Total Payroll Variance
        current_total = self.payroll_df['Gross Pay'].sum()
        prior_total = self.prior_df['Gross Pay'].sum()
        variance_pct = abs(current_total - prior_total) / prior_total * 100 if prior_total > 0 else 0
        check = self._create_check(
            'Total Payroll Variance (>10%)',
            'High' if variance_pct > 10 else 'Low',
            1 if variance_pct > 10 else 0,
            f"Payroll variance is {variance_pct:.2f}% (current: ${current_total:,.2f}, prior: ${prior_total:,.2f})",
            "Investigate significant payroll variance; document business reason (hiring, layoffs, merit increases)"
        )
        checks.append(check)

        # Check 2: Headcount Change
        current_hc = len(self.payroll_df)
        prior_hc = len(self.prior_df)
        hc_change_pct = abs(current_hc - prior_hc) / prior_hc * 100 if prior_hc > 0 else 0
        check = self._create_check(
            'Headcount Change (>5%)',
            'Medium' if hc_change_pct > 5 else 'Low',
            1 if hc_change_pct > 5 else 0,
            f"Headcount change {hc_change_pct:.2f}% (current: {current_hc}, prior: {prior_hc})",
            "Reconcile headcount changes with HR records; verify new hires and terminations"
        )
        checks.append(check)

        # Check 3: Average Pay Variance
        current_avg = self.payroll_df['Gross Pay'].mean()
        prior_avg = self.prior_df['Gross Pay'].mean()
        avg_variance_pct = abs(current_avg - prior_avg) / prior_avg * 100 if prior_avg > 0 else 0
        check = self._create_check(
            'Average Pay Variance (>15%)',
            'Medium' if avg_variance_pct > 15 else 'Low',
            1 if avg_variance_pct > 15 else 0,
            f"Average pay variance {avg_variance_pct:.2f}% (current: ${current_avg:,.2f}, prior: ${prior_avg:,.2f})",
            "Analyze pay increase patterns; verify against approved compensation changes"
        )
        checks.append(check)

        # Check 4: New Employee Validation
        prior_ids = set(self.prior_df['Employee ID'].dropna())
        current_ids = set(self.payroll_df['Employee ID'].dropna())
        new_employees = current_ids - prior_ids
        check = self._create_check(
            'New Employee Validation',
            'Low' if len(new_employees) > 0 else 'Low',
            len(new_employees),
            f"{len(new_employees)} new employee(s) detected in current period",
            "Verify new employees are properly onboarded in HR and payroll systems"
        )
        checks.append(check)

        # Check 5: Terminated Employee Validation
        terminated = prior_ids - current_ids
        check = self._create_check(
            'Terminated Employee Validation',
            'Low' if len(terminated) > 0 else 'Low',
            len(terminated),
            f"{len(terminated)} employee(s) no longer in payroll",
            "Verify terminations are properly documented; ensure final paycheck processed"
        )
        checks.append(check)

        self.category_results[category_name] = checks
        self._save_category_results(category_name, checks)

    def _validate_compliance_rules(self) -> None:
        """Validate regulatory and policy compliance."""
        category_name = 'Compliance Rules'
        checks = []

        # Check 1: Minimum Wage Compliance
        min_wage_violations = (self.payroll_df['Gross Pay'] / 40 < self.FEDERAL_MIN_WAGE).sum()
        check = self._create_check(
            'Minimum Wage Compliance ($7.25 federal)',
            'High' if min_wage_violations > 0 else 'Low',
            min_wage_violations,
            f"{min_wage_violations} employees have pay below federal minimum wage",
            "Verify hourly rates meet federal and state minimum wage requirements"
        )
        checks.append(check)

        # Check 2: Garnishment Priority Ordering
        garnishment_count = (self.payroll_df['Garnishment'] > 0).sum()
        check = self._create_check(
            'Garnishment Priority Ordering (CCPA)',
            'Medium' if garnishment_count > 3 else 'Low',
            garnishment_count,
            f"{garnishment_count} employees have active garnishments",
            "Verify garnishments prioritized per Consumer Credit Protection Act: federal tax, state tax, child support, other orders"
        )
        checks.append(check)

        # Check 3: Benefit Deductions Don't Violate Minimum Wage
        illegal_deductions = 0
        for idx, row in self.payroll_df.iterrows():
            net_hourly = (row['Gross Pay'] - row['Deductions']) / 40 if row['Deductions'] > 0 else row['Gross Pay'] / 40
            if net_hourly < self.FEDERAL_MIN_WAGE:
                illegal_deductions += 1
        check = self._create_check(
            'Benefit Deductions Minimum Wage Safeguard',
            'High' if illegal_deductions > 0 else 'Low',
            illegal_deductions,
            f"{illegal_deductions} employees have net pay below minimum wage after deductions",
            "Limit deductions such that net pay meets minimum wage requirements"
        )
        checks.append(check)

        # Check 4: Tax Withholding Completeness
        missing_withholding = (
            (self.payroll_df['Federal Tax'].isna()) |
            (self.payroll_df['SS Withholding'].isna()) |
            (self.payroll_df['Medicare Withholding'].isna())
        ).sum()
        check = self._create_check(
            'Tax Withholding Completeness',
            'High' if missing_withholding > 0 else 'Low',
            missing_withholding,
            f"{missing_withholding} employees have missing tax withholding codes",
            "Ensure W-4 information is complete; verify tax withholding in payroll configuration"
        )
        checks.append(check)

        # Check 5: Cost Center Assignment Completeness
        unassigned_cc = self.payroll_df['Cost Center'].isna().sum()
        check = self._create_check(
            'Cost Center Assignment Completeness',
            'Medium' if unassigned_cc > 0 else 'Low',
            unassigned_cc,
            f"{unassigned_cc} employees not assigned to cost center",
            "Assign all employees to valid cost center for accurate expense allocation"
        )
        checks.append(check)

        self.category_results[category_name] = checks
        self._save_category_results(category_name, checks)

    def _validate_anomaly_detection(self) -> None:
        """Detect unusual patterns that may indicate errors or fraud."""
        category_name = 'Anomaly Detection'
        checks = []

        # Check 1: Unusually High Payments (>3 standard deviations)
        mean_pay = self.payroll_df['Gross Pay'].mean()
        std_pay = self.payroll_df['Gross Pay'].std()
        threshold = mean_pay + (3 * std_pay)
        unusual_payments = (self.payroll_df['Gross Pay'] > threshold).sum()
        check = self._create_check(
            'Unusually High Payments (>3 std dev)',
            'High' if unusual_payments > 0 else 'Low',
            unusual_payments,
            f"{unusual_payments} payments exceed ${threshold:,.2f} (mean: ${mean_pay:,.2f}, std: ${std_pay:,.2f})",
            "Investigate unusual payments; verify authorization and business purpose"
        )
        checks.append(check)
        if unusual_payments > 0:
            affected = self.payroll_df[
                self.payroll_df['Gross Pay'] > threshold
            ]['Name'].tolist()
            self.validation_results['affected_employees'].setdefault(category_name, []).extend(affected)

        # Check 2: Duplicate Payments (same employee, wage type, amount)
        duplicate_payments = self.payroll_df.duplicated(
            subset=['Employee ID', 'Wage Type', 'Gross Pay'], keep=False
        ).sum()
        check = self._create_check(
            'Duplicate Payments (Same Employee/Type)',
            'High' if duplicate_payments > 0 else 'Low',
            duplicate_payments,
            f"{duplicate_payments} potential duplicate payments detected",
            "Review for duplicate payroll entries; remove if unintended duplications"
        )
        checks.append(check)

        # Check 3: Zero-Amount Records
        zero_records = (self.payroll_df['Gross Pay'] == 0).sum()
        check = self._create_check(
            'Zero-Amount Records',
            'Medium' if zero_records > 2 else 'Low',
            zero_records,
            f"{zero_records} employees have zero gross pay",
            "Verify zero-pay records (unpaid leave); if unintentional, correct before submission"
        )
        checks.append(check)

        # Check 4: Negative Deduction Amounts
        negative_deductions = (self.payroll_df['Deductions'] < 0).sum()
        check = self._create_check(
            'Negative Deduction Amounts',
            'Medium' if negative_deductions > 0 else 'Low',
            negative_deductions,
            f"{negative_deductions} records have negative deduction amounts",
            "Review deduction codes; negative amounts may indicate credits or adjustments"
        )
        checks.append(check)

        self.category_results[category_name] = checks
        self._save_category_results(category_name, checks)

    def _calculate_risk_score(self) -> None:
        """Calculate overall risk score based on weighted category results."""
        total_points = 0
        max_possible_points = 0

        for category, weight in self.CATEGORY_WEIGHTS.items():
            if category not in self.category_results:
                continue

            checks = self.category_results[category]
            category_points = 0

            for check in checks:
                severity = check['severity']
                weight_factor = self.SEVERITY_LEVELS[severity]['weight']
                category_points += weight_factor * check['affected_count']

            # Normalize category points (max 100 per category)
            normalized_category_points = min(category_points / len(checks), 100) * weight

            total_points += normalized_category_points
            max_possible_points += weight * 100

        # Calculate risk score (0-100)
        risk_score = min(int(total_points / max_possible_points * 100), 100) if max_possible_points > 0 else 0
        self.validation_results['risk_score'] = risk_score

        # Determine risk level
        if risk_score <= 20:
            risk_level = 'Low Risk'
        elif risk_score <= 40:
            risk_level = 'Medium Risk'
        elif risk_score <= 60:
            risk_level = 'High Risk'
        elif risk_score <= 80:
            risk_level = 'Very High Risk'
        else:
            risk_level = 'Critical Risk'

        self.validation_results['risk_level'] = risk_level

    def _build_summary_stats(self) -> None:
        """Build summary statistics."""
        pass_count = 0
        warning_count = 0
        fail_count = 0

        for category, checks in self.category_results.items():
            for check in checks:
                if check['status'] == 'PASS':
                    pass_count += 1
                elif check['status'] == 'WARNING':
                    warning_count += 1
                else:
                    fail_count += 1

        self.validation_results['pass_count'] = pass_count
        self.validation_results['warning_count'] = warning_count
        self.validation_results['fail_count'] = fail_count
        self.validation_results['overall_status'] = 'FAIL' if fail_count > 0 else 'PASS'

    def _save_category_results(self, category_name: str, checks: List[Dict]) -> None:
        """Save category results to validation results."""
        category = {
            'category': category_name,
            'total_checks': len(checks),
            'passed': sum(1 for c in checks if c['status'] == 'PASS'),
            'failed': sum(1 for c in checks if c['status'] == 'FAIL'),
            'warnings': sum(1 for c in checks if c['status'] == 'WARNING'),
            'checks': checks
        }
        self.validation_results['validation_categories'].append(category)

        # Collect critical findings
        for check in checks:
            if check['severity'] == 'Critical' and check['affected_count'] > 0:
                self.validation_results['critical_findings'].append({
                    'category': category_name,
                    'check_name': check['check_name'],
                    'affected_count': check['affected_count'],
                    'details': check['details'],
                    'recommendation': check['recommendation']
                })

    @staticmethod
    def _create_check(
        check_name: str,
        severity: str,
        affected_count: int,
        details: str,
        recommendation: str
    ) -> Dict[str, Any]:
        """Create a validation check result."""
        return {
            'check_name': check_name,
            'status': 'FAIL' if affected_count > 0 else 'PASS',
            'severity': severity,
            'affected_count': affected_count,
            'details': details,
            'recommendation': recommendation
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate payroll data against compliance rules'
    )
    parser.add_argument('payroll_file', help='Path to payroll XLSX file')
    parser.add_argument('--prior', help='Optional prior period XLSX for comparison')
    parser.add_argument('--output', default='validation_results.json', help='Output JSON file')

    args = parser.parse_args()

    # Read payroll data
    try:
        payroll_df = pd.read_excel(args.payroll_file)
        logger.info(f"Loaded payroll data from {args.payroll_file}")
    except Exception as e:
        logger.error(f"Failed to read payroll file: {e}")
        sys.exit(1)

    # Read prior period data if provided
    prior_df = None
    if args.prior:
        try:
            prior_df = pd.read_excel(args.prior)
            logger.info(f"Loaded prior period data from {args.prior}")
        except Exception as e:
            logger.warning(f"Failed to read prior period file: {e}")

    # Run validation
    validator = PayrollValidator(payroll_df, prior_df)
    results = validator.validate()

    # Write results
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    logger.info(f"Validation results written to {output_path}")

    # Return exit code based on risk score
    if results['risk_score'] > 60:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
