# SAP Payroll Transactions & Infotypes Reference

A quick reference guide for essential SAP transactions and infotypes used in US payroll operations in SAP Payroll Control Center (PCC).

---

## Core Payroll Transactions

### PA30: Maintain HR Master Data
**What It Does**: Create, edit, and maintain employee infotypes (master data). This is the primary transaction for all employee setup and changes.

**When to Use**:
- New hire setup (create IT0001, IT0002, IT0006, IT0008, IT0009, IT0210, IT0208, IT0209, IT0206, IT0207)
- Employee changes (salary increase, position change, cost center change, address change, W-4 update, bank detail change)
- Termination setup (end-date infotypes, final compensation)

**Navigation Path**: SAP Menu → Human Resources → Personnel Management → Data → Maintain → Employee → PA30

**Key Shortcuts**:
- **SAP Easy Access**: Type "PA30" in command box, press Enter
- Shortcut: Ctrl+F5 (depending on SAP config)

**Common Tips**:
- Use "Infotype" dropdown to search for specific infotype (0001, 0210, etc.)
- Set date range at top of screen to find specific infotype instances
- Use "Copy" button to duplicate previous IT0001 for easy date continuation
- Always confirm start/end dates have no gaps
- Click "Infotype Catalog" button to view all available infotypes and their purposes

**Infotype Fields to Know**:
- **Start Date / End Date**: Validity period for this infotype record
- **Status**: Active vs. Inactive indicator (if infotype supports it)
- **Sequence Number**: For infotypes with multiple records; determines priority
- **Changed By / Date**: Audit trail (system-maintained)

---

### PA20: Display HR Master Data
**What It Does**: View employee infotypes without editing. Read-only transaction; cannot make changes.

**When to Use**:
- Review employee setup before payroll run
- Audit trail: Check when employee data was last changed
- Investigation: Look up employee address, bank details, tax setup
- Pre-payroll validation: Verify all required infotypes are present and current

**Navigation Path**: SAP Menu → Human Resources → Personnel Management → Data → Display → Employee → PA20

**Key Shortcuts**:
- SAP Easy Access: Type "PA20"
- Same transaction family as PA30; same infotype structure

**Common Tips**:
- More efficient than PA30 for quick lookups (no risk of accidental changes)
- Use date range filters to find specific infotype records by effective date
- Click "Change Log" to see audit trail of who changed what and when
- Can print infotype summaries for documentation

---

### PC00_M10_CALC: US Payroll Run
**What It Does**: Execute the US payroll calculation. Processes time data, applies wage types, calculates taxes, deductions, and gross-to-net in SAP PCC Fiori app.

**When to Use**:
- Production payroll run (monthly, bi-weekly, weekly depending on company)
- Payroll simulation/testing before final run
- Retroactive payroll (previous period recalculation)
- Off-cycle bonus or correction payroll

**Navigation Path**: SAP Fiori App: "Process Payroll" or via SAP Easy Access: Type "PC00_M10_CALC"

**Key Execution Steps**:
1. Select payroll area (e.g., "US0001")
2. Select payroll period (e.g., "01/2025" for January 2025)
3. Select run type:
   - "A" = Regular payroll
   - "B" = Additional (off-cycle)
   - "C" = Correction (prior period)
4. Select simulation mode:
   - "Simulate" = Test run (no results saved)
   - "Production" = Actual payroll (results saved)
5. Click "Start"
6. Monitor progress; review log for errors/warnings

**Output**:
- Payroll results (wages, taxes, deductions, net pay per employee)
- GL posting preview
- Alerts flagged (missing data, configuration issues)

**Common Tips**:
- Always run in "Simulate" mode first to catch errors before production
- Review log for any warnings (missing tax data, time data issues, etc.)
- Press F5 to refresh if run appears hung
- Use "Breakpoint" feature to stop execution at specific point for debugging

---

### PC00_M10_CDTA: DME File Creation (Bank Payments)
**What It Does**: Generate DME (Data Medium Exchange) file for bank/ACH processing. Creates the file with employee bank account details and payment amounts for direct deposit processing.

**When to Use**:
- Before payroll release (to prepare ACH file for bank)
- Post-payroll to reconcile bank file format
- Testing: Generate preliminary DME to validate employee bank details

**Navigation Path**: SAP Fiori: "My Payroll Processes" → "Payroll Release" → or SAP Easy Access: Type "PC00_M10_CDTA"

**Key Execution Steps**:
1. Select payroll area and period
2. Select preliminary (test) or final (production)
3. Select file format (depends on your bank/processor; typically "NACHA" for US ACH)
4. Click "Create"
5. Review output file for:
   - Employee name, bank routing, account number
   - Payment amount per employee
   - Batch total (sum of all payments)

**Output**: DME file (typically .txt or .asc format) ready for bank upload

**Common Tips**:
- Run "Preliminary" DME before payroll release to catch bank detail issues
- If DME shows $0 for an employee, check if:
  - Net pay is negative or zero
  - Bank details (IT0009) are missing or inactive
  - Employee marked as inactive
- Coordinate with Finance on final file format and timing
- Keep audit trail of all DME files generated per payroll cycle

---

### PC00_M10_CEDT: Remuneration Statement (Payslips)
**What It Does**: Generate payslips (remuneration statements) for employee distribution. Also used for W-2 report generation.

**When to Use**:
- Generate payslips for distribution to employees (email, print, portal)
- W-2 preparation at year-end
- Employee payslip inquiries (employee asks for copy of past payslip)

**Navigation Path**: SAP Fiori: "My Payroll Processes" → "Payroll Release" → or SAP Easy Access: Type "PC00_M10_CEDT"

**Key Execution Steps**:
1. Select payroll area and period(s) (can select multiple periods for annual W-2)
2. Select employee(s) (all or specific)
3. Select output format (PDF, online portal, etc.)
4. Click "Start"
5. Download or view output

**Output**: PDF payslips (one per employee per period) showing:
- Gross wages (by wage type)
- Deductions (taxes, benefits, garnishments)
- Net pay
- YTD totals
- Employee tax/benefits summary (on W-2 reports)

**Common Tips**:
- For W-2: Select all 12 periods of the year (01 through 12)
- Verify payslip totals before distribution to employees (spot-check a few)
- Employee complaints about payslip usually indicate missing deductions or wrong gross amount
- Archive PDF copies for audit trail

---

### PC_PAYRESULT: Display Payroll Results
**What It Does**: View detailed payroll calculation results after payroll run. Drill into wage types, taxes, deductions by employee or in summary view.

**When to Use**:
- After PC00_M10_CALC completes; review results before release
- Alert investigation (missing data, negative net pay, etc.)
- Employee inquiry: Show employee detail of their gross, taxes, deductions
- GL reconciliation: Review GL posting amounts before posting

**Navigation Path**: SAP Fiori: "Payroll Results" or SAP Easy Access: Type "PC_PAYRESULT"

**Key Views**:
- **Summary View**: All employees, wage types, taxes, deductions at a glance
- **Employee Detail View**: Drill into individual employee (all wage types, deductions, net pay)
- **GL Posting Preview**: Cost center allocation before GL posting
- **Alert/Warning Summary**: Flags any data issues requiring resolution

**Common Tips**:
- Use "Filter" to drill into specific employee or wage type
- Compare to prior period to catch unusual changes
- Review "GL Posting" tab to confirm cost center distribution
- Export to Excel if needed for reconciliation with Finance
- Use "Alert" section to identify issues before release

---

### PU19: Delete Payroll Results
**What It Does**: Remove saved payroll results from the system (if payroll was run in production mode but needs to be re-done).

**When to Use**:
- Payroll run was made in error (wrong period, wrong data)
- Need to re-run payroll with corrections before GL posting
- Accidental duplicate payroll run

**Navigation Path**: SAP Easy Access: Type "PU19"

**Critical Warnings**:
- Use only BEFORE GL posting; once posted to GL, do NOT use PU19
- If results already posted to GL, use correction entry in GL instead
- Always backup payroll results before deletion
- Require manager/supervisor approval before executing PU19

---

### PU03: Change Payroll Status
**What It Does**: Change the payroll area status (Open, Locked, Released, Exit). Used to manage payroll workflow and unlock locked payroll areas.

**When to Use**:
- Release payroll area after payroll run complete and validated (change from "Locked" to "Released")
- Unlock a payroll area that is stuck in "Locked" status due to hung process
- Transition payroll area to "Exit" status for off-cycle processing or final payroll

**Navigation Path**: SAP Easy Access: Type "PU03"

**Key Status Workflow**:
1. **Open**: Default; ready for payroll processing
2. **Locked**: During payroll run; prevents other users from processing
3. **Released**: Payroll complete and validated; ready for GL posting
4. **Exit**: Special status for off-cycle payroll; prevents time data updates

**Common Tips**:
- Do NOT force status change unless you're certain no payroll process is active
- Check SM37 (Job Overview) and SM04 (Users) before manually unlocking
- Document any manual status changes in payroll log
- Releasing from "Locked" to "Released" allows GL posting to proceed

---

### SM37: Job Overview
**What It Does**: Monitor background job execution. Track payroll interface jobs, time transfer jobs, GL posting jobs, and diagnostic jobs.

**When to Use**:
- Monitor long-running payroll job (PC00_M10_CALC)
- Check if time transfer interface job completed successfully
- Diagnose job failures (timeouts, errors, incomplete runs)
- Identify which user/job is locking the payroll area

**Navigation Path**: SAP Menu → System → Administration → Jobs → Job Overview OR SAP Easy Access: Type "SM37"

**Key Searches**:
- Search for "PC00_M10" (payroll jobs)
- Search for "CAT" or "Time" (time transfer jobs)
- Search for "RFDPOST" (GL posting job)
- Filter by date/time to find jobs run in specific window

**Common Tips**:
- Look for "Active" jobs to see what's running now
- Look for "Finished" jobs to see status (completed successfully or errors)
- Click job name to see logs/errors
- If job is hung (status "Active" for > 1 hour), request Basis team to kill it

---

### SE16N: Table Browser (Debugging)
**What It Does**: Browse and search SAP database tables directly. Advanced tool for diagnostics.

**When to Use**:
- Debug complex issues (wage type calculations, cumulative limits not working)
- Verify data integrity (confirm wages are in database as expected)
- Extract data for reconciliation (query payroll results table directly)

**Navigation Path**: SAP Easy Access: Type "SE16N"

**Common Payroll Tables**:
- **COEP**: Cost Element Postings (GL posting detail)
- **T512C**: Payroll Tables (configuration)
- **PPALOG**: Payroll Master Data Log (audit trail)
- **HRPY_RESULT**: Payroll Results (wage type detail)

**Warning**: SE16N is powerful but can slow system if not used carefully; don't run large queries

---

## Infotype Reference (Employee Master Data)

### IT0001: Organizational Assignment
**What It Is**: Employee's position, department, cost center, job classification, and reporting line.

**Key Fields**:
- Organizational Unit (cost center)
- Position
- Job
- Start Date / End Date
- Employment Status (full-time, part-time, contract)

**Payroll Impact**:
- Cost center used for GL posting (labor cost allocation)
- Job classification determines FLSA exempt/non-exempt status
- Employment status affects benefits eligibility

**Mandatory**: Yes, for all employees

**SAP Transaction**: PA30 (maintain), PA20 (display)

---

### IT0002: Personal Data
**What It Is**: Employee's name, date of birth, gender, marital status, nationality.

**Key Fields**:
- First Name, Last Name
- Date of Birth
- Gender (M/F)
- Marital Status (Single, Married, Divorced, Widowed)
- Nationality/Country of Citizenship

**Payroll Impact**:
- DOB used for age-based benefits eligibility (e.g., dependent age limits)
- Marital status influences tax withholding filing status options
- Nationality flags non-resident alien withholding (if applicable)

**Mandatory**: Yes, for all employees

**SAP Transaction**: PA30, PA20

---

### IT0006: Address (Personal)
**What It Is**: Employee's home address (street, city, state, zip, country).

**Key Fields**:
- Street Address
- City / State / ZIP
- Country
- Phone Number
- E-mail Address

**Payroll Impact**:
- State of residence used for state tax withholding determination
- Address used for W-2 mailing and payroll document delivery
- Local/municipal tax may depend on residence address

**Mandatory**: Yes; required for W-2 and tax compliance

**SAP Transaction**: PA30, PA20

---

### IT0008: Basic Pay
**What It Is**: Employee's base salary, hourly rate, or pay scale assignment.

**Key Fields**:
- Salary Amount (annual salary, if salaried)
- Hourly Rate (if hourly)
- Pay Scale Group & Level (if using SAP pay scale)
- Start Date / End Date (validity of this pay)
- Currency

**Payroll Impact**:
- Basis for gross wage calculation
- Subject to federal/state tax withholding
- Determines OT calculation base (hourly employees)

**Mandatory**: Yes, for all employees

**SAP Transaction**: PA30, PA20

**Common Changes**:
- Salary increase: Update IT0008 with new amount, effective date
- Pay scale promotion: Update with new pay scale level, effective date

---

### IT0009: Bank Details
**What It Is**: Employee's direct deposit bank account information for ACH transfers.

**Key Fields**:
- Bank Country
- Bank Key (Routing Number, ABA code - 9 digits)
- Bank Account Number
- Account Holder Name
- Account Type (Checking C / Savings S)
- Account Currency

**Payroll Impact**:
- Required for direct deposit processing
- Used in DME (bank file) generation for ACH
- Missing/invalid IT0009 prevents direct deposit

**Mandatory**: For employees receiving direct deposit; optional if receiving check

**SAP Transaction**: PA30, PA20

**Tips**:
- Multiple accounts: Can create multiple IT0009 records with split percentages
- Verify bank details with employee before first payroll
- Quarterly audit: Confirm all active employees have valid IT0009

---

### IT0014: Recurring Payments / Deductions
**What It Is**: Recurring benefit/deduction amounts (e.g., health insurance premium, union dues, garnishment) applied every payroll period.

**Key Fields**:
- Deduction Type / Wage Type (e.g., health insurance, union dues)
- Amount or Percentage
- Start Date / End Date
- Frequency

**Payroll Impact**:
- Deduction amounts subtracted from gross to calculate net pay
- Pre-tax vs. post-tax determination affects taxable wages
- Used for benefit contributions and mandatory deductions

**Mandatory**: If employee has recurring deductions

**SAP Transaction**: PA30, PA20

---

### IT0015: Additional Payments
**What It Is**: One-time or irregular payments/deductions (e.g., bonus, commission, retroactive pay adjustment, back-owed premium).

**Key Fields**:
- Wage Type / Payment Type
- Amount
- Number of Units (if hourly, e.g., hours)
- Start Date
- Text/Memo

**Payroll Impact**:
- Added to gross wages in current payroll period
- Subject to withholding unless marked as non-taxable
- Used for bonuses, commissions, corrections, adjustments

**Mandatory**: Only when needed for specific payments/adjustments

**SAP Transaction**: PA30, PA20

**Common Uses**:
- Bonus entry
- Retroactive salary adjustment
- Correction of prior payroll error
- Commission
- Reimbursement (if taxable)

---

### IT0206: Benefit Plan
**What It Is**: Employee's benefit plan elections (health insurance plan, dental, vision, 401k, FSA enrollment).

**Key Fields**:
- Benefit Plan Code (e.g., "PPO", "HDHP", "401K")
- Start Date / End Date
- Waived Indicator (if employee waived coverage)

**Payroll Impact**:
- Determines which deductions/contributions apply to payroll
- Missing/expired IT0206 may trigger "Benefit Enrollment Gap" alert
- Coordinated with IT0207 (Benefit Deductions)

**Mandatory**: For employees enrolled in benefits; optional for those waiving coverage

**SAP Transaction**: PA30, PA20

**Coordination**: Should be created in conjunction with IT0207 (amounts)

---

### IT0207: Benefit Deductions (Amounts)
**What It Is**: Specific deduction amounts for each benefit plan elected (IT0206).

**Key Fields**:
- Deduction Type (health insurance, FSA, HSA, etc.)
- Amount per Period
- Pre-tax or Post-tax Indicator
- Start Date / End Date

**Payroll Impact**:
- Deduction amounts subtracted from gross wages
- Pre-tax deductions reduce federal/state taxable wages
- Post-tax deductions do NOT reduce taxable wages

**Mandatory**: If IT0206 exists, IT0207 should define the deduction amounts

**SAP Transaction**: PA30, PA20

**Example**:
- IT0206: Employee enrolled in "PPO health" plan
- IT0207: PPO monthly deduction = $400 (pre-tax)

---

### IT0208: State Tax Data
**What It Is**: Employee's state income tax withholding setup (state of residence, filing status, special rules).

**Key Fields**:
- State (e.g., "NY" for New York)
- Filing Status (Single, Married, Head of Household, etc.; state-specific)
- Exemptions / Dependents (state form equivalent of federal W-4)
- Withholding Amount

**Payroll Impact**:
- Determines state income tax withholding
- Multi-state employees may have multiple IT0208 records (one per state)
- State tax reciprocity agreements affect which states to withhold

**Mandatory**: For employees with state income tax requirements (most states)

**SAP Transaction**: PA30, PA20

**Common Issues**:
- Multi-state employee: Wrong state selected (should withhold both NY and NJ if no reciprocity)
- Reciprocity confusion: NJ-PA no reciprocity; IL-IN has reciprocity
- Date gaps: Employee transferred from CA to NY; old CA IT0208 not end-dated

---

### IT0209: Unemployment Insurance
**What It Is**: State unemployment insurance (SUI) state assignment. Determines which state's SUI rate/wage base applies.

**Key Fields**:
- State (e.g., "CA" for California)
- Start Date / End Date

**Payroll Impact**:
- Determines SUI withholding amount (employee + employer)
- Multi-state: May have multiple IT0209 if employee works in multiple SUI states
- SDI/PFL (CA) also tied to this assignment

**Mandatory**: Yes, for all employees

**SAP Transaction**: PA30, PA20

**Notes**:
- Typically same state as IT0208, but not always (e.g., employee works in TX but lives in CA)

---

### IT0210: Federal Tax Data (US)
**What It Is**: Employee's federal income tax withholding setup from Form W-4.

**Key Fields**:
- Filing Status (Single, Married Filing Jointly, etc.)
- Federal Exemptions or Dependents (from W-4)
- Extra Withholding (additional $ per paycheck)
- Tax Authority (Federal)
- Status (Active/Inactive)

**Payroll Impact**:
- Determines federal income tax withholding per paycheck
- Must be updated whenever employee submits new W-4
- Missing IT0210 triggers "Missing Tax Data" alert

**Mandatory**: Yes, for all employees

**SAP Transaction**: PA30, PA20

**Common Issues**:
- Blank/inactive IT0210: New hires without completed W-4
- Wrong filing status: Employee married but filed as Single
- Exemptions/dependents outdated: Employee had child; didn't update W-4

---

### IT0194: Garnishment
**What It Is**: Court-ordered wage garnishment details (child support, tax levy, creditor garnishment, student loan).

**Key Fields**:
- Garnishment Type (e.g., "CHILDSP" for child support)
- Garnishment Start Date / End Date
- Garnishment Amount or Percentage
- Order Reference / Court Case Number

**Payroll Impact**:
- Deduction from net pay (after tax calculation)
- Subject to federal/state garnishment limits
- Multiple garnishments require priority sequencing

**Mandatory**: Only if employee is subject to garnishment

**SAP Transaction**: PA30, PA20

**Coordination**: Works with IT0195 (Garnishment Terms) for calculation details

---

### IT0195: Garnishment Terms
**What It Is**: Detailed calculation parameters for garnishment (disposable income formula, frequency, limits).

**Key Fields**:
- Calculation Method (percentage, fixed amount, etc.)
- Frequency of Payment
- Exemption Amount
- Maximum Limit

**Payroll Impact**:
- Determines exact garnishment calculation (% of disposable income vs. fixed amount)
- Ensures compliance with federal 25% limit (for creditor garnishments)
- Higher limits may apply for child support/tax levies

**Mandatory**: If IT0194 exists, IT0195 provides calculation rules

**SAP Transaction**: PA30, PA20

---

## Quick Infotype Setup Checklist (New Hire Payroll)

**Mandatory for All Hires**:
- [ ] IT0001 (Org Assignment): Department, position, cost center
- [ ] IT0002 (Personal Data): Name, DOB, gender, marital status
- [ ] IT0006 (Address): Home address, state (for tax purposes)
- [ ] IT0008 (Basic Pay): Salary or hourly rate
- [ ] IT0009 (Bank Details): Bank routing, account (for direct deposit)
- [ ] IT0210 (Federal Tax): Filing status, exemptions from W-4
- [ ] IT0208 (State Tax): State of residence, filing status
- [ ] IT0209 (SUI): Unemployment insurance state

**Conditional**:
- [ ] IT0007 (Time Recording): If hourly employee needing time tracking
- [ ] IT0206 + IT0207 (Benefits): If employee enrolled in health insurance, 401k, FSA
- [ ] IT0014/0015 (Recurring/Additional): If recurring deductions or one-time payments
- [ ] IT0194/0195 (Garnishment): If subject to court order garnishment

---

**Remember**: Always verify infotype dates have no gaps, and confirm all mandatory infotypes are present before first payroll run.
