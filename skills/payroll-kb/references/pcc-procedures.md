# SAP Payroll Control Center (PCC) Procedures Reference

This guide covers the standard SAP PCC workflows for US payroll operations, including monitoring, production payroll, off-cycle processing, key transactions, and Fiori apps.

## PCC Fiori Apps Overview

### 1. My Payroll Processes
**Purpose**: Dashboard for your assigned payroll processing tasks and alerts
**When to use**: Start of every payroll cycle; monitoring your work items
**Key features**:
- View all your active process instances
- See pending alerts assigned to you
- Filter by status (New, In Process, Done, Rejected)
- Quick actions: open, forward, reassign
- Performance dashboard: KPIs and SLA tracking

### 2. Process Payroll
**Purpose**: Execute payroll production steps (release, trigger, post, exit)
**When to use**: During production payroll execution phase
**Key features**:
- Release payroll (control record management)
- Trigger batch jobs (PC00_M10_CALC)
- Post to Finance (FI module)
- Generate bank/DME files
- Perform posting simulation
- Exit payroll
- Job monitoring and error handling

### 3. Monitor Payroll
**Purpose**: Track payroll process progress and alert status
**When to use**: Throughout payroll cycle; especially during production
**Key features**:
- Real-time job status
- Process flow visualization
- Alert status tracking (by type, severity, assignee)
- Bulk operations (reassign alerts, reject, approve)
- Historical runs and audit trail

### 4. Payroll Activity Manager
**Purpose**: Manage discrete payroll activities and corrections
**When to use**: Off-cycle corrections, bonus runs, manual payments
**Key features**:
- Create and manage payroll activities
- Retroactive adjustments
- Bonus run setup
- Correction runs
- Activity-specific wage type mappings

## Payroll Cycle Phases

### Phase 1: Pre-Payroll (Days 1-3 of cycle)

**Objectives**: Ensure all input data is ready, no alerts block processing

**Key tasks**:

1. **Time and Attendance Review**
   - Check time card uploads from HCM (if applicable)
   - Identify exceptions: missing time, overage, unapproved leave
   - Escalate to timekeeper/manager for correction
   - Ensure all time is approved before payroll opens

2. **Personnel Master Data Verification**
   - Review any changes made since last payroll
   - Use **PA03** (Payroll Status) to check master data for payroll-relevant infotypes
   - Verify: salary, pay scale, tax data, bank details, benefits elections
   - Flag any pending changes with future effective dates

3. **Alert Pre-Check** (Optional but recommended)
   - Run payroll in test mode or check staging environment
   - Identify alerts that will block processing
   - Resolve high-priority alerts early (missing W-4, invalid bank details, cost center issues)

4. **Cutoff and Freeze**
   - Set HR master data freeze (IT0008 assignment, IT0200 salary entries)
   - No new hires or terminations enter the current cycle (unless retroactive)
   - All manual time entries locked
   - Document cutoff time for audit trail

### Phase 2: Monitoring (Days 4-5 of cycle)

**Objectives**: Track payroll start, monitor alert processing, ensure timely issue resolution

**Key workflow**:

1. **Payroll Opens**
   - Finance/Payroll manager releases payroll in Process Payroll app
   - System creates payroll processing instances per payroll area
   - PCC pulls master data snapshot for the period
   - Alerts begin generating as data validation occurs

2. **Alert Generation & Assignment**
   - Monitoring alerts auto-assigned to area owners (by cost center, location, or team)
   - Each alert enters "New" status → Team reviews and transitions to "In Process"
   - Alert types: missing data, configuration errors, compliance flags, warnings
   - Use Monitor Payroll app to track alert volume and aging

3. **Alert Resolution**
   - Open each alert to understand the issue (alert detail shows affected employees, root cause suggestion)
   - For data-missing alerts: retrieve info from HR, correct in master data, mark alert "Done"
   - For configuration alerts: coordinate with payroll/HR ops to fix setup
   - For warnings: review, document reason to proceed, mark "Done" with notes
   - **Critical**: Resolve all "blocking" alerts before moving to production

4. **Team Monitoring** (for team leads)
   - Monitor workload distribution
   - Reassign alerts if a team member is overloaded
   - Escalate unsolved alerts as due date approaches
   - Flag trends (e.g., "5 employees missing W-4 data" vs individual issues)

5. **Monitoring Closure**
   - All alerts reach "Done", "Resolved", or documented "Acknowledged with Risk"
   - Finance approves readiness to move to production
   - Monitoring phase closes; production phase begins

### Phase 3: Production Payroll (Day 6-7 of cycle)

**Objectives**: Execute payroll calculation, validation, posting, and transmission

**Workflow in Process Payroll app**:

#### Step 1: Release Payroll (Unlock for calculation)

**Navigation**: Process Payroll app → [Select payroll area/company code] → Release Payroll

**What happens**:
- Control record for the payroll area is marked "Releasable"
- Locks are removed so batch jobs can run
- Period remains open for SAP to calculate

**SAP Transaction equivalent**: **PU22** (Payroll Control Record)
- Check control record status: must show "Open" with no date in "Payroll Processed"
- If locked, check who released/ran last period; may need unlock

**Checklist before release**:
- All alerts from monitoring phase resolved or approved to proceed
- IT0008 (Assignment) changes applied and not blocked
- Wage type configuration verified in **SM30 V_T511F** (if custom wage types used)
- No pending retroactive changes that will block calculation

#### Step 2: Trigger Payroll Run (Execute calculation)

**Navigation**: Process Payroll app → [Payroll area] → Trigger Payroll Run

**What happens**:
- Submits batch job **PC00_M10_CALC** (US Payroll Calculation)
- SAP calculates gross pay, deductions, taxes, net pay for all eligible employees
- Results stored in payroll results table (PCL2)
- Job runs asynchronously; monitor progress in Process Payroll or **SM37** (Job Overview)

**SAP Transaction equivalent**: **SM37** (Job Overview)
- Monitor job status: scheduled → active → completed/error
- If error, review job log to identify blocking issue (usually wage type missing, table data inconsistent, formula error)

**Typical runtime**: 5-30 minutes (depends on employee count, complexity, system load)

**Checklist during run**:
- Don't release another payroll run until first one completes
- Monitor job log; don't wait for completion before checking on it
- If job takes >30 min longer than usual, investigate (system hang, lock contention, etc.)

#### Step 3: Post-Run Validation

**After job completes**:

1. **Check Payroll Results** (in Process Payroll app or **PC_PAYRESULT** Fiori app)
   - Spot-check 5-10 employees: verify gross, deductions, net match expectations
   - Check for obvious errors: $0 pay, negative net, missing tax withholding
   - For any anomalies, review employee's IT0200 (salary), IT0207 (federal tax), IT0208 (state tax)

2. **Run Payroll Results Report**
   - **Transaction SE16N**: Open table **PCL2** (Payroll results)
   - Quick checks: max salary, min salary, avg salary, net pay distribution
   - Look for outliers (negative net, unusually high/low values)

3. **Reconciliation Report**
   - Use **PC_PAYRESULT** to generate run-level summary: total gross, total deductions, total tax, total net
   - Compare to previous month (if routine): alert on >5% variance without explanation
   - If bonus/retroactive run, prepare variance explanation for approvers

#### Step 4: Posting Simulation (Optional but recommended)

**Navigation**: Process Payroll app → [Payroll area] → Posting Simulation

**What happens**:
- SAP simulates posting to GL accounts (Finance module FI)
- Generates provisional journal entries for labor cost, tax liabilities, net pay liability
- Does NOT commit to FI; for preview only

**Why do it**:
- Verify GL account mappings are correct
- Catch cost allocation issues before real posting
- Review for unexpected debit/credit balances

**Typical accounts**:
- **6100xx**: Labor cost (gross pay) by cost center
- **2100xx**: Tax withholding liabilities (federal, FICA, state, local)
- **2200xx**: Voluntary deduction liabilities (401k, health insurance, etc.)
- **2300xx**: Net pay liability (payable to employees)

#### Step 5: Bank File & DME Generation

**For Direct Deposit / ACH**:

**Navigation**: Process Payroll app → [Payroll area] → Generate DME/Bank File

**What happens**:
- SAP creates file in bank's expected format (NACHA for ACH, ABA for Fedwire, etc.)
- File includes: employee bank account, routing number, net pay amount, employee ID
- File ready for upload to bank portal for ACH transmission
- File typically generated before posting so bank can process same business day

**SAP Transaction equivalent**: **PCLT** (Payroll Bank File Generation) or **PG00** (Payment Run)

**Security note**:
- DME files contain sensitive banking data; handle per data security policy
- Encrypt before transmission if not using secure bank portal
- Verify file integrity (row count, total amount) before bank upload
- Audit trail: who generated, when, what bank file number

#### Step 6: Post to Finance (GL Posting)

**Navigation**: Process Payroll app → [Payroll area] → Post to Finance

**What happens**:
- Payroll results are posted as GL entries to Finance module (FI)
- Labor costs capitalized to cost centers, tax/deduction liabilities recorded
- Interfaced to subledgers (if configured) for AR/AP
- Payroll period locked from further changes (unless reversal initiated)

**Before posting, verify**:
- Posting simulation was reviewed and approved
- All accounting/approvers have signed off
- Period is not closed in Finance (if multi-company setup)

**After posting**:
- Review GL posting report: match to simulation
- Reconcile payroll liability accounts to accruals
- Flag any GL accounts with unexpected balances for investigation

#### Step 7: Exit Payroll (Close period)

**Navigation**: Process Payroll app → [Payroll area] → Exit Payroll

**What happens**:
- Payroll period is marked "Processed" in control record
- SAP generates payroll posting reports and audit logs
- Period locks; no new payroll calculations allowed for this period (retroactive changes go through Payroll Activity Manager)
- Payroll cycle officially closes

**After exit**:
- Generate remuneration statement (paystubs) for distribution
- Archive payroll results per compliance retention policy
- Document any exceptions/notes from the payroll run for future reference

---

## Off-Cycle Payroll Processing

**When to use off-cycle**:
- Employee termination and final pay (after regular payroll)
- Bonus payments (can be separate from regular payroll or combined)
- Wage corrections discovered mid-period (retro adjustment)
- Special payments (relocation, separation bonus, etc.)
- Catch-up payment (back pay from prior period)

**Workflow**:

1. **Access Payroll Activity Manager** app
2. **Create Payroll Activity**:
   - Select payroll area and employee(s)
   - Choose activity type: Bonus, Correction, Special Payment, Termination Final Pay
   - Set effective date (usually past or current date)
3. **Map Wage Types**:
   - Specify which wage types apply to this activity (e.g., "Bonus" wage type code, "Correction" wage type)
   - Enter amounts
4. **Submit for Processing**:
   - Activity routes through approval workflow (payroll manager, Finance approver)
   - Once approved, available for inclusion in next off-cycle payroll run
5. **Execute Off-Cycle Payroll**:
   - In Process Payroll app, select "Off-Cycle Run"
   - Select applicable activities (bonus payments, corrections, terminations)
   - Follow same production steps: Release → Trigger → Validate → Post → Exit
   - Off-cycle payroll has separate control record and results, doesn't affect regular payroll

**Tax and FLSA considerations**:
- Bonus withholding: can use supplemental flat rate (6% to 22% federal) or aggregate with regular pay
- Termination check: all earned wages must be paid; check state law for timing (same day, next business day, etc.)
- Overtime: off-cycle bonus payments don't affect overtime calculation for regular payroll
- Garnishment: off-cycle payments may have separate garnishment processing rules; check with Compliance

---

## Key SAP Transactions Reference

### Personnel Master Data

| Transaction | Purpose | When to use |
|---|---|---|
| **PA30** | Personnel master maintenance | Add/edit employee data, update salary, fix errors |
| **PA03** | Display payroll status | Check what master data is active for payroll |
| **SE16N V_PA0001** | Employee master query | Bulk search, verify hire dates, status |
| **SE16N V_PA0008** | Organizational assignment | Verify cost center, manager, payroll area |
| **SE16N V_PA0200** | Salary data query | Check compensation, effective dates |
| **SE16N V_PA0207** | Federal tax query | Verify W-4, withholding elections |
| **SE16N V_PA0208** | State tax query | Verify state residence, local tax setup |
| **SE16N V_PA0201** | Bank details query | Verify direct deposit account, routing |

### Payroll Execution

| Transaction | Purpose | When to use |
|---|---|---|
| **PU22** | Payroll control record | Check payroll period status, release lock |
| **PC00_M10_CALC** | US payroll calculation (batch job) | Not directly accessed; submitted via Process Payroll app |
| **PC_PAYRESULT** | Payroll results display (Fiori) | Review calculated pay, gross, tax, net |
| **SE16N PCL2** | Payroll results table (direct) | Query specific employee payroll results |
| **PA03** | Payroll status | Check overall payroll period readiness |
| **SM37** | Background job monitor | Track payroll job execution, view logs |
| **PCLT** | Bank file generation | Generate DME file for ACH transmission |
| **SE16N PCLV** | Payroll variation log | Identify changes from previous period |

### Monitoring & Reporting

| Transaction | Purpose | When to use |
|---|---|---|
| **Monitor Payroll (Fiori app)** | Alert and process tracking | Track alerts, status, aging, SLA |
| **My Payroll Processes (Fiori app)** | Work item dashboard | See your assigned alerts and tasks |
| **PC_PAYSLIP** | Electronic paystub (Fiori) | Review paystub for employee |
| **RPMTLSTD** | Payroll Master List | Generate master data snapshot report |
| **RPUAUD00** | Payroll audit trail | Track changes to payroll data |

### Wage Type & Configuration

| Transaction | Purpose | When to use |
|---|---|---|
| **SM30 V_T511F** | Wage type maintenance | Define/edit wage types, tax treatment |
| **SE16N T511** | Wage type characteristics (direct query) | Verify tax class, wage type logic |
| **RPUCOMP00** | Payroll control configuration | Check cumulative wage type settings |
| **SM37** | Customizing job monitor | Check if wage type customizing is running |

### Finance Integration

| Transaction | Purpose | When to use |
|---|---|---|
| **FB50** | GL account posting | Manual GL entries (if needed for adjustment) |
| **SE16N BSID** | Open AR items | Find payroll-related AR issues |
| **SE16N BSLN** | GL line items | Verify payroll posting to GL |
| **RPSCO000** | Payroll to GL reconciliation report | Reconcile payroll totals to GL |

---

## Common Procedures & Troubleshooting

### Procedure: Running a Retroactive Adjustment

**Scenario**: Salary increase effective mid-month; need to recalculate prior pay.

**Steps**:

1. **Document the Change**:
   - Capture effective date, old rate, new rate
   - Get approval from HR and Finance
   - Identify all employees affected

2. **Make Master Data Change** (PA30):
   - Entry type IT0200 (salary)
   - New salary amount, effective date (the mid-month date)
   - Old salary lines no longer active as of this date

3. **Create Payroll Activity**:
   - Access Payroll Activity Manager
   - Select "Retroactive Adjustment"
   - Link to affected employees and payroll period
   - SAP will recalculate pay from the effective date through end of month

4. **Review Impact**:
   - Run payroll calculation on activity
   - Compare to original run: employee should show higher gross, possibly different tax
   - If impact looks wrong, recheck IT0200 entry effective date

5. **Post Off-Cycle**:
   - Follow off-cycle payroll posting steps
   - Issue corrected pay via off-cycle check or adjusted ACH payment
   - Prepare variance explanation for Finance reconciliation

### Procedure: Processing an Employee Termination

**Scenario**: Employee terminated mid-month; need to process final pay.

**Steps**:

1. **Record Termination in Master Data** (PA30, IT0001):
   - Entry type IT0001 (employment status)
   - Status "Termination" or "Released"
   - Termination date (last day worked)
   - Reason code (resignation, layoff, retirement, etc.)

2. **Calculate Unused Vacation Payout**:
   - Check IT0261 (vacation/leave balance)
   - Calculate payout: days remaining × daily rate
   - Verify state law (some states require full payout; others allow forfeiture)

3. **Check for Pending Garnishments**:
   - Review IT0285 (garnishment orders) for this employee
   - Are there any remaining garnishment amounts due?
   - Flag for Compliance if active garnishment exists

4. **Create Termination Activity**:
   - Payroll Activity Manager → Create activity type "Termination Final Pay"
   - Include final wages (regular + vacation payout)
   - Map wage types: regular hours (prorated), vacation payout
   - Set effective date = termination date

5. **Submit for Approval**:
   - Route to Finance and HR approver
   - Approval workflow supports manager sign-off

6. **Process Off-Cycle**:
   - Once approved, run off-cycle payroll for termination activity
   - Final check: net pay amount, no negative pay, all deductions processed correctly
   - Post to Finance

7. **Post-Termination Tasks**:
   - Issue final paystub and W-2 (if year-end)
   - Coordinate with Compliance for COBRA notice (if applicable)
   - Mark IT0001 as past-dated to prevent future payroll inclusion
   - Archive employee payroll file

---

## Best Practices & Tips

1. **Always use Team Monitoring view during monitoring phase**: Catch alert trends early (e.g., if 20 employees missing W-4, it's a data load issue, not 20 individual problems).

2. **Never skip Posting Simulation**: Takes 2 minutes; can reveal GL mapping errors before they post permanently.

3. **Check job logs proactively**: Don't wait for payroll to fail visibly. Check SM37 every 10 minutes during payroll run for early warnings.

4. **Document exceptions**: If you resolve an alert in an unusual way (e.g., "Manager approved negative net pay due to high deduction"), write a note in the alert for audit trail.

5. **Keep master data changes out of payroll period**: If a change is needed mid-cycle, use retroactive adjustment through Payroll Activity Manager, not direct master data edits.

6. **Test wage type changes before production**: New wage type or change to tax treatment? Run a test payroll first (in UAT or use Process Payroll simulation).

7. **Communicate payroll schedule**: Let Finance, managers, employees know cutoff time, expected paystub delivery date. Set expectations.

8. **Archive payroll results**: After exit, save PCL2 export and final GL posting report per compliance retention (typically 3-7 years for payroll).

