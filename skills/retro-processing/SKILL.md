---
name: retro-processing
description: |
  Analyze, plan, and validate SAP retroactive payroll adjustments. Supports retroactive salary changes,
  organizational reassignments, tax corrections, benefit modifications, and complex multi-period retro scenarios.
  Keywords: retroactive payroll, retro adjustment, retro processing, backdated change, retro accounting date,
  RRDAT, retro impact, /551, /552, /553, PU03, retro simulation, retro GL impact, retro correction,
  back pay, salary increase retro, retro tax adjustment, retro for terminated employee, multiple retro periods,
  year boundary retro
tags: [payroll, retroactive, adjustment, SAP, PCC, compliance]
---

# Retro-Processing Skill

## Overview

**PROOF-OF-CONCEPT**: This skill is an exploratory analysis tool and should be used for reference purposes only. It does not replace professional payroll judgment or formal retro processing procedures.

The retro-processing skill analyzes retroactive payroll adjustment impacts from XLSX exports of before/after
payroll results. It automates comparison of wage type changes, estimates GL posting differences, classifies
retro types, and flags complex scenarios including year-boundary crossings and terminated employee
corrections. It does NOT execute retro processing in SAP — it provides the analysis support.

**What SAP already provides natively:**
- **Simulation Mode** (RPCALCU0 with simulation flag / PCC Simulation step): Runs payroll calculation without updating results, showing what retro changes *would* produce
- **PU03** (Payroll Status): Shows retro accounting dates (RRDAT) and earliest retro period (ERA/EPRA)
- **/551, /552, /553 wage types**: System-generated retro difference, subsequent adjustment, and recalculation wage types visible in standard payroll results and Wage Type Reporter
- **RPUAUD00** (Audit Report): Shows changed master data records that triggered retro

**What this skill adds:**
- **Pre-retro impact analysis from exports** — compare simulation vs. production XLSX exports side by side, with AI-suggested retro type classification (salary change, org reassignment, tax correction, benefit change, termination reversal)
- **Preliminary risk indicators per employee** — provides financial and compliance risk indicators for each retro adjustment (SAP shows amounts but doesn't classify risk)
- **GL impact estimation** — estimates which GL accounts may be affected and by how much, before you run the actual posting (RPCIPE00)
- **Edge case flagging** — highlights potential year-boundary crossings, terminated employee retros, multi-period cascading effects, and missing master data (SAP's simulation mode calculates but doesn't flag these patterns)
- **Review XLSX report** with review checklist — structured documentation for retro review workflows
- Works from **XLSX exports** — accessible to team leads and approvers who don't have SAP transaction access

Retroactive payroll processing is one of the most complex payroll operations. A single retro error can
cascade across multiple GL accounts, create tax compliance issues, and generate employee disputes. This
skill reduces risk by providing structured analysis before execution and validation after.

## When to Use

- **Analyzing retro impact**: Compare payroll results before and after a retroactive change
- **Planning retro execution**: Estimate GL postings, tax impacts, and employee payment amounts
- **Validating retro scenarios**: Check for edge cases like year boundaries or terminated employee
  corrections
- **Risk assessment**: Classify retro adjustments by financial and compliance risk
- **Audit trail**: Generate detailed documentation for retro approval workflows
- **Multi-period retro**: Analyze cascading effects when multiple retro periods are involved

## Core Capabilities

### Impact Analysis
- **Automated employee identification**: Detects all employees affected by retro changes
- **Wage type breakdown**: Shows exactly which wage types changed and by how much
- **Net pay calculation**: Isolates employee payment impact (/551 equivalent)
- **Tax impact estimation**: Federal, state, and FICA changes
- **GL impact estimation**: Predicts which GL accounts will have difference postings

### Retro Classification
Automatically classifies retro changes into types:
- Pay Rate Change (salary, hourly adjustments)
- Organizational Reassignment (cost center, department, company code changes)
- Tax Correction (filing status, exemption changes)
- Benefit Change (enrollment, plan elections)
- Termination Reversal (reinstatement of separated employees)
- Late Time Entry (retroactive time ticket entry)

### Risk Indicators
- **Financial risk indicators**: Classifies adjustments as Low, Medium, High, or Critical based on amount
- **Compliance risk indicators**: Flags edge cases requiring manual review
- **Variance thresholds**: Highlights potential data quality issues

### Edge Case Flagging
- Year-boundary crossings (GL account structure changes, tax tables)
- Terminated employee retro (ERD restrictions, correction procedures)
- Multi-period retro (cascading effects)
- Missing master data
- Tax jurisdiction changes

## Input Requirements

### Current Results (after retro)
XLSX file with payroll calculation results post-retro. Must include:
- **Employee_ID**: Unique employee identifier (required)
- **Employee_Name**: Employee name (optional, for readability)
- **Wage_Type**: SAP wage type code (required)
- **Wage_Type_Description**: Descriptive name (optional, for reporting)
- **Amount**: Amount for this wage type (required)
- **Cost_Center**: Cost center code (optional)
- **Department**: Department name (optional)
- **Payroll_Area**: PA code (optional)
- **Period**: Period in YYYYMM format (optional, inferred if not provided)

### Prior Results (before retro)
XLSX file with same structure but payroll results pre-retro. Used as baseline for comparison.

### Optional Configuration
- Column mappings (if XLSX uses non-standard names)
- Retro period range (YYYYMM format)
- Risk thresholds (custom amounts for Low/Medium/High/Critical)

## Retro Types

### Pay Rate Change
Salary or hourly rate adjustment effective retroactively. Most common retro type.
- Affects wage types: /100, /101 (salary), /102 (hourly)
- Cascades to: /551 (recalc difference), /560 (payment amount)
- GL impact: Direct salary expense increase/decrease

### Organizational Reassignment
Cost center, department, or company code change with retroactive effective date.
- Affects: Cost center, department codes
- Does not typically change amounts but reclassifies to different GL accounts
- GL impact: High (moves amounts between multiple accounts)

### Tax Correction
Filing status, exemption, or tax jurisdiction change, retroactively applied.
- Affects wage types: /103 (tax withholding), /104 (state tax)
- Requires recalculation of tax tables for retro period
- GL impact: Wage tax expense accounts

### Benefit Change
Health insurance, retirement, FSA enrollment change effective retroactively.
- Affects: /200s (benefit deductions), /210s (employer contributions)
- May trigger catch-up contributions
- GL impact: Benefit expense and deduction accounts

### Termination Reversal
Rehire of terminated employee with retro effective date, or correction of ERD.
- Most complex retro type; involves multiple validations
- Requires verification of ERD restrictions
- GL impact: New employee baseline needed

### Late Time Entry
Time tickets entered retroactively for hours worked in prior periods.
- Affects: Hourly wages, overtime
- May require retro time evaluation (RPTIME00)
- GL impact: Labor expense and overtime accounts

## Impact Analysis Workflow

### 1. Data Preparation
- Load current_results and prior_results XLSX files
- Validate column structure and data types
- Detect column mappings (handles non-standard naming)

### 2. Employee-Level Comparison
For each employee, compare wage types between current and prior:
- Identify new wage types (not in prior)
- Identify removed wage types (in prior, not in current)
- Calculate delta for changed wage types

### 3. Aggregate Analysis
- **Total retro impact**: Sum of all employee deltas
- **Wage type summary**: Which wage types changed most frequently
- **Cost center impact**: Which cost centers affected
- **Department impact**: Which departments affected

### 4. Classification
Use wage type deltas to infer retro type:
- /100, /101, /102 changes → Pay Rate Change
- Cost center changes → Organizational Reassignment
- /103, /104 changes → Tax Correction
- /200s changes → Benefit Change
- Multiple high-risk indicators → Termination Reversal flag

### 5. Risk Indicators
Calculate preliminary risk indicators per employee:
- **Low**: < $500 delta
- **Medium**: $500–$2,000 delta
- **High**: $2,000–$5,000 delta
- **Critical**: > $5,000 delta

**Note**: These are preliminary indicators and require professional review and validation before retro processing execution.

### 6. Edge Case Detection
Check for:
- Year-boundary crossing (periods span calendar year change)
- Terminated employees with retro (review ERD)
- Multiple retro periods (identify which is first, which are subsequent)
- Missing wage types in prior (possible data quality issue)

## GL Impact Assessment

### Estimation Methodology
1. **Base GL mapping**: Standard SAP wage type → GL account mapping
2. **Retro classification**: Refine mapping based on retro type
3. **Difference posting**: Estimate difference GL accounts (if used)
4. **Reconciliation**: Flag accounts with potential large variances

**Note**: GL impact estimates are preliminary and require professional review before execution.

### Difference GL Accounts
SAP creates difference postings for /551, /552, /553:
- **GL Range**: Typically 4xxx (expense) or 2xxx (liability)
- **Clearing accounts**: If used, difference may post to clearing instead of final account
- **Period variance**: Different GL posting period than retro period

### GL Impact Categories
- **Direct Impact**: Wage type amounts directly affect GL accounts
- **Indirect Impact**: Changes in cost center/department allocation
- **Tax Impact**: Changes to wage tax liability
- **Benefit Impact**: Deduction and employer contribution accounts

## Output

### JSON Analysis Output
```json
{
  "affected_employees": [
    {
      "employee_id": "E001",
      "employee_name": "John Doe",
      "total_retro_delta": 2500.00,
      "retro_type": "Pay Rate Change",
      "risk_level": "High",
      "wage_type_changes": {
        "/100": { "prior": 5000.00, "current": 7500.00, "delta": 2500.00 },
        "/103": { "prior": 625.00, "current": 937.50, "delta": 312.50 }
      },
      "cost_center": "4100",
      "edge_cases": []
    }
  ],
  "retro_summary": {
    "total_employees_affected": 13,
    "total_retro_amount": 18750.00,
    "by_retro_type": { "Pay Rate Change": 10, "Org Reassignment": 2, "Tax Correction": 1 },
    "by_risk_level": { "Low": 5, "Medium": 6, "High": 2, "Critical": 0 }
  },
  "gl_impact": {
    "estimated_accounts_affected": ["4100", "2100", "2110", "3000"],
    "total_difference_amount": 18750.00
  },
  "edge_case_warnings": []
}
```

### XLSX Report Output
Multi-sheet workbook with:
- **Summary**: High-level overview
- **Employee Detail**: Per-employee breakdown
- **By Retro Type**: Grouped analysis
- **GL Impact**: Account-level estimates
- **Risk Indicators**: Preliminary risk assessment
- **Edge Cases**: Detailed flags
- **Review Checklist**: Documentation for professional review

## Example Scenarios

### Scenario 1: Mid-Year Salary Increase
**Situation**: Employees approved for 5% salary increase effective 3 months ago.
**Retro Type**: Pay Rate Change
**Analysis**:
- Wage type /100 increases by 5% × 3 months = 2.5% of annual
- /103 federal tax increases proportionally
- /104 state tax increases proportionally
- No cost center changes
**GL Impact**: Increase to salary expense, increase to wage tax liability

### Scenario 2: Organizational Restructuring
**Situation**: 8 employees transferred to new cost center effective 2 months ago.
**Retro Type**: Organizational Reassignment
**Analysis**:
- Same wage amounts, different cost center
- No change to /551 (net pay unchanged)
- GL accounts remain same, only account assignments change
**GL Impact**: Reclassification between GL accounts, no net dollar change

### Scenario 3: Year-Boundary Tax Change
**Situation**: Employee marital status changed in December, retro to January.
**Retro Type**: Tax Correction, Year-Boundary Crossing
**Analysis**:
- Jan–Nov with old filing status: Jan uses 202x tax table
- Dec onwards with new filing status: Dec uses different tax table
- Two different tax tables apply in same retro period
- May require two separate retro processing runs
**GL Impact**: Tax withholding accounts for Jan–Nov, then Dec

### Scenario 4: Terminated Employee Correction
**Situation**: Employee separated in November, reinstated in January with retroactive pay for December.
**Retro Type**: Termination Reversal
**Analysis**:
- Employee ERD was November
- December was "separated" period
- January retro restores December
- Requires verifying ERD eligibility for retro period
- Validate pension, benefit accruals for December
**GL Impact**: Significant (restores salary, benefits, taxes for one month)

## Edge Cases

### Year-Boundary Crossing
When retro period spans calendar year boundary (e.g., retro from October to January):
- Tax tables change (different tax withholding tables for 202x vs 202y)
- GL accounts may change (GL structure may be reorganized)
- Multiple GL posting periods required
- **Action**: Review GL mapping for both years before retro

### Terminated Employee Retro
Processing retro for employee with ERD in retro period:
- ERD may restrict retro eligibility
- Pension/benefit accruals may have been finalized at ERD
- May require separate correction procedures
- **Action**: Review ERD with HR, confirm retro is permitted

### Multiple Retro Periods
When multiple retro periods are processed (first retro, then subsequent adjustment):
- First retro creates /551 values
- Subsequent retro may generate /552 (subsequent adjustment)
- Results are not simply cumulative
- **Action**: Process in sequence, validate each result before next retro

### Missing Master Data
Wage type or GL account codes may have changed between periods:
- Prior period used wage type that no longer exists
- Cost center or company code was reorganized
- GL account was deleted or consolidated
- **Action**: Reconstruct missing mappings before retro

### Tax Jurisdiction Change
Employee changed work location or domicile during retro period:
- Different state tax tables apply
- Local tax may change
- Previous retro may not have accounted for new jurisdiction
- **Action**: Recalculate taxes for all periods in retro span

### Wage Type Configuration Change
Wage type amount or processing changed between periods:
- Calculation basis may differ
- Rounding rules may differ
- Valuation rules may differ
- **Action**: Review PCR and wage type configuration versions

## Best Practices

### Pre-Retro Validation
1. Obtain clear business justification for retro from HR/Management
2. Verify retro effective date in writing
3. Confirm all affected employees with HR
4. Review prior payroll runs to ensure baseline is clean
5. Validate GL account structure for retro period

### Simulation Before Execution
1. Always run retro simulation first (PC_PAYRESULT simulation mode)
2. Compare simulation results with this tool's impact analysis
3. Validate GL postings match expectations
4. Obtain approval on simulation results before actual execution
5. Document all simulation-to-execution deltas

### Retro Processing Sequence
1. First retro of a period: /551 (Recalc Difference) is generated
2. Subsequent retro of same period: /552 (Subsequent Adjustment) used
3. Do not re-execute first retro after subsequent retro (would double-adjust)
4. Process retros in chronological order (oldest first)

### Post-Retro Validation
1. Reconcile /551, /552, /553 wage types
2. Validate GL postings to accounts
3. Confirm employee net pay changes match expectations
4. Verify tax withholding is accurate for retro period
5. Send retro payment confirmations to employees
6. Document approval and execution in retro log

### Documentation Requirements
1. Maintain retro request documentation (business justification, approval)
2. Keep simulation results with before/after comparison
3. Store this tool's impact analysis JSON and XLSX output
4. Document any edge cases and how they were resolved
5. Maintain GL posting variance log
6. Preserve approval checklist signatures

## References

- **SAP Payroll Configuration Guide**: Retroactive Accounting (RRDAT/ERA/EPRA)
- **SAP Transactions**: PU03 (Retro Periods), PC00_M10_CALC (Calculate), PC_PAYRESULT (Review)
- **Wage Type Reference**: /551, /552, /553, /560, /562 (retro-related wage types)
- **GL Impact Assessment**: Difference table logic, wage type-GL mapping
- **Edge Case Procedures**: Year boundaries, terminated employees, multi-period retro
- See `references/` directory for detailed technical documentation

---

**Skill Version**: 1.0
**Last Updated**: February 2025
**Author**: SAP Payroll Integration Team
