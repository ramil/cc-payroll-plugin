# Payroll Risk Assessment Framework

## Overview

The Payroll Risk Assessment Framework provides a structured methodology for evaluating payroll compliance risk on a 0-100 scale. This framework guides validation prioritization, escalation decisions, and resource allocation for payroll compliance activities. Risk assessments inform whether payroll can be processed, whether management review is required, and what remediation actions are necessary.

---

## Risk Scoring Methodology

### Score Components

The overall risk score is calculated from six validation categories, each weighted based on business impact:

| Category | Weight | Description | Score Range |
|----------|--------|-------------|-------------|
| **Data Completeness** | 20% | All required fields populated | 0-100 |
| **Calculation Accuracy** | 25% | Mathematical correctness of wages/taxes | 0-100 |
| **Wage Base Limits** | 15% | Compliance with annual/quarterly limits | 0-100 |
| **Prior Period Comparison** | 15% | Anomaly detection vs. prior periods | 0-100 |
| **Compliance Rules** | 15% | Regulatory and policy compliance | 0-100 |
| **Anomaly Detection** | 10% | Fraud/error detection patterns | 0-100 |

**Formula**:
```
Risk Score = (DataCompleteness×20 + CalcAccuracy×25 + WageBase×15 +
              PriorPeriod×15 + ComplianceRules×15 + AnomalyDetection×10) / 100
```

Each category score (0-100) is calculated from individual check results, weighted by severity:

### Severity-Based Weighting

| Severity | Weight | Points | Meaning |
|----------|--------|--------|---------|
| **Critical** | 100 | 25 points each | System-blocking issue; prevents processing |
| **High** | 50 | 12.5 points each | Major compliance issue; requires remediation |
| **Medium** | 20 | 5 points each | Moderate risk; address before processing |
| **Low** | 5 | 1.25 points each | Minor issue; monitor and document |

**Example Calculation**:
```
Category: Data Completeness (8 checks)
- Missing Employee IDs: FAIL (Critical, 2 employees affected) = 2 × 25 = 50 points
- Missing Names: PASS = 0 points
- Blank Gross Pay: FAIL (Critical, 1 employee) = 1 × 25 = 25 points
- Missing Cost Center: FAIL (High, 3 employees) = 3 × 12.5 = 37.5 points
- Missing Wage Type: PASS = 0 points
- Missing Department: FAIL (Medium, 2 employees) = 2 × 5 = 10 points
- Missing Payroll Area: PASS = 0 points
- Duplicate Records: FAIL (High, 1 duplicate) = 1 × 12.5 = 12.5 points

Total Category Points: 135 points
Normalized (0-100): (135 / 200 max points) × 100 = 67.5 → Category Score: 67 (High Risk)
```

---

## Risk Level Classification

### Overall Risk Score Interpretation

| Score | Risk Level | Description | Action | Process? |
|-------|----------|-------------|--------|----------|
| **0-20** | **Low Risk** | All checks pass; minimal findings; safe to process | Approve for processing | YES |
| **21-40** | **Medium Risk** | Some findings; remediation recommended before processing | Review and remediate | Conditional |
| **41-60** | **High Risk** | Multiple issues or critical findings; requires mgmt review | Management approval required | NO |
| **61-80** | **Very High Risk** | Significant compliance issues; escalate immediately | Director/VP approval | NO |
| **81-100** | **Critical Risk** | Severe violations or multiple critical findings | STOP processing; investigate | NO |

### Processing Decision Tree

```
Risk Score ≤ 20?
├─ YES → "Low Risk" → Standard approval → Process payroll
├─ NO → Risk Score ≤ 40?
│   ├─ YES → "Medium Risk" → Review findings
│   │   ├─ Remediate all HIGH/CRITICAL items
│   │   ├─ Revalidate with remediated data
│   │   ├─ Document exceptions/approvals
│   │   └─ Process if corrected score ≤ 20
│   ├─ NO → Risk Score ≤ 60?
│   │   ├─ YES → "High Risk" → Management review required
│   │   │   ├─ Finance Manager reviews all findings
│   │   │   ├─ Determines if remediation or exception approval
│   │   │   ├─ If manageable: Remediate and revalidate
│   │   │   └─ If approved exception: Document authorization
│   │   ├─ NO → Risk Score ≤ 80?
│   │   │   ├─ YES → "Very High Risk" → Director approval required
│   │   │   │   ├─ VP/Director reviews and must approve in writing
│   │   │   │   ├─ Investigation of root cause required
│   │   │   │   ├─ Remediation plan documented
│   │   │   │   └─ Enhanced controls/monitoring during processing
│   │   │   ├─ NO → "Critical Risk" → STOP - Do not process
│   │   │   │   ├─ Escalate to CFO immediately
│   │   │   │   ├─ Conduct thorough investigation
│   │   │   │   ├─ Complete remediation required
│   │   │   │   ├─ Revalidate with cleaned data
│   │   │   │   └─ Process only after approval from CFO
```

---

## Category-Specific Risk Profiles

### Data Completeness (Weight: 20%)

**Definition**: All required employee, compensation, and organizational data is populated.

**Risk Profile**:
- **High Risk**: Missing core data elements (employee ID, gross pay, cost center)
- **Medium Risk**: Missing secondary data (department, payroll area)
- **Low Risk**: All mandatory fields populated; minor data quality issues

**Sample Checks** (8 total):
1. Missing employee IDs (Critical)
2. Missing employee names (Critical)
3. Blank gross pay amounts (Critical)
4. Missing cost center (High)
5. Missing wage type (High)
6. Missing department (Medium)
7. Missing payroll area (Medium)
8. Duplicate records (High)

**Business Impact**:
- Missing core data prevents system processing
- Duplicate records cause overpayment or confusion
- Cost center missing prevents accurate allocation to GL
- Missing wage type prevents correct tax/deduction coding

**Typical Findings**:
- 95% of payroll data complete (3-5 minor issues) = Low Risk
- 90% complete (5-10 issues including 1-2 critical) = Medium Risk
- 85% complete (>10 issues or >2 critical items) = High Risk

---

### Calculation Accuracy (Weight: 25%)

**Definition**: Payroll calculations (gross, taxes, deductions, net) are mathematically correct.

**Risk Profile**:
- **Critical Risk**: Net pay > gross pay; negative gross pay; tax > gross pay
- **High Risk**: Overtime incorrect rate; wage base limits violated; garnishment > 25%
- **Medium Risk**: Rounding errors; minor deduction issues
- **Low Risk**: All calculations verified and correct

**Sample Checks** (6 total):
1. Negative gross pay (Critical)
2. Net pay > gross pay (Critical)
3. Tax withholding > gross pay (Critical)
4. Overtime rate validation (High)
5. FICA calculation (6.2% SS, 1.45% Med) (High)
6. Garnishment limit (≤25%) (High)

**Business Impact**:
- Calculation errors result in overpayment/underpayment
- Incorrect tax withholding creates IRS liability
- Wage base limit violations cause duplicate taxation
- Garnishment over-collection violates consumer protection law (CCPA)

**Typical Findings**:
- All calculations verified (automated validation or manual review) = Low Risk
- 1-2 minor errors (rounding, one employee affected) = Medium Risk
- Multiple calculation errors or >5 employees affected = High Risk
- Critical errors (net > gross, negative pay) on any employee = Critical Risk

---

### Wage Base Limits (Weight: 15%)

**Definition**: Annual and per-period wage base limits are applied correctly for all payroll taxes.

**Risk Profile**:
- **Critical Risk**: Multiple employees exceeding SS base; systematic limit violations
- **High Risk**: 1-3 employees exceeding SS base; FUTA limit exceeded
- **Medium Risk**: Isolated limit violations; properly documented and corrected
- **Low Risk**: All wage base limits verified and applied correctly

**Sample Checks** (4 total):
1. Social Security wage base ($176,100 annual 2025) (High)
2. FUTA wage base ($7,000 annual) (Medium)
3. Additional Medicare threshold ($200,000 income) (Medium)
4. State SUI limits (varies by state) (Medium)

**Wage Base Limits Reference**:
| Tax | Annual Limit (2025) | Rate | Notes |
|-----|-------------------|------|-------|
| **Social Security** | $176,100 | 6.2% (employee) / 6.2% (employer) | Stop withholding when limit reached |
| **Medicare** | None | 1.45% (employee) / 1.45% (employer) | Continues throughout year |
| **Additional Medicare** | Over $200,000 | 0.9% (employee only) | Applies to high-income earners |
| **FUTA** | $7,000 | 0.6% (employer only) | Stop accrual when limit reached |
| **State SUI** | Varies | Varies | CA: $10,000; NY: $11,800; TX: $9,000; FL: $10,500; IL: $12,240 |

**Business Impact**:
- Continuing withholding after SS base reached results in overcollection
- Failure to stop withholding creates employee refund obligation
- FUTA over-accrual creates employer tax overpayment
- State SUI violations subject to state penalties

**Typical Findings**:
- All limits applied correctly; verified through YTD tracking = Low Risk
- 1-2 employees near limit; proper handling documented = Low Risk
- 1-2 employees exceeding limit with remediation plan = Medium Risk
- Multiple employees exceeding limit undetected = High Risk
- Systematic failure to apply limits = Critical Risk

---

### Prior Period Comparison (Weight: 15%)

**Definition**: Current period payroll is compared to prior periods to detect anomalies, trends, and potential errors.

**Risk Profile**:
- **High Risk**: >10% payroll variance; >5% headcount change; unexplained changes
- **Medium Risk**: 5-10% payroll variance; 2-5% headcount change; documented variance
- **Low Risk**: <5% variance; consistent month-to-month; documented changes

**Sample Checks** (5 total):
1. Total payroll variance >10% (High)
2. Headcount change >5% (Medium)
3. Average pay variance >15% (Medium)
4. New employee validation (Low)
5. Terminated employee validation (Low)

**Variance Thresholds**:
| Metric | Green (<) | Yellow (5-10%) | Red (>10%) |
|--------|-----------|----------------|-----------|
| **Payroll Variance** | 5% | 5-10% | 10%+ |
| **Headcount Change** | 2% | 2-5% | 5%+ |
| **Average Pay Change** | 5% | 5-15% | 15%+ |

**Business Impact**:
- Large unexplained variances may indicate missing data or calculation errors
- Headcount anomalies warrant reconciliation to HR records
- Pay variances require documentation of merit increases, bonuses, organizational changes
- Unvalidated new/terminated employees create data inconsistency

**Typical Findings**:
- Payroll consistent month-to-month; documented changes explained = Low Risk
- Variance within expected range; properly documented = Low Risk
- Variance 5-10%; explanation provided and validated = Medium Risk
- Variance >10% without adequate explanation = High Risk
- Multiple unexplained variances across categories = High Risk

---

### Compliance Rules (Weight: 15%)

**Definition**: Payroll compliance with federal/state regulations and company policies.

**Risk Profile**:
- **Critical Risk**: Minimum wage violations; tax withholding incomplete
- **High Risk**: Garnishment priority violations; excessive deductions
- **Medium Risk**: Cost center assignment issues; compliance documentation gaps
- **Low Risk**: All compliance requirements met; documentation complete

**Sample Checks** (5 total):
1. Minimum wage compliance ($7.25 federal) (High)
2. Garnishment priority ordering (Medium)
3. Benefit deductions minimum wage safeguard (High)
4. Tax withholding completeness (High)
5. Cost center assignment completeness (Medium)

**Regulatory Landscape**:
| Regulation | Requirement | Penalty |
|-----------|-----------|---------|
| **FLSA** | Minimum wage $7.25; overtime 1.5x | Back wages + penalties |
| **CCPA** | Garnishment priority; 25% max | Contempt of court; back wages |
| **IRS** | Tax withholding; W-4 on file | Employer liability for under-withholding |
| **State Labor** | State minimum wage (varies) | Back wages + penalties |
| **Internal Controls** | SOX segregation of duties | Audit deficiency or weakness |

**Business Impact**:
- Minimum wage violations create liability for back wages + penalties (up to 3 years)
- Improper garnishment ordering violates CCPA; subject to court action
- Missing tax withholding creates IRS compliance issues and penalties
- SOX control deficiencies impact financial reporting certification

**Typical Findings**:
- All employees above minimum wage; proper tax withholding; SOX controls in place = Low Risk
- 1-2 employees near minimum after deductions; corrected promptly = Medium Risk
- Multiple minimum wage violations; incomplete tax withholding = High Risk
- Systematic compliance failures across multiple requirements = Critical Risk

---

### Anomaly Detection (Weight: 10%)

**Definition**: Statistical outlier detection for individual transactions that may indicate errors or fraud.

**Risk Profile**:
- **High Risk**: Unusual payments >3 standard deviations; duplicate payments
- **Medium Risk**: Zero-amount records; negative deductions without documentation
- **Low Risk**: Normal transaction distribution; explained anomalies

**Sample Checks** (4 total):
1. Unusually high payments (>3 std dev) (High)
2. Duplicate payments same employee/type (High)
3. Zero-amount records (Medium)
4. Negative deduction amounts (Medium)

**Statistical Methodology**:
- Calculate mean gross pay: Sum(Gross Pay) / Count
- Calculate standard deviation: sqrt(Sum((Pay-Mean)²) / Count)
- Flag threshold: Mean + (3 × StdDev)
- Automated detection via `validate_payroll.py` script

**Example**:
```
50 employees with average gross pay of $2,500 (std dev $500)
Threshold = $2,500 + (3 × $500) = $4,000
Any employee with gross pay >$4,000 flagged for review
```

**Business Impact**:
- Unusual payments may indicate data entry errors or system bugs
- Duplicates result in overpayment and bank/employee issues
- Zero-amount records may indicate termination errors or system issues
- Negative deductions may indicate credit/refund processing errors

**Typical Findings**:
- No statistical outliers; normal distribution of pay = Low Risk
- 1-2 outliers with documented business reason (bonus, commission) = Low Risk
- Multiple outliers; 1-2 duplicates; limited documentation = Medium Risk
- Many outliers; numerous duplicates; unclear business purpose = High Risk
- Systematic fraud indicators (many duplicates, organized pattern) = Critical Risk

---

## Risk Appetite and Decision Framework

Organizations must define their risk appetite - the level of risk they are willing to accept in payroll processing. This guides management decisions on processing conditions.

### Risk Appetite Profiles

#### Profile 1: Conservative (Financial Services, Healthcare, Government)
- **Target Risk Score**: <20 (Low Risk)
- **Processing Condition**: Automatic approval only if score <20
- **Management Review**: Required if score >15
- **Processing Threshold**: Score must be <40 for any processing; VP approval required
- **Philosophy**: Payroll accuracy is paramount; processing delays are acceptable
- **Typical**: Companies with significant audit/compliance requirements

#### Profile 2: Moderate (Manufacturing, Retail, Services)
- **Target Risk Score**: <40 (Medium Risk)
- **Processing Condition**: Approval at score <30; additional review 30-50; no processing >50
- **Management Review**: Required if score >30
- **Processing Threshold**: Score must be <50; Finance Manager approval required
- **Philosophy**: Balance accuracy with operational efficiency
- **Typical**: Most mid-sized companies

#### Profile 3: Aggressive (Early-stage, Fast-growing)
- **Target Risk Score**: <60 (High Risk)
- **Processing Condition**: Approval if score <40; Director review 40-60; VP review >60
- **Management Review**: Required only if score >40
- **Processing Threshold**: Score must be <70; VP approval required
- **Philosophy**: Prioritize operational speed; accept higher audit risk
- **Caveat**: Not recommended; higher penalty/audit exposure

### Decision Matrix

| Risk Score | Conservative | Moderate | Aggressive |
|-----------|--------------|----------|-----------|
| 0-20 | Process | Process | Process |
| 21-40 | Mgr Review | Process | Process |
| 41-60 | VP Approval | Mgr Review | Process |
| 61-80 | Director Approval | VP Approval | Mgr Review |
| 81+ | Do Not Process | Do Not Process | Director Approval |

**Recommendation**: Adopt Moderate risk appetite (target <40 processing threshold)

---

## Escalation Triggers and Thresholds

Escalation supports appropriate management visibility and approval for high-risk payroll.

### Escalation Matrix

| Finding | Threshold | Escalate To | Action | Timeline |
|---------|-----------|-------------|--------|----------|
| **Risk Score** | >40 | Finance Manager | Review findings | Before processing |
| **Risk Score** | >60 | VP Finance | Approve in writing | Before processing |
| **Risk Score** | >80 | CFO | Investigate + remediate | Before processing |
| **Critical Findings** | 1+ | Finance Manager | Resolve before processing | Before processing |
| **Employees with Issues** | >20% | Mgr + Auditor | Root cause analysis | Within 24 hrs |
| **Calculation Errors** | >$10,000 impact | Finance Manager | Review and approve | Before processing |
| **Regulatory Violation** | Any | Compliance/Legal | Assess exposure | Within 24 hrs |
| **SOX Control Failure** | Any | Internal Audit | Document deficiency | Within 48 hrs |

### Escalation Approval Matrix

| Escalation Level | Authority | Approval | Documentation |
|-----------------|-----------|----------|----------------|
| **Manager Level** (Risk >40) | Payroll Manager | Email approval with findings addressed | Forward to CFO |
| **Finance Manager Level** (Risk >60) | Finance Manager | Formal approval memo | Attach to payroll package |
| **VP Level** (Risk >70) | VP Finance | Written approval + risk assessment | Board/Audit Committee notification |
| **CFO Level** (Risk >80) | Chief Financial Officer | Executive approval + remediation plan | Legal/Audit review |

---

## Common Violation Penalties

Understanding potential penalties for compliance failures informs risk prioritization.

### Federal Penalties

| Violation | Statute | Penalty | Multiplier | Total Risk |
|----------|---------|---------|-----------|-----------|
| **Late payroll tax deposit** | IRC §6656 | 2% (1-5 days) / 5% (6-15 days) / 10% (>15 days) | Days late | 2-15% of tax |
| **Incorrect W-2** | IRC §6721 | $50-$100 per form | Count of forms | $5K-$50K per year |
| **Late W-2 filing** | IRC §6721 | $50-$100 per form | Count × months late | Up to $300/form |
| **Form 941 underreport** | IRC §6651 | 5% per month unpaid | Months late | 5-25% of tax |
| **FLSA minimum wage violation** | FLSA §206 | Back wages + penalties | 3-year lookback | $10K-$100K+ |
| **FLSA overtime violation** | FLSA §207 | Back wages + 50% penalty | 3-year lookback | $20K-$200K+ |
| **Willful failure to withhold tax** | IRC §6682 | 75% of unpaid tax + penalties | Criminal | Imprisonment + fines |

### State Penalties (Examples)

| Violation | State | Penalty | Notes |
|----------|-------|---------|-------|
| **Late SUI deposit** | CA/NY/TX | 5-10% per month | Varies by state |
| **Late unemployment filing** | All states | $50-$500 per month | State-specific rates |
| **Failure to provide W-2** | CA | $10-$50 per form | California penalty |
| **Wage statement violations** | CA | $50-$150 per pay period | Labor Code §200 |
| **Independent contractor misclass** | CA/NY | Back wages + penalties + treble damages | Potential class action |

### Estimated Total Risk Exposure

Example for 50-employee payroll with compliance violations:
- **Late tax deposit** (1 month): 5% × $150,000 = $7,500
- **Incorrect W-2 wage** (20 employees): $100 × 20 = $2,000
- **FLSA minimum wage** (3 employees, 6 months): $4,000 back wages + 50% = $6,000
- **State SUI underreporting** (1 quarter): $5,000
- **Interest and penalties** (estimated): $8,000
- **Total Exposure**: ~$28,500+

**Risk Mitigation**: Pre-submission validation (risk score <40) prevents most penalties through early detection and remediation.

---

## Best Practices for Risk Management

1. **Establish baseline**: Run validation on 3 prior months; document typical risk patterns
2. **Set thresholds**: Define acceptance criteria per risk appetite profile
3. **Automate validation**: Run `validate_payroll.py` on every payroll before processing
4. **Escalate promptly**: Notify management immediately of risk score >40
5. **Document decisions**: Record approval decisions and business justifications
6. **Trend analysis**: Track risk scores month-to-month; identify patterns
7. **Root cause analysis**: When issues occur, investigate cause and implement preventive control
8. **Audit compliance**: Include risk scoring in internal audit scope quarterly

---

**Document Version**: 1.0 | **Last Updated**: February 2025 | **Classification**: Internal Use Only
