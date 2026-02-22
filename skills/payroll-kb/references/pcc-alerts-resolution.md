# PCC Alerts Resolution Guide

A comprehensive reference for diagnosing and resolving 15 common SAP Payroll Control Center (PCC) alerts. Each alert includes root causes, step-by-step resolution, and prevention measures.

---

## Alert 1: Missing Tax Data

### What It Means
Employee is flagged because required tax infotype (IT0210) is missing, blank, or inactive. Federal income tax withholding cannot be calculated without tax data.

### Common Root Causes (Ranked by Frequency)
1. New hire without completed W-4 form; IT0210 not created
2. IT0210 marked as inactive or expired (end date in past)
3. IT0210 deleted or purged during prior cleanup
4. Employee transferred from another payroll system; tax data not migrated

### Resolution Steps
1. **Verify Missing Data**: Transaction PA20 → Select employee → Infotype 210 → Check for records
2. **Request W-4 from Employee**: Obtain completed Form W-4 or W-4C (federal); also obtain state W-4 if applicable (CA, NY, IL, etc.)
3. **Create IT0210 Record**:
   - Transaction PA30 → Select employee
   - Create new infotype 210 (Tax Data, US)
   - Enter: Filing Status, Federal Exemptions/Dependents, Extra Withholding amount
   - Enter: Infotype start date (payroll period start or hire date)
   - Leave end date blank (active indefinitely until updated)
4. **Create State Tax Infotypes**:
   - IT0208 (State Tax) for state of residence
   - IT0209 (Unemployment Insurance State) for SUI state
5. **Verify in Payroll Calculation**: Run payroll simulation (PC00_M10_CALC) to confirm withholding is now calculated
6. **Flag Employee**: Educate that W-4 is a federal legal requirement; maintain in personnel file

### SAP Transaction Codes
- **PA30**: Maintain HR Master Data (create/edit IT0210, IT0208, IT0209)
- **PA20**: Display HR Master Data (review infotypes)
- **PC00_M10_CALC**: US Payroll Run (simulation mode to test)
- **PC_PAYRESULT**: Display Payroll Results (verify withholding calculation)

### Prevention Tips
- Implement payroll onboarding checklist: W-4, direct deposit form, state tax forms due on hire date
- Run pre-payroll validation report: Check for missing IT0210 before payroll run
- Set IT0210 end date notification: Reminder to update W-4 annually (or when employee life event occurs)

---

## Alert 2: Invalid Bank Details

### What It Means
Employee's direct deposit information (IT0009) is missing, incomplete, or invalid. Bank account will not receive direct deposit until corrected.

### Common Root Causes
1. IT0009 record missing (employee never set up direct deposit)
2. Bank account number empty or invalid format
3. Routing number missing or incorrect
4. Account type (Checking vs Savings) not specified or incorrect
5. Bank account marked inactive (end date in past)

### Resolution Steps
1. **Verify Current Bank Info**: PA20 → Select employee → Infotype 009 → Review record
2. **Obtain Bank Details from Employee**:
   - Bank name
   - Routing number (ABA code, 9 digits)
   - Account number (length varies; typically 8-17 digits)
   - Account type (Checking or Savings)
   - Account holder name (must match employee name or be authorized alternate)
3. **Create or Update IT0009**:
   - PA30 → Select employee → Create/Edit Infotype 009
   - Enter bank routing number (9 digits)
   - Enter account number (validate format with payroll processor; some remove hyphens)
   - Select account type: Checking (C) or Savings (S)
   - If split deposits (% to multiple accounts): Create multiple IT0009 records with valid date ranges
   - Ensure start date ≤ payroll period; leave end date blank (active)
4. **Verify with Payroll Processor**: Contact bank/ACH processor to confirm routing + account validity (optional but recommended for high-dollar accounts)
5. **Test DME Generation**: Run PC00_M10_CDTA (preliminary DME, bank file) in test mode to confirm account appears in file
6. **Educate Employee**: Direct deposit setup instructions; recommend employee verify bank routing + account with their bank

### SAP Transaction Codes
- **PA30**: Maintain IT0009 (Bank Details)
- **PA20**: Display IT0009
- **PC00_M10_CDTA**: DME File Creation (test bank file generation)

### Prevention Tips
- Require direct deposit setup as part of new hire onboarding
- Quarterly audit of IT0009: Flag inactive or expired records
- Partner with payroll processor: ACH validation before payroll release
- Employee communication: Encourage employees to update bank details if changing banks

---

## Alert 3: Missing Time Data

### What It Means
Time records were not transferred/imported for time-relevant employees (those with IT0007 Time Recording infotype). Payroll cannot calculate wages accurately without hours worked.

### Common Root Causes
1. Time management system not integrated or interface down
2. Employee time records not submitted in time attendance system
3. Time import/interface job failed or was skipped
4. Employee IT0007 infotype says "time-relevant" but time data never uploaded
5. Time data for specific period missing (e.g., employee on leave, time records purged)

### Resolution Steps
1. **Verify Time Recording Status**: PA20 → Select employee → Infotype 007 (Time Recording) → Check "Time Recording Relevant" indicator
2. **Check Time Transfer Interface**:
   - Review time transfer job logs (SM37 → Search for "Time" or "CAT" jobs)
   - Verify no errors in last run; re-run if failed
3. **Validate Time Data Exists**:
   - CATS transaction (Collaborative Time Sheet) or equivalent time system → Look up employee's time records for pay period
   - Confirm hours entered for all work days
4. **Review Payroll Time Integration**:
   - PC00_M10_CALC (payroll run) → Review "Time Data" section of payroll results
   - Look for warning: "No time data found" vs. actual hours loaded
5. **Reconcile Hours**:
   - If time data partially loaded, identify missing days/hours
   - Request employee resubmit time records or manager approve in time system
   - Re-run time transfer interface
6. **Update Employee IT0007** (if employee should no longer be time-relevant):
   - PA30 → Infotype 007 → Mark as inactive if employee is salaried (not hourly)
7. **Run Payroll Again**: After time data corrected, re-run payroll calculation

### SAP Transaction Codes
- **PA20**: Display IT0007 (Time Recording setup)
- **CATS**: Collaborative Time Sheet entry/review
- **SM37**: Monitor background jobs (time transfer interface jobs)
- **PC00_M10_CALC**: Payroll run (review time data integration)
- **PC_PAYRESULT**: Display payroll results (time data detail section)

### Prevention Tips
- Clear communication: Time entry deadlines before payroll cutoff
- Payroll workflow: Build time transfer into pre-payroll checklist (run interface job X days before payroll)
- Escalation: If time missing for salaried employee, verify IT0007 doesn't have "time recording" flag
- Audit: Monthly spot-check of time vs. payroll data (random sample)

---

## Alert 4: Wage Type Collision

### What It Means
Two or more wage types with conflicting configurations or values exist in the same payroll period for the employee. System cannot determine which wage type to use.

### Common Root Causes
1. Manual IT0015 (Additional Payments) entry conflicts with recurring wage type
2. Off-cycle payroll was not reversed before running next standard cycle
3. Bonus entered multiple times (duplicate IT0015 records)
4. Wage type configuration error: same wage type triggered by multiple rules
5. Retroactive adjustment created overlapping wage type entries

### Resolution Steps
1. **Identify Conflicting Wage Types**: PC_PAYRESULT → Review payroll results for employee → Look for duplicate or suspicious wage types with similar values
2. **Check Additional Payments (IT0015)**: PA20 → Infotype 015 → Review all records for the pay period; look for duplicates
3. **Investigate Root Cause**:
   - Was an off-cycle adjustment run but not reversed?
   - Was the same bonus entered twice?
   - Did payroll rule configuration change mid-cycle?
4. **Resolution by Cause**:
   - **Duplicate IT0015**: PA30 → Delete extra record(s); keep only intended one
   - **Off-Cycle Not Reversed**: Run corrective off-cycle payroll to zero out (or use PU19 to delete results if not yet posted to GL)
   - **Retroactive Adjustment Overlap**: Review retroactive change date; may need to split wage type by date range
5. **Recalculate Payroll**: Run PC00_M10_CALC again to confirm conflict resolved
6. **Validate Results**: Review PC_PAYRESULT; confirm only one instance of each wage type per period

### SAP Transaction Codes
- **PA20**: Display IT0015 (Additional Payments)
- **PA30**: Maintain IT0015
- **PC_PAYRESULT**: Display payroll results (review wage type detail)
- **PC00_M10_CALC**: Payroll calculation
- **PU19**: Delete payroll results (if results not yet posted to GL and need to be removed)

### Prevention Tips
- Implement approval workflow: All additional payments (bonuses, adjustments) require approval before entry
- Pre-payroll validation: Run report to identify duplicate wage types per employee
- Change control: Document wage type configuration changes; communicate to payroll team before next cycle
- Off-cycle procedures: Maintain log of off-cycle runs; document intent (bonus, correction, adjustment)

---

## Alert 5: Retroactive Change Detected

### What It Means
A change to employee master data (salary, cost center, tax status, etc.) has an effective date in the past. This change may affect payroll results from prior periods and requires recalculation (retro payroll).

### Common Root Causes
1. Delayed salary increase effective date; entered today but should have been effective 2 pay periods ago
2. Promotion with cost center change dated retroactively
3. Tax setup change (W-4, state tax) applied with past effective date
4. Corrected infotype entry: Employee was on wrong pay grade; now corrected retroactively
5. System import/migration: Historical records loaded with past dates

### Resolution Steps
1. **Identify Retroactive Change**: PCC monitoring dashboard or payroll error report should flag retroactive infotypes
2. **Review Changed Infotype**: PA20 → Select employee → Find infotype with past date
3. **Assess Impact**:
   - Which pay periods are affected?
   - What wage types or tax calculations change?
   - What is the difference in net pay per period?
4. **Decide: Rerun vs. Manual Correction**:
   - **Option A (Recommended)**: Run retroactive payroll for affected periods (see Common Procedures - Retroactive Adjustments)
   - **Option B (Manual)**: Calculate impact manually; enter adjustment via IT0015 in first affected period
5. **Document Retroactive Change**: Log in system who made change, why, when, and impact amount
6. **Coordinate with Finance**: Notify if retroactive change affects GL posting; may need to reverse prior GL entries
7. **Employee Communication**: If retro change increases net pay, notify employee of adjustment; if it decreases, explain reason

### SAP Transaction Codes
- **PA20**: Display all infotypes; identify ones with past dates
- **PC00_M10_CALC**: Retroactive payroll run (see Retroactive Procedures)
- **PC_PAYRESULT**: Compare results before/after retroactive change
- **PA30**: Maintain infotypes; use correct effective dates going forward

### Prevention Tips
- Data governance: Require justification + approval for any retroactive effective date
- System defaults: Set effective date to "today" by default; require explicit action to change
- Training: Educate HR on IT change procedures; emphasize importance of accurate effective dates
- Review process: Monthly data quality check for infotypes with dates in past 90 days

---

## Alert 6: Benefit Enrollment Gap

### What It Means
Employee is eligible for benefits (based on hire date, employment status, age, etc.) but has no active benefit plan elections (IT0206) in payroll system. Enrollment may be missing or expired.

### Common Root Causes
1. New hire completed W-4/tax setup but benefit enrollment form not yet entered in payroll system
2. Employee benefits enrollment expired; no renewal/continuation
3. Employee did not enroll during open enrollment window
4. Benefits data not migrated from benefits system to payroll IT0206
5. Employee ineligible for benefits (part-time, contract worker) but infotype not flagged

### Resolution Steps
1. **Verify Eligibility**: PA20 → Infotype 001 (Org Assignment) → Confirm employment status (Full-time? Part-time? Contract?)
2. **Check Benefit Plan Infotypes**:
   - Infotype 206 (Benefit Plan) → Review for employee
   - Infotype 207 (Benefit Deductions) → Review for deduction amounts
3. **Identify Gap**:
   - Is employee eligible but no IT0206? → Enroll
   - Is employee ineligible? → Document reason (part-time, pending vesting, etc.)
4. **Resolution**:
   - **If eligible**: Coordinate with HR/Benefits to obtain enrollment forms (medical, dental, 401k) → Create IT0206 and IT0207 records with effective dates
   - **If ineligible**: Mark IT0206 as inactive or add comment explaining ineligibility
5. **Verify Deductions**: Once IT0206 created, confirm IT0207 (Benefit Deductions) populated with correct amounts
6. **Payroll Impact**: Re-run PC00_M10_CALC to confirm benefit deductions now appear in payroll

### SAP Transaction Codes
- **PA20**: Display IT0206 (Benefit Plan), IT0207 (Benefit Deductions)
- **PA30**: Maintain IT0206, IT0207
- **PC00_M10_CALC**: Payroll run (verify deductions calculated)

### Prevention Tips
- Hire-to-payroll workflow: Include benefits enrollment as mandatory step before first payroll
- Benefits system integration: Automate transfer of enrollment data from benefits system to SAP IT0206/0207
- Annual audit: Review all employees for IT0206 gaps; investigate missing/expired enrollments
- Communication: Remind employees of open enrollment deadlines; process elections promptly

---

## Alert 7: Cost Center Assignment Missing

### What It Means
Employee lacks required cost center assignment (typically in IT0001 - Organizational Assignment or IT0027 - Cost Assignment). Payroll cannot allocate labor costs to correct cost center for GL posting.

### Common Root Causes
1. New hire created in time system but HR org assignment not yet completed
2. Employee transferred; old cost center assignment end-dated but new one not created
3. Employee IT0001 missing or has gap in dates (end date before start date of new record)
4. Contingent worker or contract employee without cost center setup
5. System interface failure: HR org data not synced to payroll

### Resolution Steps
1. **Verify Org Assignment**: PA20 → Infotype 001 → Review for active record with valid date range
2. **Check Cost Assignment**: PA20 → Infotype 027 (Cost Assignment) → Review for cost center, cost object, project code
3. **Identify Issue**:
   - Missing IT0001? Create org assignment with hire date or first day of pay period
   - Date gap? Create new IT0001 record with continuous coverage (end date of previous = start date - 1 of new)
   - No IT0027? Create cost assignment record
4. **Create/Update Assignment**:
   - PA30 → Infotype 001 → Enter: Organizational Unit (cost center), Position, Job, start date
   - PA30 → Infotype 027 → Enter: Cost Center, Cost Object, Project Code (if applicable)
5. **Validate**: Confirm no date gaps; confirm cost center exists in financial system (CO module)
6. **Run Payroll**: PC00_M10_CALC to confirm cost center now appears in GL posting records

### SAP Transaction Codes
- **PA20**: Display IT0001, IT0027
- **PA30**: Maintain IT0001, IT0027
- **OM00**: Display organizational hierarchy (verify cost center exists and is active)
- **PC00_M10_CALC**: Payroll run (review GL posting preview)

### Prevention Tips
- Workflow integration: HR org assignment must be completed before payroll processing
- Pre-payroll validation: Report all employees with missing cost centers; escalate to HR
- Contingent worker setup: Establish standard cost center for contract workers (e.g., "General Labor")
- Data governance: Require end date + 1 day gap prevention rule in system

---

## Alert 8: Overtime Threshold Exceeded

### What It Means
Employee worked or is scheduled to work hours beyond configured maximum/threshold (typically 40 hours/week for FLSA overtime or company policy maximum). Alert signals potential FLSA compliance issue or policy violation.

### Common Root Causes
1. Employee worked overtime but wage type for OT premium not calculated or configured incorrectly
2. Comp time tracking: Employee took comp time instead of OT pay (may not be FLSA-compliant depending on agreement)
3. Time entry error: Hours incorrectly entered in time system (e.g., 80 instead of 8)
4. Manager approval gap: Overtime worked but not pre-approved per company policy
5. Payroll system configuration: OT wage type not triggered automatically at 40-hour threshold

### Resolution Steps
1. **Review Time Data**: CATS (or time system) → Look up employee hours for week/pay period → Verify accuracy
2. **Check OT Configuration**: PT40 (Payroll Time config) or payroll rules → Confirm OT wage type (wage type for hours over 40) is defined
3. **Assess Compliance**:
   - Is this legitimate FLSA OT? (Confirm employee is non-exempt; check status in IT0001)
   - Is OT premium being paid? (1.5x or 2x regular rate per FLSA/agreement)
4. **Resolution**:
   - **If time entry error**: Correct hours in time system; re-run time transfer
   - **If legitimate OT**: Verify OT wage type calculated; if not, configure payroll rule to trigger at 40+ hours
   - **If policy violation**: Notify manager; discuss with employee re: authorization
   - **If comp time**: Document employee agreement; ensure compliant with FLSA (generally not allowed for non-exempt employees)
5. **Re-Run Payroll**: PC00_M10_CALC → Verify OT premium applied and gross wages reflect OT calculation

### SAP Transaction Codes
- **CATS**: Time entry/review
- **PT40**: Payroll Time configuration (OT rules)
- **PA20**: Display IT0001 (confirm employee FLSA exempt status)
- **PC00_M10_CALC**: Payroll run (verify OT calculation)
- **PC_PAYRESULT**: Review wage type detail (confirm OT premium appears)

### Prevention Tips
- Manager training: Enforce approval process for all OT before time entry
- Payroll rule: Automatically calculate OT premium for non-exempt employees at 40+ hours
- FLSA audit: Quarterly review of OT by department; confirm all OT is paid at 1.5x minimum
- Time entry validation: Set system rule to warn if hours > 10/day or > 50/week

---

## Alert 9: Garnishment Calculation Error

### What It Means
A court-ordered wage garnishment (child support, tax levy, creditor garnishment, student loan) has an issue in disposable income calculation or payment calculation. Payroll may be withholding incorrect amount.

### Common Root Causes
1. Disposable income calculated incorrectly (using gross instead of net after tax/mandatory deductions)
2. Garnishment priority incorrect (multiple garnishments; order of priority not followed)
3. Garnishment amount exceeds federal/state limit (e.g., 25% of disposable income)
4. Garnishment infotype (IT0194/0195) entry has wrong dates or amounts
5. Garnishment combined with child support creates calculation complexity

### Resolution Steps
1. **Obtain Garnishment Order**: Request copy of court order or levy notice from HR/Legal
2. **Review Garnishment Setup**: PA20 → Infotype 0194 (Garnishment) and 0195 (Garnishment Terms) → Verify:
   - Garnishment type (child support, tax levy, creditor, student loan)
   - Disposable income calculation method
   - Maximum withholding amount (should not exceed 25% of disposable for creditor; higher % for child support/tax)
   - Start/end dates align with court order dates
3. **Calculate Disposable Income**:
   - **Formula**: Gross wages MINUS federal tax - FICA - state/local tax - mandatory deductions (health insurance, 401k) = Disposable income
   - **NOT included in reduction**: Voluntary deductions (charitable, union dues per some rulings)
   - Verify payroll system using correct formula
4. **Verify Priority Order** (Federal law priority):
   1. Child support/alimony (FICA priority below support in most states)
   2. Federal tax liens
   3. State income tax garnishments
   4. Federal student loan garnishments
   5. Creditor garnishments (lowest priority)
5. **Calculate Correct Amount**:
   - Example: Gross $2,000; Fed Tax $200; FICA $153; State Tax $80 = Disposable $1,567
   - 25% limit for creditor garnishment: $1,567 × 25% = $391.75/pay period
   - If court ordered $500, cap at $391.75 (federal limit)
6. **Correct IT0194/0195**: PA30 → Update garnishment amount, effective date, or calculation rules as needed
7. **Re-Run Payroll**: PC00_M10_CALC → Verify garnishment amount now correct

### SAP Transaction Codes
- **PA20**: Display IT0194 (Garnishment), IT0195 (Garnishment Terms)
- **PA30**: Maintain IT0194, IT0195
- **PC00_M10_CALC**: Payroll run (verify garnishment calculation)
- **PC_PAYRESULT**: Review wage type detail (garnishment line item)

### Prevention Tips
- Garnishment procedure: Require copy of court order before creating IT0194
- Disposable income calculation: Train payroll team on correct formula; document in SOPs
- Compliance audit: Quarterly review of all active garnishments; compare to court orders
- Employee communication: Notify employee of garnishment setup and expected deduction per paycheck

---

## Alert 10: Tax Reciprocity Conflict

### What It Means
Employee's residence state and work state have conflicting or unclear withholding rules. System flagged because configuration doesn't match tax reciprocity status (or reciprocity agreement changed).

### Common Root Causes
1. Employee transferred from one state to another; tax setup not updated
2. NJ resident working in NY or vice versa (common misconception: many think NJ-NY has reciprocity, but it doesn't)
3. Reciprocity agreement is state-specific and new employee setup didn't account for it
4. Multi-state employment: Employee works in 3 states but payroll config only has 1 or 2
5. IT0208 (State Tax) record shows wrong state or multiple states without apportionment

### Resolution Steps
1. **Clarify Employee Situation**: Determine residence state and ALL work locations/states
2. **Check Reciprocity**: Review state tax authority website or www.wwd.org for reciprocal tax agreements
   - **Common Reciprocal Agreements**: IL-IN, IL-KY, IL-MO, IL-WI, MD-VA, etc.
   - **NOT Reciprocal**: NJ-PA (both tax), NJ-NY (both tax), PA-DE (both tax)
3. **Determine Withholding State(s)**:
   - **Rule**: Withhold residence state + any non-reciprocal work states
   - **Example 1**: NJ resident, NY work, no reciprocity → Withhold both NJ and NY
   - **Example 2**: IL resident, IN work, reciprocity applies → Withhold IL only
   - **Example 3**: PA resident, multi-state (PA, NY, CT) → Withhold all 3
4. **Update IT0208**:
   - PA30 → Infotype 0208 → Create/edit for correct state(s)
   - If multi-state: Create multiple IT0208 records (one per state) with valid date ranges
   - For split withholding: Allocate % of wages to each state (document apportionment method)
5. **Document in IT0006**: Update Address infotype to show residence address (state)
6. **Run Payroll Simulation**: PC00_M10_CALC → Verify correct states' taxes now withheld
7. **Educate Employee**: Explain withholding state choice (reciprocity or non-reciprocal rule)

### SAP Transaction Codes
- **PA20**: Display IT0208 (State Tax), IT0006 (Address/Residence)
- **PA30**: Maintain IT0208, IT0006
- **PC00_M10_CALC**: Payroll run (verify state tax calculation)
- **PC_PAYRESULT**: Review state tax detail by state

### Prevention Tips
- Multi-state hiring process: Require residence state + ALL work location states upfront
- Tax reciprocity guide: Create quick reference doc for payroll team (IL-IN reciprocal, NJ-NY NOT, etc.)
- Data governance: Flag any employee with residence ≠ work state for compliance review
- Annual audit: Confirm reciprocity agreements still apply; state laws can change

---

## Alert 11: Pay Scale Reclassification Pending

### What It Means
Employee's pay scale or job grade has changed, and an indirect valuation wage type (compensates based on new pay scale) has not yet been recalculated. Prior payroll used old pay scale; system flagged need to recalculate.

### Common Root Causes
1. Employee promoted; new position has higher pay scale effective date in past (retroactive)
2. Pay scale matrix updated (annual adjustment); employee's current grade should reflect new rates
3. Wage type for "base salary per pay scale" not recalculated after IT0001/IT0008 change
4. Retroactive job change entered but retro payroll not yet run
5. System configuration: Pay scale wage type not configured to auto-update on position change

### Resolution Steps
1. **Verify Job/Position Change**: PA20 → Infotype 001 → Review for recent position/job changes
2. **Identify Affected Pay Periods**: Which periods were affected by job change? Should old rate or new rate apply to which period?
3. **Check Wage Type Configuration**: Payroll rules → Confirm wage type for "Base Salary by Pay Scale" is configured
4. **Decide: Recalculate vs. Manual Entry**:
   - **Option A**: Run retroactive payroll to recalculate wage type (see Retroactive Procedures)
   - **Option B**: Manually calculate difference and enter via IT0015 (Additional Payments) as adjustment
5. **Execute Resolution**:
   - If retro payroll: Run PC00_M10_CALC for affected past pay periods
   - If manual: PA30 → Create IT0015 record with salary difference amount and effective date
6. **Verify Results**: PC_PAYRESULT → Confirm new pay scale rate and gross wages
7. **GL Impact**: Notify Finance if retro adjustment affects GL posting; document in change log

### SAP Transaction Codes
- **PA20**: Display IT0001 (Position), IT0008 (Basic Pay)
- **PA30**: Maintain IT0001, IT0008, IT0015 (Additional Payments)
- **PC00_M10_CALC**: Retroactive payroll run
- **PC_PAYRESULT**: Review results with new pay scale rate

### Prevention Tips
- Change control: All position/pay scale changes must be flagged for payroll review
- Retroactive adjustment workflow: Process any retro changes within 1-2 pay cycles to avoid backlog
- Payroll rule config: Auto-trigger wage type recalculation when IT0008 or IT0001 changes
- Communication: Notify employee of pay scale change and effective date

---

## Alert 12: Payroll Area Lock Conflict

### What It Means
Payroll area is locked by another user or process (payroll run, GL posting, correction process), preventing the current payroll operation from proceeding.

### Common Root Causes
1. Another payroll admin is running payroll in the same area simultaneously
2. Payroll run completed but never released from "locked" status
3. GL posting in progress; payroll area locked until posting finishes
4. Correction payroll in progress; area locked until correction released
5. System crash or hung process left payroll area in locked state

### Resolution Steps
1. **Check Payroll Area Status**: PRAA transaction → Select payroll area → View status
   - Status should be: Open, Locked, Released, Exit
   - "Locked" = process in progress; must wait or unlock
2. **Identify Who/What Has Lock**:
   - SM04 (User List) → Look for payroll users currently in system
   - SM37 (Job Overview) → Look for active background jobs related to payroll area
   - SLG1 (Application Log) → Search for payroll area lock events
3. **Resolution by Cause**:
   - **Another admin running payroll**: Coordinate; wait for them to finish and release payroll area
   - **Hung process**: Contact that admin; ask them to release the lock (PRAA → Release button)
   - **Stuck lock (no active user/job)**: Use PU03 (Change Payroll Status) to manually change area from Locked to Open or Release
   - **GL posting locked**: Wait for posting to complete (usually 5-15 minutes); check with Finance
4. **Unlock Payroll Area**:
   - PU03 → Select payroll area → Change status from Locked → Open
   - Only do this if you confirm no process is actively using the area
5. **Retry Operation**: Once unlocked, re-run your payroll operation (PC00_M10_CALC, payroll release, GL posting)
6. **Document**: Log the lock conflict and resolution in payroll change log

### SAP Transaction Codes
- **PRAA**: Payroll Area overview (view status, lock/unlock)
- **PU03**: Change Payroll Status (manually unlock if necessary)
- **SM37**: Monitor background jobs (check for stuck payroll jobs)
- **SM04**: User list (identify concurrent payroll users)
- **SLG1**: Application Log (audit lock events)

### Prevention Tips
- Workflow discipline: Payroll run must complete AND be released before next admin can run
- Communication: Use shared calendar or Slack to notify when running payroll; prevent concurrent runs
- Timeout management: If a process hangs, escalate to SAP Basis admin to kill job + unlock area
- Monitoring: Set up daily check of payroll area status to catch stuck locks early

---

## Alert 13: Negative Net Pay

### What It Means
Employee's calculated net pay is negative (deductions exceed gross wages). Paycheck cannot be issued, and situation must be resolved before payroll release.

### Common Root Causes (Ranked by Frequency)
1. Garnishment amount exceeds gross wages (over 25% of disposable income not properly capped)
2. Multiple garnishments without proper priority/limit applied
3. Back-owed benefit contributions (e.g., health insurance premium adjustment, 401k true-up)
4. Manual adjustment (IT0015) entered with negative amount that exceeded gross
5. Corrective payroll: Overpayment being recovered in single paycheck

### Resolution Steps
1. **Review Payroll Results**: PC_PAYRESULT → Select employee → Review gross wages and all deductions
2. **Identify Issue**:
   - Is garnishment too high? (Should not exceed 25% of disposable for creditor garnishments)
   - Are there multiple garnishments stacking? (Need to apply priority rules)
   - Is there a large deduction adjustment? (Back-owed premium, correction?)
3. **Resolution by Cause**:
   - **Garnishment too high**:
     - Recalculate disposable income: Gross - federal tax - FICA - state/local tax - mandatory deductions
     - Cap garnishment at 25% of disposable (or state/federal law limit)
     - Update IT0194 with corrected amount
   - **Multiple garnishments**:
     - Verify priority order per federal law (child support > federal tax lien > state tax > federal student loan > creditor)
     - Allocate disposable income in priority order; later garnishments get $0 if limit reached
   - **Large adjustment**:
     - Contact Finance/HR to confirm if back-owed amount is correct
     - Option 1: Recover over multiple paychecks (spread deduction across 2-4 paychecks)
     - Option 2: Issue partial deduction in current paycheck; defer remainder to future paychecks
4. **Correct and Recalculate**: Update garnishment/deduction → Re-run PC00_M10_CALC
5. **Verify Positive Net Pay**: Confirm net pay is now > $0
6. **Document Resolution**: Log the negative net pay situation and how it was resolved

### SAP Transaction Codes
- **PC_PAYRESULT**: Display payroll results (identify negative net pay line item)
- **PC00_M10_CALC**: Payroll run (recalculate after adjustments)
- **PA30**: Maintain IT0194 (garnishment), IT0015 (deductions/adjustments)

### Prevention Tips
- Pre-payroll validation: Report all garnishments + deductions that sum > 50% of gross
- Garnishment cap rule: Payroll system should auto-cap at 25% of disposable; alert if exceeded
- Manager escalation: Negative net pay requires manager + Finance approval before payroll release
- Employee communication: Notify employee of unusual large deduction (back-owed, garnishment) in advance

---

## Alert 14: Social Security Wage Base Exceeded

### What It Means
Employee cumulative Social Security (OASDI) wages have exceeded the annual wage base limit ($168,600 for 2025). Further OASDI withholding should stop, but system either over-withheld or didn't stop automatically.

### Common Root Causes
1. Payroll system did not track cumulative OASDI wages correctly
2. Employee had multiple employers (one is primary; may not know about dual employment)
3. Configuration error: OASDI wage type not configured to stop at wage base
4. Bonus or retroactive pay in final pay period pushed employee over wage base; system didn't adjust
5. Off-cycle or correction payroll added wages that weren't counted in cumulative

### Resolution Steps
1. **Verify Wage Base**: Confirm 2025 OASDI wage base = $168,600 (check current year before next Jan 1)
2. **Calculate Cumulative OASDI Wages**:
   - Pull payroll results year-to-date (PC_PAYRESULT)
   - Sum all gross wages subject to OASDI (most employees; exclude NRA exempt, some others)
   - Check if cumulative exceeds wage base
3. **Identify Issue**:
   - Did employee exceed wage base? On which paycheck?
   - Was OASDI withheld AFTER wage base exceeded? (Should have stopped)
   - Is this a multi-employer situation (employee also worked elsewhere)?
4. **Resolution**:
   - **If over-withheld by primary employer**: Calculate excess OASDI × 6.2%; issue as refund or credit on final paycheck
   - **If multi-employer**: Employee will need to claim credit on Form 1040 (IRS will reconcile; employer does not refund)
   - **If system didn't stop**: Correct payroll configuration; re-run affected paychecks if necessary
5. **Communicate to Employee**: Explain OASDI wage base; if over-withheld, indicate will be refunded on W-2 or final paycheck
6. **Update Configuration**: Verify OASDI wage type configured to auto-stop at wage base; test before next year

### SAP Transaction Codes
- **PC_PAYRESULT**: Review cumulative OASDI wages (drill into summary)
- **PC00_M10_CALC**: Payroll run (verify OASDI stops when wage base hit)
- **SE16N**: Table browser (query cumulative wage totals if needed)

### Prevention Tips
- Pre-payroll audit: Monthly review of high-earner cumulative OASDI; identify those near wage base
- Configuration test: Each January, verify OASDI wage type auto-stops at current wage base
- Employee communication: Advise multi-employer employees to track OASDI across jobs; file Form 1040 if over-withheld
- Year-end reconciliation: Confirm total OASDI withheld ≤ (wage base × 6.2%) per employee

---

## Alert 15: Year-End Adjustment Required

### What It Means
W-2 preparation flagged data discrepancy or missing correction from prior periods. W-2 values don't reconcile to quarterly 941 filings or payroll summary. Correction (W-2c amendment) or adjustment may be needed.

### Common Root Causes
1. Withholding error discovered during W-2 prep (e.g., wrong W-4 used for part of year)
2. Pre-tax deduction amount incorrect (401k over-contribution, FSA not stopped when plan closed)
3. Retroactive pay adjustments made in final paycheck; not reflected in prior period W-2s
4. Off-cycle or bonus processed late; included in wrong payroll period
5. Multi-state employee: W-2 state withholding doesn't match 941 quarterly state filing

### Resolution Steps
1. **Generate W-2 Report**: PC00_M10_CEDT (Remuneration Statement) or equivalent W-2 report in SAP
2. **Reconcile to 941**:
   - Pull 941 forms filed for year
   - Sum quarterly federal withholding from 941
   - Compare to W-2 Box 2 (federal tax withheld)
   - Look for discrepancies
3. **Investigate Discrepancy**:
   - If W-2 > 941: Employee was under-withheld on some paychecks; over-withheld to compensate later
   - If W-2 < 941: Over-withholding not recredited; IRS overpayment situation
   - If multi-state: Compare W-2 state witholding to state quarterly filings (540-ES, etc.)
4. **Identify Root Cause**:
   - Review payroll period by period (PC_PAYRESULT) for each pay period
   - Look for anomalies: missing periods, zero withholding, unusual adjustments
   - Check for prior-period corrections or off-cycle entries
5. **Determine Action**:
   - **If small discrepancy (< $100)**: May be acceptable rounding difference
   - **If material discrepancy**:
     - **Option A**: Issue W-2c (amended W-2) with corrected amounts
     - **Option B**: If error in employer's favor, may carry forward as adjustment to next year (consult tax counsel)
     - **Option C**: If error in employee's favor, issue refund or credit on next paycheck
6. **File W-2c if Needed**:
   - File Copy A with IRS
   - Provide Copy B/C to employee
   - Deadline: Within 60 days of discovery (or before statute expires)
7. **Update Configuration for Next Year**: Correct the underlying payroll rule, W-4 setup, or deduction that caused error

### SAP Transaction Codes
- **PC00_M10_CEDT**: Remuneration Statement / W-2 Report
- **PC_PAYRESULT**: Review each payroll period for accuracy
- **PA20**: Display IT0210, IT0015, IT0208 for the employee (identify setup errors)
- **SE16N**: Query cumulative tables for year-to-date reconciliation

### Prevention Tips
- Monthly reconciliation: Run mini W-2 reconciliation each month to catch errors early
- Quarterly 941 review: Immediately compare 941 quarterly to payroll summary; flag discrepancies
- Change log: Document all retroactive adjustments, off-cycle entries, mid-year corrections
- Year-end timeline: Begin W-2 prep 2 weeks before deadline; allocate time for reconciliation/corrections
- Configuration review: Annually review payroll rules (withholding, deductions) for accuracy before Jan 1

---

## Alert Resolution Best Practices

1. **Act Quickly**: Address alerts before payroll release if possible; escalate if resolved too late
2. **Document**: Log every alert, root cause, and resolution in payroll change log
3. **Verify**: Always re-run payroll calculation after correction to confirm alert resolved
4. **Communicate**: Notify affected employee of significant corrections (withholding changes, deductions, retro pay)
5. **Escalate**: If alert recurs or you're unsure of cause, escalate to SAP Support or tax counsel
6. **Learn**: Track alert patterns; use to improve data governance and payroll controls

---

**Remember**: Alert resolution requires both technical SAP navigation and payroll domain knowledge. When in doubt, consult your tax advisor and SAP support.
