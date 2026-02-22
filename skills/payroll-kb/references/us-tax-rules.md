# US Payroll Tax Rules & Compliance Reference

This guide covers federal, state, and local tax withholding, FLSA overtime rules, and special situations. **All information current as of 2025; verify before each payroll cycle. Consult your tax advisor and legal team for your specific business situation.**

---

## Federal Income Tax Withholding

**Regulatory Authority**: Internal Revenue Code Section 3401; IRS Pub 15 (Circular E)

### 2025 Tax Tables & Rates

**Standard Deduction** (affects W-4 calculations):
- Single: $14,600
- Married Filing Jointly: $29,200
- Head of Household: $21,900

### W-4 Form Options

**Current Form (2024 revision; still in use in 2025)**:
- No "allowances" (old system removed)
- Instead: Step 2C - Claim dependents (each = $2,000 on dependent credit)
- Step 3 - Other income (from second job, retirement, etc.)
- Step 4 - Deductions (itemized or standard; only if not claimed on joint return)
- Step 4b - Extra withholding (dollar amount per pay period)

**How SAP implements W-4**:
- Store in **IT0207** (Federal Tax infotype):
  - **W-4 Revision Date**: date form was signed (required for IRS compliance)
  - **Withholding Status**: Single, Married, Head of Household
  - **Dependent Credits**: number of dependents (affects tax calculation)
  - **Extra Withholding Amount**: additional $ to withhold per pay check
  - **Number of Jobs**: affects calculation if employee has multiple jobs

**Key dates**:
- New W-4 effective: typically the next payroll period after receipt
- If no W-4 on file: SAP defaults to Single, 0 dependents (maximum withholding)
- If employee claims exempt: special flag in IT0207; requires written certification

### 2025 Withholding Tables

**Biweekly (most common)**:
- Single: See IRS Pub 15 Table 4
  - Example: $1,500 gross → $160-$180 federal withholding (depends on dependents, other income)
- Married: See IRS Pub 15 Table 5
  - Lower withholding than Single for same gross (married two-income adjustment available)

**Monthly**:
- Different table (roughly 4.3 weeks); typically higher withholding per week

**Seasonal/Irregular**:
- Use annualized method: annual gross ÷ 52 weeks × number of weeks worked
- Or use aggregate method: run-to-date gross vs. year-to-date threshold

**Supplemental Wages** (bonus, commission, off-cycle):
- Option 1 - Flat Rate: 22% federal withholding (6% if over $1M for year)
- Option 2 - Aggregate: Treat as if paid with regular pay, use standard withholding tables
- SAP default: flat rate; can override in wage type configuration or individual payroll activity

### Federal Tax Compliance Checkpoints

| Issue | Action | Frequency |
|---|---|---|
| W-4 on file | All employees must have executed W-4 before first pay | At hire; annually if changed |
| W-4 expiry | No formal expiry, but IRS recommends employee review every 3 years | Proactive outreach Q1 |
| Income verification | W-4 assumes employee will not have federal income tax liability at EOY | Validate at year-end; follow up if exempt claim |
| Tax payment | Deposit federal withholding to IRS (either Semi-Weekly or Monthly) | Per deposit schedule |
| Form 941 | Report quarterly federal withholding, FICA, employer FICA match | Quarterly (due 4/30, 7/31, 10/31, 1/31) |
| Form 940 | Report annual FUTA | Annual (due 1/31 following year) |

---

## FICA Taxes (Social Security & Medicare)

**Regulatory Authority**: Internal Revenue Code Section 3101 (employee portion), 3111 (employer portion)

### 2025 Rates & Limits

| Tax | Employee Rate | Employer Rate | Wage Base | Notes |
|---|---|---|---|---|
| **Social Security** | 6.2% | 6.2% | $168,600 | Stops after employee hits limit mid-year |
| **Medicare (standard)** | 1.45% | 1.45% | Unlimited | Applies to all wages |
| **Medicare (additional)** | 0.9% | — | >$200K (single), >$250K (MFJ) | Applies to wages over threshold; employer does not match |

### Social Security Wage Base Management in SAP

**Key IT infotype**: IT0207 (Federal Tax) → "Social Security Wage Limit"

**How it works**:
- SAP tracks year-to-date Social Security wages
- When cumulative wages exceed $168,600, Social Security tax withholding stops
- SAP automatically manages this; mark as "inactive" once limit reached
- At year-end, verify total employees who hit limit match headcount expectations

**Common error**: Employee changes pay frequency mid-year (e.g., hourly to salary); SAP may not recalculate correctly. Verify IT0207 has correct run-to-date balance before payroll.

### Additional Medicare Tax (0.9%)

**Threshold** (2025): $200,000 (single filer); $250,000 (MFJ); $125,000 (married filing separately)

**How to track in SAP**:
- IT0207 allows "Medicare Threshold" entry
- If employee's year-to-date wages exceed threshold, additional 0.9% withholding applies
- Apply to wages in payroll period that crosses threshold

**Important**: Additional Medicare tax is withheld from employee only (employer does NOT match). Some employers make up the employer match voluntarily; verify your policy in IT0200 or wage type configuration.

### FUTA (Federal Unemployment Tax)

**Regulatory Authority**: Internal Revenue Code Section 3301-3311

**Rate** (2025): 6.0% on first $7,000 of each employee's wages

**State Credit**: Most states allow 5.4% credit toward FUTA, reducing effective FUTA to 0.6%

**When FUTA applies**:
- Applies to wages paid to each employee up to $7,000 per calendar year
- Once employee reaches $7,000 YTD, no more FUTA for rest of year
- Unlike Social Security, no ongoing "limit tracking" needed; FUTA is simple cumulative calculation

**Employer-only tax** (no employee withholding)

**Annual reporting**: Form 940 (due 1/31 following year); include all employees and total FUTA paid

**SAP setup**: FUTA is typically calculated as a wage type (not a deduction); configure in **SM30 V_T511F** wage type maintenance.

---

## State Income Tax Withholding

**Note**: State tax rules vary widely; below is a general framework. **Verify your states' specific requirements.**

### States with No Income Tax (2025)
- Alaska, Florida, Nevada, South Dakota, Tennessee, Texas, Washington, Wyoming
- Some: New Hampshire (interest/dividend income only); Tennessee (eliminated 2021)

**Strategy for employees working in no-tax states**:
- Update IT0208 (State Tax infotype) to mark "No State Tax" or state code of residence
- Verify withholding election so no state withholding applied
- Note: If employee is resident of state with income tax but works in no-tax state, typically withhold tax of residence state

### States with Income Tax (Sample rules; not exhaustive)

**California** (highest-tax state):
- Graduated rates: 1% to 13.3%
- Uses Form CA W-4 (state-specific); SAP IT0208 maps CA W-4 data
- Supplemental income (bonus): Treated as regular income; no separate flat rate
- Special rules for non-residents (work in CA but live elsewhere)
- **Important**: California SUI/SDI applies; also Paid Family Leave (PFL) tax

**New York** (similar to federal):
- Form IT-2104 (state W-4); similar structure to federal form
- City tax (NYC, Yonkers, etc.): Additional local withholding
- No state-specific supplemental withholding rules

**Texas** (no state income tax):
- No withholding
- But: Franchise tax applies (not withheld from employees)

**Multi-state**: If employee works in multiple states or is non-resident:
- Primary work location determines state of withholding
- Secondary states typically not withheld
- Exception: Some states require resident withholding regardless of where work performed
- **Recommendation**: Document work location and state of tax residency in IT0208 for each employee

### State Unemployment Insurance (SUI/SUTA)

| State | Rate (2025 range) | Wage Base | Notes |
|---|---|---|---|
| CA | 1.5% - 6.2% | $7,000 | Rate depends on employer experience rating (new employers: 3.4%) |
| TX | 0.6% - 6.0% | $9,000 | Experience rating system |
| NY | 3.6% - 6.2% | $10,300 | Employer-only; employee surcharge possible in deficit years |
| FL | 0.6% - 5.4% | $7,000 | Experience rating |

**How it works**:
- Employer-only tax (no employee withholding, except NY surcharge)
- Paid quarterly
- Wage base limit: once employee reaches limit, no more SUI for rest of year
- SAP calculates as wage type; configured per payroll area (company code + payroll area = SUI liability)

**Form 940** (federal) cross-checks SUI; discrepancies can trigger IRS audit.

### State Disability Insurance (SDI) & Paid Family Leave (PFL)

**States with SDI** (employee-withheld):
- California: 1.0% of gross (cap: varies by year; 2025 check current amount)
- New Jersey: 0.5% of gross
- New York: 0.6% of gross
- Rhode Island: 1.3% of gross
- Puerto Rico: 0.6% of gross

**States with PFL** (Paid Family Leave; mostly employee-withheld):
- California, New Jersey, New York, Washington: Varying rates (0.5% - 1.75%)
- Federal FAMILY and Medical Leave Act (FMLA) does NOT require wage withholding; state PFL does

**In SAP**:
- Configure as deduction wage types (IT0200 or wage type in SM30)
- Mark as "tax-deductible" if applicable (usually yes for pre-tax deductions)
- Annual caps: once employee hits cap, no more deduction for rest of year

---

## FLSA (Fair Labor Standards Act) - Overtime Rules

**Regulatory Authority**: 29 U.S.C. Section 201 et seq.; DOL Wage & Hour Division

### Exempt vs. Non-Exempt Classification

**Non-Exempt** (entitled to overtime):
- Paid hourly, typically
- Owed overtime (1.5x regular rate) for hours over 40/week (federal standard)
- Some states: daily OT (CA: 8 hrs/day, 4+ hrs of OT in day), weekly threshold may differ

**Exempt** (no overtime):
- Salary ≥ $58,656/year (2025 threshold; increases each Jan 1)
- Job duties: executive, administrative, professional, computer, sales
- Must meet salary AND duties tests
- **Common error**: Paying salary to someone who does non-exempt work; if challenged, employer owes back OT

**In SAP**:
- IT0008 (Organizational Assignment) or IT0200 (Salary): Mark employee classification
- Or configure in custom IT (if company has extended classification field)
- Used for wage type determination: which overtime rules apply

### Federal Overtime Calculation

**Standard OT** (federal):
- Regular rate = gross pay (including certain bonuses, piece rate) ÷ hours worked
- OT rate = regular rate × 1.5
- Applied to hours over 40/week
- Exception: Certain bonuses, shift premiums, geographical pay may be excluded; verify your wage type setup

**Example**:
- Employee: $20/hour, hourly rate wage type
- Week 1: 45 hours
  - Regular: 40 hrs × $20 = $800
  - OT: 5 hrs × $30 = $150
  - Gross: $950
  - Fed withholding: calculated on $950 (not on overtime rate separately)

**SAP wage type setup**:
- Create wage type for "Straight Time" (40/44 hours × rate)
- Create wage type for "Overtime" (hours over 40/44 × 1.5 × rate)
- In payroll run, time data drives which wage type is used
- If time tracking not automated, manual entry required; flag for review

### State Overtime Rules

**California** (most complex):
- Daily OT: Hours 8-12 in a day = 1.5x; hours 12+ = 2x
- Weekly OT: Hours 40+ in a week = 1.5x (double-time if crosses into daily+weekly)
- 7th day: 1.5x if employee works 6 consecutive days (2x if 7+ hrs on 7th day)
- Applies to "alternate workweek" schedules (e.g., 4/10 can have 40 hours without OT if structured correctly)

**New York**:
- OT: Hours over 40/week at 1.5x
- No daily OT rule (unlike CA)
- Premium pay for Sunday work or split-shift premium (if applicable to industry)

**Texas** (and most others):
- Follow federal FLSA rules (40/week at 1.5x)
- No state-specific additional rules

**Multi-state employees**:
- If employee works in multiple states, apply most favorable (or all) rules to that portion of time
- Example: Remote employee in CA but company in TX → apply CA OT rules to CA time
- Requires time tracking by state/location; coordinate with time system

### Wage Components Included in "Regular Rate"

**Included** (affects OT rate):
- Base hourly rate or salary
- Commissions
- Piecework rate
- Most bonuses (if tied to production, hours worked)
- Tips (if employer claims tip credit, which SAP typically does not)

**Excluded** (does not affect OT rate):
- Discretionary bonuses
- Gifts
- Expense reimbursements
- Shift premium (sometimes; depends on structure)
- Overtime premium itself
- Certain geographic pay (verify with legal)

**In SAP**:
- Document which wage types are included in "regular rate" for OT calculation
- Create separate wage type for "OT premium" so it's not double-counted
- Verify calculation in PC_PAYRESULT after payroll runs with overtime

---

## Special Situations & Compliance

### Multi-State Employees

**Scenario**: Employee works in multiple states or relocates mid-period.

**Actions**:
1. **Determine Primary Work Location**: Where did employee spend majority of hours?
2. **Update IT0208** (State Tax): Mark primary state and effective date of change
3. **Change State Withholding**: SAP updates on next payroll
4. **Allocate Wages**: If employee worked X% in State A, Y% in State B:
   - Calculate gross allocation by state
   - Apply respective state tax withholding
   - May require manual journal entry post-payroll if SAP doesn't support multi-state allocation
5. **Notify Employee**: Tax withholding will change; may affect net pay temporarily
6. **Tax Compliance**: Prepare amended state tax returns if mid-year transfer and year-end filing needed

**State-specific considerations**:
- CA → TX move: CA requires final tax return filing; TX has no income tax (simplifies)
- TX → CA move: CA penalizes employers for underpayment if late in year; calculate catch-up withholding
- Reciprocal Agreements (PA/NJ, VA/DC, etc.): Some states waive non-resident tax if opposite state taxes; check for applicability

### Remote Workers

**Rule**: Typically tax employee based on work location, not company location.

**Example**: Employee works from home in California but works for a Texas company → subject to California income tax.

**SAP setup**:
- IT0008 (Organizational Assignment): Note "remote" or mark work location as CA
- IT0208 (State Tax): Set to CA
- Verify California wages don't exceed state-specific exceptions

### Non-Resident Alien Withholding (NRA)

**Scope**: Foreign nationals on visa (H-1B, L-1, O-1, etc.)

**Federal rule**: NRAs typically withheld at maximum rate (supplemental wage withholding) unless they have Social Security Number and W-4

**Common confusion**:
- Many companies over-withhold NRA taxes; withholding should equal tax liability at year-end
- IRS Pub 519 provides detailed NRA withholding rules
- State tax: Varies; some states exempt NRAs

**In SAP**:
- IT0207 (Federal Tax): Flag as "NRA" or "Non-Resident Alien"
- SAP can apply special withholding calculation
- Recommend: Use flat 22% supplemental rate (safest) or consult tax advisor for case-by-case

**Action item**: Annual NRA tax reconciliation; if over-withheld, explore filing for refund eligibility.

### Fringe Benefits & Taxable Income

**Examples of taxable fringe benefits** (included in gross, subject to withholding):
- Health insurance employer contribution (non-cafeteria)
- Life insurance over $50,000
- Commuting benefits (exceeds monthly limit)
- Gym membership
- Entertainment/meals (varies if "working meal")

**Examples of non-taxable benefits** (excluded from gross):
- Health insurance (cafeteria/HSA)
- 401(k) contributions (pre-tax)
- Dependent care FSA
- Adoption assistance (limited)
- Qualified tuition assistance (limited)
- Health savings account (HSA)

**In SAP**:
- Create separate "benefit" wage types for taxable fringes
- Mark IT0200 or wage type as "taxable" vs. "non-taxable"
- Include taxable fringes in gross for withholding calculation
- Exclude non-taxable fringes from gross

**Common error**: Including health insurance as taxable when it should be pre-tax; results in over-withholding federal/state, employee overpays tax.

### Relocation & Moving Expense Reimbursement

**Federal rule**: Deduction for work-related moving expenses was temporarily suspended (2018-2025 for individuals); currently being reassessed by Congress.

**Current status** (verify for 2026): Employer reimbursement is taxable income to employee unless specifically excluded under active tax rules.

**In SAP**: Create "moving expense reimbursement" wage type; mark as taxable unless your tax advisor confirms exclusion applies.

### Garnishments & Levy Priorities

**Legal framework**: Consumer Credit Protection Act (CCPA); state garnishment laws vary.

**Federal priority order**:
1. Child support / spousal support (HIGHEST)
2. Federal tax lien / levy
3. Federal student loan default
4. State/local taxes
5. Other creditors (credit card, medical, etc.)

**Limits on withholding**:
- CCPA: Maximum 60% of "disposable earnings" per week for non-child-support
- Child support: Can be up to 65% if employee has second family; up to 50% if current family (higher if arrears)
- **Disposable earnings**: Gross minus mandatory deductions (federal, FICA, state, local taxes); NOT voluntary deductions

**In SAP**:
- Create garnishment wage types (per court order or garnishment type)
- Mark sequence/priority in wage type maintenance
- Calculate disposable earnings as basis for garnishment limit
- SAP can track cumulative garnishment; flag if exceeds legal limit

---

## Year-End W-2 & Tax Compliance Timeline

| Date | Action | Owner |
|---|---|---|
| Jan 1 | Finalize any prior-year corrections; run final YTD reports | Payroll |
| Jan 15 | Last regular payroll for tax year (federal requirement for W-2 reporting window) | Payroll |
| Jan 31 | Forms 940, 941-X (corrections), state unemployment reports due | Compliance/Finance |
| Feb 15 | e-file W-2s (if using e-filing service); print W-2s for employee distribution | Payroll/HR |
| Feb 28 | W-2 distribution deadline to employees (IRS requirement) | HR |
| March 31 | Form 945 (non-payroll backup withholding) due if applicable | Finance |
| April 15 | Federal tax deposit deadline (if using monthly deposit schedule) | Finance |

**W-2 prep in SAP**:
- Run **PC00_M10_CEDT** (Remuneration Statement) in December
- This generates year-to-date totals from PCL2 (payroll results table)
- Verify Box 1 (gross), Box 2 (federal withheld), Boxes 3-6 (FICA), Box 20 (state tax)
- Flag any missing state/local wage boxes
- Reconcile to payroll reports
- Generate W-2 file (typically via RPUAUD00 or custom reporting tool)

---

## Compliance Audit Checklist

**Annual (every Jan):**
- Verify all employees have current W-4 on file (IT0207)
- Review W-4 effective dates; follow up if any older than 3 years
- Reconcile payroll to GL; investigate variances >1%
- Reconcile year-end FICA, FUTA, state SUI to Form 941, 940

**Quarterly (Apr, Jul, Oct, Jan):**
- Verify Form 941 (quarterly) correctness before filing
- Check SUI tax deposits were timely
- Reconcile payroll tax liability accounts to accrual

**Ongoing (every payroll):**
- Verify all employees have valid state tax code (IT0208)
- Check for employees with zero federal withholding; is there valid Form 8274 (exempt certification)?
- Monitor for negative net pay; flag for investigation
- Verify garnishment calculations and priority sequence
- Check for wage base limit management (Social Security, FUTA, state SUI)

**At risk: Compliance penalties range from $100-$10,000 per violation, and up to criminal penalties for intentional underpayment.**

