# SAP PCC Payroll Alert Catalog

Complete catalog of 25+ alert types organized by category. Each alert includes description, root causes, resolution steps, blocking status, and typical severity.

---

## DATA QUALITY ALERTS

### 1. Missing Tax Data

**Description**: Employee record missing required tax information (Federal Tax ID, state withholding allowances, exemptions, or residence state).

**Category**: Data Quality

**Blocking**: Yes (prevents payroll calculation)

**Typical Severity**: Medium to High

**Affected Employees**: 1-1000+ (often batch import issue)

**Root Causes**:
- New employee data not fully entered from HR system
- Tax data removed by payroll freeze without re-entry
- Withholding form not received from employee
- State change without updating residence
- System migration data loss or corruption
- Batch import missing tax columns

**Resolution Steps**:
1. Access PA30 to view employee master record
2. Check PA40 for tax identification numbers (Tax ID, SSN)
3. Verify PE10 tax data entry (federal, state, local withholding)
4. Compare with HR system or latest W4 form from employee
5. Update missing fields in PA40 or PE10
6. Run tax recalculation in PT61
7. Validate tax deductions match expectations
8. Document correction and mark alert resolved

**SAP Transactions**: PA30, PA40, PE10, PE03, PT61

**SLA**: P2 (4-hour resolution)

**Prevention**:
- Mandatory tax data audit before payroll run
- Employee self-service portal for tax form updates
- Integration of HR and payroll tax data

---

### 2. Invalid Bank Details

**Description**: Employee bank account information is missing, invalid, or unverified (account number, routing number, or account type mismatch).

**Category**: Data Quality

**Blocking**: Yes (prevents ACH processing)

**Typical Severity**: Medium

**Affected Employees**: 1-100 (typically direct deposit dependent)

**Root Causes**:
- Employee provided incomplete account information
- Routing number incorrect or outdated
- Account type changed (checking to savings) without notification
- Bank merger with routing number change
- Typo in account number during data entry
- Employee terminated but direct deposit not removed

**Resolution Steps**:
1. Access PA39 to view bank account details
2. Verify account format: routing number (9 digits), account number (10-12 digits)
3. Contact employee to confirm correct bank information
4. Validate routing number against Federal Reserve routing table
5. Update PA39 with correct account information
6. Run ACH validation test
7. Confirm employee acknowledgment of account change
8. Document update and mark alert resolved

**SAP Transactions**: PA39, PA40, PT09 (ACH processing)

**SLA**: P2 (4-hour resolution)

**Prevention**:
- Bank account verification during onboarding
- Annual bank account re-verification audit
- ACH pre-notification periods for account changes
- Employee self-service bank account updates

---

### 3. Missing Employee Data

**Description**: Employee master record incomplete or missing required fields (name, SSN, address, hire date, employment type, or department).

**Category**: Data Quality

**Blocking**: Varies (may block compliance reporting)

**Typical Severity**: Low to Medium

**Affected Employees**: 1-50

**Root Causes**:
- Incomplete employee record at hire
- Data purged during system cleanup
- Employee record created as placeholder without full details
- Temporary assignment missing permanent data
- System migration with data mapping errors

**Resolution Steps**:
1. Identify which fields are missing in PA30
2. Reference employee file or HR system for accurate data
3. Update PA40 with complete employee information
4. Verify all required fields per SAP configuration
5. Run data quality validation report
6. Confirm updates with HR if needed
7. Document changes and mark alert resolved

**SAP Transactions**: PA30, PA40, HR00

**SLA**: P3 (1-day resolution)

**Prevention**:
- Mandatory field validation at hire
- Regular employee master data audits
- Integration with HR system to auto-populate

---

### 4. Time Data Discrepancies

**Description**: Employee's time data does not match expected hours (missing time entries, duplicate entries, or calculated hours do not match submitted timesheet).

**Category**: Data Quality

**Blocking**: Varies (impacts payroll accuracy)

**Typical Severity**: Low to Medium

**Affected Employees**: 1-100 (varies by payroll period)

**Root Causes**:
- Employee failed to submit timesheet on time
- Time entry system did not sync with payroll system
- Duplicate hours entered in time system
- Retroactive time entry missed initial import
- Time off code not properly entered
- Shift change not updated in payroll

**Resolution Steps**:
1. Access PE02 to view employee time entries
2. Compare PE02 entries with submitted timesheet
3. Identify discrepancies (missing days, duplicate hours, wrong time off)
4. Contact employee or supervisor for clarification
5. Update time entries in PE02 with corrected hours
6. Run PE03 time evaluation to validate
7. Confirm time matches payroll calculation in PT61
8. Document correction and mark alert resolved

**SAP Transactions**: PE02, PE03, PT61

**SLA**: P3 (1-day resolution)

**Prevention**:
- Automated time tracking system integration
- Time entry deadline enforcement
- Daily time data reconciliation report

---

### 5. Cost Center Missing

**Description**: Employee record missing required cost center assignment or cost center is inactive/invalid for payroll processing.

**Category**: Data Quality

**Blocking**: Yes (prevents GL posting)

**Typical Severity**: Medium

**Affected Employees**: 1-50 (typically new hires or transfers)

**Root Causes**:
- Employee hired or transferred without cost center update
- Cost center was closed or inactivated
- Wrong cost center assigned during onboarding
- Employee works across multiple cost centers without allocation
- System migration cost center mapping error

**Resolution Steps**:
1. Access PA30 to check cost center assignment (Org Assignment)
2. Verify cost center is active in COA (chart of accounts)
3. Confirm correct cost center with employee's manager/HR
4. Update PA40 with correct active cost center
5. For multi-cost-center employees, split salary using percentage allocation
6. Validate GL posting in FAGLL03
7. Document correction and mark alert resolved

**SAP Transactions**: PA30, PA40, KO05, FAGLL03

**SLA**: P2 (4-hour resolution)

**Prevention**:
- Cost center assignment mandatory at hire
- HR-Payroll cost center sync
- Monthly cost center reconciliation

---

### 6. Duplicate Employee Records

**Description**: System identifies duplicate or near-duplicate employee records with different employee IDs but same person.

**Category**: Data Quality

**Blocking**: May block payroll processing for duplicates

**Typical Severity**: Medium to High

**Affected Employees**: 2+ (duplicates)

**Root Causes**:
- Employee hired under different legal entity or cost center
- System migration data duplication
- Manual record entry error during onboarding
- Name variation in data entry (Jr., Jr, etc.)
- Rehire of former employee with new ID
- Contractor data mixed with employee data

**Resolution Steps**:
1. Identify duplicate records using employee name, SSN, birth date
2. Determine which record is primary and which is duplicate
3. Review both records for data completeness
4. Consolidate data (choose most complete record)
5. Merge or delete duplicate record following SAP procedure
6. Update all references to point to primary record ID
7. Run reconciliation to ensure no orphaned data
8. Document merge and mark alert resolved

**SAP Transactions**: PA20, PA30, PA40, SUIM (find usage)

**SLA**: P2 (4-hour resolution)

**Prevention**:
- Employee ID lookup before hire
- Name/SSN verification during onboarding
- Regular duplicate detection audit

---

## COMPLIANCE ALERTS

### 7. Tax Reciprocity Violation

**Description**: Employee is subject to tax reciprocity agreement but payroll is withholding incorrect state taxes (e.g., employee works in PA but lives in NJ under reciprocal agreement).

**Category**: Compliance

**Blocking**: Yes (prevents legal tax withholding)

**Typical Severity**: High

**Affected Employees**: 1-50 (typically regional border employees)

**Root Causes**:
- Reciprocity agreement not configured in tax setup
- Wrong work state (CWAGE) configured for employee
- Wrong home state (residence) configured
- Tax reciprocity rule changed by state (annually)
- Employee moved; residency status not updated

**Resolution Steps**:
1. Verify employee's home state and work state in PA30
2. Check reciprocal agreement between states (e.g., PA-NJ reciprocity)
3. Access PE05 to verify reciprocity configuration
4. Update work state or tax configuration if incorrect
5. Run tax recalculation in PT61
6. Validate new tax withholding vs. expected amount
7. Document reciprocity rule applied and mark alert resolved
8. May require employee letter explaining withholding change

**SAP Transactions**: PA30, PE05, PE03, PT61

**SLA**: P2 (4-hour resolution)

**Prevention**:
- Annual reciprocity agreement review
- State tax configuration audit
- Employee state/residence verification

---

### 8. Garnishment Error

**Description**: Court-ordered garnishment (wage attachment, child support, tax levy) is not being processed or is calculated incorrectly.

**Category**: Compliance

**Blocking**: Yes (prevents legal obligation fulfillment)

**Typical Severity**: High (regulatory violation)

**Affected Employees**: 1-20 (garnishment holders)

**Root Causes**:
- Court order not entered into system
- Garnishment amount or calculation incorrect
- Garnishment expired but not removed from system
- Multiple garnishments not prioritized correctly
- Supporting wage calculation incorrect
- Garnishment remittance not tracked properly

**Resolution Steps**:
1. Obtain court order or legal documentation
2. Verify current garnishment status in PE04
3. Validate garnishment amount, effective date, expiration date
4. Check supporting wage calculation (max garnishable amount)
5. If creating new garnishment: enter in PE04 with court order reference
6. If correcting: update amount or dates in PE04
7. Run payroll simulation to verify correct garnishment processing
8. Confirm remittance schedule for garnishment payment
9. Document court order reference and mark alert resolved

**SAP Transactions**: PE04, PT04 (simulate payroll), PT09 (payroll run)

**SLA**: P1 (1-hour resolution)

**Prevention**:
- Legal/Compliance team monthly review of garnishments
- Court order tracking system
- Garnishment validation before payroll run

---

### 9. Regulatory Filing Delay

**Description**: Regulatory filing deadline is approaching or has passed without completion (tax returns, wage reports, audit responses).

**Category**: Compliance

**Blocking**: Yes (regulatory obligation)

**Typical Severity**: Critical (penalties/interest)

**Affected Employees**: All (affects company compliance)

**Root Causes**:
- Filing calendar not tracked or missed
- Supporting payroll data not ready for filing
- Payroll audit findings not resolved
- Regulatory agency requesting additional information
- System unable to generate required report format

**Resolution Steps**:
1. Identify specific filing requirement and deadline
2. Determine filing status (not started, in progress, completed)
3. Identify missing data or supporting documentation
4. Gather payroll data needed for filing
5. Generate regulatory report (W2, 941, FUTA, etc.)
6. Submit filing to regulatory agency
7. Obtain filing confirmation number
8. Document filing confirmation and mark alert resolved

**SAP Transactions**: PA03, PE51 (tax filing status), custom regulatory reports

**SLA**: P1 (immediate action)

**Prevention**:
- Regulatory filing calendar
- Automated deadline reminders
- Payroll-to-filing process integration

---

### 10. Benefits Compliance Gap

**Description**: Employee is missing required benefit enrollment, has expired coverage, or is not receiving mandated benefits.

**Category**: Compliance

**Blocking**: May affect future payroll

**Typical Severity**: Medium

**Affected Employees**: 1-500 (may be group alert)

**Root Causes**:
- Open enrollment deadline missed
- Benefits election not entered into system
- Dependent coverage expired
- Life event not triggered benefit update
- Benefit plan rule change not applied
- Employee eligibility overlooked

**Resolution Steps**:
1. Determine which benefit is missing or expired
2. Check employee eligibility (tenure, hours, employment status)
3. Review benefit enrollment status in HR system
4. If employee-initiated missing: follow up with employee for election
5. If system-initiated missing: configure in payroll system
6. Update benefit deduction/contribution in PT60
7. Validate benefit posting in payroll run PT61
8. Document benefit update and mark alert resolved

**SAP Transactions**: PE06 (benefits), HR00, PT60, PT61

**SLA**: P2 (4-hour resolution)

**Prevention**:
- Benefits enrollment deadline automation
- Annual compliance audit
- Eligibility validation at hire

---

### 11. Wage Law Violation

**Description**: Payroll calculation violates wage law (minimum wage, overtime rules, shift differential rules, or meal/rest break requirements).

**Category**: Compliance

**Blocking**: May prevent lawful payroll

**Typical Severity**: High

**Affected Employees**: 1-100+ (may be batch issue)

**Root Causes**:
- Wage rules not properly configured for jurisdiction
- Wage type calculation incorrect
- Overtime rules not applied to hours worked
- Shift differential not properly paid
- Minimum wage increase not reflected in salary
- Meal/rest break deduction applied incorrectly

**Resolution Steps**:
1. Identify which wage law is violated
2. Verify jurisdiction-specific wage rule requirements
3. Check wage type configuration in PT40/PT50
4. Compare calculated wage vs. legal requirement
5. Adjust wage type calculation or gross pay
6. For retroactive violation: run retro pay adjustment
7. Run payroll validation to confirm compliance
8. Document wage law citation and mark alert resolved

**SAP Transactions**: PT40, PT50, PT04 (simulate), PT09 (payroll run)

**SLA**: P1-P2 (depending on scope)

**Prevention**:
- Wage law configuration review annually
- Jurisdiction-specific rule training
- Payroll calculation audit vs. legal requirements

---

## PROCESSING ALERTS

### 12. Wage Type Collision

**Description**: Two or more wage types are configured to apply to the same employee but have conflicting rules or calculations.

**Category**: Processing

**Blocking**: May prevent correct payroll calculation

**Typical Severity**: Medium

**Affected Employees**: 1-50 (varies)

**Root Causes**:
- Wage type overrides not properly configured
- Multiple bonus types both applying when only one should
- Regular and supplemental pay both calculating overtime
- Shift differential and premium pay conflict
- Rule priority not set correctly
- Wage type not removed when benefit changed

**Resolution Steps**:
1. Identify which wage types are in conflict
2. Review wage type configuration in PT40
3. Check assignment to employee in PA40
4. Determine which wage type should apply (per business rules)
5. Either remove conflicting wage type or adjust rules in PT50
6. Set rule priority if both should apply
7. Run trial payroll (PT04) to verify correct calculation
8. Document resolution and mark alert resolved

**SAP Transactions**: PT40, PA40, PT50, PT04

**SLA**: P2-P3 (4-hour to 1-day)

**Prevention**:
- Wage type rule priority review
- Employee wage type assignment audit
- Trial payroll before final run

---

### 13. Retroactive Change

**Description**: A payroll change must be applied retroactively (pay adjustment, job change, salary change, or deduction change effective past date).

**Category**: Processing

**Blocking**: May require payroll correction

**Typical Severity**: Medium

**Affected Employees**: 1-100+ (may be batch)

**Root Causes**:
- Employee submitted pay change request after deadline
- HR system change not reflected in payroll timely
- Pay effective date was backdated
- Job change not entered immediately
- Retroactive deduction from employee request
- Payroll correction needed from prior cycle

**Resolution Steps**:
1. Identify change type (salary, job, deduction, etc.)
2. Determine effective date of change
3. Assess impact on past payroll periods
4. Use RPMUD (Retroactive Change Tool) to manage change
5. Calculate arrearages or adjustments needed
6. Run trial calculation to verify impact
7. Process lump-sum adjustment or next-payroll correction
8. Obtain employee confirmation of adjustment
9. Document change authority and mark alert resolved

**SAP Transactions**: PA40, RPMUD, PT04, PT09

**SLA**: P2-P3 (depends on deadline urgency)

**Prevention**:
- Retroactive change deadline enforcement
- HR-Payroll change notification process
- Retroactive change log review

---

### 14. Overtime Threshold Exceeded

**Description**: Employee hours worked exceed overtime threshold (weekly, daily, or consecutive day limits per jurisdiction) but overtime calculation may not be correct.

**Category**: Processing

**Blocking**: No (typically informational)

**Typical Severity**: Low to Medium

**Affected Employees**: 1-50 (varies by period)

**Root Causes**:
- Employee worked more hours than anticipated
- Overtime rules not properly configured for jurisdiction
- Shift hours not properly tracked in time system
- Holiday or special hours not counted toward threshold
- Overtime multiplier incorrectly applied
- Multiple job codes affecting hours

**Resolution Steps**:
1. Verify actual hours worked from time system (PE02)
2. Confirm overtime threshold for jurisdiction (7 days, 40 hrs, etc.)
3. Check overtime calculation in wage type (PT40)
4. Run payroll simulation (PT04) to verify overtime pay
5. Confirm overtime calculation is correct and paid
6. Document business justification for overtime
7. Validate no wage law violation (rest breaks, etc.)
8. Mark alert resolved

**SAP Transactions**: PE02, PE03, PT40, PT04, PT61

**SLA**: P3-P4 (next business day)

**Prevention**:
- Overtime forecasting before hours approval
- Automated overtime calculation validation
- Regular overtime threshold review

---

### 15. Payroll Lock Condition

**Description**: Payroll run is locked and cannot be executed (all employees, specific cost center, or payroll area).

**Category**: Processing

**Blocking**: Yes (prevents payroll run)

**Typical Severity**: Critical

**Affected Employees**: Multiple (group lock)

**Root Causes**:
- Prior payroll period not released from lock
- System lock for reconciliation or audit
- Manual lock applied for approval process
- Partial payroll lock from failed prior run
- Payroll master record locked
- Period closing process incomplete

**Resolution Steps**:
1. Access PT60 to check payroll lock status
2. Identify which payroll period/cluster is locked
3. Determine lock reason (reconciliation, approval, error, etc.)
4. Resolve underlying issue if lock is safety mechanism
5. Release lock in PT60 with appropriate authorization
6. Verify all payroll data is ready for run
7. Document lock release and mark alert resolved

**SAP Transactions**: PT60, PT09, PT04

**SLA**: P1 (15-minute response)

**Prevention**:
- Lock release checklist before payroll
- Automated lock removal on sign-off
- Lock status monitoring dashboard

---

### 16. System Validation Error

**Description**: Payroll run encounters system validation error that prevents completion (data format error, missing required field, system timeout, or logic error).

**Category**: Processing

**Blocking**: Yes (prevents payroll run)

**Typical Severity**: High to Critical

**Affected Employees**: Potentially many (system-wide issue)

**Root Causes**:
- Data format issue (non-numeric in numeric field, etc.)
- Required field missing for one or more employees
- System resource timeout on large payroll run
- Wage type rule contains logic error
- Master data configuration issue
- System compatibility or version issue

**Resolution Steps**:
1. Review error message from payroll run (PT09)
2. Identify affected employees or data elements
3. Locate validation rule causing error (PT40, PT50)
4. Determine if data issue or system issue
5. If data: correct affected employee records
6. If system: review system log and configuration
7. Run trial payroll (PT04) to test resolution
8. Execute final payroll run
9. Document error and resolution, mark alert resolved

**SAP Transactions**: PT09, PT04, PT40, PT50, ST22 (system logs)

**SLA**: P1 (1-hour resolution)

**Prevention**:
- Data validation audit before payroll run
- System testing for configuration changes
- Payroll run monitoring and error handling

---

### 17. Batch Processing Failure

**Description**: Batch payroll run fails or completes with errors (partial success, some employees processed, others not).

**Category**: Processing

**Blocking**: Yes (payroll incomplete)

**Typical Severity**: Critical

**Affected Employees**: Some or all

**Root Causes**:
- System resource exhaustion during large run
- Memory timeout for complex calculations
- Wage type rule causing failure for subset of employees
- Master data issue for specific employee(s)
- Job queue hung or terminated
- File system issue preventing output

**Resolution Steps**:
1. Review batch job log for errors
2. Identify which employees/clusters failed
3. Determine failure reason (timeout, data, system)
4. For timeout: reduce batch size or increase resources
5. For data issues: correct employee records
6. Restart failed batch with corrected parameters
7. Verify all employees processed successfully
8. Document failure and resolution, mark alert resolved

**SAP Transactions**: PT09, SM37 (job log), PT04

**SLA**: P1 (1-hour resolution)

**Prevention**:
- Batch size optimization for system resources
- Pre-payroll validation run
- Job queue monitoring

---

## FINANCIAL ALERTS

### 18. Negative Net Pay

**Description**: Employee's net pay (gross minus deductions) calculates as negative amount, meaning deductions exceed earnings.

**Category**: Financial

**Blocking**: Yes (cannot legally pay negative)

**Typical Severity**: High

**Affected Employees**: 1-10 (varies)

**Root Causes**:
- High wage garnishment combined with low pay
- Debt repayment deduction exceeds earnings
- Benefit deduction calculation error
- Tax withholding miscalculation
- Multiple deductions not balanced with gross pay
- Employee has unpaid leave affecting gross

**Resolution Steps**:
1. Access payroll result in PT61 to review calculation
2. Verify gross pay amount is accurate
3. List all deductions affecting net pay
4. Identify which deduction(s) are excessive
5. Review garnishment vs. supporting wage
6. Reduce or defer lowest-priority deduction if possible
7. Contact employee/HR for guidance on resolution
8. Adjust deductions and recalculate
9. Document decision and mark alert resolved

**SAP Transactions**: PT61, PE04 (garnishment), PA40, PT04

**SLA**: P1 (1-hour resolution)

**Prevention**:
- Negative net pay validation before payroll
- Deduction prioritization rules
- Garnishment supporting wage limits

---

### 19. Cost Center Misallocation

**Description**: Payroll GL posting is charging salary to incorrect cost center or allocation is split incorrectly.

**Category**: Financial

**Blocking**: May affect GL reconciliation

**Typical Severity**: Medium

**Affected Employees**: 1-50+ (varies)

**Root Causes**:
- Employee cost center changed but not updated in payroll
- Cost center allocation percentage incorrect
- GL posting configuration maps wrong cost center
- System default overriding employee assignment
- Multi-cost-center split not properly configured

**Resolution Steps**:
1. Verify correct cost center assignment in PA30
2. Confirm allocation percentage (100% vs. split)
3. Access GL posting inquiry (FAGLL03) to view actual posting
4. Review GL posting configuration in payroll system
5. Correct employee cost center or allocation
6. Recalculate payroll with correct cost center
7. Verify GL posting corrects to right cost center
8. Reconcile GL accounts if prior posting incorrect
9. Document correction and mark alert resolved

**SAP Transactions**: PA30, FAGLL03, FB02, FB03

**SLA**: P2-P3 (4-hour to 1-day)

**Prevention**:
- Cost center assignment validation
- GL posting audit by cost center
- Cost center change notification process

---

### 20. GL Posting Error

**Description**: Payroll GL posting is missing, incorrect amount, or posted to wrong GL account.

**Category**: Financial

**Blocking**: Prevents GL reconciliation

**Typical Severity**: Medium to High

**Affected Employees**: May be multiple

**Root Causes**:
- GL posting configuration error
- Wage type not mapped to correct GL account
- Posting logic error for deduction or tax
- Manual GL entry missing from payroll
- System posting timeout or failure
- Payroll account assignment incorrect

**Resolution Steps**:
1. Review expected GL posting from payroll run
2. Query GL to verify actual posting (FB03, FAGLL03)
3. Compare expected vs. actual amount and account
4. Identify discrepancy (missing, wrong amount, wrong account)
5. Review GL posting configuration for wage type
6. Correct configuration or repost if needed
7. GL adjustment if prior posting is wrong
8. Verify GL reconciliation is now correct
9. Document posting correction, mark alert resolved

**SAP Transactions**: PT61, FB02, FB03, FAGLL03, OKB9 (GL config)

**SLA**: P2 (4-hour resolution)

**Prevention**:
- GL posting validation before payroll finalization
- Payroll-GL reconciliation audit
- GL posting configuration review

---

### 21. Payroll Accrual Variance

**Description**: Accrued payroll liability does not match payroll run amount (accrual imbalance or unreconciled difference).

**Category**: Financial

**Blocking**: May prevent period close

**Typical Severity**: Medium

**Affected Employees**: All (system-wide)

**Root Causes**:
- Accrual not created or deleted
- Manual payroll adjustment not reflected in accrual
- Prior payroll reversal not reversed in accrual
- System accrual calculation error
- Off-cycle payroll not accrued

**Resolution Steps**:
1. Run payroll-to-GL reconciliation report
2. Compare accrual liability to payroll expense
3. Identify discrepancy (amount difference)
4. Trace to specific payroll run or adjustment
5. Either adjust accrual or reverse incorrect posting
6. Recalculate accrual if system error
7. Verify reconciliation is balanced
8. Document variance and adjustment, mark alert resolved

**SAP Transactions**: F.27 (accrual), PT61, FB02, FB03

**SLA**: P2-P3 (1-day resolution)

**Prevention**:
- Weekly accrual reconciliation
- Automated payroll-accrual validation
- Period close checklist

---

### 22. Budget Variance Alert

**Description**: Payroll expense exceeds budget or budget projection (actual vs. budget variance).

**Category**: Financial

**Blocking**: May prevent budget approval

**Typical Severity**: Low to Medium

**Affected Employees**: All (group alert)

**Root Causes**:
- Unexpectedly high overtime
- Bonus or commission payment not budgeted
- Headcount increase not reflected in budget
- Salary increase not reflected in budget
- System missing budgeted amount

**Resolution Steps**:
1. Identify which payroll cost exceeded budget
2. Calculate variance amount and percentage
3. Determine root cause (overtime, bonus, headcount, etc.)
4. Review business justification
5. Update budget if permanent change, or
6. Document variance as temporary if one-time event
7. Inform finance team of variance
8. Document variance analysis, mark alert resolved

**SAP Transactions**: FB03, OKP1 (budget), Custom budget reports

**SLA**: P4 (next business day)

**Prevention**:
- Weekly payroll run vs. budget monitoring
- Budget exception thresholds
- Monthly budget variance analysis

---

## ADDITIONAL ALERTS (from Phase 1 expansion)

### 23. Benefit Calculation Error

**Description**: Benefit deduction or contribution calculates incorrectly (health insurance, 401k, FSA, etc.).

**Category**: Data Quality/Financial

**Blocking**: May affect employee satisfaction and compliance

**Typical Severity**: Medium

**Affected Employees**: 1-100+

**Root Causes**:
- Benefit rate not updated for year
- Employee benefit election not reflected in payroll
- Tier calculation incorrect for dependent coverage
- Payroll frequency change not reflected in benefit calc
- System configuration error

**Resolution Steps**:
1. Verify benefit election in HR system
2. Check benefit rate and calculation in PE06
3. Review employee tier (employee, employee+spouse, family, etc.)
4. Verify payroll frequency factor applied correctly
5. Recalculate benefit deduction
6. Run trial payroll to verify correct amount
7. Document correction and mark alert resolved

**SAP Transactions**: PE06, PA40, PT40, PT61

**SLA**: P2-P3

**Prevention**: Annual benefit rate review before open enrollment

---

### 24. Shift Differential Missing

**Description**: Employee eligible for shift differential pay (night shift, weekend premium) but differential not applied.

**Category**: Processing/Compliance

**Blocking**: May violate wage terms

**Typical Severity**: Medium

**Affected Employees**: 1-50

**Root Causes**:
- Shift assignment not updated in system
- Shift differential wage type not configured
- Employee not assigned shift differential rule
- Work schedule not properly reflected

**Resolution Steps**:
1. Verify employee work shift in PA30
2. Confirm shift differential eligibility
3. Review wage type configuration for shift differential
4. Verify assignment to employee in PT60
5. Run trial payroll to verify differential applied
6. Document and mark alert resolved

**SAP Transactions**: PA30, PT40, PT60, PT61

**SLA**: P2-P3

---

### 25. Equipment Allowance Configuration

**Description**: Employee entitled to equipment allowance (CA only) but not properly configured or paid.

**Category**: Compliance

**Blocking**: May violate wage law

**Typical Severity**: Medium

**Affected Employees**: 1-50 (CA only)

**Root Causes**:
- Equipment allowance configuration missing
- Employee not assigned allowance
- Allowance rate incorrect
- Job code does not trigger allowance

**Resolution Steps**:
1. Verify job requires equipment allowance
2. Check PT40/PT50 for allowance wage type
3. Verify employee assignment
4. Calculate correct monthly/weekly allowance
5. Update configuration and employee assignment
6. Run trial payroll
7. Document and mark alert resolved

**SAP Transactions**: PA40, PT40, PT50, PT61

**SLA**: P2-P3

---

## Alert Severity Legend

**High Severity**: Blocks payroll, violates law, affects payment, immediate resolution required

**Medium Severity**: Impacts payroll quality, affects multiple employees or significant amount, next-shift resolution

**Low Severity**: Informational, single employee, routine resolution, can defer if needed

---

**Last Updated**: 2026-02-07
**Alert Catalog Version**: 1.0.0
**Total Alert Types**: 25+
