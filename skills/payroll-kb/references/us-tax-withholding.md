# US Tax Withholding Rules & Compliance

A comprehensive reference for US federal, state, and local payroll tax rules. **Always consult your tax advisor and legal team for your specific business situation.**

## Federal Income Tax Withholding

### W-4 Form Basics
- **Form W-4** (Employee's Withholding Certificate) determines how much federal income tax to withhold
- **Filing Status** options: Single, Married Filing Jointly, Married Filing Separately, Head of Household, Qualifying Widow(er)
- **Effective Date**: W-4 changes typically become effective on the first paycheck of the next payroll cycle following the employee's submission
- **Withholding Exemptions** (pre-2020): Previous system; Form W-4 was redesigned for tax year 2020+
- **Step-Dependent Worksheet**: Newer W-4 uses multiple steps (jobs, dependents, credits, other adjustments) instead of exemptions

### Withholding Methods

#### Percentage Method
- IRS provides tax tables updated annually (current for 2025)
- Payroll software uses lookup tables based on:
  - Gross wages
  - Pay frequency (weekly, biweekly, monthly, etc.)
  - Filing status
  - W-4 adjustments (extra withholding, claim dependents, etc.)
- Calculation: Apply IRS formula/table to compute required withholding

#### Wage Bracket Method
- Alternative method using IRS wage bracket tables
- Some payroll systems support both methods; SAP PCC uses standard IRS tables

### 2025 Federal Tax Brackets (Single Filer, Standard Deduction $14,600)
- 10% on income up to $11,000
- 12% on income $11,001 - $44,725
- 22% on income $44,726 - $95,375
- 24% on income $95,376 - $182,100
- 32% on income $182,101 - $231,250
- 35% on income $231,251 - $578,125
- 37% on income over $578,125

**Note**: Brackets adjust annually for inflation. Verify current brackets before each calendar year.

### Common W-4 Adjustments in SAP
- **Step 3**: Claim dependents (reduces withholding)
- **Step 4a**: Multiple jobs (increases withholding if applicable)
- **Step 4b**: Spouse also working (increases withholding if applicable)
- **Step 4c**: Dependents over 17 years old (child tax credit)
- **Step 5**: Other income, deductions, or credits (increases/decreases withholding)
- **Extra Withholding**: Request additional amount withheld per paycheck (in dollars)

### SAP IT0210 (Tax Data, US) Fields
- **Country**: US
- **Tax ID**: Employee's SSN
- **Federal Filing Status**: Maps to W-4 filing status
- **Federal Exemptions/Dependents**: From W-4 Step 3
- **Federal Extra Withholding**: From W-4 Step 5
- **Tax Authority**: Federal
- **Status**: Active or inactive
- **Entry Date & Exit Date**: When tax setup applies

### Special Withholding Situations
- **Non-Resident Alien (NRA)**: Generally 30% flat withholding on US-source income; treaty exceptions apply; consult tax counsel
- **Fringe Benefits**: Many are non-taxable (health insurance, group term life up to $50K, etc.) but must be properly coded
- **Supplemental Wages**: Bonus, commissions, retroactive pay—withhold highest rate in employee's W-4 bracket or flat 22% (up to 37% if over $1M)
- **Wedding Gifts, Awards**: May be taxable; follow IRC Section 74 guidelines
- **Stock Options/RSUs**: Different withholding rules depending on plan type; coordinate with Finance/HR

---

## FICA Taxes (Social Security & Medicare)

### Social Security (OASDI)
- **Employee Rate**: 6.2%
- **Employer Rate**: 6.2%
- **Total**: 12.4%
- **Wage Base Limit (2025)**: $168,600
- **Limit Application**: Once employee cumulative wages exceed wage base, no more OASDI withholding for that calendar year
- **Calculation**: (Gross wages subject to withholding) × 6.2%, up to wage base
- **Self-Employment**: 12.4% (15.3% combined with Medicare for self-employed)

**Common Error**: Failing to stop OASDI withholding after wage base is reached. SAP PCC tracks cumulative wages and should automatically stop withholding; verify in payroll results.

### Medicare (HI)
- **Employee Rate**: 1.45%
- **Employer Rate**: 1.45%
- **Total**: 2.9%
- **Wage Base Limit**: No limit (all wages subject to Medicare)
- **Calculation**: (All gross wages) × 1.45%

### Additional Medicare Tax
- **Rate**: 0.9% (employee only; employer pays 0.9% on wages over threshold)
- **Wage Thresholds (2025)**:
  - Single: $200,000
  - Married Filing Jointly: $250,000
  - Married Filing Separately: $125,000
- **Application**: Once employee cumulative wages exceed threshold, withhold 0.9% on excess
- **Employer Obligation**: Employer matches 0.9% on wages over $200,000 (regardless of employee filing status)

**SAP Implementation**: Configure in IT0210 or wage type rules; verify Additional Medicare Tax is calculated after Social Security wage base threshold is met.

### FICA Exempt Status
- Some employees may be exempt (non-resident aliens on certain visas, some religious organizations, etc.)
- Document in IT0210 with "Exempt" indicator

---

## Federal Unemployment (FUTA)

- **Employer-Only Tax**: No employee withholding
- **Federal Rate**: 6.0% (current)
- **Wage Base (2025)**: $7,000 per employee per calendar year
- **Net Rate After State Credit**: Typically 0.6% (if state UI is paid in full and timely)
- **Credit**: Up to 5.4% credit available if employer has paid state unemployment insurance and experience rate is favorable
- **Quarterly Filing**: Form 940-EZ or 940
- **Annual Reconciliation**: Form 940 (Employer's Annual Federal Unemployment Tax Return)

**SAP Implementation**: Configure employer FUTA as wage type; automatic calculation based on gross wages up to wage base limit; verify wage base tracking resets January 1 annually.

---

## State Income Tax Withholding

### States with Income Tax (37 states + DC)
Withholding rules vary significantly by state:

#### High-Withholding States
- **California**: Progressive tax system, W-4 CA form, state SDI (Disability Insurance) 1.0%, PFL (Paid Family Leave) 0.5%
- **New York**: High tax rate, NYC and Yonkers have local income tax, form NY-4 (W-4 equivalent)
- **Illinois**: Flat 4.95% state income tax
- **Massachusetts**: Flat 5.0%
- **Texas**: No income tax (0%)

#### State-Specific Requirements
- **Form W-4**: Each state has its own (CA, NY, IL, etc.); not federal W-4
- **Filing Status**: May be different from federal (some states recognize different statuses)
- **Deductions**: Some states allow federal tax paid as deduction; varies
- **Multi-State Employees**: Complex; see Multi-State Withholding section below

### State Unemployment Insurance (SUI)
- **Employee Contribution**: 3 states only (CA, NJ, NY) plus PR
  - **CA**: 1.0% (Disability Insurance SDI) + 0.5% (Paid Family Leave PFL)
  - **NJ**: ~0.58% (shared with employer)
  - **NY**: ~0.58% (shared with employer)
- **Employer Contribution**: All states except TX; rates based on experience rating (history of claims)
- **Wage Base**: Varies by state (CA $1,552.00 for 2025; NJ $40,400 for 2025; NY $50,600 for 2025)
- **Annual Reconciliation**: State UI tax returns (Quarterly or Annual)

### State Disability Insurance (SDI) & Paid Family Leave (PFL)
- **California**: SDI 1.0% (employee) up to $1,552.00 wage base; PFL 0.5% (employee) up to $131,455 wage base (2025)
- **New Jersey**: Temporary Disability Insurance (TDI) ~0.58% (shared)
- **New York**: Disability Insurance ~0.60% (employee) + Paid Family Leave ~0.62% (employee) (2025 rates)
- **Hawaii**: Temporary Disability Insurance 0.5%
- **Rhode Island**: Temporary Disability Insurance (TDI) ~1.27% + Paid Family Leave ~1.28%

**SAP Setup**: Each state contribution is a separate wage type; configure cumulative wages tracking per state per employee.

### Local/Municipal Taxes
- **Philadelphia**: 3.8071% municipal wage tax (city income tax)
- **New York City**: Ranges 3.876%-3.876% (on salary/wages)
- **Ohio Municipalities**: Various rates (1.0%-2.5% in most)
- **Washington DC**: 8.95% top rate
- **Other Cities**: Some cities have local income taxes

**Configuration**: Set up separate wage types for each municipal tax jurisdiction; track by employee work location or residence.

---

## Multi-State Employee Withholding

### Tax Reciprocity Agreements
Some states have reciprocity agreements (waive tax for non-residents working in the state):

- **IL-IN, IL-KY, IL-MO, IL-WI**: Reciprocal tax agreements
- **NJ-PA, NJ-NY**: NJ and PA don't have reciprocity; NJ and NY do NOT (common misconception)
- **Example**: Indiana resident working in Illinois—may not owe IL tax due to reciprocity

### Where to Withhold
**General Rule**: Withhold based on **residence state** unless there is a reciprocity agreement or the employee is non-resident in work state.

**Scenarios**:
1. **Residence = Work State**: Withhold only that state (straightforward)
2. **Residence ≠ Work State (No Reciprocity)**: Withhold both states (common for NJ resident working in NY)
3. **Residence ≠ Work State (Reciprocity Applies)**: Withhold residence state only
4. **Multi-State Employer**: Employee works in multiple states—withhold all states proportionally or by primary location

### Apportionment
When employee works in multiple states:
- **Time Apportionment**: Allocate wages by % of time worked in each state (most common)
- **W-4 Allocation**: Some states allow employee to split W-4 dependents/credits across states
- **Safe Harbor**: Withhold all states; true-up at year-end on W-2

**SAP Implementation**: Set up multiple state tax withholdings per employee in IT0208 (State Taxes); configure time tracking and wage apportionment rules.

---

## Pre-Tax Deductions & Impact on Taxable Wages

The following reduce gross wages for federal and state income tax purposes:

### 401(k) Contributions
- **Employee Election**: Reduces federal, state, and local income tax wages
- **2025 Limit**: $24,500 (traditional); $30,500 with catch-up if age 50+
- **Roth 401(k)**: After-tax, does NOT reduce taxable wages (but still deducted from gross for FICA/federal calculations)
- **Impact on FICA**: 401(k) deductions do NOT reduce Social Security or Medicare taxable wages

### 403(b) & 457(b) Deductions
- Reduce federal and state income tax wages
- Same impact as 401(k) on taxable wages

### Health Savings Account (HSA)
- Reduce federal and state income tax wages
- Do NOT reduce FICA wages
- Must be paired with High-Deductible Health Plan (HDHP)

### Flexible Spending Account (FSA) / Section 125
- Reduce federal, state, and FICA wages (truly pre-tax)
- Health FSA, Dependent Care FSA
- **2025 Health FSA limit**: $3,300

### Traditional IRA Contributions
- Some deductibility if income limits met; typically contributed after-tax on paycheck
- For pre-tax treatment, coordinate with HR/Finance

### Pre-Tax Items **NOT** Reducing FICA
- 401(k) contributions
- HSA contributions
- Traditional IRA contributions (in some cases)

### Pre-Tax Items **REDUCING FICA**
- Section 125 cafeteria plans
- Dependent Care FSA
- Some health insurance premium deductions

---

## Common Tax Withholding Errors

### Error 1: Failing to Stop OASDI at Wage Base
**Symptom**: Employee shows overpayment of Social Security tax at year-end
**Root Cause**: SAP did not track cumulative OASDI wages or configuration does not automatically stop withholding
**Fix**:
1. Verify IT0210 is configured for automatic wage base tracking
2. Check cumulative wage types in payroll results (PC_PAYRESULT)
3. Calculate overpayment: (Excess wages × 6.2%)
4. Issue refund or credit on final paycheck or W-2 correction (amended W-2c)

### Error 2: Wrong State Tax Setup for Multi-State Employees
**Symptom**: Employee withholds for wrong state; NJ/NY reciprocity misunderstanding
**Root Cause**: IT0208 (State Tax) not updated when employee changes residence or work location
**Fix**:
1. Confirm employee's state of residence
2. Confirm employee's primary work location
3. Check for reciprocity agreement (www.wwd.org or state tax authority)
4. Update IT0208 with correct state(s)
5. Run payroll simulation to preview changes
6. Correct prior periods (if within SOL) and issue W-2c if necessary

### Error 3: Missing W-4 Data (IT0210 Blank)
**Symptom**: "Missing Tax Data" PCC alert; federal withholding at 0 or maximum rate
**Root Cause**: Employee did not submit W-4; IT0210 not created
**Fix**:
1. Request W-4 from employee (required for payroll processing)
2. Create IT0210 record (PA30 → Infotype 210)
3. Verify filing status, dependents, extra withholding
4. Re-run payroll calculation
5. Educate employee: W-4 is legal requirement

### Error 4: Incorrect Additional Medicare Tax Threshold
**Symptom**: Additional Medicare Tax not calculated above $200K (single) threshold
**Root Cause**: Wage type or payroll rule configured with wrong threshold or not accumulating YTD
**Fix**:
1. Verify payroll rules for Additional Medicare Tax wage type
2. Check cumulative wage tracking (should accumulate per calendar year)
3. Confirm threshold matches 2025 rules ($200K single, $250K MFJ)
4. Test in payroll simulation
5. Correct prior periods if necessary

### Error 5: Local/Municipal Tax Missing
**Symptom**: Employee not withheld for Philadelphia, NYC, DC, or Ohio municipality tax
**Root Cause**: Payroll configuration missing local tax wage types or employee location not flagged
**Fix**:
1. Determine employee work location (or residence location if applicable)
2. Verify local tax requirement for that jurisdiction
3. Create wage type for local tax (if not exists)
4. Configure payroll rule to trigger on location/assignment
5. Update IT0006 (Address) or IT0001 (Org Assignment) with location
6. Test in simulation; correct prior periods if necessary

---

## Year-End Considerations

### W-2 Preparation & Reconciliation
- **Filing Deadline**: January 31 (paper) or February 28 (e-filed) following the year
- **Box Reconciliation**:
  - Box 1: Federal taxable wages (after pre-tax deductions)
  - Box 2: Federal income tax withheld (sum of all pay periods)
  - Boxes 3-6: Social Security/Medicare wages, tips, tax
  - Boxes 12a-d: Pre-tax deductions (401k code D, HSA code W, etc.)
  - Boxes 19-20: State/local taxes withheld
- **Quarterly 941 Reconciliation**: W-2 Box 2 federal tax should match 941 total quarterly withholding
- **Correction**: If error found, issue W-2c (amended W-2) within 60 days of discovery

### Form 940 (FUTA Annual Return)
- **Due**: January 31 following the year
- **Reconciliation**: Total FUTA paid (employer contributions) must match forms submitted
- **State Credit Adjustment**: If paying state UI timely, credit up to 5.4%

### Form 941-X (Quarterly Adjustment Return)
- Used to correct errors on prior 941 filings
- Must be filed within 3 years from date of filing or 2 years from date tax was paid
- Coordinate with payroll/Finance for corrections

### W-4 Changes for Next Year
- Encourage employees to review W-4 if they owe tax or over-withheld significantly
- Update IT0210 effective January 1 of new tax year

---

## Compliance Checkpoints

### Monthly Payroll Review
- [ ] Verify federal withholding aligns with W-4 changes (new/updated IT0210 records)
- [ ] Check OASDI cumulative wages (stop withholding at wage base)
- [ ] Confirm state/local tax withholding for correct jurisdiction(s)
- [ ] Review Additional Medicare Tax calculation for high-earners
- [ ] Validate pre-tax deduction amounts in payroll

### Quarterly Filings
- [ ] 941 (Federal): Sum of federal withholding from all payroll runs; reconcile to W-2 tracking
- [ ] State UI reports: Verify wages subject to SUI match payroll
- [ ] Local tax forms (if applicable): Philadelphia wage tax, NYC, DC, etc.

### Annual Year-End
- [ ] W-2 Preparation: Run W-2 report in SAP (PC00_M10_CEDT or equivalent)
- [ ] Reconciliation: Compare W-2 totals to 941 quarterly filing and payroll summary
- [ ] 940 (FUTA): File with documentation of state UI paid
- [ ] Corrections: If discrepancies found, issue W-2c amendments
- [ ] Audit Trail: Document all corrections and timing of discovery

---

## Key Takeaways for SAP PCC

- **IT0210** = Federal tax setup (W-4 filing status, dependents, extra withholding)
- **IT0208** = State tax setup (state, filing status, special rules)
- **IT0209** = Unemployment insurance state assignment
- **Wage Types**: Configure separate wage types for federal, OASDI, Medicare, Additional Medicare, SUI, SDI, local taxes
- **Cumulative Tracking**: OASDI, FUTA, and state SUI have wage base limits; configure automatic tracking
- **SAP Transactions**: PA30 (maintain infotypes), PA20 (display), PC00_M10_CALC (run payroll), PC_PAYRESULT (review results)

---

**Remember**: Tax rules change annually, especially wage bases and rates. Always verify current rules before each tax year and consult your tax advisor for complex situations.
