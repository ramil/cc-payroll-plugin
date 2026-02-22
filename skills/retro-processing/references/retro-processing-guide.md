# Comprehensive Retroactive Payroll Processing Guide

## Table of Contents
1. [How Retroactive Accounting Works](#how-retroactive-accounting-works)
2. [SAP Retro Workflow](#sap-retro-workflow)
3. [Key SAP Transactions](#key-sap-transactions)
4. [Sub-Schema XRRO Processing](#sub-schema-xrro-processing)
5. [PCR Rules for Retro](#pcr-rules-for-retro)
6. [Payroll Driver Flags](#payroll-driver-flags)
7. [Post-Retro Validation](#post-retro-validation)

---

## How Retroactive Accounting Works

### RRDAT (Retro Record Date)

The **RRDAT** (Retroactive Record Date) is the core concept in SAP retroactive accounting. It defines the date range for which a retroactive change is applied.

**Key Characteristics:**
- **Effective Retroactively**: A change made in the current period can affect payroll results for periods in the past
- **Not a Posting Date**: RRDAT is when the change became effective, NOT when it was processed
- **Links Periods**: Connects the "change request period" to the "retro period" (period being affected)
- **Stored in Cluster**: RRDAT information is stored in payroll cluster (Cluster_C or Cluster_D)

**Example:**
- Today: March 2024
- Employee receives salary increase approval effective: January 2024
- RRDAT = January 2024
- Retro periods: January, February (to catch up with the increase)

### ERA and EPRA

**ERA (Earliest Retro Accounting)**: The earliest period for which retroactive changes are allowed
- Typically set as a company policy (e.g., previous 12 months)
- Prevents retro adjustments beyond reasonable historical limits
- Configured per payroll area

**EPRA (Earliest Period for Retro Accounting)**: The earliest period allowed for each employee
- Can be overridden per employee for special situations
- Stored in infotype 0008 (Employee Details)

### For-Period vs In-Period Processing

**For-Period Retro:**
- Change is applied for the target period retroactively
- Original payroll run for that period is recalculated
- Results in complete recalculation of all wage types
- Generates /551 wage type for differences
- Example: January payroll recalculated in March

**In-Period Retro:**
- Change is applied within the same period it's made
- No retro recalculation needed
- Adjustment is made as a regular payroll transaction
- Does not generate /551 wage type
- Example: Correcting January payroll in January

### Difference Calculation

When a retro change is executed, SAP calculates difference (DT) values:

```
DT = Current_Calculation - Prior_Calculation
```

**For Each Wage Type:**
- Prior calculation: Result from original payroll run (stored in cluster)
- Current calculation: Result from retro recalculation (newly computed)
- Difference: Posted to employee's account as /551, /552, or /553

**Difference Posting Logic:**
1. First retro of a period: Use /551 wage type
2. Subsequent retro of same period: Use /552 (Subsequent Adjustment)
3. Reversal of retro: Use /553 (Retro Change from Last)

---

## SAP Retro Workflow

The standard workflow for retroactive payroll processing in SAP Payroll follows these steps:

### 1. Identify Triggers

**Common retro triggers:**
- Salary increase/decrease effective retroactively
- Organizational change (cost center, department, company code)
- Tax status change (filing status, exemptions, jurisdiction)
- Benefit plan change (enrollment, plan election change)
- Termination correction or reinstatement
- Time ticket entry or correction
- Master data corrections (wage type configuration, GL account mapping)

**Business process:**
- HR/Management submits retro request with justification
- Payroll analyst verifies change request details
- Confirm affected employee list with HR
- Determine retro effective date (RRDAT)
- Identify all periods requiring recalculation

### 2. Review Pending Changes

**In SAP, use transaction PU03:**
- Navigate: SAP Menu → Human Resources → Payroll → Germany (or applicable payroll area) → Periodic Activities → Retro Accounting → Edit Retro Accounting Records
- Display pending RRDAT entries by employee
- Verify change details match business request
- Confirm affected periods are listed correctly
- Check that change data (wage type, GL account, etc.) is complete

**Key data to review:**
- Employee ID and name
- RRDAT (retroactive effective date)
- Change type (wage type change, org change, etc.)
- Prior values vs. new values
- Affected periods
- Master data versions being used

### 3. Simulate Retro Impact

**Simulation is CRITICAL before actual execution.**

**Use transaction PC00_M10_CALC_SIMU (Simulation):**
- Navigate: SAP Menu → Human Resources → Payroll → Payroll Control Center (PCC)
- Select relevant payroll area, company code
- Enter retro period range (from earliest retro period to current period)
- Run in simulation mode (execute checkbox unchecked)
- Do NOT check "Final" checkbox

**Expected outputs from simulation:**
- Recalculated payroll results for retro periods
- /551, /552, /553 wage types showing differences
- Tax recalculation for affected periods
- GL difference postings

**Analysis steps:**
- Compare simulation results to prior payroll runs
- Validate /551 calculations are mathematically correct
- Check that affected wage types match expectations
- Verify GL postings are routed to correct accounts
- Confirm tax recalculation is accurate (no overpayment/underpayment)
- Run this tool's impact analysis on simulation results vs. prior

### 4. Execute Retro Processing

**Once simulation is approved, execute actual retro:**

**Use transaction PC00_M10_CALC:**
- Navigate: SAP Menu → Human Resources → Payroll → Payroll Control Center (PCC)
- Select same settings as simulation
- Uncheck simulation mode
- Run payroll calculation
- Commit results (cannot undo after this step)

**System operations:**
- Locks payroll cluster to prevent concurrent modifications
- Recalculates all wage types for affected periods
- Generates new payroll results
- Creates difference postings
- Updates cluster with new baseline for future retros

### 5. Validate Retro Results

**Immediate post-retro validation (within 1 hour of execution):**

**Use transaction PC_PAYRESULT (Payroll Results):**
- Navigate: SAP Menu → Human Resources → Payroll → Germany (or applicable) → Payroll Results
- Display payroll results for retro period
- For each affected employee:
  - Verify /551 wage type is present (first retro) or /552 (subsequent retro)
  - Check that /551 value equals calculated difference
  - Confirm all affected wage types changed correctly
  - Validate net pay change matches business expectation

**GL posting validation:**

**Use transaction RPCLGA09 (Difference GL Report):**
- Navigate: SAP Menu → Accounting → General Ledger → Information System → Additional Reports → Difference GL Report
- Select retro posting period
- For each affected GL account:
  - Verify difference amount is present
  - Confirm account number is correct
  - Check amount direction (debit/credit)
  - Validate business justification (salary expense, tax withholding, etc.)

---

## Key SAP Transactions

### PU03 - Edit Retro Accounting Records

**Purpose:** View and modify retroactive accounting entries

**Navigation:** HRIS → Payroll → [Payroll Area] → Periodic Activities → Retro Accounting

**Key functions:**
- Display all RRDAT records for an employee
- Create new RRDAT entries (rarely used; usually created via HR master data changes)
- Delete RRDAT entries (requires approval)
- Review change details before processing

**Example usage:**
```
Employee: E001
Display all retro entries
RRDAT January 2024: Salary increase to $75,000 (from $70,000)
Affected periods: January, February, March
Change details: /100 (Base Salary) changed
```

### PC00_M10_CALC - Payroll Calculation

**Purpose:** Run payroll calculation (normal or retro)

**Navigation:** HRIS → Payroll → PCC (Payroll Control Center)

**Parameters:**
- Payroll area, company code, employee range
- Period range (for retro, include all affected periods plus current)
- Retro flag (auto-detected if RRDAT records exist)
- Simulation mode (check = simulation only, uncheck = execute)
- Final flag (check = commit results permanently)

**In retro mode:**
- System automatically detects RRDAT records
- Calculates retro for all periods from earliest RRDAT to current
- Generates /551 wage types for differences
- No additional parameters needed

### PC00_M10_CALC_SIMU - Payroll Simulation

**Purpose:** Run payroll calculation in simulation mode only

**Navigation:** HRIS → Payroll → PCC → Simulation Mode

**Difference from PC00_M10_CALC:**
- Forced simulation mode (never commits)
- Creates temporary result set
- Does not lock cluster
- Results are deleted after session ends
- Safe to run multiple times for testing

**Typical usage:**
1. Run simulation first to preview results
2. Review results thoroughly
3. If OK, proceed to PC00_M10_CALC for actual execution
4. If issues found, correct master data and re-simulate

### PC_PAYRESULT - Payroll Results Review

**Purpose:** View detailed payroll calculation results

**Navigation:** HRIS → Payroll → [Payroll Area] → Information → Payroll Results

**Displays:**
- Complete wage type breakdown per employee per period
- Net pay calculation
- Deduction details
- Tax calculations
- /551, /552, /553 differences (if retro was processed)

**Retro-specific review:**
- Check /551 values for first retro
- Check /552 values for subsequent retro
- Verify recalculated wage types are correct
- Validate that differences match expected amounts

### RPUAUD00 - Retro Audit Trail

**Purpose:** View audit trail of all retro processing activities

**Navigation:** HRIS → Payroll → [Payroll Area] → Information → Audit Trails → Retro Audit

**Shows:**
- When retro was executed
- Who executed it
- Which periods were affected
- Which RRDAT records were processed
- What changes were made to cluster
- GL postings that resulted

### RPCLGA09 - Difference GL Report

**Purpose:** Report on difference GL postings

**Navigation:** HRIS → Accounting → GL → Information System → GL Reports → Difference GL

**Reports:**
- All difference postings for a period
- Grouped by GL account
- Grouped by cost center
- Grouped by cost element
- By posting date

**Retro analysis use:**
- Reconcile difference amounts to /551 totals
- Identify GL accounts with unexpected postings
- Validate GL account coding is correct

---

## Sub-Schema XRRO Processing

The XRRO (Retro Processing) sub-schema is a special SAP sub-schema that handles retroactive payroll recalculation.

### Processing Sequence

**Cluster Processing Order (Normal Payroll):**
1. XPRE (Pre-processing): Validates input, prepares wage data
2. XCAL (Calculation): Computes wage types
3. XPOST (Post-processing): Finalizes results, creates postings
4. XDEL (Delivery): Transfers results to HR module and Accounting

**With XRRO (Retro) Active:**
1. XPRE: Validates retro request, loads prior payroll result from cluster
2. XRRO: **Retro sub-schema** - compares prior vs. current, calculates differences
3. XRET: Retro continuation - processes difference wage types (/551, /552, /553)
4. XPOST: Creates difference postings to GL
5. XDEL: Updates cluster with new baseline

### Difference Calculation in XRRO

**XRRO sub-schema performs:**

1. **Load Prior Result:**
   - Reads cluster entry for retro period
   - Retrieves all wage type values from original payroll run
   - Restores employee status as of retro period

2. **Recalculate Current:**
   - Runs full payroll calculation with current master data
   - Applies all wage type rules (PCR)
   - Computes updated wage type values
   - Applies current tax tables, rates, etc.

3. **Calculate Difference (DT):**
   - DT = Current_Value - Prior_Value for each wage type
   - Creates difference table entry
   - Sets sign convention (positive = increase, negative = decrease)

4. **Generate /551, /552, /553:**
   - /551 for first retro (DT directly)
   - /552 for subsequent retro (DT - previous /551)
   - /553 for reversal (negative of DT)

5. **Adjust for Tax:**
   - Recalculate taxes on retroactive changes
   - Create separate /552 or /562 entries for tax differences
   - Ensure tax withholding is accurate

### Storage in Cluster

After XRRO processing, the cluster is updated with:

**New Baseline:**
- Current wage type values become new baseline
- Cluster entry timestamp is updated
- RRDAT flag is removed (no longer pending)

**Historical Record:**
- Prior payroll result is archived (may be purged after retention period)
- Retro execution log is stored
- Audit trail records retro timestamp, user ID, changes made

---

## PCR Rules for Retro

PCR (Payroll Control Record) rules determine how wage types are calculated during retroactive processing.

### X041 - Retro Applicable Flag

**Purpose:** Determines if a wage type is eligible for retro calculation

**Rule Logic:**
```
IF retro flag is active AND
   X041 flag = "1" (retro applicable)
THEN
   Include this wage type in retro calculation
ELSE
   Skip this wage type (use prior value without recalculation)
END
```

**Common configurations:**
- **X041 = 1:** Standard wage types (/100, /101, /102, /103, /104, etc.)
  - These are recalculated during retro
  - Differences flow to /551

- **X041 = 0:** One-time payments, manual adjustments
  - NOT recalculated during retro
  - Kept as-is from prior payroll

**Example:**
- /100 (Base Salary): X041 = 1 → Recalculated
- /110 (Bonus): X041 = 1 → Recalculated
- /120 (One-time payment): X041 = 0 → NOT recalculated

### X042 - Difference Posting Flag

**Purpose:** Controls how differences are posted to GL

**Rule Logic:**
```
IF retro flag is active AND
   X042 flag = "1" (post differences)
THEN
   Create GL posting for /551 difference amount
   Route to GL account specified in wage type
ELSE
   Do NOT create GL posting
   Accumulate in /551 but do not post
END
```

**Common configurations:**
- **X042 = 1:** Wage types with GL impact
  - /100 (Salary): Post to expense account 4100
  - /103 (Tax): Post to liability account 2100
  - /200 (Deductions): Post to deduction account 2200

- **X042 = 0:** Internal wage types without direct GL posting
  - /560 (Payment): Not posted separately
  - /551 itself: May not post (handled separately)

### X043 - Blocking Flag

**Purpose:** Prevents retro processing for specific wage types or conditions

**Rule Logic:**
```
IF X043 flag = "1" (blocked)
THEN
   Do NOT process this wage type in retro
   Raise warning or error
ELSE
   Include in retro processing
END
```

**Use cases:**
- Wage types with special handling requirements
- Wage types not yet configured for retro
- Wage types with known data quality issues
- Temporary blocking during system maintenance

---

## Payroll Driver Flags

Payroll driver flags are settings that control retro execution behavior at the employee and payroll area level.

### RETRO Flag (Payroll Area)

**Location:** HRIS → Payroll → [Payroll Area] → Settings → Retro Flag

**Options:**
- **Active (1):** Retro processing is enabled for this payroll area
- **Inactive (0):** Retro processing is disabled (no RRDAT records will be processed)

**Impact:**
- If inactive, the payroll driver will ignore any RRDAT records
- System will warn if attempting retro with flag inactive
- Used to temporarily disable retro (e.g., during maintenance)

### ERA (Earliest Retro Accounting)

**Location:** HRIS → Payroll → [Payroll Area] → Settings → ERA

**Definition:** Earliest period for which retro changes are allowed company-wide

**Typical setting:** 12 months (e.g., if current month is March 2024, ERA allows retro back to March 2023)

**Configuration:**
```
Company Code: 1000
Payroll Area: 01 (Germany)
ERA: 202303 (March 2023)
Current Period: 202403 (March 2024)
Retro allowed: March 2023 - March 2024 (12 months)
Retro blocked: Before March 2023
```

**Override capability:**
- Can be overridden per employee in infotype 0008
- Requires documented business justification
- Audit trail records override authorization

### Retro Lock Flags

**Infotype 0008 (Employee Settings):**
- **EPRA (Earliest Period for Retro Accounting):** Earliest period allowed for this employee
- **RRDA (Retro Processing Lock):** If set, blocks all retro for this employee

**Use case:**
```
Employee: E001
Lock all retro after separation
RRDA lock set on termination date
Subsequent retro requests for this employee are rejected
```

---

## Post-Retro Validation

After executing retro payroll, a comprehensive validation checklist must be completed.

### Validation Checklist

#### 1. Payroll Results Validation

**Check in PC_PAYRESULT:**
- [ ] All affected employees have /551 or /552 wage types
- [ ] /551 amounts are non-zero (indicating changes)
- [ ] Changed wage types match business justification (e.g., /100 changed for salary increase)
- [ ] Net pay (/560) change is positive or negative as expected
- [ ] No unexpected wage types changed

**Sample output:**
```
Employee: E001
Period: 202401 (January 2024)
/100 (Base Salary): Prior 5000.00, Current 5416.67 (5% increase)
/551 (Retro Difference): 416.67 (= 5416.67 - 5000.00)
```

#### 2. Tax Validation

**Check in PC_PAYRESULT:**
- [ ] Federal tax (/103) recalculated (if salary changed)
- [ ] State tax (/104) recalculated (if applicable)
- [ ] FICA taxes correct (if applicable)
- [ ] No overpayment or underpayment of taxes
- [ ] Tax difference wage types (/552, /562) are present if tax changed

**Validation formula:**
```
Prior_Tax = Original_Tax_From_Period
Current_Tax = Tax_On_Recalculated_Wage
Tax_Difference = Current_Tax - Prior_Tax
Expected_/552 = Tax_Difference (approximately)
```

#### 3. GL Impact Validation

**Check in RPCLGA09:**
- [ ] Difference postings are present for affected accounts
- [ ] Total difference amounts match /551 + /552 totals
- [ ] GL accounts are correct (no postings to wrong accounts)
- [ ] Debit/credit direction is correct (positive/negative amounts)
- [ ] Posting amounts reconcile to employee results

**Reconciliation formula:**
```
SUM(GL_Differences) = SUM(Employee_/551) + SUM(Employee_/552) ± Rounding
(Should be equal, within rounding tolerance)
```

#### 4. Cost Center Allocation

**Check in RPCLGA09 or cost center report:**
- [ ] Cost center allocation is correct
- [ ] Employees are assigned to right cost centers
- [ ] Org changes are reflected (if applicable)
- [ ] Cost center amounts reconcile to employee totals

#### 5. Payroll Journal Entry

**Check in FI module:**
- [ ] Payroll interface created GL entry
- [ ] Entry is in correct posting period
- [ ] Entry amount matches GL differences total
- [ ] Entry is in correct company code

**Sample entry:**
```
Posting Date: 20240331 (posting period for retro)
GL Account 4100 (Salary Expense)    DR  2500.00
GL Account 2100 (Tax Liability)     CR    625.00
GL Account 2200 (Benefits Payable)  CR    500.00
GL Account 1100 (Employee Payable)  CR  1375.00
Cost Center: 4100 (or per employee allocation)
```

#### 6. Payroll Run Sequence Validation

**Check payroll history:**
- [ ] All retro periods have been recalculated
- [ ] Retro runs are in correct sequence (earliest first)
- [ ] No gaps in retro period coverage
- [ ] Current period payroll includes retro results

**Example valid sequence:**
```
Original payroll: Jan 2024 (no retro)
Original payroll: Feb 2024 (no retro)
Original payroll: Mar 2024 (no retro)
[Retro request for Jan effective increase]
Retro run 1: Jan 2024 (recalculate with new rate)
Retro run 2: Feb 2024 (recalculate with new rate)
Retro run 3: Mar 2024 (recalculate with new rate)
New payroll: Apr 2024 (includes retro results)
```

#### 7. Employee Communication

**Actions to take:**
- [ ] Send retro notification to affected employees
- [ ] Provide payslip showing retro adjustment (/551 amount)
- [ ] Explain reason for retro (salary increase, correction, etc.)
- [ ] Provide payment timing for retro amount
- [ ] Answer employee questions about adjustment

**Sample notification:**
```
Subject: Retroactive Payroll Adjustment

Dear E001,

Your payroll for January 2024 has been retroactively adjusted due to a salary
increase approved effective January 1, 2024.

Adjustment Details:
- Previous payroll: $5,000.00
- Retroactive increase: 5% ($416.67)
- Total adjusted pay: $5,416.67
- Retro adjustment (/551): $416.67

Taxes have been recalculated accordingly. You will receive payment of the $416.67
adjustment in your April 2024 paycheck.

Questions? Contact Payroll Department.
```

#### 8. Regulatory Compliance

**Actions to take:**
- [ ] Verify retro is compliant with local labor laws
- [ ] Confirm wage and hour requirements are met (if hourly)
- [ ] Verify tax adjustments comply with IRS rules
- [ ] Check for equal pay requirements (if applicable)
- [ ] Document business justification for audit trail

#### 9. Audit Trail Documentation

**Records to maintain:**
- [ ] Original payroll results (before retro) - archived
- [ ] RRDAT records showing effective dates and changes
- [ ] Retro execution log (timestamp, user, system settings)
- [ ] Simulation results (compared to actual execution)
- [ ] GL posting documentation
- [ ] Employee communication (notifications, approvals)
- [ ] Sign-off by payroll manager and finance

---

**End of Guide**

For additional information, see:
- `retro-wage-types.md` - Technical wage type reference
- `retro-edge-cases.md` - Edge case catalog and resolution procedures
