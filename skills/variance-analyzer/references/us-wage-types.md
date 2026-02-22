# US Payroll Wage Types Reference

This reference covers common US payroll wage types found in SAP payroll result exports. Each entry includes typical wage type codes, descriptions, expected occurrence, and variance behavior notes.

> **Important — Wage Type Code Mapping:**
> SAP wage type codes (LGART) are customer-configurable. The codes below (0100-6090 range) represent one common numbering convention. The test data and `wage-type-categories.md` use a different convention (1000-4200 range). When analyzing customer data, match on **Wage Type Text / Description**, not on the specific numeric code. Here is the mapping between this reference and the test data:
>
> | This Reference | Test Data / wage-type-categories.md | Description |
> |---|---|---|
> | 0100 | 1000 | Basic Pay / Regular Salary |
> | 0110 | 1010 | Hourly Regular Pay |
> | 0200 | 1100 | Overtime Premium 1.5x |
> | 0300 | 1200 | Bonus / Incentive Pay |
> | 1000 | 2001 | Federal Income Tax |
> | 1020 | 2003 | Social Security Tax - EE |
> | 1040 | 2004 | Medicare Tax - EE |
> | 1100 | 2002 | State Income Tax |
> | 2000 | 2100 | Medical Insurance - EE |
> | 2020 | 2101 | Dental Insurance - EE |
> | 2100 | 2200 | 401(k) Deferral |
> | 3000 | 3001 | Social Security Tax - ER |
> | 3020 | 3002 | Medicare Tax - ER |
> | 3040 | 3500 | FUTA |
> | 3060 | 3600 | SUTA |

## Regular Earnings & Base Wages

### Regular Salary (Wage Type 0100-0105)
- **Description:** Fixed monthly or annual salary paid to salaried employees
- **Frequency:** Every paycheck (monthly, biweekly, semi-monthly)
- **Expected Amounts:** Consistent across periods (unless raise/promotion)
- **Variance Drivers:**
  - Salary increase (promotion, raise)
  - New hire (prorated)
  - Terminated employee (missing)
- **Variance Threshold:** >5% or >$500
- **Notes:**
  - Should be extremely stable month-to-month
  - Large variances indicate data entry error or system issue
  - Watch for duplicate loads or partial period amounts

### Hourly Regular Pay (Wage Type 0110-0115)
- **Description:** Hourly pay for regular (non-overtime) hours worked
- **Frequency:** Every paycheck
- **Expected Amounts:** Variable based on hours worked
- **Variance Drivers:**
  - Hours worked variance (seasonal, project-based)
  - Rate change (promotion, skill tier increase)
  - New hire (partial month)
  - Termination (partial month)
  - Unpaid leave (vacation, sick, FMLA)
- **Variance Threshold:** >7% or >$300
- **Notes:**
  - Naturally variable; higher percentage threshold appropriate
  - Compare against hours worked data if available
  - Look for pattern changes (increased absenteeism, schedule changes)

## Overtime & Supplemental Pay

### Overtime 1.5x (Wage Type 0200-0205)
- **Description:** Overtime compensation at 1.5x base rate (premium for hours >40/week or >8/day per state)
- **Frequency:** As needed (variable each period)
- **Expected Amounts:** Highly variable
- **Variance Drivers:**
  - Unexpected rush projects or demand spikes
  - Understaffing due to turnover/absences
  - New employees ramping up slowly
  - Seasonal business cycles
  - Organizational efficiency improvements
- **Variance Threshold:** >10% or >$500
- **Notes:**
  - Most volatile wage type; high variance normal
  - Focus on trends across multiple periods rather than single-period spikes
  - Investigate if OT disappears entirely (understaffing resolved, or system issue?)
  - Look for individual employees with unusual OT patterns (possible off-hours work)

### Overtime 2.0x / Double Time (Wage Type 0210)
- **Description:** Double-time compensation for hours exceeding 12/day or 60/week (state-dependent)
- **Frequency:** Rare, project-dependent
- **Expected Amounts:** Sporadic, often $0
- **Variance Drivers:**
  - Major project push
  - Critical deadline
  - Temporary staffing shortage
- **Variance Threshold:** >15% or >$500 (higher tolerance)
- **Notes:**
  - May not appear every period; treat zero amounts as normal
  - Flag only if appears unexpectedly (check project status)

### Holiday Pay / Holiday OT (Wage Type 0220-0225)
- **Description:** Premium or straight-time pay for hours worked on company holidays
- **Frequency:** Specific to holiday calendar
- **Expected Amounts:** Predictable based on holiday calendar
- **Variance Drivers:**
  - Holiday calendar changes
  - Weekend holiday shift coverage staffing changes
  - Holiday observance policy changes
- **Variance Threshold:** >10% or >$300
- **Notes:**
  - Should align with company holiday calendar
  - Unusual variation indicates policy change or data error
  - Verify against calendar (not all years have same holiday distribution)

### Shift Differential (Wage Type 0230-0235)
- **Description:** Premium pay for work on less desirable shifts (night shift, weekend)
- **Frequency:** As applicable to shift structure
- **Expected Amounts:** Variable based on shift assignments
- **Variance Drivers:**
  - Shift assignment changes
  - Staffing changes on specific shifts
  - Operating hour changes
  - Bid/rotation cycles
- **Variance Threshold:** >10% or >$200
- **Notes:**
  - Varies by organizational shift structure
  - Track by shift and shift worker population
  - May spike if new shift created or existing shift fully staffed

### Bonuses (Wage Type 0300-0310)
- **Description:** Performance bonuses, discretionary bonuses, annual/quarterly bonuses
- **Frequency:** Project/performance dependent (quarterly, annually, or ad-hoc)
- **Expected Amounts:** Highly variable, may be zero
- **Variance Drivers:**
  - Performance vs. targets
  - Discretionary management decisions
  - Plan changes
  - New employees (may not qualify)
  - Terminations (pro-rata or forfeited)
- **Variance Threshold:** >15% or >$1,000 (high tolerance)
- **Notes:**
  - Often zero in some periods (if bonus month); normal volatility
  - Watch for consistency of eligible population
  - Flag if bonus criteria changed unexpectedly

### Commission Pay (Wage Type 0320-0330)
- **Description:** Commission or piece-rate compensation
- **Frequency:** Every paycheck (if commission structure)
- **Expected Amounts:** Highly variable based on sales/activity
- **Variance Drivers:**
  - Sales volume changes
  - Market conditions
  - Product mix changes
  - Commission rate changes
  - New sales representatives (ramp period)
- **Variance Threshold:** >15% or >$500
- **Notes:**
  - Treat similarly to overtime for variance tolerance
  - Monitor trends across sales team
  - Watch for individual rep anomalies (new rep, territory change, performance issue?)

## Deductions & Withholdings

### Federal Income Tax (Wage Type 1000-1010)
- **Description:** Federal income tax withheld based on W-4 form and gross pay
- **Frequency:** Every paycheck
- **Expected Amounts:** Proportional to gross pay, varies with W-4 elections
- **Variance Drivers:**
  - W-4 form changes (filing status, dependents, additional withholding)
  - Gross pay changes (triggers different tax brackets)
  - Tax code changes (rare, annual)
- **Variance Threshold:** >3% or >$200
- **Notes:**
  - Lower threshold than wages (tax is tightly calculated)
  - Track against gross pay changes (should correlate)
  - Flag if rate is significantly off expected (possible error)
  - Verify any large changes correspond to W-4 updates

### Social Security / FICA Tax (Wage Type 1020-1030)
- **Description:** 6.2% Social Security tax (employee portion) on gross pay (subject to annual wage base)
- **Frequency:** Every paycheck (until wage base met)
- **Expected Amounts:** 6.2% of gross pay, subject to annual limit (~$168,600 in 2026)
- **Variance Drivers:**
  - Gross pay changes
  - Year-to-date wage base approaching limit (common in Q4)
  - New hires (fresh wage base)
  - Terminated employees (partial month)
- **Variance Threshold:** >2% or >$100
- **Notes:**
  - Should be perfectly proportional to gross pay
  - CRITICAL VARIANCE: If appears to drop unexpectedly, may indicate wage base limit reached
  - Flag if rate deviates from 6.2% (check system setup)
  - Monitor YTD amounts to anticipate when limit will be reached

### Medicare Tax (Wage Type 1040-1050)
- **Description:** 1.45% Medicare tax on all gross pay (no limit), plus Additional Medicare tax (0.9%) on higher earners
- **Frequency:** Every paycheck
- **Expected Amounts:** 1.45% of gross pay + 0.9% for earnings >$200K single ($250K married)
- **Variance Drivers:**
  - Gross pay changes
  - Additional Medicare tax threshold reached (annual)
  - Wage code changes
- **Variance Threshold:** >2% or >$50
- **Notes:**
  - Similar to FICA; should track gross pay closely
  - Additional Medicare tax creates year-end spikes for high earners
  - Flag if rate deviates from 1.45% base (check system setup)

### State Income Tax (Wage Type 1100-1199, varies by state)
- **Description:** State income tax withheld per state tax law and W-4 equivalent forms
- **Frequency:** Every paycheck
- **Expected Amounts:** Highly variable by state (0% in no-income-tax states like FL, TX, WA)
- **Variance Drivers:**
  - W-4 equivalent form changes (varies by state, not all states use W-4)
  - Gross pay changes
  - Multi-state employees (allocate by state)
  - State tax code/rate changes (annual)
  - Relocation (employee moves out of state)
- **Variance Threshold:** >5% or >$200 (varies by state implementation)
- **Notes:**
  - Threshold and behavior varies significantly by state
  - Zero in no-income-tax states (FL, TX, WA, NV, SD, WY, AK)
  - Flag multi-state variations (must allocate by state of work)
  - Each state has different deduction/credit rules; work with tax specialist if unsure

### Local Income Tax (Wage Type 1200-1299, varies by locality)
- **Description:** Local/city income tax (if applicable, limited to select cities/counties)
- **Frequency:** Every paycheck (if applicable)
- **Expected Amounts:** Varies by locality, often zero
- **Variance Drivers:**
  - Relocation (employee moves to taxing locality)
  - Gross pay changes
  - Local tax code changes
- **Variance Threshold:** >10% or >$50 (low absolute threshold due to small amounts)
- **Notes:**
  - Only applicable in select cities (New York City, Columbus OH, Philadelphia PA, etc.)
  - May be zero for most employee population
  - Flag unexpected appearance (employee relocation?)

## Benefits & Deductions

### Medical Insurance (Wage Type 2000-2010)
- **Description:** Pre-tax health insurance premium deduction
- **Frequency:** Every paycheck
- **Expected Amounts:** Based on coverage level (Employee, Family, Employee+Spouse, etc.) and plan premium
- **Variance Drivers:**
  - New benefit elections (open enrollment)
  - Plan changes (premium increases)
  - Dependent/family status changes (marriage, birth, divorce)
  - New hire (deduction start)
  - Termination (deduction stop)
  - Coverage level changes (Employee → Family, etc.)
- **Variance Threshold:** >5% or >$50
- **Notes:**
  - Typically largest single deduction
  - Expect changes during open enrollment periods
  - Watch for employees with zero medical (possible error if group coverage required)
  - Track enrollment by coverage level to explain aggregate variances

### Dental Insurance (Wage Type 2020-2030)
- **Description:** Pre-tax dental insurance premium deduction
- **Frequency:** Every paycheck (if elected)
- **Expected Amounts:** Fixed plan premium, varies by plan (typically $15-$50/pay period)
- **Variance Drivers:**
  - New/terminated election (open enrollment, new hire, termination)
  - Plan premium changes
  - Dependent changes
- **Variance Threshold:** >10% or >$50
- **Notes:**
  - Optional benefit; zero is normal if not elected
  - Lower absolute amounts; percentage threshold more meaningful
  - May fluctuate if coverage is optional add-on

### Vision Insurance (Wage Type 2040-2050)
- **Description:** Pre-tax vision insurance premium deduction
- **Frequency:** Every paycheck (if elected)
- **Expected Amounts:** Fixed plan premium, varies by plan (typically $5-$20/pay period)
- **Variance Drivers:**
  - New/terminated election
  - Plan premium changes
  - Dependent changes
- **Variance Threshold:** >15% or >$20
- **Notes:**
  - Low cost benefit; percentage variance more meaningful
  - Zero common if not elected
  - Often bundled with medical for increased participation

### 401(k) / Retirement Plan (Wage Type 2100-2120)
- **Description:** Pre-tax employee contribution to qualified retirement plan
- **Frequency:** Every paycheck
- **Expected Amounts:** Based on deferral election ($100-$23,500 annually in 2026, adjusted for age)
- **Variance Drivers:**
  - New deferral election (new hire, open enrollment)
  - Deferral amount change
  - Contribution election termination
  - Annual limit reached (common in Q4 for high earners)
  - New hire (deduction start)
  - Termination (deduction stop)
- **Variance Threshold:** >5% or >$100
- **Notes:**
  - Track per-employee elections to understand aggregate changes
  - Watch for high-income employees hitting annual limit
  - Some employees will show zero (no election); normal
  - Verify new hires are enrolled or have enrollment notice

### Roth 401(k) (Wage Type 2130-2140)
- **Description:** Post-tax employee contribution to Roth retirement plan
- **Frequency:** Every paycheck
- **Expected Amounts:** Based on election (limited by total 401k+Roth limit)
- **Variance Drivers:**
  - New Roth election
  - Roth amount changes
  - Termination of Roth elections
  - Annual limit interactions
- **Variance Threshold:** >10% or >$100
- **Notes:**
  - Less common than traditional 401k
  - Interacts with 401k limit; coordinate when reviewing
  - Post-tax (deducted after taxes, not pre-tax)

### HSA / Health Savings Account (Wage Type 2150-2160)
- **Description:** Pre-tax health savings account contribution (only available if enrolled in HDHP)
- **Frequency:** Every paycheck
- **Expected Amounts:** Varies by election (annual limit $4,150 individual, $8,300 family in 2026)
- **Variance Drivers:**
  - New HSA election (usually in conjunction with HDHP enrollment)
  - Contribution amount changes
  - HDHP coverage eligibility changes
  - Annual limit reached
- **Variance Threshold:** >10% or >$100
- **Notes:**
  - Only employees on HDHP plan eligible
  - Zero is normal for non-HDHP employees
  - May see decrease if HDHP enrollment drops (open enrollment impact)
  - Watch for coordination with medical insurance changes

### FSA / Flexible Spending Account (Wage Type 2170-2180)
- **Description:** Pre-tax dependent care or medical care FSA contribution
- **Frequency:** Every paycheck
- **Expected Amounts:** Varies by election (annual limit $3,200 medical FSA, $5,000 dependent care in 2026)
- **Variance Drivers:**
  - New FSA election (open enrollment)
  - Election termination
  - Life event eligibility changes
  - Month-to-month variation (true-up at year-end)
- **Variance Threshold:** >15% or >$100
- **Notes:**
  - Optional benefit; zero common
  - "Use it or lose it" rule creates variability
  - Track monthly to catch premiums approaching/exceeding limits (possible tax issue)
  - Watch for mid-year election changes due to life events

### Life Insurance - Employee (Wage Type 2200-2210)
- **Description:** Life insurance premium, employee-paid portion (typically supplemental)
- **Frequency:** Every paycheck (if elected)
- **Expected Amounts:** Fixed per election, typically $10-$50/pay period
- **Variance Drivers:**
  - New election (typically at hire or open enrollment)
  - Coverage level changes
  - Termination of coverage
  - Age-based rate increases (if applicable)
- **Variance Threshold:** >10% or >$50
- **Notes:**
  - Basic life insurance often employer-paid (not employee deduction)
  - Supplemental life subject to employee election
  - Zero normal if not elected
  - May have age-banding changes (age milestone increases rate)

### Life Insurance - Employer Paid (Wage Type 2215)
- **Description:** Employer-paid life insurance premium (often non-taxable to limit)
- **Frequency:** Every paycheck
- **Expected Amounts:** Fixed per employee or per-coverage level, varies by plan design
- **Variance Drivers:**
  - New employees (coverage starts)
  - Terminated employees (coverage stops)
  - Plan changes
  - Coverage level changes
- **Variance Threshold:** >5% or >$100
- **Notes:**
  - Non-deductible from paycheck (but tracked for accounting)
  - Appears as earnings offset or separate payroll item
  - Flag if disappears unexpectedly (system issue?)

### Dependent Care Account (Wage Type 2220)
- **Description:** Pre-tax dependent care FSA contribution
- **Frequency:** Every paycheck
- **Expected Amounts:** Varies by election (up to $5,000/year in 2026)
- **Variance Drivers:**
  - New election or election change
  - Qualifying dependent changes
  - Life event eligibility changes
  - Year-end true-up/forfeiture
- **Variance Threshold:** >15% or >$100
- **Notes:**
  - Highly variable month-to-month
  - Subject to "use it or lose it" rules
  - May drop to zero if no qualifying dependents

## Employer-Paid Costs & Taxes

### Employer Social Security (Wage Type 3000-3010)
- **Description:** Employer portion of Social Security tax (6.2% of employee gross pay)
- **Frequency:** Every paycheck (per employee gross pay)
- **Expected Amounts:** 6.2% of respective employee gross pay, subject to annual wage base (~$168,600 in 2026)
- **Variance Drivers:**
  - Employee gross pay changes
  - Employee headcount changes
  - Wage base limit reached for high earners
  - New hires
  - Terminations
- **Variance Threshold:** >2% or >$100
- **Notes:**
  - Directly correlates to employee SS tax (deduction 1020)
  - Should be perfectly proportional to gross payroll
  - Watch for high earner wage base limit timing
  - Flag if drops unexpectedly for specific employee (check gross pay)

### Employer Medicare (Wage Type 3020-3030)
- **Description:** Employer portion of Medicare tax (1.45% of all employee gross pay, no limit)
- **Frequency:** Every paycheck
- **Expected Amounts:** 1.45% of total employee gross pay
- **Variance Drivers:**
  - Employee gross pay changes
  - Headcount changes
- **Variance Threshold:** >2% or >$50
- **Notes:**
  - Similar to employee Medicare (1.45% proportional)
  - No annual limit (unlike Social Security)
  - Should track total payroll changes closely
  - Flag if rate deviates from 1.45%

### FUTA / Federal Unemployment Tax (Wage Type 3040-3050)
- **Description:** Federal unemployment insurance tax (0.6% on employee gross pay, subject to annual wage base limit ~$7,000 in 2026)
- **Frequency:** Every paycheck (until wage base limit reached)
- **Expected Amounts:** 0.6% of employee gross pay (subject to wage base, so appears to drop in Q4)
- **Variance Drivers:**
  - Gross payroll changes
  - Headcount changes
  - New hires (fresh wage base)
  - Wage base limit being reached for employees (common in later pay periods)
  - Experience rating changes (credits)
- **Variance Threshold:** >1% or >$100
- **Notes:**
  - Annual wage base limit causes natural drop in Q4 (expected and normal)
  - Monitor timing to ensure limit calculation is correct
  - Experience rating/tax rate varies by employer, state, and industry
  - Flag if rate is significantly off expected (system setup issue)

### SUTA / State Unemployment Tax (Wage Type 3060-3080, varies by state)
- **Description:** State unemployment insurance tax (varies by state, typically 0.5%-6% on employee gross pay)
- **Frequency:** Every paycheck
- **Expected Amounts:** Varies by state experience rating, typically $0.50-$2.00 per employee per pay period
- **Variance Drivers:**
  - State tax rate changes (annual rate adjustments)
  - Experience rating changes (based on claims/separations)
  - Gross payroll changes
  - Headcount changes
  - Multi-state employees (allocate by state of work)
- **Variance Threshold:** >5% or >$200
- **Notes:**
  - Varies dramatically by state and experience rating
  - May see annual rate changes in Q1 (new experience ratings)
  - High-turnover industries see higher rates
  - Work with payroll specialist to understand state-specific rules

### Workers Compensation (Wage Type 3100-3120)
- **Description:** Workers compensation insurance premium (varies by state and job classification)
- **Frequency:** Every paycheck or periodic (monthly/quarterly)
- **Expected Amounts:** Varies by classification rate (0.5%-5%+ depending on hazard level)
- **Variance Drivers:**
  - Gross payroll changes
  - Classification changes (employee moves to higher-risk role)
  - New hires
  - Headcount changes
  - Premium rate changes (annual)
  - Audit adjustments
- **Variance Threshold:** >3% or >$200
- **Notes:**
  - Varies widely by job classification and state
  - Manufacturing, construction have higher rates than office work
  - Flag classification changes (may indicate job change or error)
  - May see periodic true-ups if premium was estimated

## Leave Pay

### Vacation Pay / PTO (Wage Type 4000-4010)
- **Description:** Pay for accrued and used vacation days/hours
- **Frequency:** Variable (as taken, or payout at termination)
- **Expected Amounts:** Varies by hours taken and rate
- **Variance Drivers:**
  - Vacation usage patterns (seasonal peaks)
  - New vacation accrual policies
  - Carryover balance changes
  - Termination payouts
  - Scheduling changes (summer schedules)
- **Variance Threshold:** >15% or >$300
- **Notes:**
  - Highly variable by season and employee usage
  - Watch for spikes in Q4 (year-end carryover payouts)
  - May be zero if employees not using or accrual is restricted
  - Flag if employee with large balance suddenly takes zero (possible system issue?)

### Sick Leave / Sick Pay (Wage Type 4020-4030)
- **Description:** Pay for sick days used
- **Frequency:** Variable (as taken)
- **Expected Amounts:** Varies by hours taken and rate
- **Variance Drivers:**
  - Illness patterns (seasonal flu, COVID)
  - New sick leave policies
  - FMLA tracking (may be separate)
  - Headcount changes
  - New employees (different accrual rates)
- **Variance Threshold:** >20% or >$200
- **Notes:**
  - Most variable leave type (unpredictable illness)
  - May see seasonal spikes (winter illness, pandemic surges)
  - Watch for individuals with excessive usage (possible policy violation?)
  - May interact with disability/FMLA (coordinate review)

### FMLA / Leave of Absence Pay (Wage Type 4040-4050)
- **Description:** Pay for protected unpaid leave (FMLA) or employer-paid continuation during leave
- **Frequency:** Variable (during leave periods)
- **Expected Amounts:** Varies by leave terms (may be full pay, partial, or zero)
- **Variance Drivers:**
  - New leave instances
  - End of leave periods
  - Disability/pregnancy leave
  - Parental leave
  - Unpaid vs. paid leave terms
- **Variance Threshold:** >20% or >$500
- **Notes:**
  - Discrete event-driven (spikes when someone goes on leave)
  - Coordinate with HR leave management system
  - Flag for completeness (all leave being tracked in payroll?)
  - May be separate from sick/vacation (watch for double-counting)

### Holiday Pay (Wage Type 4060)
- **Description:** Pay for company holidays (straight-time, not premium)
- **Frequency:** Per holiday calendar
- **Expected Amounts:** Fixed per holiday per employee not working
- **Variance Drivers:**
  - Holiday calendar changes
  - Headcount on holiday (some staff work)
  - Part-time employee coverage
  - Shutdown periods (plant closures)
- **Variance Threshold:** >10% or >$200
- **Notes:**
  - Should align with published holiday calendar
  - Flag if doesn't match expected holidays
  - Coordinate with Holiday OT variance (separate premium concept)
  - May be zero if no holidays or all employees working

## Garnishments & Court-Ordered Deductions

### Wage Garnishment (Wage Type 5000-5010)
- **Description:** Court-ordered wage garnishment for child support, spousal support, or creditor judgment
- **Frequency:** Every paycheck (while order active)
- **Expected Amounts:** Varies per court order (typically 10%-50% of disposable income)
- **Variance Drivers:**
  - New garnishment orders
  - Garnishment termination (obligation met)
  - Modification of orders (child support adjustment, remarriage)
  - Gross pay changes (affects disposable income calculation)
  - Employee termination
- **Variance Threshold:** >20% or >$100 (high tolerance, discrete events)
- **Notes:**
  - Highly sensitive; must follow court orders exactly
  - Flag unexplained appearances/disappearances (possible missed order notification?)
  - Verify affected employees have proper compliance documentation
  - May require payroll priority coordination with other garnishments

### Child Support (Wage Type 5020-5030)
- **Description:** Specific child support garnishment (often subset of garnishment, may be separated for accounting)
- **Frequency:** Every paycheck (while order active)
- **Expected Amounts:** Per court order
- **Variance Drivers:**
  - New orders
  - Order terminations
  - Order modifications
  - Income changes (may trigger recalculation)
- **Variance Threshold:** >15% or >$100
- **Notes:**
  - May be combined with wage garnishment or separate
  - Requires careful compliance (federal/state mandates)
  - Prioritized above most other deductions by law

### Loan Repayment / Advance Repayment (Wage Type 5040-5050)
- **Description:** Employee loan or paycheck advance repayment
- **Frequency:** Per loan terms (typically biweekly)
- **Expected Amounts:** Fixed per loan agreement
- **Variance Drivers:**
  - New loans issued
  - Loans paid off early
  - Loan term changes
  - Employee termination
- **Variance Threshold:** >10% or >$100
- **Notes:**
  - Usually fixed amount per paycheck
  - Flag if appears/disappears without explanation (system issue?)
  - Ensure loan balance is tracked separately for accounting

### Overpayment Repayment (Wage Type 5060)
- **Description:** Repayment of prior period overpayment or unearned benefit
- **Frequency:** Per repayment agreement (may be one-time or recurring)
- **Expected Amounts:** Varies per prior issue
- **Variance Drivers:**
  - New overpayment discovery
  - Overpayment repayment completion
- **Variance Threshold:** >20% or >$500 (high tolerance)
- **Notes:**
  - Usually temporary (appears once, resolves)
  - Flag if recurring (possible systematic issue)
  - Coordinate with HR/Accounting for prior period investigation

## Other Deductions & Voluntary Contributions

### Health Insurance (Post-Tax) (Wage Type 6000)
- **Description:** Post-tax health insurance deduction (in addition to pre-tax if applicable)
- **Frequency:** Every paycheck
- **Expected Amounts:** Per plan premium
- **Variance Drivers:**
  - Plan changes (supplement or replacement)
  - New elections
  - Coverage level changes
  - Premium increases
- **Variance Threshold:** >5% or >$50
- **Notes:**
  - May be supplement to pre-tax medical or alternative plan
  - Coordinate with pre-tax medical deduction (watch for double deductions)

### 529 Savings Plan (Wage Type 6020-6030)
- **Description:** Post-tax contribution to college savings plan
- **Frequency:** Every paycheck (if elected)
- **Expected Amounts:** Varies by election
- **Variance Drivers:**
  - New plan election
  - Election changes
  - Termination of contributions
  - Children graduating (plan termination)
- **Variance Threshold:** >15% or >$100
- **Notes:**
  - Optional benefit; zero normal
  - Post-tax contribution (after taxes)
  - May be limited by employer participation

### Charitable Donations (Wage Type 6040)
- **Description:** Employee charitable giving (payroll deduction donation)
- **Frequency:** Per employee election
- **Expected Amounts:** Varies by employee election (often tied to campaigns)
- **Variance Drivers:**
  - Campaign periods (United Way, etc.)
  - New employee election
  - Campaign termination
- **Variance Threshold:** >20% or >$100
- **Notes:**
  - Usually campaign-driven (Q4 giving, United Way)
  - May spike during giving campaigns
  - Zero normal during non-campaign periods

### Union Dues (Wage Type 6050-6060)
- **Description:** Union membership dues
- **Frequency:** Every paycheck (if employee is union member)
- **Expected Amounts:** Fixed per union contract or agreement
- **Variance Drivers:**
  - Union dues rate changes (per contract renegotiation)
  - New union members
  - Termination of union employees
  - Non-union status changes
- **Variance Threshold:** >2% or >$20 (tight tolerance)
- **Notes:**
  - Highly standardized; variance indicates rate change or membership change
  - Zero normal for non-union employees
  - Flag rate variance (check union contract for effective date)

### Other Deductions (Wage Type 6070-6090)
- **Description:** Catch-all for parking, transit passes, phone stipends, or other miscellaneous deductions
- **Frequency:** Varies
- **Expected Amounts:** Varies by benefit type
- **Variance Drivers:**
  - Program participation changes
  - Benefit amount changes
  - Termination of programs
- **Variance Threshold:** >15% or varies
- **Notes:**
  - Review by specific deduction type
  - Coordinate with benefits administration for changes
  - May be monthly or periodic

---

## Quick Reference: Variance Sensitivity

**High Sensitivity (Flag >3% or >$100):**
- Regular/Hourly Pay
- Federal Tax, FICA, Medicare
- Employer SS, Medicare, FUTA

**Medium Sensitivity (Flag >5% or >$200):**
- Medical, Dental, Vision Insurance
- 401K, HSA, FSA
- Employer SUTA
- Overtime
- Wage Garnishment

**Low Sensitivity (Flag >10% or >$500):**
- Vacation/PTO, Sick Leave
- Bonuses, Commissions
- Supplemental benefits
- Other miscellaneous deductions

This is a reference only—actual thresholds should be configured based on business requirements and materiality assessments specific to your organization.
