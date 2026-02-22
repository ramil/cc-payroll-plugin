# Common Payroll Procedures & SOPs

Step-by-step standard operating procedures for the most common payroll tasks in SAP PCC.

---

## 1. Running Production Payroll in PCC

### Pre-Run Checklist (Day Before or Start of Payroll)

- [ ] **Verify payroll area status** (PRAA transaction): Should be "Open"
- [ ] **Confirm payroll period**: Month/year correct? All pay dates included?
- [ ] **Time data transfer**: Run time interface job (SM37); confirm time records loaded for all time-relevant employees
- [ ] **HR changes processed**: New hires, terminations, job changes all entered in SAP (PA30) with correct effective dates
- [ ] **Tax/bank updates**: Any W-4 changes, W-4C forms, new direct deposit accounts entered (IT0210, IT0009, IT0208)
- [ ] **Verify no date gaps**: PA20 spot-check 5-10 employees for continuous infotype coverage
- [ ] **Back up current payroll results** (if re-running): Document prior run details in case needed for rollback
- [ ] **Notify team**: Slack/email to confirm no one else running payroll simultaneously

### Step-by-Step Payroll Execution

**Step 1: Start Payroll Simulation** (Highly Recommended)
1. Open SAP Fiori app "Process Payroll" (or SAP Easy Access: PC00_M10_CALC)
2. **Select Payroll Area**: Choose area (e.g., "US0001" for US Payroll)
3. **Select Period**: Enter period (e.g., "01/2025" for January 2025)
4. **Select Run Type**:
   - "A" = Regular payroll (standard monthly/bi-weekly run)
   - "B" = Additional (off-cycle bonus, correction)
   - "C" = Correction (re-run of prior period)
5. **Select Mode**: Choose "SIMULATE" (test run; no results saved)
6. **Start**: Click "Start" button

**Step 2: Review Simulation Results**
1. Wait for run to complete (monitor SM37 if long-running)
2. Open PC_PAYRESULT to view results
3. **Check Summary**:
   - Total employees: Does count match expected?
   - Total gross wages: Does it align with prior period ± expected changes?
   - Total taxes: Do withholdings look reasonable?
   - Total net pay: Does it equal (gross - taxes - deductions)?
4. **Spot-Check 5-10 Employees**: Click into individual employee results
   - Is gross amount correct (salary, hourly × hours)?
   - Are taxes calculated (federal, OASDI, Medicare, state)?
   - Are deductions present (benefits, garnishments)?
   - Is net pay positive (not negative)?
5. **Check Alerts** (PC_PAYRESULT → Alert tab):
   - "Missing Tax Data": Any employees flagged? Resolve before production.
   - "Negative Net Pay": Any employees? Investigate/fix.
   - "Missing Bank Details": Any? Ask employees for bank info.
   - Other alerts: Review/resolve.

**Step 3: Resolve Any Issues Found in Simulation**

*If critical alerts found* (missing tax data, negative net pay, major wage discrepancy):
1. **Identify root cause**: Check PA20 for employee infotypes
2. **Correct in PA30**: Update IT0210 (tax), IT0015 (adjustments), bank details, etc.
3. **Re-run simulation**: PC00_M10_CALC again to verify fix worked
4. **Repeat until clean**: No critical alerts, results look reasonable

*If minor discrepancies* (within 1-2%):
- Document issue
- Proceed to production if acceptable
- Note for investigation in next cycle

**Step 4: Run Production Payroll** (Once Simulation Approved)
1. Repeat Steps 1-2 above, but in Step 5, select mode: "PRODUCTION"
2. System changes payroll area status from Open → Locked (during run)
3. Wait for completion
4. Open PC_PAYRESULT; perform same spot-check as Step 2
5. Confirm results match simulation (should be identical unless data changed)

### Post-Run Validation

- [ ] **Generate DME file** (preliminary): PC00_M10_CDTA
  - Verify bank account count = expected employee count
  - Spot-check routing numbers and account numbers
  - Confirm total payment amount = total net pay
- [ ] **Generate payslips**: PC00_M10_CEDT
  - Verify format (all required fields visible)
  - Spot-check 3-5 payslips for accuracy
- [ ] **GL posting preview**: PC_PAYRESULT → GL Posting tab
  - Verify cost centers; allocations reasonable
  - Confirm GL posting balances (debit = credit)
- [ ] **Release payroll area**: PU03 transaction
  - Change status from Locked → Released
  - This allows GL posting and DME file to proceed

### Payroll Release Checklist

Before clicking "Release", confirm:
- [ ] All payroll results reviewed and validated
- [ ] No critical alerts remaining
- [ ] Payslips reviewed (spot-check)
- [ ] DME file generated and validated
- [ ] GL posting preview reviewed with Finance
- [ ] Payroll team sign-off obtained
- [ ] Any last-minute changes from HR processed and re-run confirmed

### Common Issues & Fixes

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Time data not loaded | Time transfer job didn't run or failed | Check SM37; re-run time interface job |
| Missing tax data alert | IT0210 not created for new hire | Create IT0210 (PA30); re-run payroll |
| Negative net pay | Garnishment too high or deductions exceed gross | Adjust IT0194 amount; recalculate |
| Gross wages too low | Hours not transferred, or IT0008 salary wrong | Verify time data; check IT0008 in PA20 |
| GL posting unbalanced | Cost center allocation issue | Review PC_PAYRESULT GL tab; contact Finance |

---

## 2. Processing a Mid-Period Termination

### Final Pay Requirements by State

**Note**: Consult your state labor department for exact rules. Below are general guidelines.

| State Category | Timing | Rules |
|---|---|---|
| Immediate (CA, IL, NY, TX, WA, OH, NJ, PA) | Final check with next regular payroll or within X days | Accrued unused vacation/PTO must be paid; final wages due immediately or next pay cycle |
| Final with next payroll | Within 30 days | Unused PTO paid; final wages included in next regular paycheck |
| Less common | Within pay period | State-specific; verify with HR |

### Step-by-Step Termination Process

**Step 1: HR Notification & Documentation**
1. Receive termination notice from HR (employee name, last day worked, reason)
2. Confirm final day of employment (e.g., Friday, 2/28/2025)
3. Obtain PTO balance (from HR or Time system)
4. Confirm final check timing requirement (same-day, next payroll, within X days)

**Step 2: Update Employee Infotypes**
1. Transaction PA30 → Select employee
2. **Infotype 0000 (HR Status)**: End-date employee
   - Click on IT0000 record
   - Set End Date = Last day of employment (e.g., 2/28/2025)
3. **Infotype 0001 (Org Assignment)**: End-date position assignment
   - Set End Date = Last day (e.g., 2/28/2025)
   - This stops time tracking and benefits
4. **Infotype 0008 (Basic Pay)**: End-date if on final paycheck
   - Only if final check issued immediately; otherwise leave active through last paid period
5. **Confirm no date gaps**: IT0000 end date = IT0001 end date for clean termination

**Step 3: Calculate & Enter Final Compensation**
1. **Accrued PTO/Vacation Payout**:
   - Confirm PTO balance with HR (e.g., 40 hours remaining)
   - PA30 → Create IT0015 (Additional Payment):
     - Wage Type: "PTO_Payout" (or company wage type for vacation payout)
     - Hours: 40
     - Amount: Calculated as (hours × regular hourly rate) or (days × daily rate)
     - Effective Date: Last day of employment
2. **Any Other Final Payments**:
   - Bonus owed but not yet paid? Add IT0015
   - Expense reimbursement? Add IT0015
3. **Deductions to Remove**:
   - Do NOT deduct benefits (401k, health insurance) from final check unless state law requires
   - DO deduct garnishments (still in effect through final paycheck)

**Step 4: Process Final Paycheck Options**

**Option A: Include in Next Regular Payroll Cycle** (Most Common)
1. Run regular payroll for the pay period that includes the employee's last worked day
2. Employee's IT0000 end-dated stops time clock; no further hours accrue
3. Final check = regular paycheck + PTO payout (IT0015)
4. This is simplest; coordinates with normal payroll schedule

**Option B: Off-Cycle Final Paycheck** (If Immediate Payment Required)
1. Create separate off-cycle payroll for just this employee
2. PA30 → Ensure IT0000 end-dated
3. PA30 → Ensure IT0015 with PTO payout created
4. Run PC00_M10_CALC with Run Type "B" (Additional)
5. Select payroll area, period (current or next), employee
6. Calculate and release immediately if state requires
7. Coordinate with payroll area status (may need to be in "Exit" mode for off-cycle)

### Post-Termination Steps

1. **Benefits Termination**: Coordinate with HR/Benefits
   - Final benefit deductions processed on final paycheck
   - Benefits elections end (no coverage after last day)
   - Provide COBRA notice if applicable
2. **Final Tax Documents**:
   - Generate final payslip (PC00_M10_CEDT)
   - Note: W-2 will be issued at year-end (even if terminated mid-year)
3. **Exit Communication**:
   - Notify employee of final check amount and date
   - Advise of 1099 if applicable (contractor)
   - Return of company property (badge, laptop, etc.)
4. **Payroll File Cleanup**:
   - Archive final payslip
   - Document termination date in payroll notes
   - Update payroll roster to exclude from future runs

### Common Termination Timing Rules (by State)

- **Immediate States** (CA, IL, NY, WA): Final wage due immediately (same day of termination or with next payroll)
- **Delayed States** (TX, OH): Final wage due within 30 days or next regular payroll cycle
- **PTO/Vacation**: Most states require payout; some allow forfeiture if policy predates employment (verify state law)

---

## 3. Handling Retroactive Pay Adjustments

### Identifying Retroactive Changes

Retroactive changes occur when:
- Salary increase effective 2 pay periods ago, but entered today
- Promotion with position change dated retroactively
- Tax setup correction (wrong W-4 applied; now corrected)
- New infotype entry with past start date (e.g., cost center change effective 1 month ago)

### Decision: Retro Payroll vs. Manual Correction

| Approach | When to Use | Pros | Cons |
|----------|------------|------|------|
| **Retroactive Payroll** | Salary increase, position change, major tax change affecting multiple pay periods | Accurate recalculation; auditable; payroll system recalcs all taxes correctly | Time-intensive; requires deleting prior payroll results; risky if GL posted |
| **Manual Correction (IT0015)** | Small one-time adjustment; only 1-2 pay periods affected | Quick; no re-calculation needed; minimal system impact | May not perfectly match retro payroll calculation; less audit trail |

### Retroactive Payroll Process (Recommended for Material Changes)

**Pre-Requisite**: Payroll results must NOT be posted to GL yet. If GL posted, use manual correction instead.

**Step 1: Gather Information**
1. Identify which pay periods affected (e.g., periods 10-12 of prior year if change effective 10/2024)
2. Calculate impact per period (e.g., salary increase $1,000/month = $3,000 total for 3 periods)
3. Confirm effective date of change (e.g., 10/15/2024)

**Step 2: Delete Affected Payroll Results**
1. Transaction PU19: Delete Payroll Results
2. Select payroll area, period(s) to delete
3. Select "Simulation" to test delete before committing
4. Delete affected periods (e.g., periods 10, 11, 12 of prior year)
5. Confirm deletion (system will warn; confirm you intend to delete)

**Step 3: Update Employee Infotype with Past Effective Date**
1. PA30 → Select employee
2. Create/update infotype with past effective date (e.g., IT0008 with 10/15/2024 start date)
3. End-date the prior infotype record effective 10/14/2024
4. Confirm no date gaps
5. Save changes

**Step 4: Run Retroactive Payroll**
1. PC00_M10_CALC
2. Select payroll area
3. Select periods to recalculate (e.g., periods 10, 11, 12)
4. Select Run Type: "C" (Correction)
5. Mode: "SIMULATE" first
6. Review results; confirm all taxes and deductions recalculated with new amount
7. If OK, re-run in "PRODUCTION" mode
8. Repeat for each affected period if system requires separate runs

**Step 5: Verify Results**
1. PC_PAYRESULT → Review each recalculated period
2. Confirm gross, taxes, net all reflect retroactive change
3. Compare to prior payslips for affected periods
4. Calculate total retro amount owed to employee (e.g., 3 months × $1,000 = $3,000)

**Step 6: Issue Retro Payment**
1. Create IT0015 (Additional Payment) in first paycheck after completion of retro payroll
   - Description: "Retroactive Pay Adjustment (10/2024-12/2024)"
   - Amount: Total retro owed (calculated in Step 5)
2. Include in next normal payroll run
3. Generate payslip; notify employee of retro payment

### Manual Correction Approach (Quick Fix for Small Adjustments)

Use if:
- GL already posted (can't delete payroll results)
- Adjustment < 5% of gross
- Only 1-2 pay periods affected
- Timing is urgent

**Steps**:
1. PA30 → Select employee
2. Create IT0015 (Additional Payment) for the difference amount
3. Calculate net impact (adjust for taxes; retro payments often gross-up)
4. Include in next payroll run
5. Document as "Correction for period X" in IT0015 text

### GL and Finance Coordination

After retroactive adjustment:
1. Calculate GL impact (difference in labor cost allocation)
2. Notify Finance of GL corrections needed
3. Finance creates reversing/correcting GL entries if needed
4. Document in payroll change log: What changed, why, effective date, GL impact

### Communication with Employee

1. Notify employee promptly of retroactive change
2. Explain effective date and reason for adjustment
3. Provide payslip showing retro payment
4. If amount is substantial, offer to discuss (may raise questions about past paychecks)

---

## 4. Processing Garnishments

### Garnishment Types & Priority Order

**Federal Legal Priority** (must follow this order):
1. **Child Support / Alimony** (FICA priority below support in most states)
2. **Federal Tax Lien** (IRS)
3. **State Income Tax Lien**
4. **Federal Student Loan Garnishment** (ED)
5. **Creditor Garnishment** (lowest priority; most common type)

**Amount Limits**:
- **Creditor Garnishment**: Max 25% of disposable income OR 30 times federal minimum wage (whichever is less)
- **Child Support**: Up to 50% if no other family support; 60% if other dependents
- **Tax/Student Loan**: Up to 15% or amount specified in notice
- **State-specific limits**: Some states more restrictive (e.g., PA limits creditor garnishment)

### Step-by-Step Garnishment Setup

**Step 1: Receive & Validate Court Order**
1. Obtain copy from HR/Legal of court order or levy notice
2. Verify:
   - Employee name, SSN match payroll records
   - Court case number / levy case reference
   - Garnishment type (child support, tax, creditor, student loan)
   - Garnishment amount or calculation method (% of disposable, fixed amount, etc.)
   - Start and end dates of garnishment
   - Where to send garnishment payments (payee/account details)
3. Document receipt date in payroll file

**Step 2: Calculate Disposable Income** (if not specified in order)

**Disposable Income Formula**:
```
Gross Wages
MINUS: Federal Income Tax (estimated)
MINUS: FICA (Social Security + Medicare)
MINUS: State/Local Income Tax
MINUS: Mandatory Deductions (health insurance premium, 401k, etc.)
= DISPOSABLE INCOME

Garnishment = Disposable Income × Percentage (e.g., 25% for creditor)
OR Garnishment = Fixed amount from court order (capped at 25% of disposable)
```

**Example**:
- Gross: $2,000
- Federal Tax: $200
- FICA: $153
- State Tax: $80
- Health Insurance: $300
- **Disposable Income**: $2,000 - $200 - $153 - $80 - $300 = $1,267
- **Garnishment (25% limit for creditor)**: $1,267 × 25% = $316.75/paycheck
- **Court ordered amount**: $400; **Capped at**: $316.75

**Step 3: Enter Garnishment in SAP**
1. PA30 → Select employee
2. **Create IT0194 (Garnishment)**:
   - Type: CHILDSP (child support), TAX (tax levy), CREDGARN (creditor), STUDLOAN (student loan)
   - Start Date: Date garnishment effective
   - End Date: Date garnishment expires (if specified in order)
   - Reference: Court case number / order number
3. **Create IT0195 (Garnishment Terms)**:
   - Garnishment Amount: Fixed amount ($316.75 from example) OR
   - Garnishment Percentage: 25% of disposable income (if calculation-based)
   - Frequency: Per paycheck (usually)
   - Maximum per period: Cap amount (if applicable)

**Step 4: Verify Configuration in Payroll Rules**
1. Confirm payroll rule properly calculates garnishment (after tax, after benefits)
2. Test in payroll simulation (PC00_M10_CALC) to confirm amount calculated correctly
3. Review PC_PAYRESULT to confirm garnishment line item appears

**Step 5: Setup Payment Processing**
1. Determine garnishment payment method:
   - Separate check to payee (court-ordered recipient)?
   - ACH to bank account (if levy)?
   - Manual payment?
2. Coordinate with Finance/Accounting for payment processing
3. Document payment frequency and recipient details in file

### Multiple Garnishments (Priority Sequencing)

If employee has more than one garnishment:

1. **Apply in legal priority order**:
   - Child support garnishment first (reduces disposable)
   - Tax lien next
   - Federal student loan next
   - Creditor garnishments last
2. **Calculate sequentially**:
   - Garnishment #1: Takes up to allowed limit from disposable
   - Garnishment #2: Takes from remaining disposable after #1
   - Example:
     - Disposable: $1,000
     - Child support: $500 (allowed unlimited for support)
     - Remaining after #1: $500
     - Creditor garnishment (25% limit): $500 × 25% = $125 (remaining after #1)
     - Total garnish: $500 + $125 = $625

### Managing Garnishment Changes

**Garnishment Ends** (End date reached):
1. PA30 → IT0194 / IT0195 → Confirm end date
2. System should automatically stop deduction after end date
3. Payroll run on or after end date should show $0 garnishment

**Garnishment Amount Increases**:
1. Receive modification order from court
2. PA30 → End-date old IT0194/IT0195 effective day before change
3. Create new IT0194/IT0195 with increased amount, new start date
4. Confirm effective date of change and test in payroll sim

**Garnishment Satisfies** (Employee paid off debt):
1. Receive satisfaction letter from court/creditor
2. PA30 → End-date IT0194/IT0195 immediately
3. Confirm deduction stops on next payroll run

### Compliance & Audit Trail

- Maintain copies of all court orders in employee file
- Document garnishment setup (dates, amounts, calculations) in payroll log
- Track all garnishment payments made (when, amount, to whom)
- Audit: Quarterly review of all active garnishments; confirm still valid
- Legal holds: If employee disputes, pause deduction pending legal review

---

## 5. Off-Cycle Payroll Processing

Off-cycle payroll is used for:
- Mid-period bonus or commission
- Correction/adjustment payment
- Emergency payroll
- Targeted payment to specific employees

### Prerequisites

1. **Payroll Area Status**: Must be "Open" or "Exit"
   - If in "Locked" or "Released", change to "Open" first (PU03 transaction)
2. **Time Data Locked**: Time records for the period should be locked (prevent new entries during off-cycle)
3. **Payroll Period**: Determine which payroll period this belongs to
4. **Approval**: Off-cycle payments typically require manager + Finance approval

### Step-by-Step Off-Cycle Process

**Step 1: Create Additional Payment (IT0015)**
1. PA30 → Select employee
2. Create IT0015 (Additional Payment):
   - Wage Type: "OFFCYCLE" or appropriate bonus/correction code
   - Amount: Bonus amount, correction amount, etc.
   - Effective Date: Pay date (or period date)
   - Text: "Q3 Bonus" or "Payroll Correction - Period 10" (for audit trail)
3. Save and exit PA30

**Step 2: Run Off-Cycle Payroll**
1. PC00_M10_CALC
2. Select payroll area
3. Select period: Choose the period this off-cycle belongs to (or current period if uncertain)
4. Run Type: "B" (Additional/Off-Cycle)
5. Mode: "SIMULATE" first to review
6. Employees: Select specific employee or all (usually just the employee(s) with bonuses)
7. Start payroll run

**Step 3: Review Off-Cycle Results**
1. PC_PAYRESULT → Review off-cycle payroll results
2. Spot-check:
   - Gross amount: Does it reflect the bonus/correction?
   - Taxes: Are taxes calculated on the bonus (typically 22% flat for supplemental wages)?
   - Deductions: Are benefits/garnishments applied?
   - Net pay: Positive? Reasonable?
3. Confirm no unintended wage types included

**Step 4: Release Off-Cycle Payroll**
1. PU03 → Change payroll area status to "Released" once validated
2. Generate off-cycle payslip (PC00_M10_CEDT)
3. Set up payment method (ACH, check, etc.)
4. Coordinate with Finance/Accounting for payment processing

**Step 5: GL Posting & Completion**
1. GL posting for off-cycle (usually automated)
2. Confirm GL entries match off-cycle wage amount
3. Archive payslip and documentation
4. Notify employee of off-cycle payment (timing, net amount, taxes withheld)

### Off-Cycle vs. Correction Payroll

| Scenario | Method | Details |
|----------|--------|---------|
| **Bonus in mid-period** | Off-Cycle (Run Type B) | Additional payment; full tax withholding |
| **Payroll error from prior period** | Correction (Run Type C) | Re-run prior period; recalculate all wages |
| **Commission payment** | Off-Cycle (Run Type B) | Additional wage type; supplement withholding |
| **Missed overtime** | Correction (Run Type C) if in prior period; Off-Cycle if current | Depends on timing relative to period |

---

## 6. New Hire Payroll Setup Checklist

### Pre-Payroll Setup (First Day to First Payroll)

**Day 1-2 (Hire Date)**:
- [ ] **IT0000 (HR Status)**: Create; start date = hire date
- [ ] **IT0001 (Org Assignment)**: Create; assign department, position, cost center
- [ ] **IT0002 (Personal Data)**: Create; name, DOB, gender, marital status
- [ ] **IT0006 (Address)**: Create; home address (for tax purposes)
- [ ] **IT0008 (Basic Pay)**: Create; salary amount or hourly rate
- [ ] **Collect W-4 form**: Request federal Form W-4
- [ ] **Collect State W-4**: Request state form (CA, NY, IL, etc.) if applicable
- [ ] **Collect Bank Form**: Request direct deposit authorization form

**Day 3-5 (Before First Payroll)**:
- [ ] **IT0210 (Federal Tax)**: Create; enter filing status, exemptions from W-4
- [ ] **IT0208 (State Tax)**: Create; enter state of residence, filing status
- [ ] **IT0209 (SUI)**: Create; assign unemployment insurance state
- [ ] **IT0009 (Bank Details)**: Create if direct deposit; else note "Check" payment method
- [ ] **Benefits Enrollment**: If benefits eligible (not applicable for all hires)
  - [ ] **IT0206 (Benefit Plan)**: Create if enrolled (health, dental, vision, 401k)
  - [ ] **IT0207 (Benefit Deductions)**: Create if IT0206 created; enter deduction amounts
- [ ] **IT0007 (Time Recording)**: Create if hourly; mark time-relevant if tracking hours
- [ ] **PA20 Verification**: Spot-check infotypes; confirm no date gaps, all required fields populated

### First Payroll Execution

1. **Run Payroll Simulation** (PC00_M10_CALC in SIMULATE mode)
   - Confirm new hire appears in employee count
   - Verify gross wages = expected amount (salary ÷ frequency, or hours × rate)
   - Confirm federal + state taxes calculated (not $0 if IT0210 missing)
   - Confirm net pay positive and reasonable
   - Check for alerts (missing data, configuration issues)

2. **Resolve Any Issues** (if simulation shows problems)
   - Missing IT0210? → Create it (W-4 is required)
   - Missing bank details? → Ask employee for bank info or pay by check first cycle
   - Gross amount wrong? → Verify IT0008 (Basic Pay)
   - Proceed once simulation clean

3. **Run Production Payroll** (PC00_M10_CALC in PRODUCTION mode)
   - Same steps as regular payroll
   - Repeat simulation verification
   - Release payroll area once validated

4. **Generate First Payslip** (PC00_M10_CEDT)
   - Share with new hire
   - Walk through payslip: gross, taxes, deductions, net
   - Answer questions about withholding

### Common New Hire Issues

| Issue | Fix |
|-------|-----|
| **Missing IT0210 (Tax Data)** | Collect W-4 form; create IT0210 immediately (required for federal withholding) |
| **No bank details** | Option A: Collect direct deposit form, create IT0009; Option B: Pay by check first payroll |
| **Date gaps in infotypes** | Verify all infotypes start on hire date; no end dates unless terminating |
| **Wrong cost center** | HR should assign correct cost center in IT0001; confirm before first payroll |
| **Gross amount too low/high** | Verify IT0008 (Basic Pay) amount; confirm salary or hourly rate with HR |

### First Payroll Verification

Before payslip distribution, verify:
- [ ] Gross wages correct (salary amount or hours × rate)
- [ ] Federal income tax withheld (not $0 if IT0210 present)
- [ ] FICA withheld (Social Security + Medicare)
- [ ] State income tax withheld (if applicable state)
- [ ] Benefit deductions withheld (if enrolled)
- [ ] Net pay = Gross - All Deductions (positive amount)
- [ ] Direct deposit configured (IT0009) or check payment arranged

---

## Summary Transactions Quick Reference

| Task | Transaction | Key Infotypes |
|------|-------------|---------------|
| **New Hire Setup** | PA30 | IT0001, IT0002, IT0006, IT0008, IT0009, IT0210, IT0208, IT0209 |
| **Salary Increase** | PA30 → IT0008 | IT0008 (new amount with effective date) |
| **Termination** | PA30 → IT0000, IT0001, IT0015 | End-date IT0000/IT0001; add IT0015 for PTO payout |
| **Position Change** | PA30 → IT0001 | Update IT0001 with new position/cost center; end-date old record |
| **W-4 Update** | PA30 → IT0210 | Update IT0210 filing status, exemptions, extra withholding |
| **Bank Change** | PA30 → IT0009 | End-date old IT0009; create new IT0009 with new bank details |
| **Payroll Run** | PC00_M10_CALC | (Read IT0001, IT0008, IT0009, IT0210, IT0208, IT0209, IT0014, IT0015) |
| **DME File** | PC00_M10_CDTA | (Uses IT0009 bank details, payroll results) |
| **Payslips** | PC00_M10_CEDT | (Uses all payroll results) |
| **View Results** | PC_PAYRESULT | (Displays payroll calculations, alerts) |

---

**Remember**: Always verify infotypes have no date gaps, and confirm all mandatory setup before first payroll run.
