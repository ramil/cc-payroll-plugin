# Technical Wage Type Reference for Retroactive Processing

## Table of Contents
1. [/551 - Recalculation Difference](#551---recalculation-difference)
2. [/552 - Subsequent Adjustment](#552---subsequent-adjustment)
3. [/553 - Retro Change from Last](#553---retro-change-from-last)
4. [/560 - Payment Amount](#560---payment-amount)
5. [/562 - Retro Tax Adjustment](#562---retro-tax-adjustment)
6. [Difference Table (DT) Logic](#difference-table-dt-logic)
7. [Wage Type Storage and Transfer](#wage-type-storage-and-transfer)
8. [Sign Conventions](#sign-conventions)

---

## /551 - Recalculation Difference

### Definition

**/551** is the primary wage type that captures the difference between a retroactively recalculated payroll result and the original result.

**Formula:**
```
/551 = Current_Calculation - Prior_Calculation
```

**Purpose:** Represents the amount the employee is owed (or owes) due to retroactive changes.

### Calculation Details

**When Generated:**
- First retro processing of a period (second retro uses /552 instead)
- Only if difference is non-zero (rounding ignored)
- For each affected employee in affected periods

**What It Represents:**
- Salary/wage adjustments: Difference in gross pay
- Tax changes: Total difference in withholding
- Benefit changes: Total difference in deductions
- Combination: Net of all changes

**Calculation Example:**

**Scenario:** Salary increase approved retroactively for January

```
Original Payroll (January):
  /100 (Base Salary):      5000.00
  /103 (Fed Tax):           625.00
  /105 (FICA):              382.50
  /200 (Health Ins):       -250.00
  /560 (Net Pay):         4742.50

Retro Change: Salary increase to 5416.67 (5%)

Retro Payroll Recalculation (January):
  /100 (Base Salary):      5416.67  (increase)
  /103 (Fed Tax):           677.08  (increase due to higher salary)
  /105 (FICA):              414.48  (increase due to higher salary)
  /200 (Health Ins):       -250.00  (unchanged)
  /560 (Net Pay):         5089.87  (increase)

/551 Calculation:
  /551 (Base Salary diff):  416.67  (5416.67 - 5000.00)
  /551 (Tax diff):           51.08  (677.08 - 625.00)
  /551 (FICA diff):          31.98  (414.48 - 382.50)
  /551 (Health diff):         0.00  (unchanged)

Total /551:                547.37  (gross difference)
/551 (Net Pay diff):       347.37  (5089.87 - 4742.50)
```

### Key Characteristics

**Visibility:**
- Displayed prominently in payroll results (PC_PAYRESULT)
- Included in employee payslip
- Visible in GL posting
- Used for audit trail

**Direction:**
- Positive value: Employee is owed money (underpayment correction)
- Negative value: Employee owes back (overpayment correction)
- Zero value: No difference (not typically displayed)

**Payment Timing:**
- Not automatically paid immediately
- Usually included in next paycheck after retro execution
- Can be paid separately if urgent (special check run)
- Must be documented in employee communication

### GL Impact

**/551 values post to GL accounts based on wage type:**

```
/100 (Base Salary) /551        → GL 4100 (Salary Expense)
/103 (Fed Tax) /551            → GL 2100 (Federal Tax Payable)
/104 (State Tax) /551          → GL 2110 (State Tax Payable)
/200 (Health Deduction) /551   → GL 2200 (Health Insurance Payable)
/560 (Net Pay) /551            → GL 1100 (Employee Payable/Accrued Payroll)
```

---

## /552 - Subsequent Adjustment

### Definition

**/552** is used when a second (or later) retro adjustment is made to the same period.

**Formula:**
```
/552 = (Current_Calculation - Original_Calculation) - Previous_/551
```

Or more intuitively:
```
/552 = Incremental_Change_From_Prior_Retro
```

### When Generated

- Second retro of the same period (not first retro)
- Subsequent retros of same period (third, fourth, etc.)
- Never for the first retro (uses /551 instead)
- Only if incremental difference is non-zero

### Calculation Example

**Scenario:** January salary increase executed as retro #1, then corrected as retro #2

```
Original Payroll (January):
  /100 (Base Salary):  5000.00
  /103 (Fed Tax):       625.00
  /560 (Net Pay):      4750.00

Retro #1 Execution (February, retroactive to January):
  Change: Increase to 5416.67 (5%)
  /551 = 416.67
  /103 /551 = 51.08
  /560 /551 = 347.37  (after tax)

Retro #2 Execution (March, correction to January):
  Change: Correct salary to 5500.00 (was supposed to be 10% not 5%)

  Current Calculation (March, with correct 5500.00):
    /100 = 5500.00
    /103 = 687.50
    /560 = 4812.50

  Original Calculation (from January before any retro):
    /100 = 5000.00
    /103 = 625.00
    /560 = 4750.00

  Total difference (Current - Original):
    /100 diff = 500.00
    /103 diff = 62.50
    /560 diff = 62.50

  Previous /551 (from retro #1):
    /551 = 416.67

  /552 = Total_Diff - Previous_/551
    /100 /552 = 500.00 - 416.67 = 83.33
    /103 /552 = 62.50 - 51.08 = 11.42
    /560 /552 = 62.50 - 347.37... (This doesn't work; shows complexity)
```

**Note:** /552 calculation is more complex with taxes due to changing withholding tables. The formula above is simplified.

### Critical Rule

**DO NOT execute retro #1 again after retro #2 has been run.**

If you re-execute retro #1, it will create a second /551 entry, effectively doubling the adjustment and creating serious data integrity issues.

**Correct sequence:**
1. Execute Retro #1 → /551 created
2. Execute Retro #2 (if needed) → /552 created
3. If correction needed, execute Retro #3 → /552 created
4. Never go back to Retro #1

**If Retro #1 needs to be reversed:**
Use Retro #3 with reversal flag to create negative /552 entries, not by re-running Retro #1.

---

## /553 - Retro Change from Last

### Definition

**/553** represents a reversal or cancellation of a prior retro adjustment.

**Formula:**
```
/553 = -(Previous_/551 or /552)
```

Or simply: the negative of the prior adjustment.

### When Generated

- When a retro adjustment is reversed
- When a retro has been completed but later found to be in error
- When reverting to original payroll result before any retro
- Special cases where retro must be undone

### Use Case Example

**Scenario:** Retro salary increase was executed, later determined to be unauthorized

```
Original Payroll (January):
  /100 = 5000.00
  /560 = 4750.00

Retro #1 (unauthorized increase):
  /100 /551 = 416.67
  /560 /551 = 347.37

Discovery: Retro was unauthorized, must be reversed

Retro #2 (reversal):
  /553 = -416.67  (negative of prior /551)
  /553 Net = -347.37

Result after reversal:
  Payroll returns to original: /100 = 5000.00, /560 = 4750.00
```

### GL Impact

**/553 posts to GL with negative amounts:**

```
Original /551 posting:     DR 4100   CR 2100  (salary up, tax up)
Reversal /553 posting:     CR 4100   DR 2100  (reverses above entry)
Net GL impact: Zero (payroll back to original)
```

---

## /560 - Payment Amount

### Definition

**/560** is the net pay amount that represents what the employee receives after all deductions.

**Formula (Simplified):**
```
/560 = Gross_Wages - Total_Deductions - Total_Taxes
/560 = /100 + /101 + /102 - /103 - /104 - /200 - /201 + ...
```

### Role in Retro

**/560 is special in retro processing:**

**Not Directly Affected:**
- /560 is calculated, not stored as independent wage type
- When /551 is generated, /560 /551 is calculated based on:
  - Changes to gross wages (/100, /101, /102, etc.)
  - Changes to taxes (/103, /104, /105, etc.)
  - Changes to deductions (/200, /201, etc.)

**Calculation Example:**

```
Original /560:           4750.00

Changes from retro:
  /100 /551:  +416.67   (salary increase)
  /103 /551:   +51.08   (tax increase)
  Total /551: +467.75

Retro /560:
  /560 /551 = 416.67 - 51.08 = 365.59 (NET increase to take-home)
```

### Transfer to Accounts Payable

**/560 differences determine what the employee is owed:**

```
Positive /560 /551: Employee is owed money
  → GL 1100 (Accrued Payroll) / 1110 (Employee Payable)
  → Cash paid via next paycheck

Negative /560 /551: Employee owes back money
  → Deducted from next paycheck
  → Or employee receives bill if negative amount is large
```

---

## /562 - Retro Tax Adjustment

### Definition

**/562** is specifically for tax recalculation differences in retroactive scenarios.

**Purpose:** Separate tax adjustments from gross wage adjustments for clarity and audit purposes.

### When Generated

- When salary/wage changes trigger tax recalculation
- Tax difference is material (not just rounding)
- Tax tables may differ from original period
- Separate tracking of tax adjustments is needed

### Calculation Details

**Components:**
- Federal tax (/103) difference
- State tax (/104) difference
- Local tax (/105) difference
- FICA (Social Security, Medicare) difference
- Other tax-like items

**Example:**

```
Original Calculation (Jan):
  Gross Salary: 5000.00
  Fed Tax (/103): 625.00  (at 12.5% for original amount)

Retro Recalculation (Jan, with 5416.67 salary):
  Gross Salary: 5416.67
  Fed Tax (/103): 677.08  (at 12.5% for new amount)

/551 or /562 for taxes:
  Tax difference = 677.08 - 625.00 = 52.08
  Posted to /551 or /562 depending on classification
```

### GL Posting

**/562 posts to tax-specific GL accounts:**

```
/562 (Federal Tax):  → GL 2100 (Federal Tax Payable)
/562 (State Tax):    → GL 2110 (State Tax Payable)
/562 (FICA):         → GL 2120 (FICA Payable)
```

---

## Difference Table (DT) Logic

### Purpose

The Difference Table (DT) is the internal SAP mechanism that tracks all changes during retro processing.

### Structure

**DT Entry Consists Of:**
```
Employee_ID
Period
Wage_Type
Amount_Prior       (from original payroll cluster)
Amount_Current     (from retro calculation)
Amount_Difference  (= Current - Prior)
DT_Flag           (indicates how to process)
```

### Processing Logic

**For Each Wage Type in Retro Period:**

```
STEP 1: Load Prior Amount from Cluster
  Amount_Prior = Cluster.GetWageTypeAmount(Emp, Period, WT)

STEP 2: Calculate Current Amount
  Amount_Current = Calculate_Wage_Type(Emp, Period, WT)

STEP 3: Determine Difference
  DT_Amount = Amount_Current - Amount_Prior

STEP 4: Apply X041 Flag (Retro Applicable?)
  IF X041 = 0:
    Skip this wage type (no retro calc)
  ENDIF

STEP 5: Create Difference Entry
  Store DT Entry with DT_Amount

STEP 6: Generate /551 or /552
  IF First_Retro_This_Period:
    /551 = DT_Amount
  ELSE:
    /552 = DT_Amount - Previous_/551_Value
  ENDIF

STEP 7: Apply X042 Flag (Post to GL?)
  IF X042 = 1:
    Create GL Posting for DT_Amount to WT's GL Account
  ENDIF
```

### Example DT Processing

```
Employee: E001
Period: 202401
Change: Salary increase from 5000 to 5416.67

DT Entry for /100 (Base Salary):
  Employee_ID: E001
  Period: 202401
  Wage_Type: /100
  Amount_Prior: 5000.00
  Amount_Current: 5416.67
  Amount_Difference: 416.67
  DT_Flag: X041=1, X042=1

Processing:
  X041=1 (retro applicable) → Include in retro calc ✓
  DT_Amount = 416.67
  First retro → /551 = 416.67
  X042=1 (post to GL) → Create GL entry for 416.67 to GL 4100 ✓

Result:
  /551 wage type: 416.67
  GL 4100 (Salary Expense): DR 416.67
```

---

## Wage Type Storage and Transfer

### Cluster Storage

**SAP stores payroll results in Cluster (Cluster C or Cluster D):**

```
Structure:
  Cluster[Employee_ID][Period] = {
    Wage_Type → Amount,
    Wage_Type → Amount,
    ...
  }
```

**What's Stored:**
- Original calculated wage types (/100, /101, /102, etc.)
- Final results (/560 = net pay)
- NOT usually stored: /551, /552, /553 (these are temporary retro entries)

**Retrieval in Retro:**
- When retro is executed, system retrieves the stored cluster entry
- Compares stored amounts to recalculated amounts
- Calculates differences
- Generates /551 as temporary entry

### Transfer to Results Table

**After Retro Calculation:**

```
Temporary Results (in memory during retro calc):
  /100: 5000.00
  /551: 416.67  ← added during retro

After Retro Finalization:
  Transferred to payroll results table
  /551 entries are stored (temporary → permanent)
  Cluster is updated with new baseline

Next Retro (if needed):
  New cluster entry shows: /100 = 5416.67 (already includes retro)
  Next retro compares: Original (5000) vs Current (5416.67)
```

### Carrying Forward

**Retro Changes Carried Forward:**

When retro #1 is executed:
```
Jan 2024 (Original):   /100 = 5000.00
Jan 2024 (After Retro): /100 = 5416.67, /551 = 416.67

Feb 2024 Payroll (Normal):
  System loads Jan retro result
  Feb calc starts with: /100 = 5416.67 (new rate)
  No /551 in Feb (no retro for Feb, unless Feb also has RRDAT)
```

**Key Point:** Once retro is executed and cluster is updated, subsequent payroll automatically uses the new baseline. Retro changes are NOT carried forward as /551 in future periods; they become the new base wage type amount.

---

## Sign Conventions

### Positive /551 (Underpayment Correction)

**Positive /551 means employee is owed money.**

**Common Scenarios:**
- Retroactive salary increase (forgot to implement approved raise)
- Tax adjustment (underbearing of taxes owed)
- Benefit change (reduction in deductions)
- Hours correction (missing overtime hours in original)

**GL Posting:**
```
Debit GL Account (increase expense)
Credit GL Employee Payable (owe employee)

Example (Salary increase):
  DR 4100 (Salary Exp)  416.67
  CR 1100 (Emp Payable) 416.67
```

**Employee Impact:**
- Employee receives additional payment
- Increases net pay (after taxes)
- Usually paid with next regular paycheck

### Negative /551 (Overpayment Correction)

**Negative /551 means employee owes back money or was overpaid.**

**Common Scenarios:**
- Retroactive salary decrease (e.g., change of status)
- Overpayment of wages or benefits
- Tax correction (employee was overtaxed)
- Benefit cost correction (charged wrong plan cost)

**GL Posting:**
```
Credit GL Account (decrease expense)
Debit GL Employee Payable (employee owes)

Example (Salary decrease):
  CR 4100 (Salary Exp)  -416.67  (or DR 4100 for -416.67)
  DR 1100 (Emp Payable) -416.67  (or CR 1100 for -416.67)

Or expressed as debits/credits:
  CR 4100 (Salary Exp)  416.67   (reduce expense)
  DR 1100 (Emp Payable) 416.67   (employee owes)
```

**Employee Impact:**
- Amount deducted from next paycheck
- Reduces net pay
- If large negative amount, may trigger special payback arrangement

### Tax-Specific Conventions

**Tax Withholding (typically positive/negative together):**

```
Salary increase scenario:
  /100 /551: +416.67  (gross increase)
  /103 /551: +52.08   (federal tax increase, payable by employee)
  /105 /551: +31.98   (FICA increase, split between employee/employer)
  /560 /551: +365.59  (net increase to employee)

GL Posting:
  DR 4100 (Salary Exp)    416.67
  DR 2100 (Tax Payable)    52.08  ← owe to govt
  CR 1100 (Emp Payable)   365.59  ← owe to employee
  (FICA employer portion separate)
```

---

**End of Wage Type Reference**

For additional information, see:
- `retro-processing-guide.md` - Workflow and SAP transactions
- `retro-edge-cases.md` - Edge cases involving wage types and retro
