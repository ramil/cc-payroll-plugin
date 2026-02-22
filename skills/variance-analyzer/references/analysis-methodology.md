# Variance Analysis Methodology

This reference document explains the mathematical framework, algorithms, and decision rules used by the variance-analyzer skill for payroll analysis.

## Variance Calculation Framework

### Basic Variance Metrics

For each employee + wage type combination:

**Absolute Variance (Dollar Amount):**
```
Variance$ = Current_Amount - Prior_Amount
```

**Percentage Variance:**
```
Variance% = (Current_Amount - Prior_Amount) / |Prior_Amount| * 100
```

**Special Cases:**
- If Prior_Amount = 0 and Current_Amount > 0: Mark as "New" (not a percentage increase)
- If Prior_Amount > 0 and Current_Amount = 0: Mark as "Eliminated" (100% decrease)
- If both are 0: No variance, skip reporting

### Direction & Favorability

**Direction Classification:**
- Increase: Current > Prior
- Decrease: Current < Prior

**Favorability (context-dependent):**
- Earnings (1000-1999): Increases favorable, decreases unfavorable
- Deductions (2000-2999): Decreases favorable, increases unfavorable
- Employer Contributions (3000-3999): Decreases favorable, increases unfavorable

---

## Tolerance Framework

### Threshold Logic

Flag a variance if **EITHER** condition is true:

```
FLAG if (|Variance%| > Percentage_Threshold) OR (|Variance$| > Absolute_Threshold)
```

### Default Thresholds

| Category | Percentage Threshold | Absolute Threshold | Rationale |
|----------|---------------------|-------------------|-----------|
| Individual Items (Employee + Wage Type) | 5% | $500 | Catches material variances; filters noise from rounding |
| Category Totals (all wage type within cost center/dept) | 2% | $1000 | Higher dollar threshold for aggregates; stricter % for trend detection |
| Gross Pay Anomalies | 30% | N/A | Significant change indicator; suggests status change or error |
| New/Terminated Employees | All records flagged | N/A | Must investigate all hire/termination events |
| Wage Type Anomalies | Any appearance/disappearance | N/A | New benefit, new deduction, benefit termination |

### Customization

Users can override thresholds via command-line:
```bash
--threshold-pct 10        # Flag variances >10% change
--threshold-abs 1000      # Flag variances >$1000 dollar amount
```

Example scenarios:
- **Strict pre-production check:** 2% / $250 (catch small errors before go-live)
- **Standard monthly review:** 5% / $500 (default)
- **Loose routine check:** 10% / $1000 (focus on major variances only)

---

## Variance Classification

### Variance Types

1. **Documented Changes:** Expected variance explained by known employment/benefit events
   - Salary increases (documented in HR system)
   - New hire (date-driven)
   - Termination (date-driven)
   - Benefit enrollment/changes (benefit system events)
   - Bonus/commission payouts (planned financial events)

2. **Anomalies:** Unexpected variance that requires investigation
   - Undocumented gross pay changes
   - New deductions appearing (unknown to HR)
   - Wage types appearing/disappearing without cause
   - Gross pay drops >30% without termination

3. **Cyclical/Seasonal:** Expected variance from regular patterns
   - Overtime spikes (seasonal, project-based)
   - Quarterly/annual bonuses
   - Annual pay increases (all employees)
   - Tax/contribution limit impacts (FICA wage base, 401k limit)

### Risk Levels

For pre-production scenarios, classify variance severity:

| Risk Level | Percentage Variance | Dollar Variance | Examples |
|-----------|-------------------|-----------------|----------|
| HIGH RISK | >10% | >$2,000 | Gross pay 20% higher, missing employee, major deduction appears |
| MEDIUM RISK | 5-10% | $500-$2,000 | Overtime spike in cost center, benefit change, salary variance |
| LOW RISK | 2-5% | <$500 | Rounding differences, small tax changes, minimal benefit variation |

---

## Anomaly Detection Algorithms

### 1. New Employee Detection

**Rule:** Employee present in current period, absent in prior period

**Flag Severity:** MEDIUM (may not be fully loaded into payroll yet)

**Investigation Checklist:**
- Verify hire date matches payroll processing date
- Check that all mandatory benefits are set up
- Confirm W-4 / I-9 documentation is complete
- Verify cost center assignment is correct
- Check for multiple wage type records (some system generate default records before full setup)

### 2. Terminated Employee Detection

**Rule:** Employee present in prior period, absent in current period

**Flag Severity:** MEDIUM (verify termination processed correctly)

**Investigation Checklist:**
- Verify termination date and final paycheck are processed
- Check for final pay adjustments (unused vacation payout, severance)
- Confirm COBRA/continuation processing
- Verify benefits termination dates
- Check for final withholding/deductions (garnishments, loan repayments)

### 3. Gross Pay Anomalies

**Rule:** |Variance in gross pay| > 30% for employee, without corresponding new hire/termination

**Flag Severity:** HIGH (may indicate processing error or status change)

**Possible Root Causes:**
- Undocumented salary change
- Job code change affecting rate
- Shift change (overtime-eligible to straight time, or vice versa)
- Unpaid leave or health leave (FMLA, disability, etc.)
- Strike or labor action
- Overpayment correction in current period
- Data entry error in SAP

**Investigation Required:** Must manually verify with HR or payroll system

### 4. Wage Type Anomalies

**Rule:** Wage type appears in current period but was zero in prior period (or vice versa)

**Flag Severity:** MEDIUM to HIGH (depends on wage type)

**For Appearance:**
- New benefit enrollment (401k, health insurance, etc.)
- New bonus/commission plan start date
- New payroll condition (shift differential, on-call, etc.)
- Error or misconfiguration (wrong wage type code)

**For Disappearance:**
- Benefit termination (termination, plan drop)
- Bonus/commission plan ended
- Payroll condition removed (shift change, different assignment)
- System setup/configuration change

### 5. Cost Center Shift Detection

**Rule:** Employee appears in different cost center than prior period

**Flag Severity:** LOW to MEDIUM (expected for transfers)

**Investigation:**
- Verify transfer is documented in HR system
- Check that gross pay remained proportional if split across cost centers
- Confirm cost center is correct for assigned location/department

---

## Statistical Anomaly Detection (Z-Score Method)

For larger datasets (30+ employees), use z-score analysis to identify statistical outliers:

**Z-Score Calculation:**
```
Z = (X - μ) / σ

Where:
  X = Individual variance (% or $)
  μ = Mean variance for wage type category
  σ = Standard deviation of variance
```

**Flagging Threshold:**
- |Z| > 2.0: Unusual (>2 standard deviations from mean)
- |Z| > 3.0: Highly unusual (>3 standard deviations from mean)

**Use Cases:**
- Salary increases: Identify employees with larger-than-average raises
- Overtime: Identify employees with unusual OT spikes
- Deductions: Identify employees with unusual withholding changes
- Bonuses: Identify disparity in bonus payments

**Note:** Z-score method supplements threshold method; not a replacement. Always combine statistical analysis with business context.

---

## Multi-Level Aggregation

The analysis produces variance summaries at multiple levels:

### Level 1: Employee + Wage Type (Most Detailed)
```
Employee E001, Wage Type 1000 (Basic Pay)
  Current: $3,500
  Prior: $3,000
  Variance: $500 (16.7%)
```

### Level 2: Employee (Gross Pay Summary)
```
Employee E001 Summary
  Current Gross: $5,200
  Prior Gross: $4,500
  Variance: $700 (15.6%)
  Flagged Items: Basic Pay +$500, Overtime +$200
```

### Level 3: Wage Type (Category Summary)
```
Wage Type 1000 (Basic Pay)
  Current Total: $125,000
  Prior Total: $120,000
  Variance: $5,000 (4.2%)
  Employees Affected: 18 (salary increases, new hires)
  Average Change: $277/employee
```

### Level 4: Cost Center (Operational Unit)
```
Cost Center 4500 (Operations)
  Current Total Payroll: $250,000
  Prior Total Payroll: $230,000
  Variance: $20,000 (8.7%)
  Top Drivers: Overtime +$12,000, Bonus +$5,000, New Hires +$8,000
```

### Level 5: Department (Business Unit)
```
Department 200 (West Region)
  Current Total Payroll: $450,000
  Prior Total Payroll: $440,000
  Variance: $10,000 (2.3%)
  By Cost Center: [breakdown]
```

### Level 6: Organization (Enterprise)
```
Total Company Payroll
  Current: $2,000,000
  Prior: $1,950,000
  Variance: $50,000 (2.6%)
  By Department: [breakdown]
```

---

## Trend Detection (Multi-Period Analysis)

When 3+ periods of data are available:

### Trend Direction

Calculate slope of variance over time:
```
Trend = (Most_Recent_Variance - Oldest_Variance) / Number_of_Periods
```

- **Positive Slope:** Increasing trend (variance growing larger)
- **Negative Slope:** Decreasing trend (variance shrinking)
- **Near-Zero Slope:** Stable (variance oscillating but relatively flat)

### Seasonality Detection

For repeating patterns (e.g., quarterly bonuses, seasonal overtime):

1. Calculate 4-period moving average for smoothing
2. Identify peaks and troughs at regular intervals
3. Mark known seasonal patterns (annual bonus, tax changes, etc.)

### Anomalous Spike Detection

Identify anomalies in trend:
```
Spike if |Current_Variance - Moving_Average| > 1.5 * σ
```

### Example: Overtime Wage Type Trend

```
Period 1 (Jan): $15,000
Period 2 (Feb): $18,000
Period 3 (Mar): $22,000
Period 4 (Apr): $19,000
Period 5 (May): $17,000

Trend: Increasing then decreasing (spike in Mar, return to normal)
Interpretation: Seasonal project completed in March; returning to baseline
Recommendation: Monitor for future spikes; expected pattern for this department
```

---

## Root Cause Pattern Library

The skill uses pattern matching to suggest root causes for significant variances:

### Earnings Increases
- **Pattern 1 (Salary Increase):** All or most employees in cost center/department increase consistently
  - Suggestion: "Annual salary increase, cost-of-living adjustment, or promotion cycle"
- **Pattern 2 (New Hire Spike):** Specific cost center increases, new employees appear in employee list
  - Suggestion: "New hire ramp; expected to contribute fully in subsequent periods"
- **Pattern 3 (Overtime Spike):** Overtime wage type increases significantly, other earnings stable
  - Suggestion: "Operational demand spike, staffing shortage, or project deadline"
- **Pattern 4 (Individual Spike):** Single employee or small group increases significantly
  - Suggestion: "Promotion, salary adjustment, or change in hours/assignment"

### Earnings Decreases
- **Pattern 1 (Termination/Resignation):** Employee missing from current period
  - Suggestion: "Employee terminated or resigned; verify exit processing"
- **Pattern 2 (Leave of Absence):** Specific employee/group decreases, still in system but reduced hours
  - Suggestion: "Unpaid leave (FMLA), disability, sabbatical, or reduced hours"
- **Pattern 3 (Shift Change):** Consistent reduction in earnings, particularly OT
  - Suggestion: "Shift change to non-OT-eligible position, scheduling change"

### Tax/Deduction Changes
- **Pattern 1 (W-4 Change):** Federal tax decreases, other taxes stable or proportional
  - Suggestion: "Employee filed new W-4 form with different withholding election"
- **Pattern 2 (Benefit Enrollment):** New deduction appears, gross pay unchanged
  - Suggestion: "New benefit enrollment (401k, health insurance, HSA); effective with current period"
- **Pattern 3 (Benefit Termination):** Deduction goes to zero, gross pay unchanged
  - Suggestion: "Benefit termination (coverage ended, plan suspension); verify in benefits system"
- **Pattern 4 (Plan Change):** Premium amounts increase across all employees
  - Suggestion: "Annual plan rate increase, plan change, or coverage tier change"
- **Pattern 5 (Wage Base Impact):** FICA, FUTA, SUTA contributions drop to zero in Q4
  - Suggestion: "Employee reached annual wage base limit for FICA/FUTA; expected in Q3-Q4"

### Employer Contribution Changes
- **Pattern 1 (Match Change):** 401k match increases/decreases proportionally with employee deferrals
  - Suggestion: "Employee increased/decreased deferral election; employer match follows"
- **Pattern 2 (Subsidy Change):** Health insurance employer contribution changes
  - Suggestion: "Annual plan rate increase, enrollment changes, or subsidy adjustment"
- **Pattern 3 (New Hire):** Employer contributions appear for new employee
  - Suggestion: "New hire; employer contributions beginning after waiting period expiration"

---

## Natural Language Commentary Generation

The skill generates natural language commentary using templates for significant variances:

### Template 1: Single-Employee Variance
```
[Employee_Name] [Wage_Type_Description] changed [Direction] [Variance$]
([Variance%]) this period. [Root_Cause_Suggestion].
```

**Example:**
"Jane Smith's Federal Tax Withholding decreased $120 (8%) this period, consistent
with updated W-4 filed last month (3 exemptions added). No further action required."

### Template 2: Wage Type Category Variance
```
[Wage_Type_Category] across [Dimension] increased [Variance$] ([Variance%])
period-over-period. [Root_Cause_Pattern]. [Number_Employees] impacted.
```

**Example:**
"Overtime in Cost Center 4500 increased $12,450 (23%) this period, driven by
staffing shortage and customer project acceleration. 8 employees affected.
Recommend monitoring; expect normalization next period if staffing improves."

### Template 3: Anomaly Flag
```
ANOMALY: [Anomaly_Type] detected. [Anomaly_Details].
Required Action: [Investigation_Checklist_Item].
```

**Example:**
"ANOMALY: New Employee detected. E051 (Sarah Johnson) appears in current period,
absent from prior. Hire date: 2026-02-01. Required Action: Verify all mandatory
benefits enrolled, W-4 on file, cost center assignment correct."

### Template 4: Risk Notification
```
HIGH RISK: [Employee_Name] / [Wage_Type] variance of [Variance%] ([Variance$])
exceeds tolerance. [Issue_Description]. Action: [Recommended_Investigation].
```

**Example:**
"HIGH RISK: Employee E012 (Bob Davis) gross pay increased 35% ($2,100) without
corresponding new hire or documented status change. Issue: Possible overpayment or
system error. Action: Cross-check against HR employment records and SAP payroll
configuration; verify hours/rate data entry."

---

## Tolerance & Threshold Configuration Reference

### Recommended Settings by Use Case

**Pre-Production Validation (Strictest):**
- Percentage: 2%
- Absolute: $250
- Rationale: Catch all errors before go-live; false positives acceptable

**Routine Monthly Review (Default):**
- Percentage: 5%
- Absolute: $500
- Rationale: Balance signal-to-noise; focus on material items

**Executive Summary (Loosest):**
- Percentage: 10%
- Absolute: $1,000
- Rationale: Focus on major variance drivers; reduce noise for C-level review

**Overtime-Heavy Analysis:**
- Overtime % Threshold: 15%
- Overtime $ Threshold: $2,000
- Other Earnings %: 5%
- Other Earnings $: $500
- Rationale: Overtime is naturally volatile; adjust thresholds accordingly

**Deduction Scrutiny (Stricter for Deductions):**
- Earnings %: 5% / $500
- Deductions %: 0.5% / $100
- Employer Contrib %: 2% / $250
- Rationale: Deductions affect take-home pay; errors are material to employee

---

## Data Quality & Edge Case Handling

### Missing Data
- Empty cells: Treat as 0
- Missing employees: Process as new hire (current) or termination (prior)
- Missing wage types: Process as new wage type (current) or wage type elimination (prior)

### Division by Zero
- Prior amount = 0, Current > 0: Mark as "New", do not calculate percentage
- Prior amount = 0, Current = 0: Skip (no variance)
- Formula: Use `max(|Prior|, 0.01)` as denominator to avoid division errors

### Duplicate Records
- Combine amounts if same employee/wage type appears multiple times in same period
- Flag as data quality warning if duplicates suggest processing errors

### Currency Handling
- Convert all amounts to USD (or organization's reporting currency)
- Maintain currency code in output for audit trail
- Flag if currency differs between current and prior periods

### Rounding & Precision
- Maintain 2 decimal places for currency amounts
- Maintain 1 decimal place for percentages
- Use banker's rounding (round-to-even) for consistency

---

**Last Updated:** 2026-02-07
