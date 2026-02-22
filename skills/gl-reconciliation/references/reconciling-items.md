# Reconciling Items Catalog

## Overview

Reconciling items are differences between payroll and GL amounts that are expected, explainable,
and can be categorized by type. This document provides a comprehensive catalog of common
reconciling items, their causes, and resolution procedures.

Reconciling items differ from unmatched items:
- **Unmatched Items**: Amounts in payroll with no corresponding GL posting, or vice versa (investigation required)
- **Reconciling Items**: Known differences that are acceptable and explained (documentation sufficient)

## Categories of Reconciling Items

### 1. Timing Differences

Timing differences occur when payroll transactions and GL postings occur in different periods.

#### 1a. Payroll Period vs GL Posting Date Difference

**Description:**
Payroll is processed for a period (e.g., Jan 1-31) but GL posting occurs on a different date
(e.g., Feb 1 or Feb 2).

**Cause:**
- SAP configuration posts payroll GL entries after payroll completion
- Multi-day payroll processing period spans period boundary
- GL posting run occurs in subsequent period (standard SAP design)

**Example:**
```
Payroll Period: January 1-31, 2024
Payroll Processed: January 31, 2024 evening
GL Posted: February 1, 2024 morning

Scenario:
  January GL: Payroll postings missing until Feb 1
  February GL: Payroll accruals appear as February expense/liability

Reconciliation Impact:
  January 31 Variance: GL lacks payroll postings, GL balance is understated
  February 1 Reversal: GL balance corrects when posting completes
```

**Resolution Steps:**
1. Verify GL posting date configuration (payroll customization)
2. Confirm posting date is 1-2 business days after period end
3. Compare payroll period vs GL posting date
4. Document as timing reconciling item
5. Verify GL balance is correct as of posting date (not period end date)

**Acceptable?** YES - This is standard GL timing and should be documented

#### 1b. Check Clearing Timeline Differences

**Description:**
Payroll processes net pay liability on period end, but actual check payments clear GL bank
account on a different date.

**Cause:**
- Net pay posted as liability on payroll date (period end)
- Check payments may be dated multiple days later (check date)
- Bank clearing may occur days/weeks later (clearing date)

**Example:**
```
Payroll Period: January 1-31, 2024
Net Pay Posted: January 31, 2024 (GL 2000)
Check Date: February 1, 2024
Check Clearing: February 5, 2024

Timing Difference:
  GL 2000 (Jan 31): $600K accrual
  GL 1000 (Feb 5): $600K bank reduction when checks clear
  Variance (Feb 1-4): +$600K in GL 2000 (timing-related)
```

**Resolution Steps:**
1. Verify check processing workflow
2. Compare payroll posting date vs check clearing date
3. Identify typical clearing timeline (usually 2-5 business days)
4. Document opening and closing balances of net pay liability
5. Verify GL 2000 closing balance reasonable for outstanding checks

**Acceptable?** YES - Standard check clearing timing, document in reconciling items

#### 1c. Accrual Reversal Timing

**Description:**
Payroll accrual from prior period is reversed in current period on different date than posting.

**Cause:**
- Month-end: Payroll accrual posted to GL on Jan 31
- Month-end close: Accrual reversal entry posted on Feb 1
- Next payroll: Actual payroll posting on Feb 15
- Timing gap: Feb 1-14 shows net zero due to reversal/posting timing

**Example:**
```
Jan 31: Payroll posting $1,000,000 (GL 6100, GL 2000)
        GL Trial Balance (Jan 31): Payroll posted

Feb 1: Accrual reversal $1,000,000 (GL 6100, GL 2000 - reversals)
       GL Trial Balance (Feb 1): Zero net impact

Feb 15: Next month payroll posting $1,000,000
        GL Trial Balance (Feb 15): Returns to accrual

Reconciliation Impact:
  Jan 31: Full payroll amounts in GL
  Feb 1-14: Zero payroll impact due to timing of reversal
  Feb 15: Payroll amounts reappear
```

**Resolution Steps:**
1. Verify accrual reversal configuration (T001P)
2. Confirm reversal date is 1st of following month
3. Trace reversal batch document (typically ACRL)
4. Verify reversal is exactly opposite of accrual
5. Document as timing reconciling item

**Acceptable?** YES - This is standard month-end accrual reversal timing

#### 1d. Retroactive Adjustment Timing

**Description:**
Retroactive payroll adjustments (for prior periods) are posted in current GL month,
creating timing mismatch between payroll period and GL posting month.

**Cause:**
- Retro adjustments processed for historical periods (e.g., Jan retroactively adjusted in Feb)
- GL posting occurs in current month (Feb)
- Difference document may be used for reclassification

**Example:**
```
Scenario: January bonus was calculated incorrectly, corrected in February

Payroll Records:
  January: Bonus posted as $10,000 (GL 6130, GL 2000)
  February: Retro adjustment discovered, posted as $5,000 additional bonus

GL Records:
  January: Bonus expense $10,000
  February: Bonus adjustment $5,000 (posted to February GL accounts)
  Total across periods: $15,000 ✓

Reconciliation Impact:
  January variance: Retro adjustment not yet posted
  February variance: Retro adjustment appears as bonus variance
  Cross-period reconciliation: Total correct
```

**Resolution Steps:**
1. Identify retro adjustment wage type and amount
2. Trace back to original payroll period
3. Verify GL posting in current month with adjustment journal
4. Confirm total across both periods equals correct payroll amount
5. Document as timing/retro adjustment reconciling item

**Acceptable?** YES - if corrected in following month, document as timing difference

### 2. Rounding Differences

Rounding differences occur when payroll aggregates amounts differently than GL posting.

#### 2a. Employee-Level vs GL-Level Rounding

**Description:**
Payroll calculates and rounds at employee level, GL consolidates and rounds at posting level,
resulting in minor rounding variances (typically $0.01 to $0.10).

**Cause:**
- Payroll calculates tax, FICA per employee (e.g., 6.2% × $1,234.56 = $76.54)
- Multiple employees' amounts are summed
- GL posts consolidated amount (sum of all employees)
- Rounding at two levels can cause minor variance

**Example:**
```
Payroll Calculation (Employee-level rounding):

Employee 1: $1,234.56 × 6.2% = $76.54 FICA
Employee 2: $2,345.67 × 6.2% = $145.43 FICA
Employee 3: $3,456.78 × 6.2% = $214.32 FICA
─────────────────────────────────────────────
Payroll Total: $436.29

GL Posting (Consolidated rounding):

Total Gross: $7,036.01
GL Amount: $7,036.01 × 6.2% = $436.2362 → GL posts $436.24

Variance: $436.29 (payroll) vs $436.24 (GL) = ($0.05) rounding difference
```

**Resolution Steps:**
1. Identify rounding variance (typically < $1.00)
2. Recalculate GL amount using consolidated gross
3. Verify variance = rounding at different aggregation levels
4. Compare to industry tolerance (typically $0.01 per employee)
5. Document as rounding reconciling item if within tolerance

**Acceptable?** YES - if variance < $0.01 × number of employees

#### 2b. Tax Calculation Table Rounding

**Description:**
IRS tax withholding tables round at different steps, causing minor variances when verified
against GL posting.

**Cause:**
- IRS W-4 tables have built-in rounding
- Different withholding methods (percentage vs fixed) round differently
- Aggregate GL posting may not match sum of individual employees' rounded amounts

**Example:**
```
Employee calculations use IRS Table 1 (2024):
  Weekly paycheck: $1,923.08
  Federal tax per table: $124.00 (per IRS rounding)
  50 employees × $124.00 = $6,200.00

GL posting aggregates directly:
  Total weekly payroll: $96,154.00 (50 × $1,923.08)
  Federal tax by formula: $96,154 × rate = $6,200.12 (before rounding)
  GL posts: $6,200.00

Variance: $0.12 due to table rounding methods
```

**Resolution Steps:**
1. Identify tax withholding variance
2. Verify IRS withholding tables are current
3. Compare table method (percentage vs fixed) impact
4. Recalculate using GL formula
5. Verify variance is acceptable IRS rounding tolerance

**Acceptable?** YES - if variance matches expected rounding tolerance per employee count

### 3. Retroactive Adjustments & Difference Documents

Retroactive adjustments use clearing accounts and difference documents to correct payroll
amounts in prior periods.

#### 3a. Difference Document Clearing

**Description:**
When payroll needs to post a correction for a prior period, SAP uses a difference document
that offsets the original posting and re-posts the correct amount.

**Cause:**
- Configuration error discovered after original payroll posting
- Employee data correction (e.g., wrong cost center, wrong tax status)
- Calculation error identified after close
- GL needs to show both reversal and correction

**Example:**
```
Scenario: Cost center assignment was wrong in January payroll

Original Posting (Jan):
  Wage Type 1000 (Salary): $100,000
  GL Account 6100: $100,000
  Cost Center: 1000 (INCORRECT - should be 2000)

Difference Document (Feb):
  Reversal: GL 6100 CC 1000 ($100,000) - reverses wrong posting
  Correction: GL 6100 CC 2000 $100,000 - posts correct allocation
  Difference Batch: Document number 1000010 (Jan payroll corrected in Feb)

GL Result:
  Jan GL 6100 CC 1000: $100,000 (before difference document)
                       -$100,000 (difference reversal)
                       = $0 (corrected)
  Feb GL 6100 CC 2000: +$100,000 (difference repost)

Cross-Period Reconciliation:
  Cost Center 1000: Variance in Jan ($100K), cleared by Feb difference doc
  Cost Center 2000: Additional $100K in Feb (difference document)
  Total GL posting: $100,000 (correct)
```

**Resolution Steps:**
1. Identify payroll difference documents (RPCPRRU0 shows source)
2. Trace original batch document
3. Compare reversal amount to original posting
4. Verify correction amount is accurate
5. Confirm variance resolved cross-period

**Acceptable?** YES - if difference document is complete and traced to original error

#### 3b. Clearing Account Reconciliation

**Description:**
Difference documents may post through clearing account (91xx series) that should net to zero.

**Cause:**
- SAP design posts reversals and corrections through clearing account
- Clearing account used as temporary holding for period-end reconciliation
- Clearing account balance should be zero or minimal after all adjustments

**Example:**
```
Clearing Account 9100 (Payroll Clearing):

Jan Payroll:
  Original incorrect posting flows through: +$100,000

Feb Difference Document:
  Reversal through clearing: -$100,000
  Correction reclassified: +$100,000 to correct GL account

Clearing Account Balance: $0 ✓

GL Reconciliation:
  Original GL account (1000): Reversed via clearing
  Correct GL account (2000): Posted via clearing
  Clearing account (9100): Nets to zero ✓
```

**Resolution Steps:**
1. Query GL account 9100 (Payroll Clearing)
2. Identify all reversals and corrections flowing through
3. Verify reversals and corrections net to zero
4. Trace clearing documents to payroll difference batches
5. Document as retro adjustment reconciling item

**Acceptable?** YES - if clearing account nets to zero or shows only pending items

### 4. Manual Journal Entries

Manual journal entries outside the payroll process can create reconciling items.

#### 4a. Accrual Reversals

**Description:**
Month-end payroll accruals are reversed in the first day of the following month
(standard accounting practice).

**Cause:**
- Payroll accrual on Jan 31 records estimated liability
- Reversal on Feb 1 reverses the accrual
- Feb 15 actual payroll posting replaces accrual with actual
- This creates temporary GL variance on Feb 1-14

**Example:**
```
Jan 31: Payroll Accrual
  Dr. GL 6100 (Payroll Expense): $1,000,000
  Cr. GL 2000 (Net Pay Liability): $1,000,000

Feb 1: Accrual Reversal
  Dr. GL 2000: $1,000,000
  Cr. GL 6100: $1,000,000
  (GL impact nets to zero for Feb 1-14 period)

Feb 15: Actual Payroll Posted
  Dr. GL 6100: $1,000,000
  Cr. GL 2000: $1,000,000
  (GL returns to normal)

GL Balance at Key Dates:
  Jan 31: +$1,000,000 (accrual)
  Feb 1: $0 (reversal nets accrual)
  Feb 15: +$1,000,000 (actual replaces accrual)
```

**Resolution Steps:**
1. Identify accrual reversal journal entry (typically document type ZA or ZB)
2. Trace to payroll accrual entry from prior period
3. Verify reversal amount equals accrual amount
4. Confirm actual payroll posting follows reversal
5. Document as timing reconciling item (accrual reversal)

**Acceptable?** YES - Standard month-end accrual reversal, document in reconciling items

#### 4b. Reclassification Entries

**Description:**
Manual reclassification entries move payroll amounts between GL accounts or cost centers
after payroll posting.

**Cause:**
- GL account mapping error discovered after payroll close
- Cost center reallocation (e.g., shared service reallocations)
- Department reorganization requiring retroactive reclassification
- Audit request requiring GL reclassification

**Example:**
```
Scenario: $50K of payroll posted to wrong GL account

Original Payroll Posting:
  GL 6100 (Wrong Account): $50,000

Manual Reclassification Entry:
  Dr. GL 6200 (Correct Account): $50,000
  Cr. GL 6100 (Wrong Account): $50,000

After Reclassification:
  GL 6100: $0 (corrected)
  GL 6200: $50,000 (correct)

Reconciliation:
  Total GL posting: Still $50,000 (correct)
  Reclassification entry: Document number 2000001 (manual entry)
```

**Resolution Steps:**
1. Identify reclassification journal entry
2. Trace original payroll posting that prompted reclassification
3. Verify reclassification amount equals original error
4. Confirm correct GL account is updated
5. Document as reclassification reconciling item

**Acceptable?** YES - if reclassification corrects a posting error and is approved

#### 4c. Audit Adjustments

**Description:**
External auditors may request GL adjustments for payroll-related items.

**Cause:**
- Auditor identifies GL posting that doesn't comply with GAAP
- Auditor requests reclassification (e.g., capitalized wages)
- Auditor identifies missing accrual
- Auditor requests GL adjustment for materiality

**Example:**
```
Scenario: Auditor identifies wages should be capitalized to equipment

Payroll Posted as Expense:
  Dr. GL 6100 (Payroll Expense): $100,000
  Cr. GL 2000 (Net Pay Payable): $100,000

Audit Adjustment:
  Dr. GL 1500 (Equipment Asset): $100,000
  Cr. GL 6100: $100,000

Result:
  GL 6100: $0 (reclassified to asset)
  GL 1500: $100,000 (capitalized)
  GL 2000: Still $100,000 (liability remains)
```

**Resolution Steps:**
1. Obtain audit adjustment proposal
2. Verify adjustment is within audit scope
3. Document business rationale
4. Post adjustment with appropriate approval
5. Document as audit adjustment reconciling item

**Acceptable?** YES - if approved by finance leadership and properly documented

### 5. Configuration Errors

Configuration errors can create systematic reconciling items that repeat monthly.

#### 5a. Wage Type to GL Account Mapping Error

**Description:**
Incorrect mapping between wage type and GL account, causing consistent monthly variance.

**Cause:**
- T52EL entry missing or incorrect GL account
- Symbolic account (KALSF) calculation rule error
- Multiple mapping entries causing ambiguous selection
- Configuration not updated after GL account restructuring

**Example:**
```
Configuration Issue:
  Wage Type 1000 (Salary) → GL Account 6100 (EXPECTED)
  But T52EL shows: Wage Type 1000 → GL Account 6999 (WRONG)

Monthly Impact:
  Payroll Wage Type 1000: $1,000,000 (should post to 6100)
  GL Account 6999: $1,000,000 (where it actually posts)
  GL Account 6100: $0 (should have posting, but doesn't)

Reconciliation Variance (repeats monthly):
  GL 6100: ($1,000,000) variance
  GL 6999: +$1,000,000 variance
```

**Resolution Steps:**
1. Query T52EL for wage type mapping
2. Verify KALSF (symbolic account) is correct
3. Check GL account is active and correct
4. Verify mapping priority if multiple entries exist
5. Correct T52EL entry and re-run payroll (off-cycle if needed)

**Acceptable?** NO - This is a configuration error, must be corrected

#### 5b. Cost Center Override Not Configured

**Description:**
Wage type should post to different cost center than employee assignment,
but override is not configured.

**Cause:**
- T52AB (Wage Type Cost Center) entry missing
- Employee grouping override (T52EM) not configured
- Manual cost center assignment not applied

**Example:**
```
Configuration Issue:
  Employee assigned to CC 1000
  Wage Type 401 (FICA-SS ER) should post to CC 9000 (shared overhead)
  But T52AB does not have override entry

Monthly Impact:
  Payroll: FICA-SS ER posts to CC 1000 (correct per config)
  GL: FICA-SS ER posts to CC 1000 (but should be CC 9000)
  Reconciliation: CC-level variance in employer tax allocation
```

**Resolution Steps:**
1. Identify wage types requiring cost center override
2. Check T52AB for existing overrides
3. Configure T52AB entry for wage type + new cost center
4. Test with employee sample
5. Re-run payroll (off-cycle) if needed to correct prior period

**Acceptable?** NO - Configuration error, must be corrected for consistent allocation

### 6. Unusual Items

#### 6a. Off-Cycle Payroll

**Description:**
Payroll run outside the regular monthly payroll cycle (e.g., employee separation, bonus).

**Cause:**
- Employee separation with final paycheck
- Special bonus or incentive payment
- Court-ordered garnishment
- Manual payroll correction

**Example:**
```
Regular Payroll: Jan 15 (monthly payroll)
  Total: $1,000,000

Off-Cycle Payroll: Jan 28 (separation payroll for terminated employee)
  Total: $25,000

GL Variance (Monthly):
  Regular payroll posts to Feb GL accounts (standard timing)
  Off-cycle payroll posts to Feb GL accounts
  Total GL posting: $1,025,000 (includes off-cycle)
  Monthly payroll: Only $1,000,000

Reconciliation:
  Payroll (regular): $1,000,000 ✓
  Payroll (off-cycle): $25,000 (separate reconciliation)
  GL Total: $1,025,000 ✓
```

**Resolution Steps:**
1. Identify off-cycle payroll runs in period
2. Separate reconciliation for off-cycle from regular payroll
3. Verify off-cycle processing dates
4. Trace GL postings for off-cycle batch
5. Document as separate off-cycle reconciliation

**Acceptable?** YES - if documented as separate reconciliation

## Reconciling Items Summary Table

| Item Type | Category | Example | GL Impact | Acceptable | Resolution |
|-----------|----------|---------|-----------|-----------|-----------|
| GL posting after period end | Timing | Jan payroll posts Feb 1 | Feb GL shows accrual | YES | Document timing |
| Check clearing delay | Timing | Checks clear 5 days later | Liability remains 5 days | YES | Document clearing timeline |
| Accrual reversal | Timing | Feb 1 reversal of Jan 31 accrual | Net zero Feb 1-14 | YES | Document as reversing entry |
| Retro adjustment | Timing/Retro | Jan error corrected in Feb | Cross-period correction | YES | Trace to original error |
| Difference document | Retro | Reversal + repost in clearing | Clearing nets to zero | YES | Verify clearing zero balance |
| Rounding variance | Rounding | Employee vs GL rounding | < $0.01 per employee | YES | Calculate tolerance |
| Tax table rounding | Rounding | IRS table rounding | < $0.10 per period | YES | Verify to IRS tables |
| Accrual entry | Manual JE | Month-end accrual | GL reverses Feb 1 | YES | Verify reversal entry |
| Reclassification | Manual JE | GL account error corrected | Corrects posting | YES | Verify approval |
| Audit adjustment | Manual JE | Auditor capitalization | GL reclassification | YES | Document audit request |
| Wage type mapping | Config Error | Wrong GL account | Systematic monthly variance | NO | Correct T52EL |
| Cost center override | Config Error | Missing override | CC-level variance | NO | Configure T52AB |
| Off-cycle payroll | Unusual | Separation payment | Separate GL posting | YES | Separate reconciliation |

## Best Practices for Reconciling Items

1. **Document All**: Record all reconciling items, even if small, for audit trail
2. **Root Cause Analysis**: Understand why each reconciling item exists
3. **Resolution Timeline**: Indicate if temporary (timing) or permanent (config error)
4. **Monthly Tracking**: Track recurring reconciling items to identify systemic issues
5. **Approval**: Have reconciling items reviewed and approved by supervisor
6. **Trending**: Plot reconciling items over time to detect deterioration
7. **Reference**: Trace reconciling items to supporting documentation (difference docs, JE docs)
8. **Escalation**: Escalate non-timing reconciling items for root cause correction
9. **Prevention**: Use reconciling items to identify process improvements
10. **Closeout**: Ensure all reconciling items are resolved before final month-end close

## References

- Reconciliation Methodology (reconciliation-methodology.md)
- GL Account Mapping Reference (gl-account-mapping.md)
- SAP RPCPRRU0 Report (Payroll GL Posting)
- SAP T-Codes: SM30 (Table Maintenance), FB04 (GL Account Inquiry)
