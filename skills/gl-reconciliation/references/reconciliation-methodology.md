# Payroll-to-GL Reconciliation Methodology

## Overview

This document provides detailed procedures for reconciling SAP payroll results to general ledger
postings. Four primary reconciliation types ensure comprehensive validation of payroll accounting:
gross-to-net, employer costs, tax liabilities, and cost center allocation.

## Gross-to-Net Reconciliation

### Purpose

Validates the complete payroll calculation walkdown from gross compensation through deductions to
net pay, confirming that the result matches GL liability postings.

### Procedure

#### Step 1: Calculate Payroll Gross

Sum all wage types classified as income in the payroll run:

**Gross Components:**
- 1000: Regular Salary
- 1010: Overtime
- 1020: Shift Differential
- 1030: Bonus
- Other income-type wage types

**Calculation:**
```
Total Gross Payroll = Sum of all income wage type amounts
Example: $1,000,000 (50 employees, avg $20K)
```

#### Step 2: Identify All Deductions

Extract all deduction-type wage types from payroll:

**Pre-Tax Deductions (reduce taxable income):**
- 201-203: Health/dental/vision insurance (employee portion)
- 301-304: 401k, FSA, HSA, 403b deferrals
- Example: -$150,000 total

**Taxes Withheld (required by government):**
- 101: Federal income tax withholding
- 102: State income tax withholding
- 103: Local income tax withholding
- 110: FICA-SS employee withholding
- 111: FICA-Medicare employee withholding
- Example: -$200,000 total

**Post-Tax Deductions (after-tax):**
- 305: Roth 401k
- 306: Post-tax benefits
- 401-407: Employer taxes (not a deduction, but expense)
- Example: -$50,000 total

#### Step 3: Calculate Payroll Net

**Formula:**
```
Net Pay = Gross - Pre-Tax Deductions - Taxes Withheld - Post-Tax Deductions

Example:
  Gross                              $1,000,000
  Less: Pre-tax deductions           ($150,000)
  Less: Tax withholdings             ($200,000)
  Less: Post-tax deductions           ($50,000)
  ────────────────────────────────────────────
  NET PAY PAYABLE                      $600,000
```

#### Step 4: Reconcile to GL Net Pay Account

Query GL account 2000 (Net Pay Payable) for the payroll period:

**GL Query:**
```
Account: 2000 (Net Pay Payable)
Period: January 2024
Amount: $600,000
```

**Comparison:**
```
Payroll Calculated Net Pay              $600,000
GL Account 2000 Posted Amount           $600,000
Variance                                    $0.00  ✓ MATCHED
```

#### Step 5: Reconcile Gross Components

For each income wage type, verify GL posting to corresponding GL account:

**Example Validation:**
```
Wage Type 1000 (Salary)
  Payroll Total:     $800,000
  GL Account 6100:   $800,000
  Variance:              $0.00  ✓

Wage Type 1010 (Overtime)
  Payroll Total:     $100,000
  GL Account 6110:   $100,000
  Variance:              $0.00  ✓

Wage Type 1030 (Bonus)
  Payroll Total:     $100,000
  GL Account 6130:   $100,000
  Variance:              $0.00  ✓
```

### Common Issues & Resolution

**Issue: Net Pay doesn't match GL account 2000**

Resolution Steps:
1. Verify all wage types included in payroll calculation
2. Check for rounding differences (acceptable if < $0.01)
3. Verify GL posting date vs payroll period date
4. Check for accrual reversals in current period
5. Validate no manual journal entries posted to 2000 outside payroll process

**Issue: Gross components don't match GL**

Resolution Steps:
1. Verify wage type to GL account mapping (T52EL)
2. Check if wage type is excluded from GL posting (T52EK, NTAV field)
3. Validate calculation rule (KALSF) includes this component
4. Check for cost center splits (same wage type, multiple GL postings)
5. Verify no reclassification journals between payroll and GL

## Employer Cost Reconciliation

### Purpose

Validates that employer-paid taxes and benefit contributions are properly recorded in GL
expense accounts.

### Covered Costs

| Cost Type | Wage Type | GL Account | Calculation |
|-----------|-----------|-----------|-------------|
| FICA-SS Employer | 401 | 6200 | 6.2% × gross |
| FICA-Medicare Employer | 402 | 6201 | 1.45% × gross |
| FUTA | 403 | 6202 | 0.6% × first $7,000 (varies) |
| SUI | 404 | 6203 | State % × gross |
| Health Insurance | 405 | 6210 | Fixed monthly per employee |
| Dental Insurance | 406 | 6211 | Fixed monthly per employee |
| Vision Insurance | 407 | 6212 | Fixed monthly per employee |
| Life Insurance | 408 | 6213 | Typically per $1K coverage |

### Procedure

#### Step 1: Extract Employer Cost Amounts

For each employer cost wage type in payroll, sum total amounts:

**Example Payroll Results:**
```
Wage Type 401 (FICA-SS ER)        $62,000
Wage Type 402 (FICA-Med ER)       $14,500
Wage Type 403 (FUTA)               $3,500
Wage Type 404 (SUI)                $8,000
Wage Type 405 (Health Ins ER)     $50,000
Wage Type 406 (Dental Ins ER)      $5,000
Wage Type 407 (Vision Ins ER)      $2,000
Wage Type 408 (Life Ins ER)        $1,500
────────────────────────────────────────────
Total Employer Costs             $146,500
```

#### Step 2: Verify GL Postings

Query each corresponding GL expense account:

**GL Query Results:**
```
Account 6200 (FICA-SS ER)         $62,000 ✓
Account 6201 (FICA-Med ER)        $14,500 ✓
Account 6202 (FUTA)                $3,500 ✓
Account 6203 (SUI)                 $8,000 ✓
Account 6210 (Health Ins ER)      $50,000 ✓
Account 6211 (Dental Ins ER)       $5,000 ✓
Account 6212 (Vision Ins ER)       $2,000 ✓
Account 6213 (Life Ins ER)         $1,500 ✓
────────────────────────────────────────────
Total GL Postings                $146,500 ✓ MATCHED
```

#### Step 3: Identify Cost by Category

Break down by employer cost category for detailed review:

**Tax Costs:**
```
FICA-SS: $62,000 (6.2% of $1,000,000 gross)
FICA-Med: $14,500 (1.45% of $1,000,000)
FUTA: $3,500 (0.6% of cap)
SUI: $8,000 (varies by state)
Subtotal: $88,000
```

**Benefit Costs:**
```
Health: $50,000
Dental: $5,000
Vision: $2,000
Life: $1,500
Subtotal: $58,500
```

#### Step 4: Cost Center Validation

Verify employer costs allocated by cost center match GL cost center postings:

**Example:**
```
Cost Center 1000:
  Payroll ER Costs: $50,000
  GL Sum (all accounts, CC 1000): $50,000 ✓

Cost Center 2000:
  Payroll ER Costs: $60,000
  GL Sum (all accounts, CC 2000): $60,000 ✓

Cost Center 3000:
  Payroll ER Costs: $36,500
  GL Sum (all accounts, CC 3000): $36,500 ✓
```

### Common Issues & Resolution

**Issue: Employer tax variance (e.g., FICA-SS off)**

Resolution Steps:
1. Verify gross amount used in calculation (should exclude pre-tax deductions)
2. Confirm calculation rate (6.2% for FICA-SS, may vary for SUI)
3. Check for wage caps (FICA-SS capped at ~$168,600 in 2024)
4. Validate employee count and individual calculations
5. Check for off-cycle payroll not included in main run

**Issue: Benefit costs don't match GL**

Resolution Steps:
1. Verify employee benefit elections in each cost center
2. Check for timing (when benefits become effective)
3. Validate GL posting accounts are correct (check T52EL)
4. Verify cost center splits for shared benefit costs
5. Check for manual benefit adjustments outside payroll

## Tax Liability Reconciliation

### Purpose

Validates that payroll tax withholdings are properly recorded as GL liabilities, ensuring
accurate tax payment and compliance reporting.

### Withholding Categories

| Tax Type | Wage Type | GL Account | Notes |
|----------|-----------|-----------|-------|
| Federal Income Tax | 101 | 2100 | IRS tables updated annually |
| State Income Tax | 102 | 2120 | Varies by employee state |
| Local Income Tax | 103 | 2130 | City/county specific |
| FICA-SS Employee | 110 | 2140 | 6.2% through wage cap |
| FICA-Medicare Employee | 111 | 2141 | 1.45% plus 0.9% over threshold |

### Procedure

#### Step 1: Extract Tax Withholding Amounts

Sum each tax withholding wage type from payroll:

**Example Payroll Results:**
```
Wage Type 101 (Federal Tax)        $100,000
Wage Type 102 (State Tax)           $50,000
Wage Type 103 (Local Tax)           $15,000
Wage Type 110 (FICA-SS)             $62,000
Wage Type 111 (FICA-Med)            $14,500
────────────────────────────────────────────
Total Employee Tax Withholdings   $241,500
```

#### Step 2: Reconcile GL Liability Accounts

Query each GL liability account for the payroll period:

**GL Query Results:**
```
Account 2100 (Federal Tax)         $100,000 ✓
Account 2120 (State Tax)            $50,000 ✓
Account 2130 (Local Tax)            $15,000 ✓
Account 2140 (FICA-SS)              $62,000 ✓
Account 2141 (FICA-Med)             $14,500 ✓
────────────────────────────────────────────
Total GL Tax Liabilities          $241,500 ✓ MATCHED
```

#### Step 3: Verify Employer Tax Payables

Also reconcile employer portion of FICA (accrued as liability):

**Employer FICA:**
```
Wage Type 401 (FICA-SS ER)
  Payroll Amount: $62,000
  GL Account 2142 (FICA-SS ER Payable): $62,000 ✓

Wage Type 402 (FICA-Med ER)
  Payroll Amount: $14,500
  GL Account 2143 (FICA-Med ER Payable): $14,500 ✓
```

#### Step 4: By-Jurisdiction Validation

Break down tax liabilities by jurisdiction for compliance reporting:

**Example:**
```
Federal Income Tax Withholding
  Total: $100,000
  GL Account 2100: $100,000 ✓
  Due: Quarterly estimated tax + 941 annual

State Income Tax Withholding
  CA: $25,000 → GL Account 2120
  NY: $15,000 → GL Account 2120
  TX: $10,000 → GL Account 2120
  Total: $50,000 ✓

Local Income Tax Withholding
  NYC: $12,000 → GL Account 2130
  Other: $3,000 → GL Account 2130
  Total: $15,000 ✓
```

#### Step 5: Period-End GL Balance Validation

Ensure GL liability balances are reasonable:

**Opening Balance + Current Month Accrual - Payments = Closing Balance**

Example:
```
Account 2100 (Federal Tax)
  Opening Balance (12/31):      $30,000
  Jan Payroll Accrual:         $100,000
  Jan Tax Payments (Q1 deposit):($90,000)
  Closing Balance (1/31):        $40,000

  Reasonability Check: $40,000 reasonable for Feb 2 payment date
```

### Common Issues & Resolution

**Issue: Tax withholding amount incorrect**

Resolution Steps:
1. Verify withholding method in employee master (IRS form W-4 equivalent)
2. Check for allowances/exemptions impact
3. Validate tax calculation rules are applied (T52EK, KALSF)
4. Confirm tax tables are current (updated annually)
5. Check for mid-year W-4 changes (compare dates)

**Issue: Tax liability GL account variance**

Resolution Steps:
1. Verify GL account is correct for tax type (federal, state, local)
2. Check for tax payment posts that reduce liability
3. Verify no reclassification entries
4. Check for accrual entries that offset payroll posting
5. Validate GL posting is to liability account, not expense

**Issue: Period-end liability balance doesn't reconcile to tax filing**

Resolution Steps:
1. Verify tax liability account includes all payments/deposits
2. Check for inter-period differences (accrual vs cash basis)
3. Confirm GL posting dates align with tax payment schedule
4. Validate no manual adjustments outside payroll
5. Reconcile to 941/940 forms due

## Benefit Deduction Reconciliation

### Purpose

Validates that employee deductions for benefits are properly recorded as GL liabilities and that
employer cost contributions are recorded as GL expenses.

### Deduction Categories

| Benefit Type | EE Deduction WT | GL Liability | ER Cost WT | GL Expense |
|--------------|-----------------|-------------|-----------|-----------|
| Health Insurance | 201 | 2210 | 405 | 6210 |
| Dental Insurance | 202 | 2211 | 406 | 6211 |
| Vision Insurance | 203 | 2212 | 407 | 6212 |
| Life Insurance | 204 | 2213 | 408 | 6213 |
| FSA Deduction | 302 | 2311 | - | - |
| HSA Deduction | 303 | 2312 | - | - |
| 401k Deferral | 301 | 2310 | - | - |

### Procedure

#### Step 1: Extract Benefit Deduction Amounts

Sum employee benefit deductions and employer contributions:

**Employee Deductions (Payroll):**
```
Wage Type 201 (Health Ins):    $100,000 (GL Liability 2210)
Wage Type 202 (Dental Ins):     $15,000 (GL Liability 2211)
Wage Type 203 (Vision Ins):      $8,000 (GL Liability 2212)
Wage Type 301 (401k):          $150,000 (GL Liability 2310)
Wage Type 302 (FSA):            $25,000 (GL Liability 2311)
────────────────────────────────────────────────────
Total EE Benefit Deductions    $298,000
```

**Employer Contributions (Payroll):**
```
Wage Type 405 (Health Ins):    $100,000 (GL Expense 6210)
Wage Type 406 (Dental Ins):     $10,000 (GL Expense 6211)
Wage Type 407 (Vision Ins):      $5,000 (GL Expense 6212)
────────────────────────────────────────────────────
Total ER Benefit Costs          $115,000
```

#### Step 2: Reconcile GL Accounts

**GL Liability Accounts (Employee Deductions):**
```
Account 2210 (Health Ins Payable):   $100,000 ✓
Account 2211 (Dental Ins Payable):    $15,000 ✓
Account 2212 (Vision Ins Payable):     $8,000 ✓
Account 2310 (401k Payable):         $150,000 ✓
Account 2311 (FSA Payable):           $25,000 ✓
────────────────────────────────────────────────────────
Total GL Benefit Liabilities         $298,000 ✓
```

**GL Expense Accounts (Employer Contributions):**
```
Account 6210 (Health Ins Expense):   $100,000 ✓
Account 6211 (Dental Ins Expense):    $10,000 ✓
Account 6212 (Vision Ins Expense):     $5,000 ✓
────────────────────────────────────────────────────────
Total GL Benefit Expenses            $115,000 ✓
```

#### Step 3: Validate Benefit Election Changes

Verify any benefit changes during period are reflected:

**Check:**
1. New hire benefit elections implemented immediately
2. Mid-period benefit changes effective date correct
3. Benefit terminations for separated employees
4. Annual benefit election changes (open enrollment)

#### Step 4: Reconcile to Benefit Provider

Verify GL liability amounts match benefit provider invoices/reports:

**Example:**
```
Health Insurance Plan (ABC Insurance)
  GL Payable (2210): $100,000 (from payroll)
  Invoice from ABC: $100,000 (50 emp × $2,000/month)
  Amount Paid: $100,000
  Difference: $0.00 ✓
```

## Cost Center Allocation Reconciliation

### Purpose

Validates that payroll costs are allocated to GL cost centers matching payroll cost center
assignments.

### Procedure

#### Step 1: Summarize Payroll by Cost Center

Calculate total payroll (all wage types) by cost center:

**Example:**
```
Cost Center 1000 (Engineering):
  Total Payroll: $400,000 (50 employees)

Cost Center 2000 (Sales):
  Total Payroll: $300,000 (40 employees)

Cost Center 3000 (Admin):
  Total Payroll: $300,000 (60 employees)

Grand Total: $1,000,000
```

#### Step 2: Summarize GL Postings by Cost Center

Query GL for all payroll-related accounts grouped by cost center:

**GL Query (sum all 6xxx and 2xxx accounts by cost center):**
```
Cost Center 1000:
  GL Postings: $400,000 ✓

Cost Center 2000:
  GL Postings: $300,000 ✓

Cost Center 3000:
  GL Postings: $300,000 ✓

Grand Total: $1,000,000 ✓
```

#### Step 3: Identify Variances

Flag any cost centers with mismatches:

**Example with Variance:**
```
Cost Center 1000:
  Payroll: $400,000
  GL: $400,000 ✓

Cost Center 2000:
  Payroll: $300,000
  GL: $297,500 ✗ Variance: ($2,500)

Cost Center 3000:
  Payroll: $300,000
  GL: $302,500 ✓ (includes $2,500 adjustment)
```

#### Step 4: Investigate Cost Center Mismatches

For variances, identify root cause:

**Investigation Steps:**
1. Verify employee cost center assignments (PA0001, PA0027)
2. Check for mid-period cost center transfers
3. Identify GL manual entries crediting/charging cost centers
4. Verify GL cost center posting logic in RPCPRRU0
5. Check for cost center overrides at wage type level (T52AB)

#### Step 5: Cost Center Detail Breakdown

For variances, break down by wage type to isolate issue:

**Example:**
```
Cost Center 2000 - Payroll vs GL by Wage Type:

1000 (Salary):      Payroll $200K, GL $200K ✓
1010 (OT):          Payroll $50K, GL $50K ✓
101 (Fed Tax):      Payroll ($40K), GL ($40K) ✓
110 (FICA-SS):      Payroll ($12.4K), GL ($12.4K) ✓
401 (FICA-SS ER):   Payroll $12.4K, GL $12.4K ✓
405 (Health):       Payroll $9K, GL $6.5K ✗ Variance: ($2.5K)
─────────────────────────────────────────────────────

Issue: Health insurance for CC 2000 shows $2.5K underpostage in GL
Resolution: Health benefit allocation rules may differ from payroll assignment
```

## Period-End Close Reconciliation Checklist

Complete the following steps before approving payroll close:

### Pre-Reconciliation (Day 1-2 of close month)

- [ ] Verify payroll period dates match GL posting dates
- [ ] Confirm all employees processed (no missed batches)
- [ ] Check for off-cycle/special payroll runs
- [ ] Validate no duplicate payroll postings
- [ ] Confirm GL accounts are open for period

### Reconciliation Execution (Day 3-4)

- [ ] Run gross-to-net reconciliation
- [ ] Run employer cost reconciliation
- [ ] Run tax liability reconciliation
- [ ] Run cost center allocation reconciliation
- [ ] Generate reconciliation report in Excel

### Variance Investigation (Day 4-5)

- [ ] Review all unmatched items
- [ ] Investigate variances exceeding tolerance
- [ ] Document reconciling items (timing, rounding, etc.)
- [ ] Verify manual journal entries (if any)
- [ ] Validate retroactive adjustments

### GL Account Reconciliation (Day 5-6)

- [ ] Verify accrued payroll liability opening balance (from last period)
- [ ] Add: Current month payroll accrual
- [ ] Less: Payroll payments/check clearings
- [ ] Verify: Ending liability balance reasonable for next pay dates
- [ ] Reconcile: Liability account to GL trial balance

### Tax Reconciliation (Day 6)

- [ ] Verify federal income tax withholding total
- [ ] Verify state income tax withholding by state
- [ ] Verify FICA employee withholding
- [ ] Reconcile to tax deposit schedule
- [ ] Verify tax payments made timely

### Benefit Reconciliation (Day 6)

- [ ] Verify benefit deduction totals match plan invoices
- [ ] Reconcile employer benefit costs to plan charges
- [ ] Verify new/terminated benefit elections processed
- [ ] Check for missing benefit deductions

### Cost Center Reconciliation (Day 7)

- [ ] Verify total payroll allocated to all cost centers
- [ ] Reconcile cost center totals to GL
- [ ] Investigate significant cost center variances
- [ ] Verify no cost center reassignments impacting GL

### Final Approval (Day 7-8)

- [ ] Controller review of reconciliation report
- [ ] Sign-off on variances/reconciling items
- [ ] Approve GL posting (if not auto-posted)
- [ ] File reconciliation workbook with close documentation
- [ ] Post close documentation note

## Key SAP Reports for Validation

### RPCPRRU0 - Payroll Posting Report

Main payroll-to-GL posting report. Validates:
- Wage type allocation rules
- GL account determination
- Cost center assignment
- Manual entry impact
- GL account balances post payroll

**Usage:**
```
Report: RPCPRRU0
Period: January 2024
Company Code: 1000
Payroll Area: 01
Options: With GL reconciliation, with cost center breakdown
```

### RPDKON00 - Payroll GL Reconciliation

Automated reconciliation of payroll GL postings. Compares:
- Gross to net calculation
- Deductions and withholdings
- Employer taxes and benefits
- GL postings

**Usage:**
```
Report: RPDKON00
Period: January 2024
Tolerance: 0.01
Output: Unmatched items only
```

### PC00_M99_CIPE - Payroll Results per Employee

Detailed payroll register showing all wage types per employee. Use to:
- Validate individual employee calculations
- Trace specific gross/net amounts
- Verify deductions and tax withholdings

**Usage:**
```
Report: PC00_M99_CIPE
Payroll Area: 01
Period: January 2024
Sort: Employee, Cost Center
```

## References

- SAP Payroll Configuration Guide
- SAP FI-GL General Ledger Module Documentation
- Month-End Close Procedure Manual
- Tax Compliance and Reporting Guide
- Internal GL Account Chart and GL Account Hierarchy
