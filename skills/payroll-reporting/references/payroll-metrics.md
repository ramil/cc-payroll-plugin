# Payroll Metrics Definitions and Calculations

This reference document defines the payroll metrics used in reports, their formulas, and benchmark ranges for US companies.

---

## Core Payroll Cost Metrics

### Total Gross Pay
**Definition:** The sum of all employee earnings before deductions.

**Formula:**
```
Total Gross Pay = SUM(Wage Types 1000-1999) per period
```

**Components:**
- Basic pay (wage type 1000)
- Overtime pay (wage type 1100)
- Bonuses (wage type 1200)
- Commissions and incentives (wage type 1300+)
- Other earnings

**Use Case:** Benchmark against budget, compare period-over-period, analyze staffing changes

**Notes:**
- Does NOT include employer contributions
- Only reflects what employees earned (before taxes)

---

### Total Net Pay (Take-home)
**Definition:** The amount employees actually receive after all deductions.

**Formula:**
```
Total Net Pay = Total Gross Pay - All Deductions (wage types 2000-2999)
```

**Deductions typically include:**
- Federal income tax (wage type 2001)
- State income tax (wage type 2002)
- FICA-OASDI (Social Security) (wage type 2003)
- FICA-Medicare (wage type 2004)
- Health insurance premiums (wage type 2100)
- 401(k) contributions (wage type 2200)
- Other deductions (wage type 2300+)

**Use Case:** Verify total payroll disbursement amount, reconcile to bank transfer

---

### Total Employer Cost (Total Payroll Burden)
**Definition:** The complete cost to the company to employ the workforce for the period.

**Formula:**
```
Total Employer Cost = Total Gross Pay + Employer Contributions (wage types 3000-3999)
```

**Employer contributions typically include:**
- Employer FICA-OASDI (Social Security) (wage type 3001)
- Employer FICA-Medicare (wage type 3002)
- Employer health insurance contribution (wage type 3100)
- Employer 401(k) match (wage type 3200)
- Unemployment insurance (wage type 3300)
- Workers compensation (wage type 3400)

**Use Case:** Full cost accounting, budget planning, cost per FTE analysis

**Benchmark Range (US):** Employer contributions typically add 20-35% to gross pay depending on:
- Industry (healthcare/tech higher)
- Geography (urban vs. rural)
- Benefit generosity (matching, insurance subsidies)

---

## Per-Employee Metrics

### Average Gross Pay Per Employee
**Definition:** Mean gross pay amount across active employees.

**Formula:**
```
Average Gross Pay Per Employee = Total Gross Pay / Active Headcount (FTE)
```

**Use Case:** Analyze compensation levels, identify department salary variations, track salary trends

**Benchmark Range (US):** Varies significantly by industry and role
- Entry-level/operational: $35,000 - $55,000
- Mid-level/professional: $60,000 - $100,000
- Management/specialist: $100,000 - $200,000

---

### Cost Per Employee (Total Burden)
**Definition:** The average total cost to employ one FTE for the period.

**Formula:**
```
Cost Per Employee = Total Employer Cost / Active Headcount (FTE)
```

**Use Case:** Departmental cost comparison, resource planning, budget allocation

**Benchmark Range (US):** Typically 125-135% of average gross pay
- Lower-benefit industries: 120-125%
- High-benefit industries: 135-150%

---

## Tax and Deduction Metrics

### Effective Tax Rate
**Definition:** Percentage of gross pay withheld for all taxes.

**Formula:**
```
Total Tax Withholdings = Federal Tax (2001) + State Tax (2002) + FICA-OASDI (2003) + FICA-Medicare (2004)

Effective Tax Rate = Total Tax Withholdings / Total Gross Pay * 100%
```

**Use Case:** Verify tax calculations, detect over/under withholding, reconcile to tax filing

**Benchmark Range (US):** Varies significantly by state and employee situation
- Federal income tax alone: 12-22% (varies by filing status, dependents)
- FICA-OASDI: 6.2% (flat)
- FICA-Medicare: 1.45% (flat)
- State income tax: 0-5% (varies by state)
- Combined typical range: 20-35% of gross pay

---

### Benefits Load Rate
**Definition:** Percentage of gross pay deducted for voluntary benefits.

**Formula:**
```
Total Benefits Deductions = Health Insurance (2100) + 401k (2200) + Other Benefits (2300+)

Benefits Load Rate = Total Benefits Deductions / Total Gross Pay * 100%
```

**Use Case:** Analyze benefit takeup and participation, budget benefits administration costs

**Benchmark Range (US):** Typically 3-8% of gross pay
- Conservative participation (low enrollment): 2-4%
- High participation (good benefits): 5-8%
- Very generous plans: 8-12%

---

### Tax Expense (Employer Taxes)
**Definition:** Total employer tax obligations.

**Formula:**
```
Employer Tax Expense = Employer FICA-OASDI (3001) + Employer FICA-Medicare (3002) +
                       Unemployment Insurance (3300) + Workers Compensation (3400)
```

**Use Case:** Calculate payroll tax accrual, reconcile to tax payment schedule

**Benchmark Range (US):**
- Employer FICA-OASDI: 6.2% of gross pay
- Employer FICA-Medicare: 1.45% of gross pay
- Unemployment insurance: 0.6-3.4% (varies by state, employer history)
- Workers compensation: 0.5-2% (varies by industry classification)
- Combined typical range: 8-12% of gross pay

---

## Workload and Productivity Metrics

### Overtime Ratio
**Definition:** Percentage of overtime pay relative to regular base pay.

**Formula:**
```
Overtime Pay = Wage Type 1100 (overtime hours * overtime rate)
Regular Base Pay = Wage Type 1000 (basic pay)

Overtime Ratio = Overtime Pay / Regular Base Pay * 100%
```

**Use Case:** Identify understaffing, track operational efficiency, analyze labor cost increases

**Benchmark Range (US):** Varies significantly by industry
- Administrative/office: 0-2% (minimal overtime expected)
- Manufacturing: 2-5% (normal operational variance)
- Retail/operations: 3-8% (seasonal variation)
- 24x7 operations: 5-10% (expected due to shift coverage)

**Red Flag Alert:** Sustained overtime above 10% suggests potential staffing shortage or operational issue.

---

### Bonus and Incentive Payout Ratio
**Definition:** Percentage of gross pay paid as discretionary bonuses/incentives.

**Formula:**
```
Bonus Pay = Wage Type 1200 + Commissions (1300+)

Bonus Ratio = Bonus Pay / Total Gross Pay * 100%
```

**Use Case:** Analyze incentive program costs, forecast discretionary spending, compare departments

**Benchmark Range (US):** Varies significantly by industry and role
- Non-incentive roles: 0% (no bonus expected)
- Sales roles: 10-30% (significant commission/bonus)
- Management: 5-15% (annual bonuses)
- Executive: 20-50% (bonus-heavy compensation)

---

## Headcount Metrics

### Active Headcount (FTE)
**Definition:** Number of active, payrolled employees during the payroll period.

**Calculation:**
- Count unique Employee IDs with wage type 1000 (basic pay) in the period
- Each employee counted once, regardless of hours worked
- Exclude terminated employees (status = "Terminated" or pay date before termination date)

**Use Case:** Staffing analysis, cost per employee, trend tracking

**Notes:**
- FTE = Full-Time Equivalent (treat full-time as 1.0, part-time proportionally)
- If actual hours available, calculate as: FTE = Total Hours Worked / 2080 (annual standard)

---

### New Hire Count
**Definition:** Number of employees with first pay date in the current period.

**Calculation:**
- Identify employees with hire date in payroll period
- Exclude rehires/boomerangs (optional: flag these separately)
- Count each unique employee once

**Use Case:** Staffing trends, hiring rate analysis, onboarding impact on payroll

---

### Termination Count
**Definition:** Number of employees with final pay date in the current period.

**Calculation:**
- Identify employees with termination date in payroll period
- Count severance/final pay separately
- Note involuntary vs. voluntary terminations if available

**Use Case:** Turnover analysis, separation cost impact, workforce planning

---

### Turnover Rate
**Definition:** Percentage of workforce that separated during the period, annualized.

**Formula:**
```
Monthly Turnover Rate = Terminations in Period / Average Active Headcount * 100%

Annualized Turnover Rate = Monthly Turnover Rate * 12
```

**Benchmark Range (US):** Varies significantly by industry
- Professional services: 15-25% annually (expected, market-driven)
- Manufacturing: 20-40% annually
- Retail: 50-100% annually (high seasonal turnover)
- Healthcare: 15-30% annually (varies by role)
- Tech: 10-15% annually (competitive market)

**Interpretation:**
- Below 15% annually: Good retention, stable workforce
- 15-25% annually: Normal market rate for most industries
- Above 35% annually: High turnover, potential culture/compensation issues

---

## Cost Center and Department Metrics

### Cost Per Department
**Definition:** Total payroll cost allocated to a specific department or cost center.

**Formula:**
```
Cost Per Department = SUM(Total Employer Cost) for all employees in that department
```

**Breakdown options:**
- By wage type category (earnings, deductions, contributions)
- By cost center (GL code)
- By department (organizational unit)

**Use Case:** Department budget reconciliation, cost allocation, profitability analysis

---

### Headcount Per Department
**Definition:** Number of active employees in a department.

**Calculation:**
```
Headcount Per Department = COUNT(unique Employee IDs) in department
```

**Use Case:** Departmental staffing analysis, resources planning

---

### Average Salary Per Department
**Definition:** Mean gross pay in a department.

**Formula:**
```
Average Salary Per Department = Total Gross Pay in Department / Headcount in Department
```

**Use Case:** Compensation equity analysis, salary benchmarking across departments

---

## Variance and Trend Metrics

### Period-over-Period Variance
**Definition:** Month-to-month or quarter-to-quarter change in a metric.

**Formula (Absolute):**
```
Absolute Variance = Current Period Amount - Prior Period Amount
```

**Formula (Percentage):**
```
Percentage Variance = (Current Period - Prior Period) / Prior Period * 100%
```

**Use Case:** Trend identification, anomaly detection, forecasting

**Interpretation:**
- Positive variance: Increase (more pay, more headcount, more cost)
- Negative variance: Decrease
- Variance > 5%: Significant change, investigate root cause

---

### Wage Increase / Cost of Living Adjustment (COLA)
**Definition:** Average salary increase from prior period, excluding headcount changes.

**Formula:**
```
COLA = (Current Avg Salary Per Employee - Prior Avg Salary Per Employee) / Prior Avg Salary Per Employee * 100%
```

**Use Case:** Merit increase tracking, inflation impact analysis, budget planning

**Benchmark Range (US):** Typically 2-4% annually
- Below 2%: Below inflation, may affect retention
- 2-3%: Typical market practice
- 3-4%: Generous, above inflation
- Above 4%: Significant increases, budget impact

---

## Data Quality Metrics

### Processing Status Summary
**Definition:** Count of records by processing status.

**Calculation:**
```
Completed Records = COUNT(Status = "Completed")
Pending Records = COUNT(Status = "Pending")
Error Records = COUNT(Status = "Error")
```

**Use Case:** Payroll control validation, exception management, SLA tracking

**Interpretation:**
- 100% Completed: Payroll processed successfully
- Pending records: Still in process, may impact final numbers
- Error records: Manual intervention required, must be resolved before approval

---

### Missing Data Assessment
**Definition:** Count of records or fields with missing required data.

**Check for:**
- Employee ID: Required, unique identifier
- Employee Name: Required for HR records
- Cost Center: Required for GL posting
- Department: Required for reporting
- Wage Type: Required for categorization
- Amount: Should never be null (0 is OK if intentional)
- Pay Date: Required for period identification

**Use Case:** Data quality validation, exception reporting, control testing

---

## Reference Tables

### US Wage Type Convention Summary
| Range | Category | Purpose | Examples |
|-------|----------|---------|----------|
| 1000-1999 | Earnings | Employee compensation | Basic pay, overtime, bonus, commission |
| 2000-2999 | Deductions | Taxes and benefits withheld | Federal tax, FICA, health insurance, 401k |
| 3000-3999 | Employer Contributions | Employer-paid benefits and taxes | Employer FICA, health insurance, 401k match |
| 4000+ | Informational | Reference data, benefit status | FTE counts, benefit eligibility, status flags |

---

### Cost Center Naming Convention
Typical SAP payroll cost center structure:
```
41XX = Sales (4100-4199)
42XX = Marketing (4200-4299)
43XX = Operations (4300-4399)
44XX = Administration (4400-4499)
45XX = Finance (4500-4599)
```

(Varies by organization; refer to company GL chart of accounts)

---

### Department Code Summary
Common department codes in payroll:
```
100 = Sales
200 = Operations/Manufacturing
300 = Administration/Finance
400 = HR/People Operations
500 = IT/Technology
600 = Marketing
700 = Customer Success/Support
```

(Varies by organization; refer to org chart or HRIS records)

---

## Benchmark Interpretation Guide

When reviewing metrics against benchmarks:

1. **Industry Context:** Manufacturing, healthcare, and tech have different norms
2. **Company Size:** Large enterprises vs. startups have different cost structures
3. **Geographic Variation:** Cost of living varies significantly by region
4. **Historical Trend:** Your own 3-month or 12-month average is the best benchmark
5. **Business Cycle:** Seasonal or cyclical industries have normal variance

**Always compare:**
- Current period to prior period (trend)
- Current period to budget (forecast accuracy)
- Your metrics to industry peers (competitive position)
- Department A to Department B (internal equity)
