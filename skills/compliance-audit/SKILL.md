---
name: compliance-audit
title: Compliance Audit Skill for SAP Payroll
version: 1.0.0
description: |
  Exploratory pre-submission review and SOX-related check support for payroll processing.
  Reviews data completeness, calculation accuracy, wage base limits, prior period comparisons,
  compliance rules, and generates analysis with indicative risk scoring for payroll review.
keywords:
  - payroll compliance
  - pre-submission validation
  - SOX compliance
  - audit trail generation
  - payroll audit
  - compliance check
  - pre-production checklist
  - wage base limit
  - tax validation
  - FLSA compliance
  - garnishment compliance
  - Form 941
  - W-2 reporting
  - ACA reporting
  - payroll risk assessment
  - internal controls
  - segregation of duties
author: SAP Payroll Team
license: Proprietary
---

# Compliance Audit Skill

## Overview

**PROOF-OF-CONCEPT**: This skill is an exploratory analysis aid and does not replace formal audit procedures, SOX controls, or professional compliance review. It should be used for reference purposes only.

The Compliance Audit skill provides exploratory pre-submission review for SAP Payroll data exports. It runs 30+ checks against federal regulations, wage base limits, and internal controls — working from XLSX exports without requiring SAP transaction access.

**What SAP already provides natively:**
- **PCC Validation Rules** (Manage Configuration app): Configurable rules that check payroll-relevant data and generate alerts during monitoring and production steps
- **SAP Hard Stops**: Schema-level checks that prevent payroll calculation when critical data is missing (IT0001, IT0008, IT0210, IT0009)
- **PCC Approval Workflows** (Manage Workflows app): Multi-level approval for payroll release
- **ICS Framework**: Dual control principle and basic audit trail in PCC

**What this skill adds:**
- **Exploratory post-calculation review** — SAP hard stops catch input errors *before* payroll runs; this skill reviews *results after* calculation (e.g., does the calculated FICA amount seem reasonable? Does net pay make sense? Are wage base limits respected?)
- Works from **XLSX exports** — no SAP access required (ideal for BPO quality assurance, external audit preparation, or independent control testing)
- **Indicative risk scoring (0-100)** with severity-weighted findings — SAP/PCC doesn't provide an aggregate indicative risk score
- **Review workbook** with 7 tabs including review checklist, compliance calendar, and affected employee lists — PCC doesn't generate this output format
- **Prior period comparison** highlighting potential headcount anomalies, payroll total shifts, and trend breaks — PCC validation rules check within a single period, not across periods
- **Statistical anomaly flagging** (3-sigma outliers, duplicate detection) — PCC validation rules are deterministic, not statistical

This skill assists payroll teams to:
- Review data completeness before processing
- Check calculation accuracy (gross pay, taxes, deductions)
- Flag potential wage base limit issues for Social Security, Medicare, FUTA, and state SUI
- Compare current period against prior periods to highlight potential anomalies
- Assess alignment with federal and state regulations
- Generate analysis for SOX and internal audit review purposes
- Assess indicative payroll risk on a 0-100 scale with suggested remediation guidance

## When to Use

Use this skill when:
- Preparing payroll for submission to bank/tax authorities
- Conducting pre-production validation before go-live
- Performing monthly or quarterly compliance reviews
- Responding to audit inquiries from external or internal auditors
- Investigating payroll discrepancies or exceptions
- Testing payroll system changes before deployment
- Validating payroll data from third-party processors
- Preparing for annual compliance certifications (SOX, internal controls)
- Analyzing trends or anomalies in payroll patterns

## Core Capabilities

### 1. Data Completeness Review
Checks for required fields before processing:
- Employee identification (employee ID, name)
- Wage information (gross pay, wage types)
- Organizational data (cost center, department, payroll area)
- Flags processing with incomplete or missing data

### 2. Calculation Accuracy Review
Checks mathematical correctness of payroll calculations:
- Gross pay calculation and reasonableness
- Net pay relationship to gross pay
- Tax withholding relationship to gross pay
- Overtime rate alignment with federal/state law
- FICA calculations (6.2% Social Security, 1.45% Medicare)
- Garnishment limit alignment (25% maximum of disposable income)

### 3. Wage Base Limit Review
Checks alignment with annual wage base limits:
- Social Security wage base: $176,100 (2025)
- FUTA wage base: $7,000
- Additional Medicare threshold: $200,000
- State-specific SUI wage base limits
- Flags potential over/under withholding of payroll taxes

### 4. Prior Period Comparison Analysis
Detects trends and anomalies:
- Total payroll variance analysis (>10% threshold)
- Headcount change detection (>5% threshold)
- Average pay variance tracking (>15% threshold)
- New employee validation
- Terminated employee validation
- Requires optional prior period XLSX for comparison

### 5. Compliance Rules Review
Checks alignment with regulatory and policy requirements:
- Minimum wage review ($7.25 federal, state minimums)
- Garnishment priority ordering per CCPA
- Benefit deductions relationship to minimum wage
- Tax withholding completeness
- Cost center assignment completeness
- Consistent wage type usage

### 6. Anomaly Flagging
Highlights unusual patterns that may indicate review areas:
- Unusually high payments (>3 standard deviations)
- Duplicate payments for same employee/wage type
- Zero-amount records for review
- Negative deduction amounts
- Outlier flagging for individual review

## Validation Categories

### Data Completeness (8 checks)
- Missing employee IDs
- Missing employee names
- Blank gross pay amounts
- Missing cost center assignments
- Missing wage type codes
- Missing department codes
- Missing payroll area codes
- Duplicate employee records (same employee, same period)

### Calculation Accuracy (6 checks)
- Negative gross pay detection
- Net pay exceeding gross pay
- Tax withholding exceeding gross pay
- Overtime rate validation (1.5x regular rate)
- FICA calculation verification (SS 6.2%, Medicare 1.45%)
- Garnishment limit compliance (≤25% of disposable income)

### Wage Base Limits (4 checks)
- Social Security wage base ceiling ($176,100 in 2025)
- FUTA wage base ceiling ($7,000)
- Additional Medicare threshold ($200,000 income)
- State SUI wage base limits (varies by state)

### Prior Period Comparison (5 checks)
- Total payroll variance >10%
- Headcount change >5%
- Average pay variance >15%
- New employee validation (employment date consistency)
- Terminated employee validation (separation date consistency)

### Compliance Rules (5 checks)
- Minimum wage compliance ($7.25 federal, state variations)
- Garnishment priority ordering per Consumer Credit Protection Act
- Benefit deduction minimum wage safeguard
- Tax withholding completeness (no missing withholding codes)
- Cost center assignment completeness (all employees assigned)

### Anomaly Detection (4 checks)
- Unusually high payments (>3 standard deviations)
- Duplicate payments (same employee, wage type, amount)
- Zero-amount records
- Negative deduction amounts

## Workflow

### Standard Validation Workflow

```
1. Prepare payroll data in XLSX format
   └─ Ensure columns: Employee ID, Name, Gross Pay, Wage Types, Cost Center, Department, Payroll Area

2. Run validate_payroll.py
   └─ python validate_payroll.py payroll_data.xlsx
   └─ Optionally include prior period: --prior prior_period.xlsx
   └─ Specify output: --output validation_results.json

3. Review validation_results.json
   └─ Check overall risk score (0-100)
   └─ Review all CRITICAL severity findings
   └─ Assess HIGH severity findings
   └─ Plan remediation for MEDIUM/LOW items

4. Run generate_audit_report.py
   └─ python generate_audit_report.py validation_results.json
   └─ Produces: audit_report.xlsx with 7 worksheets

5. Review audit_report.xlsx
   └─ Executive Summary: Overall risk assessment
   └─ Critical Findings: Items for review
   └─ All Checks Detail: Complete review results
   └─ Affected Employees: List of individuals with noted items
   └─ Prior Period Comparison: Trend analysis
   └─ Compliance Calendar: Upcoming deadlines
   └─ Review Checklist: Preparer/Reviewer/Approver documentation

6. Remediate findings
   └─ Correct data errors in source system
   └─ Document exceptions and approvals
   └─ Re-run validation to confirm fixes

7. Obtain sign-offs
   └─ Preparer (initial data entry)
   └─ Reviewer (first-level validation)
   └─ Approver (final authorization to process)

8. Submit payroll
```

## Risk Scoring Methodology

Indicative risk score ranges from 0-100:

- **0-20 (Low Risk)**: All checks pass, minimal issues, appears ready for processing
- **21-40 (Medium Risk)**: Some non-critical issues, recommended for review before processing
- **41-60 (High Risk)**: Multiple issues or critical findings, recommended for management review
- **61-80 (Very High Risk)**: Significant compliance or control issues, recommended for escalation
- **81-100 (Critical Risk)**: Severe violations or multiple critical findings, recommended for review before processing

### Score Calculation

Each validation category contributes to overall score:

| Category | Weight | Description |
|----------|--------|-------------|
| Data Completeness | 20% | Foundation for all downstream validation |
| Calculation Accuracy | 25% | Core payroll math accuracy |
| Wage Base Limits | 15% | Tax liability accuracy |
| Prior Period Comparison | 15% | Anomaly detection |
| Compliance Rules | 15% | Regulatory compliance |
| Anomaly Detection | 10% | Fraud/error detection |

Within each category, failure severity is weighted:
- CRITICAL: 100 points per finding
- HIGH: 50 points per finding
- MEDIUM: 20 points per finding
- LOW: 5 points per finding

## Output Structure

### validation_results.json Structure

```json
{
  "validation_date": "2025-02-07T14:30:00Z",
  "payroll_file": "payroll_data.xlsx",
  "prior_period_file": "prior_period.xlsx",
  "total_records": 50,
  "risk_score": 65,
  "risk_level": "High Risk",
  "overall_status": "FAIL",
  "pass_count": 20,
  "warning_count": 8,
  "fail_count": 2,
  "validation_categories": [
    {
      "category": "Data Completeness",
      "total_checks": 8,
      "passed": 7,
      "failed": 1,
      "checks": [
        {
          "check_name": "Missing Employee IDs",
          "status": "PASS",
          "severity": "Critical",
          "affected_count": 0,
          "details": "All 50 employees have valid IDs",
          "recommendation": "No action required"
        }
      ]
    }
  ],
  "critical_findings": [],
  "affected_employees": []
}
```

### audit_report.xlsx Worksheets

1. **Executive Summary**: Risk score, pass/fail counts, key metrics
2. **Critical Findings**: All CRITICAL severity items for review
3. **All Checks Detail**: Complete results for all 30 checks
4. **Affected Employees**: Employees with noted items, grouped by check category
5. **Prior Period Comparison**: Trend analysis vs. prior period
6. **Compliance Calendar**: Upcoming filing deadlines and penalties
7. **Review Checklist**: Preparer/Reviewer/Approver documentation section

## Example Scenarios

### Scenario 1: Clean Payroll Data (Low Risk)
- All 50 employees have complete data
- All calculations verified and accurate
- No wage base limit violations
- Risk score: 15 (Low Risk)
- Action: Approve for processing

### Scenario 2: Multiple Violations (High Risk)
- 2 employees missing cost center
- 1 employee with negative gross pay
- 1 employee over SS wage base
- Risk score: 58 (High Risk)
- Action: Remediate findings and re-validate

### Scenario 3: Anomaly Detection (Very High Risk)
- 1 employee with unusual payment (>3 std dev)
- Duplicate payments detected
- Prior period payroll variance >10%
- Risk score: 72 (Very High Risk)
- Action: Escalate for investigation

## Compliance Calendar

### Monthly Obligations
- Federal payroll tax deposits (Form 941 deposits)
- State income tax withholding deposits
- State unemployment insurance (SUI) contributions
- Child support/garnishment payments

### Quarterly Obligations
- Form 941-X (amended quarterly reconciliation)
- State quarterly wage reporting
- State SUI and disability insurance reporting

### Annual Obligations
- Form W-2 (employee wage reporting)
- Form W-3 (employer transmittal)
- Form 940 (federal unemployment tax)
- Form 1098-T (education credits)
- ACA Forms 1094-C and 1095-C
- State annual reconciliations

### Key Deadlines (with typical penalties)
- Monthly deposits: Last business day of month
- Quarterly 941: Month following quarter end
- W-2 distribution: January 31
- W-2 filing with SSA: February 28 (paper) / April 2 (electronic)
- Form 940 filing: January 31
- ACA reporting: February 28 (paper) / April 2 (electronic)

## Best Practices

### Before Running Validation
1. Ensure payroll data is complete and current
2. Have prior period data available for comparison analysis
3. Document any known exceptions or approvals
4. Verify SAP system configuration matches regulatory requirements
5. Review recent changes to tax rates, wage bases, or compliance rules

### During Validation Review
1. Prioritize CRITICAL severity findings first
2. Investigate unusual anomalies even if below severity threshold
3. Document the business reason for any exceptions
4. Escalate HIGH severity findings to payroll management
5. Track remediation actions and completion dates

### After Validation
1. Maintain audit trail of all validation runs
2. Archive validation results with payroll records
3. Update compliance calendar based on findings
4. Plan next validation cycle (monthly, quarterly, annual)
5. Include sign-offs in permanent payroll records

### SOX Compliance Considerations
1. Segregation of duties: Ensure different individuals prepare, review, and approve
2. Change management: Document all payroll system configuration changes
3. Access controls: Restrict modification of validation rules
4. Testing: Perform control testing at least quarterly
5. Documentation: Maintain evidence of all compliance reviews

## References

- **Pre-Submission Checklist**: `/references/pre-submission-checklist.md`
- **SOX Controls Framework**: `/references/sox-controls.md`
- **Compliance Calendar**: `/references/compliance-calendar.md`
- **Risk Assessment Framework**: `/references/risk-framework.md`

For federal tax requirements, refer to IRS publications:
- Publication 505: Tax Withholding and Estimated Tax
- Publication 15-B: Employer's Tax Guide to Fringe Benefits
- Publication 80: Federal Tax Guide for Employers in Puerto Rico

---

**Version 1.0.0** | Last Updated: February 2025 | Proprietary
