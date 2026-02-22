# SAP PCC Payroll Alert Priority Framework

## Overview

The priority framework provides a structured methodology for assigning alert priority levels (P1-P4) based on multiple factors including severity, business impact, timeline, and affected employee count. This framework aims to support consistent alert handling and proper resource allocation.

## Priority Level Definitions

### P1 - CRITICAL

**Response SLA**: 15 minutes
**Resolution SLA**: 1 hour
**Escalation**: Immediate escalation to on-call payroll manager

**Definition**: Blocking issues that prevent payroll processing or create legal/regulatory violations.

**Characteristics**:
- Prevents payroll run from completing
- Payroll deadline is within 24 hours
- Affects 10 or more employees simultaneously
- Regulatory violation with immediate filing deadline
- Legal compliance risk with financial/reputational penalties
- Critical system failure affecting payroll engine
- Production down event

**Triggering Conditions** (any one is sufficient):
1. Payroll run is blocked and cannot proceed
2. Payroll deadline is less than 24 hours AND alert is unresolved
3. 10+ employees affected by same issue
4. Regulatory/legal violation with penalties
5. Negative Net Pay affecting multiple employees
6. Payroll Lock condition preventing processing
7. Tax Calculation Engine failure or timeouts

**Assignment Logic**:
1. Immediate page to on-call payroll manager
2. Assign to senior specialist with full payroll knowledge
3. May require system administrator involvement
4. Coordinate with payroll leadership

**Escalation Path**:
- 0-5 min: Acknowledge and begin investigation
- 5-10 min: Escalate to payroll manager if not making progress
- 10-15 min: Escalate to payroll director
- After 15 min: Daily escalation until resolution

**Examples**:
- Employee Smith has negative net pay of -$500 due to garnishment error
- Payroll run fails with "Tax Module Timeout" error for all employees
- Regulatory audit alert: W2 filing deadline is today
- Garnishment validation failure for court order (active, enforceable)
- System corruption detected in payroll master data
- Multiple employees with blocked status (hard lock)

**Typical Resolution Time**: 15-45 minutes

---

### P2 - HIGH

**Response SLA**: 1 hour
**Resolution SLA**: 4 hours
**Escalation**: Notify team lead and assign senior specialist

**Definition**: High-impact issues affecting payroll quality or affecting 3-10 employees.

**Characteristics**:
- Affects 3-10 employees
- Payroll deadline is 2-7 days away
- Financial impact exceeds $10,000 or exceeds average weekly payroll by 5%
- Medium-severity blocking alert
- Data quality issue requiring specialist knowledge
- Cannot be auto-resolved by system
- May cause payment delays if not addressed

**Triggering Conditions** (evaluate multiple factors):
1. 3-10 employees affected by same issue
2. Payroll deadline 2-7 days away AND high/medium severity
3. Financial impact $10,000+ or 5%+ of weekly payroll
4. Medium-severity data quality issue
5. Missing critical compliance data (tax ID, IFTA, etc.)
6. Wage type collision affecting multiple cost centers
7. Retroactive change within 5-7 days of deadline
8. Invalid bank account details for ACH-dependent employees

**Assignment Logic**:
1. Notify team lead within 15 minutes
2. Assign to available senior specialist
3. May require cross-functional coordination
4. Escalate to team lead if no progress after 2 hours

**Escalation Path**:
- 0-30 min: Acknowledge and assign to specialist
- 30-60 min: Check progress; escalate if blocked
- 60-120 min: Escalate to team lead if not resolved
- After 2 hours: Escalate to payroll manager
- After 4 hours: Escalate to payroll director

**Examples**:
- 6 employees missing tax data for current payroll
- 4 employees with invalid bank details in ACH run
- Wage type collision in 3 cost centers affecting 8 employees
- Cost center missing for 5 high-value employees
- Retroactive change affecting 3 employees, deadline is 5 days
- Tax reciprocity calculation error affecting benefits

**Typical Resolution Time**: 1-3 hours

---

### P3 - MEDIUM

**Response SLA**: 4 hours
**Resolution SLA**: 1 day
**Escalation**: Assign to next available team member

**Definition**: Moderate-impact issues with contained scope, routine specialist resolution.

**Characteristics**:
- Affects 1-3 employees
- Payroll deadline is 7+ days away
- Financial impact $1,000-$10,000
- Non-blocking but affects data quality
- Predictable resolution path
- Standard specialist can resolve independently
- May impact next payroll if not addressed

**Triggering Conditions** (evaluate multiple factors):
1. 1-3 employees affected
2. Payroll deadline 7+ days away
3. Financial impact $1,000-$10,000
4. Non-blocking alert
5. Single employee data discrepancy
6. Overtime threshold exceeded
7. Tax reciprocity issue for single employee
8. Benefit gap identified
9. Time card discrepancy requiring research

**Assignment Logic**:
1. Assign to next available team member
2. Standard priority in team queue
3. Can be batched with similar alerts
4. No special escalation unless timeline shifts

**Escalation Path**:
- If timeline changes to P2 threshold: escalate
- If financial impact grows: reassess priority
- If complexity increases: escalate to team lead
- Standard escalation after 1 day if unresolved

**Examples**:
- Employee Johnson's overtime exceeds threshold by 2 hours
- Single employee with tax reciprocity issue
- Benefit gap identified for one employee
- Time data discrepancy for temporary employee
- One employee missing non-critical documentation
- Wage calculation exception for special case

**Typical Resolution Time**: 15-45 minutes (within 1-day SLA)

---

### P4 - LOW

**Response SLA**: 1 day
**Resolution SLA**: 2 days
**Escalation**: Standard queue management

**Definition**: Non-urgent issues or informational alerts with minimal business impact.

**Characteristics**:
- Single employee affected
- Payroll deadline is 14+ days away
- Financial impact less than $1,000
- Non-blocking, informational, or advisory
- Can be resolved in routine processing
- May be combined with next scheduled payroll adjustments
- No SLA pressure

**Triggering Conditions** (evaluate multiple factors):
1. Single employee affected
2. Payroll deadline 14+ days away
3. Financial impact < $1,000
4. Informational or advisory alert
5. Pending approval (non-urgent)
6. Documentation reminder
7. Archival or historical data warning
8. System maintenance notification

**Assignment Logic**:
1. Add to standard team queue
2. Assign based on skill and availability
3. Can be batched and resolved efficiently
4. No special routing required

**Escalation Path**:
- Standard escalation after 2 days if unresolved
- Can be deferred if payroll deadline permits
- Escalate only if timeline changes

**Examples**:
- Informational alert about archival records
- Pending approval for future-dated change
- Documentation reminder (non-compliance)
- System maintenance window notification
- Routine compliance documentation request
- Optional data enrichment suggestion

**Typical Resolution Time**: 5-15 minutes (within 2-day SLA)

---

## Priority Scoring Algorithm

### Factors and Weights

```
Priority Score = (Severity × 0.35) + (Deadline × 0.30) + (Impact × 0.20) + (Type × 0.15)

Where:
- Severity: 1-100 (based on alert classification)
- Deadline: 1-100 (days to payroll deadline, inverse scale)
- Impact: 1-100 (employee count and financial impact combined)
- Type: 1-100 (blocking vs. non-blocking)
```

### Severity Scoring

| Severity Level | Score | Examples |
|---|---|---|
| Critical/High | 80-100 | Negative net pay, calculation failure, payroll lock |
| Medium | 50-79 | Data quality issues, wage collisions, missing data |
| Low/Informational | 1-49 | Informational alerts, pending approvals |

### Deadline Scoring

| Days to Deadline | Score | Priority Range |
|---|---|---|
| < 1 day (24 hours) | 100 | P1-P2 only |
| 1-2 days | 80-90 | P2 minimum |
| 2-7 days | 50-75 | P2-P3 range |
| 7-14 days | 25-50 | P3-P4 range |
| 14+ days | 1-25 | P4 range |

### Impact Scoring (Employees + Financial)

| Employees Affected | Base Score | Financial Multiplier |
|---|---|---|
| 1 | 10 | 1x if < $1K, 2x if $1-10K, 3x if > $10K |
| 2-3 | 30 | Same multiplier |
| 4-9 | 60 | Same multiplier |
| 10+ | 90 | Same multiplier |

### Alert Type Scoring

| Type | Score | Rationale |
|---|---|---|
| Blocking (prevents payroll run) | 80-100 | Cannot proceed without resolution |
| High-value | 60-80 | Significant financial impact |
| Data Quality | 40-60 | Impacts data integrity |
| Compliance | 40-60 | Regulatory consideration |
| Informational | 10-30 | No action required |

### Combined Priority Mapping

| Score Range | Assigned Priority | Rationale |
|---|---|---|
| 85-100 | P1 Critical | Immediate resolution required |
| 70-84 | P2 High | Within-shift resolution required |
| 50-69 | P3 Medium | Next-business-day resolution |
| 1-49 | P4 Low | Standard queue processing |

---

## Priority Override Rules

Certain conditions may override the calculated score:

### Automatic Escalation to P1
- Payroll freeze initiated or payroll run launched (regardless of alert severity)
- Regulatory filing deadline is today or tomorrow
- System down or service degradation affecting payroll
- Customer escalation (customer request)
- Multiple P2 alerts on same issue within 2 hours

### Automatic Escalation to P2
- Two or more alerts affecting same employee on same day
- Deadline shifts to within 48 hours
- Financial impact exceeds $25,000 (double threshold)
- Senior management escalation
- Four or more P3 alerts on same issue

### Automatic Demotion to P4
- Alert is duplicate of already-resolved alert
- Alert is informational only, no action required
- Deadline shifts to 30+ days away
- Issue resolved by system before human intervention
- Alert is superseded by later corrective action

### Deadline Proximity Override
- If payroll deadline changes, recalculate all impacted alert priorities
- Alerts within 24 hours are minimum P2 (unless P4 informational)
- Alerts within 12 hours are minimum P1 if any resolution required

---

## Escalation Matrix

### By Priority Level

```
P1 CRITICAL
├─ 0-5 min: Team lead notified
├─ 5-15 min: Payroll manager notified
├─ 15-30 min: Payroll director involved
└─ 30+ min: C-level escalation (CFO/COO)

P2 HIGH
├─ 0-15 min: Team lead notified
├─ 15-60 min: Payroll manager may be involved
├─ 60-120 min: Escalate to payroll director
└─ After 4 hours: Director escalation

P3 MEDIUM
├─ 0-4 hours: Standard assignment
├─ 4-24 hours: Team lead review if unresolved
└─ After 24 hours: Escalate to payroll manager

P4 LOW
├─ 0-1 day: Standard queue assignment
├─ 1-2 days: Normal escalation if unresolved
└─ After 2 days: Evaluate if still relevant
```

### By Condition

**Blocking Alert** (prevents payroll run):
- Always escalate to P1/P2 minimum
- Immediate team lead notification
- Do not wait for SLA timers

**Regulatory/Compliance**:
- Escalate 1 level if filing deadline is within 7 days
- Escalate 2 levels if filing deadline is within 1 day
- Involve compliance/legal team for interpretation

**Customer Escalation**:
- Escalate 1 level above calculated priority
- Notify account management immediately
- Document customer contact and requirements

**System Degradation**:
- All new alerts automatically P1/P2 during degradation
- May batch resolution once system restored
- Status updates required every 15 minutes

---

## SLA Compliance Tracking

### SLA Timeline Example (P1 Alert Created at 9:00 AM)

| Time | Event | Status |
|---|---|---|
| 09:00 | Alert created | Created |
| 09:15 | Must acknowledge | Response SLA window |
| 10:00 | Must resolve or escalate | Resolution SLA starts |
| 10:15 | No escalation yet (15 min into 1-hour window) | On track |
| 10:45 | Still working, 15 min to deadline | Warning |
| 11:00 | Must resolve or escalate to director | Escalation required |

### SLA Metrics to Track

1. **Response Time**: Time from creation to first assignment/acknowledgment
2. **Resolution Time**: Time from creation to marked resolved
3. **Escalation Time**: Time from SLA breach to escalation action
4. **Repeat Rate**: Percentage of alert types recurring within 7 days
5. **On-Time Rate**: Percentage of alerts resolved within SLA

### SLA Reporting

Generate weekly SLA report showing:
- Total alerts by priority
- SLA met vs. missed by priority
- Root causes of SLA misses
- Team member SLA compliance
- Trending (improving or declining)

---

## Special Situations

### Multi-Employee Same Root Cause
If 15 employees all have "Missing Tax Data" alert:
- Score as P2 (10+ affected)
- Investigate single root cause (e.g., batch data load error)
- Resolve root cause once (1 hour) vs. 15 individual investigations (3-4 hours)
- Batch processing SLA: 4 hours (not individual P2 4-hour SLA)

### Cascading Alerts
If resolving Alert A automatically resolves Alerts B, C, D:
- Focus on Alert A priority (highest of the group)
- Monitor for cascading resolution
- Close related alerts automatically when A is resolved

### Pre-Deadline Crunch
When payroll deadline is within 12 hours:
- All outstanding alerts become minimum P2
- Defer P3/P4 non-blocking work post-payroll
- Focus resources on P1/P2 only
- Use triage to identify what CAN wait

### System Maintenance Window
During planned maintenance:
- New alerts may be held (not escalated)
- Suppress informational alerts
- Focus on blocking issues only
- Resume normal escalation when system restored

---

**Last Updated**: 2026-02-07
**Framework Version**: 1.0.0
