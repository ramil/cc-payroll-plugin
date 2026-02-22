# Pre-Submission Validation Checklist

## Overview

This checklist aims to help verify that payroll data is complete, accurate, and compliant before submission to banks, tax authorities, and other external parties. Use this guide in conjunction with the `validate_payroll.py` script for pre-submission validation.

## Data Completeness Requirements

### Employee Master Data
- **Employee ID**: Required, unique, matches SAP employee master (PA30)
  - Must be valid SAP personnel number
  - Cannot be blank or zero
  - Check for consistency across all records in the period

- **Employee Name**: Required, matches SAP master data
  - Must match exactly as in HR system
  - Full legal name required for tax reporting
  - Check for special characters that may cause system issues

- **Employment Status**: Required
  - Active, On Leave, Terminated
  - Must be current as of payroll period end
  - Verify HR records for status changes mid-period

- **Cost Center**: Required, valid per SAP configuration
  - Must be assigned to valid cost center (transaction OKUN)
  - Used for expense allocation and analysis
  - Cannot be blank; escalate issues to cost center owner

- **Department Code**: Recommended (8 checks require this)
  - Used for organizational reporting
  - Should correspond to SAP organizational units
  - Verify alignment with cost center assignments

- **Payroll Area**: Required
  - Must be valid per payroll configuration (transaction SPKA)
  - Typically US, US-CA, US-NY, etc. for regional variations
  - Determines tax and regulatory compliance rules

- **Wage Type**: Required, valid per SAP wage type master
  - Standard wage types: 1000 (Regular), 1010 (Overtime)
  - Deduction types: /101 (Federal Tax), /102 (State Tax), /110 (FICA SS), /111 (FICA Medicare)
  - Non-recurring: /201 (Bonus), /301 (Expense Reimbursement), /401 (401k), /402 (Health Insurance), /403 (FSA)
  - Leave: /501 (Vacation), /502 (Sick)
  - Verify wage type is configured in wage type master (PE03)

### Compensation Data
- **Gross Pay Amount**: Required, must be numeric
  - Must be positive or zero (no negative gross pay)
  - Represents total compensation before deductions
  - Validate against employee's salary/hourly rate
  - Cross-check against time and attendance records

- **Regular Rate**: Required for overtime calculations
  - Used to calculate overtime at 1.5x (FLSA requirement)
  - Must match company compensation plan
  - Verify consistency month-to-month

- **Overtime Hours/Amount**: Required if applicable
  - Overtime must be 1.5x regular rate minimum per FLSA
  - Common issues: Missing overtime records, incorrect overtime rates
  - Validate against timekeeping system

- **Shift Differentials**: Document by wage type
  - Evening/Night/Weekend premiums
  - Must be properly coded in wage type master
  - Verify per union agreements or company policy

## Calculation Accuracy Verification Steps

### Gross Pay Validation
1. **Verify base compensation**
   - Regular pay = Hours * Hourly Rate (or Salary / Days Paid)
   - Overtime pay = Overtime Hours * (Hourly Rate * 1.5)
   - Commission = Per sales agreement
   - Bonus = Per plan documentation

2. **Check mathematical accuracy**
   - Sum of wage type amounts = Total gross pay
   - No rounding errors > $0.01
   - Overtime rates are exactly 1.5x (not 1.25x or 1.75x)

3. **Validate against prior periods**
   - Month-to-month consistency
   - Watch for unexplained increases/decreases
   - Flag unusual patterns for investigation

### Tax Withholding Validation
1. **Federal Income Tax**
   - Verify W-4 on file and current (update every 3 years)
   - Check for allowances that might affect withholding
   - Validate against IRS Publication 15-T tables
   - Confirm estimated annual federal tax liability

2. **Social Security Tax (FICA - 6.2%)**
   - Calculation: Gross Pay × 6.2% (employee portion)
   - But: Do NOT withhold on wages over $176,100 annual limit
   - Verify wage base tracking (transaction PUMB)
   - Check for mid-year limit adjustments

3. **Medicare Tax (FICA - 1.45%)**
   - Calculation: Gross Pay × 1.45% (employee portion)
   - Additional Medicare (0.9%) applies to income over $200,000
   - No annual wage base limit; continues year-round
   - Verify employee has confirmed Additional Medicare withholding if applicable

4. **State Income Tax**
   - Varies significantly by state and payroll area
   - Verify employee is assigned to correct state
   - Check for multiple state work (multistate resident)
   - Confirm local taxes where applicable (Pittsburgh, Columbus, etc.)

5. **Local Taxes**
   - Some cities/counties require additional withholding
   - Examples: DC, Pittsburgh, Columbus, Philadelphia
   - Verify employee residence matches payroll area code

### Deduction Validation
1. **Pre-tax Deductions** (reduce taxable wages)
   - 401(k) contributions - verify not exceeding annual limit ($24,500 in 2025)
   - Health insurance premiums - check plan elections
   - FSA contributions - verify annual limit ($3,300 in 2025)
   - Parking/transit benefits
   - All must be verified against benefit enrollment

2. **Post-tax Deductions** (do not reduce taxable wages)
   - Roth 401(k) - separate from traditional 401(k) limit
   - Garnishments - verify court orders
   - Overpayment repayments
   - Charitable donations
   - Verify supporting documentation on file

3. **Deduction Reasonableness**
   - No single deduction exceeds 50% of gross pay (except garnishment)
   - Pre-tax deductions don't create net pay below minimum wage
   - All deductions have valid authorization forms on file
   - Terminating benefits properly coded (last pay period)

### Net Pay Validation
1. **Net Pay Calculation**
   - Net Pay = Gross Pay - All Withholdings - All Deductions
   - Net Pay must be positive or zero
   - Net Pay must NOT exceed Gross Pay
   - Verify net matches actual payment

2. **Reasonableness Check**
   - Net pay should be 60-75% of gross pay typically
   - Unusually low net pay: Review deductions and withholding
   - Unusually high net pay: Verify all taxes/deductions applied

## Wage Base Limit Reference

### Social Security Wage Base (2025)
- **Annual Limit**: $176,100
- **Employee Rate**: 6.2% (up to limit)
- **Employer Rate**: 6.2% (up to limit)
- **Deadline**: Must stop withholding/paying when limit exceeded
- **Tracking**: Transaction PUMB shows YTD earnings by employee
- **Common Error**: Continuing to withhold after limit exceeded

### FUTA (Federal Unemployment) Wage Base (2025)
- **Annual Limit**: $7,000 per employee
- **Employer Tax Rate**: 0.6% (federal), varies by state (0.5-3.0%)
- **Calculation**: $7,000 × employer rate = FUTA tax per employee
- **Deadline**: Must stop accrual after $7,000 in annual wages
- **Tracking**: Verify in quarterly 940 reconciliation

### SUTA (State Unemployment Insurance) Wage Base
- **Varies by State**:
  - Most states: $7,000-$10,000 annual limit
  - California: $10,000
  - New York: $11,800
  - Texas: $9,000
  - Illinois: $12,240
  - Florida: $10,500
- **Verification**: Check state-specific requirements in compliance calendar

### Additional Medicare Tax Threshold (2025)
- **Threshold**: $200,000 for single filers ($250,000 married filing jointly, $125,000 married filing separately)
- **Rate**: Additional 0.9% beyond threshold
- **Employee Tax**: Employer withholds 0.9% on excess
- **Employer Tax**: Employer pays 0.9% (only if employee is above threshold)
- **Verification**: Confirm Additional Medicare elections on W-4 form

### State-Specific Wage Base Limits
| State | SUI Base | State Tax Rate | Notes |
|-------|----------|----------------|-------|
| California | $10,000 | 3.5% (avg) | Employer only; no employee tax |
| New York | $11,800 | 6.85% (avg) | Employer only; no employee tax |
| Texas | $9,000 | 0.42-0.80% | Employer only |
| Florida | $10,500 | 0.27-6.33% | Employer only |
| Illinois | $12,240 | 0.38-7.5% | Employer only |
| Pennsylvania | $10,500 | 3.7% avg | Employer only; employee rate varies by statute |
| Ohio | $9,000 | 0.24-10.0% | Employer only |

**Action**: Verify state-specific rates and bases for your payroll areas in transaction SPKA configuration.

## Prior Period Comparison Methodology

### Total Payroll Variance Analysis
1. **Calculation**: (Current Payroll - Prior Payroll) / Prior Payroll × 100%
2. **Flag Threshold**: >10% variance
3. **Investigation Steps**:
   - Review headcount changes (new hires, terminations)
   - Analyze merit increases or cost-of-living adjustments (COLA)
   - Check for one-time bonuses or lump-sum payments
   - Verify shift/premium changes
   - Reconcile against budgeted payroll

4. **Documentation**: Document business reason for variance
   - Budget variance explanation
   - Approval of unbudgeted increases
   - Impact analysis on annual payroll

### Headcount Change Analysis
1. **Calculation**: (Current HC - Prior HC) / Prior HC × 100%
2. **Flag Threshold**: >5% change in headcount
3. **Verification Steps**:
   - New hires: Verify start dates, offer letters, I-9 forms
   - Terminations: Verify last pay date, final check, COBRA notifications
   - Leave of absence: Ensure proper status coding
   - Transfers: Verify department/cost center changes

4. **Reconciliation**: Match against:
   - HR hire/termination records
   - Headcount reports from HR system
   - Benefits enrollment system

### Average Pay Variance Analysis
1. **Calculation**: (Current Avg - Prior Avg) / Prior Avg × 100%
2. **Flag Threshold**: >15% change in average pay
3. **Investigation**:
   - Merit increase cycles
   - Change in pay mix (salary vs hourly)
   - Bonus or incentive payouts
   - Overtime increases/decreases
   - Shift/premium changes

4. **By Employee Level**:
   - Compare salaried vs hourly separately
   - By department to identify targeted increases
   - By job level/grade

### Anomaly Investigation
1. **New Employees in Current Period**
   - Verify employment start date
   - Check pro-rata pay calculation accuracy
   - Validate benefit eligibility (3-month probation?)
   - Confirm tax withholding setup

2. **Terminated Employees Not in Current Period**
   - Verify separation date matches last pay period
   - Check final pay including accrued PTO
   - Confirm benefits termination (COBRA election)
   - Validate tax forms (W-2 vs 1099)

3. **Employees with Significant Pay Changes**
   - >20% increase: Merit increase? Promotion? Bonus?
   - >20% decrease: Demotion? Furlough? Return from leave?
   - Zero pay: Unpaid leave? Termination? Error?

## Common Errors and How to Catch Them

### Data Entry Errors
| Error | How to Catch | Prevention |
|-------|-------------|-----------|
| Transposed digits (1234 vs 1243) | Compare to prior period; flag unusual amounts | Use dropdown lists for codes; prevent free text |
| Missing leading zeros in codes | Validate code format; format as text not number | Template with correct formats |
| Duplicate records for same employee | Sort by employee ID; check for duplicates | Unique constraint in payroll system |
| Wrong employee ID | Verify name matches ID; use VLOOKUP | Employee ID dropdown or master data lookup |
| Extra spaces in fields | Use TRIM function in Excel; validate in system | Clean data before import |

### Calculation Errors
| Error | How to Catch | Prevention |
|-------|-------------|-----------|
| Overtime calculated at 1.25x instead of 1.5x | Review OT amount formula; compare to hours * rate * 1.5 | System calculation; formula validation |
| Tax withheld before wage base limit | Check YTD; verify limit applied | Wage base tracking in transaction PUMB |
| Deductions exceed gross pay | Review net pay; highlight if net < 0 | Deduction validation rules in system |
| Rounding errors accumulate | Check for amounts with 3+ decimal places | System should round to $0.01 only |
| Hours entered as decimal instead of hours:minutes | Review hourly rate calculation; validate hours reasonable | Time system exports in consistent format |

### Compliance Errors
| Error | How to Catch | Prevention |
|-------|-------------|-----------|
| Minimum wage violation | Calculate hourly rate; verify against state/federal minimum | Payroll validation; state minimum wage table |
| Garnishment exceeds 25% | Calculate: Garnishment / Gross Pay; flag if > 25% | System garnishment limit enforcement |
| Tax withholding missing | Check all employees have W-4 on file; verify withholding codes | Payroll audit; required field validation |
| Cost center missing | Sort by cost center; highlight blanks | Cost center mandatory in PA30 |
| Employee in wrong payroll area | Review state residence vs. payroll area code | Employee master data validation |

### Anomaly Errors
| Error | How to Catch | Prevention |
|-------|-------------|-----------|
| Unusually high payment | Sort by amount; investigate outliers | Compare to prior year; flag >3 std dev |
| Duplicate payment | Review daily bank reconciliation; check duplicate detection | System duplicate checking; approval workflow |
| Zero-amount records | Filter for $0 gross pay; investigate each | Require explanation for zero-pay records |
| Negative amounts | Review all deduction codes; ensure correct sign | Deduction code validation |

## SAP Transactions for Data Corrections

### Employee Master Corrections
| Transaction | Purpose | When to Use |
|-------------|---------|------------|
| **PA30** | Maintain employee master data | Update name, address, employment status, cost center, payroll area |
| **PA32** | Maintain employee organizational assignment | Update department, cost center, organizational unit |
| **PA20** | Display employee master data history | Review prior changes; audit trail |
| **PA03** | Maintain employee infotype data | Update specific infotype records (dates, amounts) |

### Payroll Configuration Corrections
| Transaction | Purpose | When to Use |
|-------------|---------|------------|
| **PE03** | Maintain wage type master | Update wage type rates, calculation rules, tax classification |
| **PU03** | Maintain wage type assignments to employees | Assign/remove wage types for specific employee groups |
| **PUMB** | Display payroll balances/YTD values | Review wage base tracking, YTD earnings by employee |
| **SPKA** | Maintain payroll area | Configure payroll area definitions, wage base limits, calendar |
| **PC03** | Maintain payroll constant | Update tax rates, wage base limits annually (e.g., SS base $176,100) |
| **OKUN** | Maintain cost centers | Validate and update cost center master data |
| **ORGA** | Maintain organizational structure | Verify organizational unit hierarchy |

### Validation and Testing
| Transaction | Purpose | When to Use |
|-------------|---------|------------|
| **PC77** | Test payroll results | Verify payroll run output before posting |
| **ECATT** | Execute automated test cases | Regression testing after configuration changes |
| **SM30** | Table maintenance | Directly edit configuration tables (use with caution) |
| **SM34** | Maintain table views | Edit payroll master data tables |

## Pre-Submission Sign-Off Checklist

### Data Completeness Review (Preparer)
- [ ] All employees have valid, unique employee IDs
- [ ] All employee names match HR master data
- [ ] All employees assigned to valid cost center
- [ ] All employees assigned to valid payroll area
- [ ] All wage types are valid and configured
- [ ] No blank gross pay amounts (except unpaid leave with documentation)
- [ ] No duplicate employee records in payroll

### Calculation Accuracy Review (Reviewer)
- [ ] Gross pay calculations are mathematically correct
- [ ] Overtime calculated at 1.5x regular rate
- [ ] No negative gross pay or net pay > gross pay
- [ ] Tax withholding rates correct (6.2% SS, 1.45% Med, per W-4 federal)
- [ ] Wage base limits applied correctly (SS $176,100 limit, FUTA $7,000, Additional Medicare $200,000)
- [ ] Garnishments do not exceed 25% of gross pay
- [ ] All deductions have valid authorization on file

### Compliance Review (Approver)
- [ ] All employees meet applicable minimum wage requirements
- [ ] Tax deposits will meet regulatory deadlines
- [ ] No employees in violation of FLSA overtime requirements
- [ ] All required tax forms (W-4, I-9) are current and on file
- [ ] Payroll amount is within 10% of prior period (or documented variance approved)
- [ ] Headcount changes reconciled to HR records
- [ ] Prior period comparison anomalies investigated and documented
- [ ] Critical findings resolved before processing
- [ ] Overall risk score acceptable (target: <40 for processing, <20 for minimal review)

---

**Document Version**: 1.0 | **Last Updated**: February 2025 | **Classification**: Internal Use Only
