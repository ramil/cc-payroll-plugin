---
name: gl-reconciliation
category: Finance & Accounting
subcategory: Payroll
plugins:
  - cc-payroll
description: |
  Automates payroll-to-GL reconciliation from SAP payroll result exports. Reconciles gross-to-net payroll
  calculations against GL postings, validates employer costs and tax liabilities, identifies timing
  differences and rounding variances, and generates multi-sheet reconciliation workbooks. Supports
  wage type to GL account mapping, symbolic account determination, cost center allocation validation,
  and RPCPRRU0 report correlation. Handles retroactive adjustments, accrual reversals, and manual
  journal entry identification. Essential for month-end payroll close and external audit compliance.
author: "SAP Finance Automation Team"
version: "1.0.0"
requires:
  - python: "3.10+"
  - packages:
      - openpyxl
      - pandas
      - jsonschema
keywords:
  - GL reconciliation
  - payroll-to-finance
  - posting variance
  - wage type mapping
  - symbolic account
  - gross-to-net
  - employer cost recon
  - tax liability recon
  - RPCPRRU0
  - reconciling items
  - cost center allocation
  - retro adjustments
  - timing differences
---

## Overview

**PROOF-OF-CONCEPT**: This skill is an exploratory analysis tool and should be used for reference purposes only. It does not replace professional payroll judgment or formal reconciliation procedures.

The **gl-reconciliation** skill analyzes SAP payroll-to-GL reconciliation data from XLSX exports
and generates detailed variance analysis, break categorization, and review-support workbooks. It works
with payroll result exports and GL posting exports — it does NOT require direct SAP system access.

**What SAP already provides natively:**
- **RPCPRRU0** (Payroll Reconciliation Report): Reconciles payroll results against FI postings, showing matched and unmatched items within SAP
- **RPCIPE00** (GL Posting Run): Posts payroll results to GL via symbolic accounts (T52EK/T52EL)
- **SE16 on T52EK/T52EL**: Shows wage type → symbolic account → GL account mappings

**What this skill adds:**
- Works from **XLSX exports** — no SAP transaction access required (ideal for BPO analysts, month-end reviewers, and external auditors who receive data extracts)
- **AI-generated draft narrative** explaining each reconciling item in business language, not just SAP codes
- **Multi-sheet review workbook** organized for month-end close reference (RPCPRRU0 output is a flat ALV grid)
- **Configurable wage type mapping** in JSON — adapts to any customer's chart of accounts without ABAP customization
- **Reconciling item classification** with resolution hints — categorizes breaks as timing differences, rounding, retro adjustments, or configuration errors
- **Cost center allocation validation** across GL and payroll simultaneously

The skill implements four primary reconciliation types:
- **Gross-to-Net Reconciliation**: Validates the payroll walkdown from gross salary through deductions to net pay
- **Employer Cost Reconciliation**: Reconciles employer-paid taxes (FICA, FUTA, SUI) and benefit costs
- **Tax Liability Reconciliation**: Validates federal, state, and local withholding liabilities
- **Cost Center Allocation**: Ensures payroll by cost center matches GL cost center distributions

## When to Use

Use **gl-reconciliation** when:
- You have payroll and GL data as **XLSX exports** and need to reconcile outside of SAP (e.g., BPO analyst, external auditor, month-end reviewer without SAP access)
- You need a **review-support workbook** with formatted sheets for reference — RPCPRRU0 output alone doesn't provide this
- You want **AI-generated draft explanations** of reconciling items for stakeholder communication
- You need to validate a **custom wage type → GL mapping** before go-live or after chart of accounts restructuring
- Investigating GL account variances between payroll results and finance records
- Reconciling retroactive payroll adjustments or off-cycle payroll
- Validating cost center allocations across multiple GL cost centers

**When to use SAP instead:** If you have SAP transaction access and just need a quick reconciliation check, run RPCPRRU0 directly. This skill is for when you need deeper analysis, formatted output, or are working from exports.

## Configuration

**Wage Type to GL Account Mapping**

The mapping between payroll wage types and GL accounts is stored in an editable JSON config file:

```
config/wage_type_mapping.json
```

This file ships with standard US payroll defaults (24 wage types). To match your SAP backend, edit this file with your actual wage type codes and GL account numbers from tables T52EK/T52EL. No Python code changes required.

**How it loads (resolution order):**
1. `--wage-type-config /path/to/custom.json` (CLI argument)
2. `config/wage_type_mapping.json` (default location in skill folder)
3. Embedded defaults (hardcoded fallback if no config file found)

See `config/README.md` for editing instructions and examples.

## Core Capabilities

**Flexible Input Matching**
- Accepts payroll and GL data in various column formats
- Auto-detects column names for wage type, employee, amount, GL account, cost center
- Handles both SAP naming conventions and custom column headers

**Multi-Type Reconciliation**
- Performs gross-to-net walkdown validation
- Reconciles employer cost components (FICA-SS, FICA-Med, FUTA, SUI, benefits)
- Validates tax withholding liabilities by jurisdiction
- Allocates payroll amounts to GL cost centers

**Wage Type to GL Mapping**
- Editable JSON config file (`config/wage_type_mapping.json`) for easy customization
- Supports symbolic account determination logic
- Maps wage type → symbolic account → GL account chain
- Configurable for any country or chart of accounts structure
- Falls back to built-in US payroll defaults if config file is missing

**Reconciling Items Identification**
- Detects timing differences (payroll vs GL period gaps)
- Identifies rounding variances and aggregation differences
- Flags retroactive adjustments and clearing account impacts
- Categorizes manual journal entries and accrual reversals

**JSON Output**
- Matched items with cross-references
- Unmatched items (in payroll but not GL, or vice versa)
- Reconciling items with classification and resolution hints
- Summary statistics by reconciliation type

**Multi-Sheet Report Generation**
- Summary sheet with match rates and variance totals
- Gross-to-Net walkdown with GL comparison
- Employer Costs breakdown by type
- Tax Liabilities by jurisdiction
- Unmatched Items detailed list
- Reconciling Items with classification

## Required Input

**Payroll Results File** (XLSX)
- Column for wage type (e.g., "Wage Type", "WT", "wage_type")
- Column for employee identifier (e.g., "Employee ID", "emp_id", "personnel_no")
- Column for amount (e.g., "Amount", "amt", "value")
- Column for cost center (optional, e.g., "Cost Center", "KOSTL")
- Derived from SAP payroll run results

**GL Postings File** (XLSX)
- Column for GL account (e.g., "GL Account", "account", "acct")
- Column for amount (e.g., "Amount", "amt")
- Column for cost center (optional, same as payroll)
- Column for posting date (e.g., "Posting Date", "BUDAT")
- Column for document number (optional, e.g., "Document", "doc_no")
- Exported from SAP FI GL line items or reconciliation reports

## Reconciliation Types

### Gross-to-Net Reconciliation
Validates the complete payroll walkdown:
1. Sum of gross salary wage types (1000 salary, 1010 overtime, etc.)
2. Subtract pre-tax deductions (401k, health insurance)
3. Calculate taxable wages and withholdings (federal, state, local, FICA)
4. Sum all deductions
5. Calculate net pay (gross - deductions)
6. Verify GL postings for net pay liability account match
7. Identify variances at each step

### Employer Cost Reconciliation
Validates employer-paid costs:
- FICA-SS and FICA-Med taxes (/401, /402 wage types)
- FUTA and SUI taxes (/403, /404 wage types)
- Health insurance and benefit employer contributions (/201-/210 wage types)
- Match to GL expense accounts (6xxx range)
- Validate cost center allocations

### Tax Liability Reconciliation
Validates withholding liabilities:
- Federal income tax withholding (/101 wage type) → GL account 2xxx
- State income tax withholding (/102 wage type) → GL account 2xxx
- Local income tax withholding (/103 wage type) → GL account 2xxx
- FICA-SS employee withholding → GL account 2xxx
- Verify opening balance + payroll accrual - payments = closing balance

### Benefit Deduction Reconciliation
Validates employee benefit deductions:
- Health insurance (/201 wage type) → GL benefit liability
- 401k contributions (/301 wage type) → GL 401k liability
- FSA/HSA deductions (/302, /303) → GL liability accounts
- Reconcile to employee benefit payroll register

## Workflow

1. **Configure Mapping** (first time only): Edit `config/wage_type_mapping.json` to match your SAP GL account structure
2. **Export Payroll Results**: Extract wage type level data from SAP payroll run
3. **Export GL Postings**: Export GL line items for payroll posting accounts
4. **Run Reconciliation**: Execute `reconcile_payroll_gl.py` with both files
4. **Review JSON Output**: Check matched/unmatched items and reconciling items
5. **Generate Report**: Execute `generate_recon_report.py` to create multi-sheet workbook
6. **Investigate Variances**: Use reconciling items classification to determine resolution
7. **Document Reconciling Items**: Record reasons for unresolved variances
8. **Approve Close**: Use final reconciliation workbook for month-end close sign-off

## Output

**JSON Output Structure**
```json
{
  "reconciliation_summary": {
    "total_payroll_amount": 1500000.00,
    "total_gl_amount": 1500000.00,
    "total_variance": 0.00,
    "matched_count": 150,
    "unmatched_payroll_count": 2,
    "unmatched_gl_count": 1,
    "reconciling_items_count": 3,
    "match_rate_percent": 98.3
  },
  "matched_items": [
    {
      "wage_type": "1000",
      "amount_payroll": 100000.00,
      "gl_account": "6100",
      "amount_gl": 100000.00,
      "cost_center": "1100",
      "variance": 0.00
    }
  ],
  "unmatched_items": [
    {
      "source": "payroll",
      "wage_type": "1010",
      "amount": 5000.00,
      "reason": "No matching GL posting found"
    }
  ],
  "reconciling_items": [
    {
      "description": "Timing difference: payroll 1/31 vs GL posting 2/1",
      "type": "timing",
      "wage_type": "1000",
      "amount": 25000.00,
      "resolution_steps": ["Verify posting date in GL", "Check period cutoff rules"]
    }
  ],
  "by_recon_type": {
    "gross_to_net": { "matched": 45, "unmatched": 1, "variance": 0.00 },
    "employer_costs": { "matched": 30, "unmatched": 1, "variance": 0.00 },
    "tax_liabilities": { "matched": 60, "unmatched": 0, "variance": 0.00 },
    "cost_center_allocation": { "matched": 100, "unmatched": 2, "variance": 100.00 }
  }
}
```

**Excel Report**
- Summary: Match rates, totals, reconciling items summary
- Gross-to-Net: Payroll walkdown with GL account comparisons
- Employer Costs: Cost breakdown by type and GL account
- Tax Liabilities: Withholding by jurisdiction and GL account
- Unmatched Items: Payroll and GL items without matches
- Reconciling Items: Classified by type with resolution hints

## Example Scenarios

**Scenario 1: Monthly Close Reconciliation**
You've completed the monthly payroll run in SAP and need to validate all postings to the GL
before closing the accounting period. Export payroll results and GL postings, run gl-reconciliation
with `--recon-type all`, and generate the report. The summary shows 100% match rate with no
reconciling items, confirming ready for close.

**Scenario 2: GL Variance Investigation**
The controller identifies a $50K variance in the gross salary GL account for January. Run
gl-reconciliation to identify which wage types don't match. The report shows a timing difference
where payroll was processed 1/31 but GL posted 2/1. You document this as a reconciling item and
note it will reverse in the next period.

**Scenario 3: Retroactive Adjustment Processing**
You need to reconcile a retroactive bonus for Q4 that was processed off-cycle in January. Run
gl-reconciliation with the bonus wage type included. The output identifies matching GL postings
and validates that the $100K bonus properly hit GL accounts 6100 (salary expense) and 2000 (net
pay liability).

**Scenario 4: Cost Center Allocation Audit**
External auditors require validation that payroll by cost center matches GL distributions. Run
gl-reconciliation with `--recon-type cost_center_allocation`. The report breaks down payroll and
GL amounts by cost center, identifying a $15K variance in cost center 2200. Investigation reveals
a cost center override on one employee was not updated in GL cost center assignment.

## Best Practices

1. **Regular Reconciliation**: Run gl-reconciliation monthly as part of period-end close, not just when variances exist
2. **Tolerance Thresholds**: Set appropriate tolerance for rounding (typically 0.01-1.00 USD depending on payroll size)
3. **Timing Documentation**: Document known timing differences (payroll vs GL posting dates) to avoid re-investigating each month
4. **Wage Type Mapping Review**: Quarterly review wage type to GL account mappings to ensure accuracy after changes
5. **Unmatched Items Root Cause**: Always investigate unmatched items; they often indicate configuration errors
6. **Cost Center Validation**: Validate cost center allocations quarterly, especially after organizational changes
7. **Reconciling Items Log**: Maintain a log of recurring reconciling items to identify systemic issues
8. **Audit Workbook**: Retain generated Excel workbooks as audit trail for external auditors
9. **Symbolic Account Configuration**: Review SAP symbolic account configuration (T52EK, T52EL) annually
10. **Period-End Checklist**: Use methodology reference to verify all reconciliation types before approving close

## References

- **gl-account-mapping.md**: Complete wage type to GL account mapping reference with symbolic account logic
- **reconciliation-methodology.md**: Detailed procedures for each reconciliation type and period-end close checklist
- **reconciling-items.md**: Catalog of common reconciling items with resolution steps
- SAP Documentation: HR-PY Payroll Configuration, FI-GL General Ledger Posting, RPCPRRU0 Report
- SAP Tables: T52EK (Wage Type to Symbolic Account), T52EL (GL Account Determination), OBYE (GL Account Master)
