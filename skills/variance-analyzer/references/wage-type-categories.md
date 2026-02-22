# SAP US Payroll Wage Type Categories

This reference document catalogs common US payroll wage types used in SAP systems and explains typical period-over-period variance patterns for each category.

> **Note:** The codes below (1000-4200 range) are used in the test data files and `generate_test_data.py`. The companion reference `us-wage-types.md` uses a different numbering convention (0100-6090 range) with more detailed variance analysis guidance per wage type. SAP wage type codes are customer-configurable — always match on **Wage Type Text** rather than code numbers when analyzing customer data.

## Regular Earnings (1000-1999 Range)

### 1000 - Basic Pay / Regular Pay
- **Description:** Standard hourly or salaried regular earnings
- **Typical Variance Explanations:**
  - Salary increase or decrease
  - Hire/termination (prorated)
  - Hours worked changes (for hourly)
  - Change from part-time to full-time or vice versa
  - Shift changes affecting base rate
- **Expected Behavior:** Stable or predictable changes based on documented employment status changes
- **Variance Threshold:** Flag >5% on total payroll or >$500 per employee

### 1100 - Overtime Pay (OT)
- **Description:** Overtime compensation (typically 1.5x for hours over 40/week)
- **Typical Variance Explanations:**
  - Operational demand changes (seasonal, project-based)
  - Understaffing or staffing additions
  - New hire ramp periods (employees learning job take longer)
  - Month-end or quarter-end pushes
  - Voluntary vs. mandatory overtime policy changes
  - Shift scheduling changes
- **Expected Behavior:** Highly variable; expected to spike during busy periods; should correlate with operational metrics
- **Variance Threshold:** Flag >10% on wage type category or >$1000 per cost center (OT is naturally volatile)

### 1200 - Bonus / Incentive Pay
- **Description:** Performance-based pay, sales commissions, spot bonuses
- **Typical Variance Explanations:**
  - Performance metrics changes
  - Sales commission changes (new contracts, lost contracts)
  - Annual/quarterly bonuses disbursed
  - Spot bonus program changes
  - Plan participation changes (new employees not yet eligible)
  - Payout timing (some periods include bonus, others don't)
- **Expected Behavior:** Highly variable; should be documented by HR/Sales; common for certain pay periods (annual bonus month, quarterly commission)
- **Variance Threshold:** Flag unusual patterns or new bonus payments; expected variance is high for bonuses

### 1300 - Shift Differential
- **Description:** Premium pay for non-standard shifts (evening, night, weekend)
- **Typical Variance Explanations:**
  - Shift rotation schedule changes
  - Employees moving on/off shift premium-eligible positions
  - New shift premium policies
  - Staffing changes in shift-eligible job codes
  - Seasonal shift adjustments
- **Expected Behavior:** Changes correlate with shift assignments; usually stable unless operations change
- **Variance Threshold:** Flag >15% on wage type or significant changes in number of employees receiving

### 1400 - Call-In Pay / On-Call Pay
- **Description:** Compensation for on-call availability or emergency call-in
- **Typical Variance Explanations:**
  - Changes in on-call scheduling policies
  - Operational incident frequency changes
  - Staff availability changes
  - Emergency events (weather, system outages) triggering more call-ins
- **Expected Behavior:** Variable; driven by operational events
- **Variance Threshold:** Unusual if non-zero in multiple consecutive periods; flag spikes

## Deductions (2000-2999 Range)

### 2001 - Federal Income Tax Withholding (FIT)
- **Description:** Federal income tax withheld from gross pay
- **Typical Variance Explanations:**
  - Employee W-4 form changes (exemptions, additional withholding, new hire W-4s)
  - Salary or bonus changes
  - Year-to-date gross pay changes (impacts tax calculation)
  - Marital status changes (M->S or S->M)
  - Job number of dependents changes
  - Tax table updates (SAP wage type configuration updates)
  - Effective date of W-4 changes
  - New hires using default withholding until W-4 submitted
- **Expected Behavior:** Should correlate with gross pay changes; large swings indicate W-4 or tax table changes
- **Variance Threshold:** Flag >10% change; investigate unexpected decreases (employee may have filed incorrect W-4)

### 2002 - State Income Tax Withholding (SIT)
- **Description:** State income tax withheld (varies by state tax tables and employee residence)
- **Typical Variance Explanations:**
  - Same as FIT, plus state-specific issues
  - Employee relocation (new state, new tax table)
  - State tax code changes (new state, different filing status by state)
  - State tax rate changes or table updates (typically annual)
  - Remote work situations (worksite vs. home state taxation)
- **Expected Behavior:** Correlated with gross pay and federal tax; should be stable unless W-4 or residence changes
- **Variance Threshold:** Flag >10% change or >$100 absolute; investigate by state if multi-state company

### 2003 - FICA-OASDI (Social Security)
- **Description:** Social Security tax (6.2% of gross up to annual wage base limit)
- **Typical Variance Explanations:**
  - Salary changes (linear relationship to gross up to wage base)
  - YTD wage base approaching or exceeding limit (OASDI stops after wage base reached, ~$168,600 in 2024)
  - New hire (full period contribution vs. partial)
  - Termination (stops accruing after termination)
  - Bonus or lump-sum payments pushed employee over wage base
  - Payroll formula changes affecting eligible wages
  - Contributions to HSA or 401k (reducing taxable wages if using pre-tax elections)
- **Expected Behavior:** Should track with gross pay; expect near-zero for high-earners near/after wage base limit in Q4
- **Variance Threshold:** Flag >5% or >$100; investigate wage base limit impacts

### 2004 - FICA-Medicare (HI)
- **Description:** Medicare tax (1.45% of all gross, additional 0.9% on earnings >$200k single/$250k married)
- **Typical Variance Explanations:**
  - Gross pay changes
  - Salary increase pushing into additional Medicare tax bracket
  - Contributions to HSA or 401k (reducing taxable wages if pre-tax)
  - New hires, terminations, or pay period count changes
- **Expected Behavior:** Near-linear with gross pay; additional Medicare tax (0.9%) applies at high income thresholds
- **Variance Threshold:** Flag >10% or >$100; investigate for high earners crossing additional Medicare tax threshold

### 2100 - Group Health Insurance Deduction (Medical)
- **Description:** Employee portion of medical/health insurance premium
- **Typical Variance Explanations:**
  - New hire enrollment (typically effective first of month following hire)
  - Termination or COBRA/continuation
  - Plan changes (employee elected different coverage level)
  - Premium rate changes (annual, mid-year changes)
  - Dependent coverage changes (employee adds/removes spouse/children)
  - Marriage/divorce triggering life event enrollment
  - Waiver or drop of coverage (employee may waive if covered elsewhere)
  - Pay period count variation (some months have 3 pay cycles)
- **Expected Behavior:** Stable unless enrollment/plan changes; often starts/stops on month boundary
- **Variance Threshold:** Flag any changes (new enrollments/terminations are expected); investigate sudden mid-period changes

### 2101 - Group Dental Insurance Deduction
- **Description:** Employee portion of dental insurance premium
- **Typical Variance Explanations:**
  - Same as health insurance plus:
  - Dental plan has lower premiums, changes less frequently
  - May be optional (many waive to save costs)
- **Expected Behavior:** Stable unless enrollment changes
- **Variance Threshold:** Flag zero changes that were non-zero in prior periods (may indicate termination vs. plan suspension)

### 2102 - Group Vision Insurance Deduction
- **Description:** Employee portion of vision insurance premium
- **Typical Variance Explanations:**
  - Same as health insurance; vision premiums typically lowest
- **Expected Behavior:** Very stable, usually small amounts
- **Variance Threshold:** Flag changes or zero amounts after non-zero prior periods

### 2200 - 401k (Defined Contribution Plan)
- **Description:** Employee elective deferral to 401k retirement plan
- **Typical Variance Explanations:**
  - New hire enrollment (typically after waiting period, e.g., 30-90 days)
  - Annual contribution limit reset (January, typically; max ~$23,500 in 2024)
  - Employee increased/decreased deferral percentage
  - Employee reached annual contribution limit (stops mid-year, resumes in January)
  - Life event changes (marriage, birth, divorce)
  - Hardship withdrawal affecting current contribution
  - Termination (stops immediately)
- **Expected Behavior:** Stable unless enrollment change; common to drop to zero in Q4 (contribution limit reached); common to restart in January
- **Variance Threshold:** Flag >20% change per employee (deferral elections are discrete); flag zero if previously non-zero (may indicate unwanted change)

### 2300 - 403b / 457 Deferrals
- **Description:** Tax-sheltered annuity or deferred compensation (non-profit, government)
- **Typical Variance Explanations:**
  - Same as 401k
  - Plan election/change cycles (often specific to organization)
- **Expected Behavior:** Stable unless enrollment change
- **Variance Threshold:** Same as 401k

### 2400 - HSA (Health Savings Account) Deduction
- **Description:** Employee contribution to health savings account (pre-tax)
- **Typical Variance Explanations:**
  - HSA enrollment (usually tied to high-deductible health plan enrollment)
  - Annual election period changes
  - Employee increased/decreased contribution
  - Annual contribution limit reset (January; max ~$4,150 single / $8,300 family in 2024)
  - Termination (account ownership transfers to employee, no future contributions)
- **Expected Behavior:** Zero if not enrolled in HSA-eligible plan; stable if enrolled
- **Variance Threshold:** Flag new enrollments and terminations; flag exceeding annual limits

### 2500 - FSA (Flexible Spending Account) Deduction
- **Description:** Employee elective deferral to health care flexible spending account (pre-tax, "use-it-or-lose-it")
- **Typical Variance Explanations:**
  - FSA enrollment during annual enrollment period
  - FSA deferral amount changes (increases/decreases per election)
  - Plan year reset (often calendar year; Jan 1)
  - Termination (FSA balances typically forfeited unless COBRA elected)
  - Dependent FSA enrollment for child care
- **Expected Behavior:** Usually annual reset in January; stable within plan year
- **Variance Threshold:** Flag zero in January-December for employees who had FSA in prior year (may indicate loss of enrollment); flag large mid-year changes

### 2600 - Garnishment / Court Order Deduction
- **Description:** Deduction per court order (child support, creditor, IRS, etc.)
- **Typical Variance Explanations:**
  - New garnishment order issued
  - Garnishment amount changes (court order modification)
  - Garnishment terminated (support obligation paid, creditor paid off)
  - Employee name/address changes affecting garnishment processing
  - Error in garnishment amount (should trigger investigation)
- **Expected Behavior:** Should be zero until court order; stable per order; zero when order satisfied
- **Variance Threshold:** Flag any changes immediately (court orders are specific); flag errors

### 2700 - Dependent Care FSA
- **Description:** Elective deferral to dependent care flexible spending account
- **Typical Variance Explanations:**
  - Enrollment during open enrollment
  - Child ages into/out of dependent care eligibility
  - Deferral amount changes
  - Plan year reset
  - Termination
- **Expected Behavior:** Zero unless dependent care arrangement in place; stable within plan year
- **Variance Threshold:** Flag zero if previously non-zero without corresponding termination

## Employer Contributions (3000-3999 Range)

### 3001 - Employer FICA-OASDI (Employer Social Security)
- **Description:** Employer's matching Social Security tax (6.2% of gross up to wage base)
- **Typical Variance Explanations:**
  - Changes in employee gross pay
  - Same wage base limit dynamics as employee OASDI (stops after limit)
  - New hires, terminations
  - Bonus or lump-sum payments
- **Expected Behavior:** Should mirror employee OASDI contribution; correlates with gross pay
- **Variance Threshold:** Flag >5% variance; investigate if doesn't track with employee OASDI proportionally

### 3002 - Employer FICA-Medicare (Employer Medicare)
- **Description:** Employer's matching Medicare tax (1.45% of all gross)
- **Typical Variance Explanations:**
  - Employee gross pay changes
  - New hires, terminations
- **Expected Behavior:** Linear relationship to total gross payroll; very stable
- **Variance Threshold:** Flag >5% variance; should track precisely with total payroll

### 3100 - Employer Group Health Insurance Contribution
- **Description:** Employer's portion of health insurance premium (often substantially larger than employee portion)
- **Typical Variance Explanations:**
  - Employee enrollment/termination
  - Dependent coverage changes (spouse/child added/removed)
  - Plan changes (employer may contribute differently to different plan tiers)
  - Premium rate changes (annual, mid-year)
  - New hire waiting period expiration (employer contribution starts after waiting period)
  - Employer subsidy changes
- **Expected Behavior:** Stable unless enrollment changes; correlated with number of employees enrolled
- **Variance Threshold:** Flag >5% on total; investigate substantial changes for accuracy

### 3101 - Employer Dental Insurance Contribution
- **Description:** Employer portion of dental insurance
- **Typical Variance Explanations:**
  - Same as health insurance contributions
  - Dental may be voluntary; fewer enrollees than medical
- **Expected Behavior:** Stable unless enrollment changes
- **Variance Threshold:** Flag >5% on total or significant enrollment changes

### 3102 - Employer Vision Insurance Contribution
- **Description:** Employer portion of vision insurance
- **Typical Variance Explanations:**
  - Same as dental/medical insurance
- **Expected Behavior:** Very stable, typically small amounts
- **Variance Threshold:** Flag unusual changes

### 3200 - Employer 401k Match
- **Description:** Employer matching contribution to employee 401k plans
- **Typical Variance Explanations:**
  - Employee deferral changes (employer match depends on employee election)
  - New hires not yet participating
  - Employees who have reached annual deferral limit (no further deferrals, no further match)
  - Plan changes (employer may change match formula, e.g., from 100% to 50%)
  - Employer discretionary contribution (separate from match)
  - Vesting schedule impacts (employer may not immediately vest all match)
- **Expected Behavior:** Correlates with employee deferrals; stable unless plan or participation changes
- **Variance Threshold:** Flag >15% on category; investigate if doesn't correlate with employee deferral changes

### 3300 - Employer 403b / 457 Match
- **Description:** Employer matching contribution to tax-sheltered annuity or 457 plan
- **Typical Variance Explanations:**
  - Same as 401k match
- **Expected Behavior:** Correlates with employee deferrals
- **Variance Threshold:** Same as 401k match

### 3400 - Employer HSA Contribution
- **Description:** Employer contribution to employee health savings accounts
- **Typical Variance Explanations:**
  - Employer HSA funding policy (may fund accounts monthly, annually, or at hire)
  - New hire timing (may receive partial-year employer contribution)
  - HSA enrollment changes
- **Expected Behavior:** Often stable and predictable if employer makes fixed contributions; may be zero if employer doesn't fund HSAs
- **Variance Threshold:** Flag unexpected changes; should be predictable

### 3500 - Employer FUTA (Federal Unemployment Tax Act)
- **Description:** Employer federal unemployment tax
- **Typical Variance Explanations:**
  - Payroll changes (gross wages subject to FUTA, capped at ~$7,000 per employee/year)
  - New hires (until wage base reached)
  - Terminations
  - Annual wage base limit reached (Q2-Q3 typically)
- **Expected Behavior:** Tracks with gross payroll up to wage base; drops near zero in Q4 for employees exceeding limit
- **Variance Threshold:** Flag >5% change on category; investigate wage base interactions

### 3600 - Employer SUTA (State Unemployment Tax Act)
- **Description:** Employer state unemployment tax (rates vary by state, industry, experience rating)
- **Typical Variance Explanations:**
  - State-specific wage base and rates (vary by state)
  - Experience rating changes (employer's unemployment claim history affects rate)
  - New hires in new states (multi-state employers)
  - State rate changes (annual)
  - Payroll changes
- **Expected Behavior:** Varies by state; stable unless tax rate changes
- **Variance Threshold:** Flag >5% per state; review if company operates in multiple states with different rates

### 3700 - Employer Workers Compensation Insurance
- **Description:** Employer workers compensation insurance premium (rates vary by job classification and claim history)
- **Typical Variance Explanations:**
  - Payroll changes (premium is often percentage of payroll by classification)
  - Employee classification changes (affects rate)
  - Annual premium updates
  - Claims experience affecting rates
  - Insurance policy changes (new carrier, new rates)
- **Expected Behavior:** Typically stable; updated annually
- **Variance Threshold:** Flag >10% on category; investigate if major deviations

## Informational / Non-Taxable (4000+ Range)

### 4000 - Imputed Income (Life Insurance, Educational Assistance)
- **Description:** Non-cash taxable benefits that have imputed tax liability (e.g., employer-paid life insurance over $50k, educational assistance, on-site meals, commuter benefits exceeding limits)
- **Typical Variance Explanations:**
  - Life insurance policy value changes
  - Spouse/dependent life insurance enrollment (increases imputed amount)
  - Educational assistance reimbursement (subject to imputed income)
  - Commuter benefit elections
  - New hire benefit loadings
- **Expected Behavior:** Usually zero or stable; changes reflect benefit changes
- **Variance Threshold:** Flag any new imputed income (may indicate benefit change); flag large increases

### 4100 - Taxable Reimbursement / Moving Expense
- **Description:** Reimbursements subject to taxation (non-qualifying reimbursements, moving assistance beyond statutory limits)
- **Typical Variance Explanations:**
  - Relocating employee reimbursements
  - Non-compliant expense reimbursements
  - Policy changes affecting tax treatment
- **Expected Behavior:** Usually zero; appears for specific events (relocations)
- **Variance Threshold:** Flag any amounts; should be exceptional

### 4200 - Backup Withholding
- **Description:** IRS backup withholding (for non-resident aliens, missing SSN, backup withholding election)
- **Typical Variance Explanations:**
  - Non-resident alien visas expiring/renewing
  - Missing or incorrect SSN provided
  - IRS backup withholding notice
- **Expected Behavior:** Usually zero; appears for specific visa/tax situations
- **Variance Threshold:** Flag any amounts; investigate for international employees

---

## Variance Pattern Analysis Guide

When analyzing variances for a wage type category:

1. **Total Wage Type Variance:** Sum variance across all employees in category
2. **Individual Employee Variance:** Identify which employees are driving the category variance
3. **Correlation Check:** Do correlated wage types change together? (e.g., gross pay up → taxes up, benefits stable or change per plan)
4. **New Hires / Terminations:** Do new/terminated employees explain the variance?
5. **Enrollment Changes:** Do benefit changes (insurance, 401k, garnishments) explain the variance?
6. **Pay Event Changes:** Are bonuses, OT, or special pays different?
7. **Rate Changes:** Did tax rates, insurance premiums, or contribution rates change?
8. **Year-to-Date Context:** For taxes and FICA, is the YTD wage base near limits (OASDI cap, Medicare threshold)?

---

**Last Updated:** 2026-02-07
