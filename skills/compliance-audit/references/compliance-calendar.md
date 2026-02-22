# US Payroll Compliance Calendar 2025

## Overview

This calendar outlines all federal and major state payroll filing obligations for 2025. Missing deadlines can result in significant penalties and IRS/state enforcement actions. Each filing deadline includes required form, submission method, penalties for late filing, and state-specific variations.

---

## Monthly Obligations

### Federal Payroll Tax Deposits

**Obligation**: Deposit federal income tax, Social Security tax, and Medicare tax withheld from employees.

**Frequency**: Monthly or semi-weekly (depends on deposit schedule rules)

**Filing Details**:
- **Form**: Electronic Federal Tax Payment System (EFTPS) or ACH payment
- **Amount**: Total of federal income tax, SS tax (6.2%), Medicare (1.45%)
- **Deadline**:
  - Semi-weekly schedule: Deposits due within 3 calendar days of pay period end
  - Monthly schedule: Deposits due by 15th of following month
- **Failure to Deposit Penalty**:
  - 2% for 1-5 days late
  - 5% for 6-15 days late
  - 10% for >15 days late
  - 15% if still unpaid after payroll tax assessment

**Audit Notes**:
- Verify deposit dates match payroll processing dates
- Confirm deposit amounts match payroll register totals
- Check for missing months or late deposits
- Test wage base limits for Social Security tax ($176,100 2025 limit)

**Transaction in SAP**: PUMB (Display payroll balances/YTD) to verify amounts

---

### State Income Tax Withholding Deposits

**Obligation**: Deposit state income tax withheld from employees.

**Frequency**: Monthly (most states), Quarterly (CA, NY), or Semi-weekly (some states)

**State-Specific Deadlines**:
| State | Frequency | Deadline | Penalty Rate |
|-------|-----------|----------|--------------|
| **California** | Quarterly (Q1, Q2, Q3) + Dec | Last day of month following quarter | 5% per month |
| **New York** | Monthly | 15th of following month | 5% per month |
| **Texas** | Varies by payroll frequency | 15th of following month | 5% per month |
| **Florida** | Monthly | 15th of following month | 5% per month |
| **Illinois** | Monthly | 15th of following month | 5% per month |
| **Pennsylvania** | Monthly | 15th of following month | 5% per month |
| **Ohio** | Monthly | 15th of following month | 5% per month |

**Filing Details**:
- Method: State-specific payment system (varies by state)
- Amount: Total state income tax withheld
- Support: Payroll register by employee showing state residence
- Reconciliation: Form 941 (federal) should match state withholding for same period

**Audit Notes**:
- Verify appropriate state assigned for each employee
- Check for missing or late deposits
- Confirm multistate residents have correct withholding allocation
- Test that local taxes withheld (if applicable)

---

### State Unemployment Insurance (SUI) Contributions

**Obligation**: Employer-paid state unemployment insurance contributions.

**Frequency**: Quarterly (most states) or Monthly (some states)

**Payment Deadlines**:
| State | Deadline | Rate (2025) | Wage Base | Notes |
|-------|----------|-----------|-----------|-------|
| **California** | 30 days after quarter end | SDI only (no employer UI) | $1,521.25 max | Employer SDI 1.0%-1.5% |
| **New York** | 10 days after quarter end | 3.0%-6.2% | $11,800 | Average rate varies |
| **Texas** | 31st of month following quarter | 0.42%-0.82% | $9,000 | New employer 0.42% |
| **Florida** | 31st of month following quarter | 0.27%-6.33% | $10,500 | Experience rating |
| **Illinois** | 10 days after quarter end | 0.38%-7.5% | $12,240 | Varies by employer |
| **Pennsylvania** | 15th of month following quarter | 3.7%-9.2% | $10,500 | May include employee portion |
| **Ohio** | 31st of month following quarter | 0.24%-10.0% | $9,000 | Experience rating |

**Filing Details**:
- Form: Quarterly SUI report (varies by state)
- Amount: Taxable wages × employer rate (verify wage base limits applied)
- Support: Payroll register with gross wages and SUI contributions by employee
- Due: 31 days after quarter end (most states)

**Audit Notes**:
- Verify state SUI wage base limit applied correctly (not federal $7,000)
- Check that SUI rate is current (rates adjusted annually)
- Confirm all employees' wages below wage base included in calculation
- Verify timely filing and payment; monitor for late payment penalties

**Quarterly Quarters**:
- Q1: Jan 1 - Mar 31 (Due: Apr 30)
- Q2: Apr 1 - Jun 30 (Due: Jul 31)
- Q3: Jul 1 - Sep 30 (Due: Oct 31)
- Q4: Oct 1 - Dec 31 (Due: Jan 31)

---

### Child Support and Garnishment Payments

**Obligation**: Remit withheld child support and wage garnishment orders.

**Frequency**: Per court order (monthly, twice-monthly, or per pay period)

**Filing Details**:
- **Form**: None; direct payment to court or designated agent
- **Amount**: Withheld per court order
- **Deadline**: Per garnishment order (typically within 5-10 business days of pay date)
- **Payment Method**: Wire, check, or state-specific payment system

**Priority Ordering** (CCPA - Consumer Credit Protection Act):
1. Federal taxes
2. State taxes
3. Child support
4. Other creditor orders
5. Voluntary wage assignments

**Audit Notes**:
- Verify garnishment amounts do not exceed 25% of disposable income
- Check priority ordering if multiple garnishments on one employee
- Confirm all garnishment orders on file and current
- Verify timely remittance to court/agent
- Ensure confidentiality of garnishment information

**Compliance**: Maintain garnishment register showing:
- Employee name and ID
- Order number and type
- Withholding per pay period
- Cumulative year-to-date
- Remittance dates and amounts

---

## Quarterly Obligations

### Form 941 - Employer's Quarterly Federal Tax Return

**Obligation**: Report federal payroll taxes for the quarter.

**Frequency**: Quarterly (Jan-Mar, Apr-Jun, Jul-Sep, Oct-Dec)

**Due Dates**:
| Quarter | Period | Due Date (2025) | Extension | Penalty |
|---------|--------|-----------------|-----------|---------|
| Q1 | Jan 1 - Mar 31 | April 30 | N/A | 5% of unpaid tax + interest |
| Q2 | Apr 1 - Jun 30 | July 31 | N/A | 5% of unpaid tax + interest |
| Q3 | Jul 1 - Sep 30 | October 31 | N/A | 5% of unpaid tax + interest |
| Q4 | Oct 1 - Dec 31 | January 31, 2026 | N/A | 5% of unpaid tax + interest |

**Filing Requirements**:
- **Form**: Form 941 (Employer's Quarterly Federal Tax Return)
- **Electronic Filing**: Required for all employers; file via EFILE or IRS e-services
- **Paper Filing**: Only if IRS granted exemption
- **E-Signature**: Authorized officer must sign electronically

**Line Items to Verify**:
1. Wage and salary information
   - Total wages paid (from payroll register)
   - Breakdown by state (multistate operations)
   - Adjustment items (retroactive changes, credits)

2. Tax withheld and payments made
   - Federal income tax withheld (from payroll)
   - SS tax withheld (6.2% up to $176,100 limit per employee)
   - Medicare tax withheld (1.45% with Additional Medicare 0.9% if applicable)
   - Employer SS and Medicare taxes (6.2% + 1.45%)

3. Credits and adjustments
   - Work Opportunity Tax Credit (WOTC) if applicable
   - Qualified Sick and Family Leave Credits (if applicable post-CARES Act)
   - Employee Retention Credit (ERC) if applicable
   - Prior period adjustments

4. Compliance certifications
   - Third-party preparer information (if applicable)
   - Authorized representative information
   - Electronic filing consent

**Prior Period Reconciliation** (to payroll register):
- Sum of monthly/semi-weekly deposits = Taxes reported on Form 941
- Form 941 taxes should match payroll register total wages and withholdings
- Investigate any discrepancies; may indicate calculation errors

**Audit Notes**:
- Verify quarterly reconciliation completed before filing
- Test wage base limits for SS tax (should stop at $176,100)
- Confirm deposits match Form 941 line items
- Check for timely filing; late penalties accrue

**SAP Transaction**: PUMB, PZRA (Payroll results) for quarterly totals

---

### Form 941-X - Corrected Quarterly Federal Tax Return

**Obligation**: File corrected Form 941 if errors discovered on previously filed Form 941.

**Frequency**: As needed (if corrections required)

**Due Date**: Within 3-year statute of limitations (typically within 3 years of original Form 941 due date)

**Correction Scenarios**:
- **Underreported wages**: Wages too low on original return
- **Underreported withholding**: Taxes withheld incorrectly calculated
- **Overreported credits**: Credits claimed but not qualified
- **Missing documents**: W-4 forms incomplete or missing

**Filing Details**:
- **Form**: Form 941-X (Corrected Quarterly Federal Tax Return)
- **Method**: Paper filing (no electronic EFILE for 941-X currently)
- **Requirement**: Form 941-X-D (employer detail) must accompany each 941-X

**Audit Notes**:
- Review if any Form 941s were corrected in the period
- Verify correction was timely and accurate
- Document business reason for correction
- Confirm additional tax or refund was resolved

---

### State Quarterly Tax Filings

**Obligation**: File quarterly payroll tax reports with state authorities.

**Frequency**: Quarterly

**State-Specific Filings**:
| State | Form | Deadline | Contains |
|-------|------|----------|----------|
| **California** | DE 9 | 30 days after quarter | Wages, SUI, SDI, withholding |
| **New York** | Form ST-3 | 10 days after quarter | Wages, withholding, UI contributions |
| **Texas** | QCEW Form | 31st of following month | Quarterly Census of Employment & Wages |
| **Florida** | Form DOR 1 | 31st of following month | Wages, UI contributions |
| **Illinois** | Form IL-941 | 30 days after quarter | Wages, withholding, UI contributions |
| **Pennsylvania** | Form UC-2 | 15 days after quarter | SUI contributions, wages |
| **Ohio** | Form OhioCheckbook | 31st of following month | SUI contributions, wages |

**Filing Details**:
- **Method**: Online filing required (most states); some allow paper filing
- **Amount**: Quarterly SUI contributions + state withholding (if applicable)
- **Reconciliation**: Match to payroll register for wages by employee
- **Due**: Within 10-31 days of quarter end (varies by state)

**Audit Notes**:
- Verify filing deadline per state (varies significantly)
- Confirm quarterly filings completed and timely
- Test wage totals match payroll register
- Reconcile to annual W-2s at year-end

---

## Annual Obligations

### Form W-2 - Wage and Tax Statement

**Obligation**: Furnish to employees summary of wages and tax withholds.

**Due Date**: January 31, 2025 (to employees)

**Filing with SSA**: February 28, 2025 (paper); April 2, 2025 (electronic)

**Filing Requirements**:
- **Form**: Form W-2 (one per employee)
- **Distribution**: Copy to employee, SSA, state revenue department, IRS
- **Electronic Filing**: Form W-3 transmittal required for SSA/IRS filing
- **Penalties**: $50-$100 per return for late/incorrect filings

**Data Elements to Verify**:
1. **Boxes 1-6**: Wages and tax information
   - Box 1: Federal taxable wages (gross less pre-tax deductions)
   - Box 2: Federal income tax withheld
   - Boxes 3-4: SS wages and tax
   - Boxes 5-6: Medicare wages and tax

2. **Boxes 7-20**: Additional tax information
   - Box 7: SS tips (if applicable)
   - Box 11: Nonqualified plans (NQD)
   - Box 12: Deferred compensation/benefits
   - Box 19: Employee address

3. **State and Local Taxes**:
   - Boxes 18-20: State/local income tax withheld
   - Boxes 15-16: Employer state/local ID and state

**Pre-W-2 Reconciliation**:
- Sum of Box 1 (federal wages) across all W-2s = Total gross pay per payroll register (less pre-tax deductions)
- Sum of Box 2 (federal tax) across all W-2s = Total federal withholding
- Sum of Box 3 (SS wages) across all W-2s = Total SS wages (capped at $176,100 per employee)
- Sum of Box 5 (Medicare wages) = Total Medicare wages (no cap)

**Audit Notes**:
- Verify all employees with earnings receive W-2
- Confirm W-2 data matches payroll register
- Check for terminated employees' final W-2s
- Verify state/local tax amounts match quarterly filings
- Test wage base limits for SS (no employee should exceed $176,100)

**SAP Transaction**: PBIL (Wage Types for Payroll Period)

---

### Form W-3 - Transmittal of Wage and Tax Statements

**Obligation**: Transmit W-2 information to SSA.

**Due Date**:
- Paper W-3 filing: February 28, 2025
- Electronic filing (via SSA BDES): April 2, 2025
- Electronic filing (via TDS): March 31, 2025

**Filing Requirements**:
- **Form**: Form W-3 (one transmittal with all W-2s)
- **Method**: Paper filing requires matching W-2 forms; electronic BDES/TDS preferred
- **Data**: Control totals matching sum of all W-2s

**Control Totals to Verify**:
- Box a: Total wages (sum of W-2 Box 1)
- Box b: Total federal income tax (sum of W-2 Box 2)
- Box c: Total SS wages (sum of W-2 Box 3, capped at $176,100 each)
- Box d: Total SS tax (sum of W-2 Box 4)
- Box e: Total Medicare wages (sum of W-2 Box 5)
- Box f: Total Medicare tax (sum of W-2 Box 6)

**Common Filing Issues**:
- **Mismatch to payroll**: W-3 control totals don't match sum of W-2s
  - Cause: Manual adjustments, correction entries, timing issues
  - Fix: Reconcile payroll register to W-2 totals; investigate discrepancies

- **Late filing**: W-3 submitted after deadline
  - Penalty: $50-$100 per month late (up to $250 per return)
  - Prevention: Plan for 2-week processing time before deadline

**Audit Notes**:
- Verify W-3 filed on time with SSA
- Confirm control totals match sum of W-2s
- Check that all required W-2s included with W-3 transmittal

---

### Form 940 - Employer's Annual Federal Unemployment Tax Return

**Obligation**: Report federal unemployment tax (FUTA) owed.

**Due Date**: January 31, 2025

**Filing Requirements**:
- **Form**: Form 940 (or 940-EZ for small employers)
- **Method**: Electronic filing via IRS EFILE
- **Amendment**: Form 940-X if corrections needed within 3 years

**FUTA Calculation**:
- **Gross Tax**: Wages up to $7,000 per employee × 0.6% federal rate
- **Credit**: State SUI paid (up to 5.4% credit), resulting in net 0.6%
- **Formula**: (Taxable Wages × 6.0%) - (State SUI Credit up to 5.4%) = Federal FUTA Tax

**Key Verification Points**:
1. **Taxable wages calculation**
   - Sum of first $7,000 wages per employee
   - Not to exceed $7,000 per employee (different from SS $176,100)
   - Match to payroll register

2. **State SUI credit**
   - Employer paid state SUI for the year
   - Not subject to SUI rate reduction (no credit reduction)
   - Match to quarterly state SUI filings

3. **Timing**:
   - FUTA is annual accrual (unlike payroll tax deposits)
   - No quarterly payments required (unlike Form 941)
   - If FUTA liability exceeds $500 in quarter, advance payment encouraged

**Audit Notes**:
- Verify wage base of $7,000 applied (not $176,100)
- Confirm state SUI credit calculation
- Check for timely filing; late penalty 0.5% per month
- Reconcile Form 940 to payroll register and state SUI filings

**SAP Transaction**: PUMB (Display payroll balances for FUTA calculation)

---

### Form 944 - Employer's Annual Federal Tax Return (Alternative Quarterly)

**Obligation**: File annual Form 944 instead of quarterly Form 941 if small employer.

**Eligibility**: IRS-approved small employers only (typically <$50,000 annual payroll)

**Due Date**: January 31, 2025 (for 2024 payroll)

**Filing Requirements**:
- **Form**: Form 944 (annual alternative to Form 941)
- **Requirement**: Must receive IRS approval to file Form 944
- **Method**: Electronic filing via EFILE
- **Note**: Applies to both federal and state reporting (CA, IL, NY do not allow 944)

**Audit Notes**:
- Verify employer is approved to file Form 944
- If transitioning from 941 to 944, verify final 941 filed for partial quarter
- Reconcile annual Form 944 to monthly payroll register
- Ensure consistent quarterly withholding throughout year

---

### ACA Forms 1094-C and 1095-C - Employer Health Insurance Reporting

**Obligation**: Report employer health insurance coverage information (ACA).

**Due Date**: February 28, 2025 (to employees); February 28/April 2 (to IRS)

**Filing Requirements**:
- **Form 1094-C**: Transmittal form (one per employer)
- **Form 1095-C**: Employee health insurance coverage (one per employee)
- **Electronic Filing**: Required for employers with 250+ tax filers

**Data Elements**:
1. **1094-C (Transmittal)**:
   - Employer identification information
   - Total number of 1095-C forms
   - Control totals (total employees, individuals covered)

2. **1095-C (Employee Detail)**:
   - Employee information (name, SSN, address)
   - Employer coverage information
   - Month-by-month coverage indicator (12 months to report)
   - Safe harbor certifications (employee offer, affordability, design of plan)

**Compliance Verification**:
1. **Coverage requirement**: Full-time employees (30+ hrs/week) offered health insurance
   - Count full-time headcount each month
   - Identify part-time employees not requiring coverage
   - Track qualifying life events affecting coverage

2. **Affordability testing**: Employee cost-share ≤9.12% of household income
   - 1095-C line 12 code must indicate safe harbor (A, B, C, or D)
   - Safe Harbor A: Employee self-only coverage <9.12% of federal poverty line
   - Other safe harbors based on W-2 wages, household income, etc.

3. **Design requirement**: Plan must provide minimum value (60% actuarial value)
   - Document plan's minimum value certification
   - Maintain actuarial value testing from health plan

**Audit Notes**:
- Verify 1095-C issued to all full-time employees
- Confirm affordability testing performed correctly
- Check coverage month indicators (typically 12 for full-year employees)
- Reconcile 1095-C headcount to payroll records
- Maintain safe harbor certification supporting affordability

**Penalties**: $50-$300 per form for late/incorrect filing (2025 penalty $50-$100 typical)

---

### ACA Form 1098-T - Qualified Education Credit (if applicable)

**Obligation**: Report qualified education expenses for employees using education benefits.

**Due Date**: March 31, 2025

**Applicability**: Only if employer offers Qualified Tuition Reduction (QTR) or similar education benefits.

**Filing Requirements**:
- **Form**: Form 1098-T (Qualified Tuition Statement)
- **Method**: Paper or electronic filing with IRS
- **Applicability**: Educational institutions and employers offering qualified education benefits

**Audit Notes**:
- Determine if employer offers qualified education benefits
- If yes, reconcile education benefit deductions to 1098-T filings
- Verify employees claim benefits on personal tax returns

---

## State-Specific Year-End Filings

### California Year-End Obligations

**Form DE 9C** (Annual SUTA Payroll Report)
- **Due**: January 31, 2025
- **Contents**: Annual wages, employee counts, SUI contributions
- **Reconciliation**: Match annual W-2 wages to payroll register

**SDI (State Disability Insurance)**
- California requires SDI withholding (1.0%)
- No employer matching; employee-only tax
- Verify SDI withholding from payroll; reconcile to DE 9C

---

### New York Year-End Obligations

**Form NYS-45** (Annual Employer PAYE Tax Reconciliation)
- **Due**: February 28, 2025
- **Contents**: Annual payroll, tax withheld, deposits made
- **Reconciliation**: Match to Form 941 federal filings

**NYC Wage Tax** (if applicable)
- NYC requires 3.876% employee withholding (if employee is NYC resident)
- Verify NYC residents identified and withheld appropriately
- Reconcile to Annual Notice of Wage Credits

---

### Texas, Florida, Illinois, Pennsylvania, Ohio Year-End Obligations

Most states with income tax file annual reconciliation with quarterly filing. Reconciliation occurs quarterly, not at year-end.

**No State Income Tax**:
- **Texas**: No state income tax; only SUI and FUTA
- **Florida**: No state income tax; only SUI and FUTA
- **Nevada, Tennessee, Washington**: No state income tax

**Year-End Reconciliation**:
- **Illinois**: Form IL-1065 (Annual Reconciliation) if differences between quarterly filings
- **Pennsylvania**: Form UC-2 reconciliation through quarterly filings
- **Ohio**: OBES (Ohio Business and Employment Services) annual filing

---

## Key Deadlines Summary - 2025

| Obligation | Deadline | Form/Method | Penalty |
|-----------|----------|-----------|---------|
| Monthly Fed Tax Deposits | Monthly (15th or 3 days) | EFTPS/ACH | 2-15% late fee |
| Monthly State Tax Deposits | Monthly (15th) | State portal | 5% per month |
| Q1 Form 941 | April 30 | E-file | 5% of tax unpaid |
| Q2 Form 941 | July 31 | E-file | 5% of tax unpaid |
| Q3 Form 941 | October 31 | E-file | 5% of tax unpaid |
| Q4 Form 941 | January 31, 2026 | E-file | 5% of tax unpaid |
| Q1-Q4 State SUI | 30 days after quarter | State portal | 5% per month |
| W-2 to Employees | January 31 | Paper/electronic | None (but IRS notification) |
| W-3 to SSA | February 28 (paper) / April 2 (e-file) | Paper/IRS e-services | $50-$100 per form |
| Form 940 FUTA | January 31 | E-file | 0.5% per month |
| 1094-C/1095-C | February 28 (employees) / February 28-April 2 (IRS) | Paper/IRS EFILE | $50-$300 per form |
| 1098-T (if applicable) | March 31 | IRS | Varies |

---

## Notes and Considerations

### Multi-State Operations
- Verify each employee's work location and residence state
- Apply correct state tax withholding (where work performed)
- File in all states where employees perform work
- Monitor wage base limits for each state (vary significantly)

### Payroll Processors
- If using third-party payroll processor, verify responsibility for filings
- Processor typically handles deposits and quarterly Form 941
- Employer responsible for final review and sign-off
- Annual filings (W-2, 940, ACA) typically employer responsibility

### System Configuration
- Maintain SAP payroll configuration with current-year tax tables
- Update annually: SS wage base ($176,100), FUTA base ($7,000), Medicare threshold ($200,000)
- Verify state SUI rates and bases updated (many states change rates annually)
- Test payroll calculations against official tax tables

### Record Retention
- Maintain payroll records for minimum 7 years
- Maintain tax documents (W-2, 941, 940) for minimum 7 years
- Maintain bank statements and deposit records for minimum 3 years
- Maintain garnishment orders for duration of garnishment + 3 years

---

**Document Version**: 1.0 | **Last Updated**: February 2025 | **Classification**: Internal Use Only
