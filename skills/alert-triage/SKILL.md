# Payroll Alert Triage Skill

```yaml
name: alert-triage
type: skill
category: payroll
version: 1.4.0
author: CC Payroll Plugin
triggers:
  - PCC alert
  - alert triage
  - alert priority
  - alert routing
  - alert monitor
  - alert resolution
  - payroll alert
  - production payroll alerts
  - team monitoring alerts
  - alert assignment
  - alert SLA
  - bulk alert processing
  - alert root cause
```

## Overview

**PROOF-OF-CONCEPT**: This skill is an exploratory analysis tool and should be used for reference purposes only. It does not replace professional payroll judgment or formal triage procedures.

The **alert-triage** skill takes raw payroll control center alert exports and applies AI-assisted analysis to deliver suggested triage, priority assignment, root cause grouping, and routing recommendations. The alert management view generates alerts based on configured validation rules. Customers export alert lists from the Team Management or My Alerts view — this skill processes that export and adds analysis support that the alert monitor does not provide natively.

**What the alert monitor gives you**: A flat list of validation rule violations per employee, with processor assignment and status.

**What this skill adds**: Priority scoring, alert domain classification, root cause analysis, team routing suggestions, SLA tracking, batch processing opportunities, and resolution guidance — all inferred from the validation rule names using payroll domain knowledge.

## When to Use

Use alert-triage when you need to:
- Import and triage alert exports from your payroll control center
- Assess which alerts to tackle first before a payroll deadline
- Determine response and resolution timelines
- Route alerts to appropriate teams or specialists
- Identify patterns across validation rule groups
- Plan workload across team members
- Monitor SLA compliance and escalation status
- Process high volumes of alerts efficiently
- Understand root causes and prevention strategies

## Input Format: PCC Alert Export (Standard 5-Column)

The input file is an XLSX export from the payroll control center's alert management view. The columns match the standard alert list output:

| Column | Description | Example |
|--------|-------------|---------|
| **Validation Rule** | The configured validation rule name that triggered the alert | "Employees with missing tax withholding data" |
| **Employee Name** | Employee's name as displayed in the alert list | "Laura Johnson" |
| **Personnel Number** | Employee personnel number | "46913810" |
| **Processor** | Assigned processor user ID (blank if unassigned) | "RWILSON" |
| **Status** | Alert workflow status | "Open", "Solution Applied", "Resolved", "Forwarded" |

### Alert Statuses

Standard alert statuses as shown in the alert management view:

- **Open**: Alert is active and not yet addressed or still requires action
- **Solution Applied**: Processor has applied a fix, pending confirmation
- **Resolved**: Alert has been fully resolved and confirmed
- **Forwarded**: Alert has been forwarded to another processor or team

### User-Provided Context

The following information is not in the export and the skill will ask when processing:

- **Payroll Deadline**: When the payroll must be submitted. Critical for priority scoring.

### Column Name Flexibility

The skill flexibly matches column names to handle variations in export format:
- Validation Rule, Validation_Rule, Rule, Alert_Type, Alert Type
- Employee Name, Employee_Name, Emp_Name, Name
- Personnel Number, Personnel_Number, Employee_ID, Employee ID, Emp_ID
- Processor, Assigned_To, Assigned To, Assignee, Owner
- Status, Alert_Status, Alert Status, Workflow_Status, Workflow Status

## Core Capabilities

### 1. Alert Domain Classification (AI-Enriched)

The skill reads the Validation Rule name and uses payroll domain knowledge to automatically classify each alert into one of four domains:

- **Data Quality**: Missing or invalid master data (tax info, bank details, time data, cost centers)
- **Compliance**: Regulatory and policy violations (garnishments, tax reciprocity, work authorization, wage rules)
- **Processing**: Payroll calculation and workflow issues (retro adjustments, overtime, wage type collisions)
- **Financial**: Monetary impact issues (negative net pay, GL variances, benefit gaps, deduction mismatches)

Classification uses both exact matching (25+ known validation rules) and fuzzy keyword matching for non-standard rule names.

### 2. Priority Assignment (P1-P4)

AI-assisted priority scoring based on:
- **Severity** derived from validation rule classification (blocking vs. non-blocking)
- **Alert volume** per validation rule (high count indicates systemic issue)
- **Days until payroll deadline** (provided by user)
- **Assignment status** (unassigned Open alerts get additional urgency)

### 3. Root Cause Grouping

Groups alerts by Validation Rule to identify patterns:
- All alerts for the same rule shown together for batch resolution
- Links employee-specific vs. system-wide issues
- Provides resolution strategies for each root cause group
- Calculates batch processing time savings

### 4. Routing Suggestions

Provides routing recommendations based on:
- **Alert domain** → team specialty mapping
- **Complexity level** → required skill level
- **Workload balancing** across processors (using existing assignment data)
- **Escalation paths** for critical issues

### 5. SLA Management

Calculates SLA deadlines and tracks compliance:
- P1 Critical: 15-min response / 1-hour resolution
- P2 High: 1-hour response / 4-hour resolution
- P3 Medium: 4-hour response / 1-day resolution
- P4 Low: 1-day response / 2-day resolution

### 6. Batch Processing

Identifies alerts that can be resolved together:
- Same Validation Rule across multiple employees (3+ alerts = batch eligible)
- Efficiency metrics (time saved through batching vs. individual resolution)

## Input Modes

### Mode 1: XLSX Export Analysis
Provide an alert export file in XLSX format from the alert management view. The skill reads the 5 standard columns (Validation Rule, Employee Name, Personnel Number, Processor, Status) and enriches with AI analysis. The skill will ask for payroll deadline context.

### Mode 2: Conversational Alert Triage
Describe alert situations conversationally:
- "We have a large batch of missing tax data alerts for our biweekly payroll"
- "One employee has a negative net pay alert with garnishment"
- "We're seeing wage type collisions in multiple cost centers"
- "How should we prioritize these alerts before the Feb 15 payroll run?"

## Alert Priority Framework

### P1 - Critical (Response: 15min, Resolution: 1hr)
**Definition**: Blocking issues that prevent payroll processing or legal compliance

**Triggers**:
- Production payroll run is blocked
- Payroll deadline is within 24 hours
- Affects 10+ employees simultaneously
- Legal/regulatory violation with penalties
- Negative net pay issues requiring immediate correction

**Escalation**: Notify payroll manager immediately

**Examples**:
- Employees with negative net pay results (multiple employees)
- Employees with garnishment order validation errors (active order)
- Employees with missing tax withholding data (large batch near deadline)

### P2 - High (Response: 1hr, Resolution: 4hrs)
**Definition**: High-impact issues affecting payroll quality or moderate employee count

**Triggers**:
- Affects 3-10 employees
- Payroll deadline is within 2-7 days
- Blocking validation rule
- Data quality issue requiring senior specialist

**Escalation**: Notify team lead and assign specialist

**Examples**:
- Employees with missing tax withholding data (batch of 5+)
- Employees with invalid bank account details
- Employees with duplicate wage type entries (multiple occurrences)
- Employees with retroactive change pending processing (near deadline)

### P3 - Medium (Response: 4hrs, Resolution: 1 day)
**Definition**: Moderate issues with contained impact, routine resolution

**Triggers**:
- Affects 1-3 employees
- Payroll deadline is 7+ days away
- Non-blocking but quality-affecting
- Standard specialist can resolve

**Escalation**: Assign to next available team member

**Examples**:
- Employees exceeding overtime hours threshold (single employee)
- Employees with missing state tax jurisdiction
- Employees with expired work authorization documents
- Employees with missing time evaluation results

### P4 - Low (Response: 1 day, Resolution: 2 days)
**Definition**: Non-urgent issues or informational alerts with minimal impact

**Triggers**:
- Affects single employee
- Payroll deadline is 14+ days away
- Non-blocking, non-critical data issues
- Can be resolved in routine processing

**Examples**:
- Employees with gross pay variance exceeding threshold (minor)
- Employees missing cost center assignment (single)
- GL posting variance within tolerance

## Routing Logic

### By Alert Domain

**Data Quality Issues** → Data Operations Team
- Check employee data records in HR and Payroll systems
- Validate with source systems
- Review and update employee master data, tax data, bank details

**Compliance Issues** → Compliance & Legal Team
- Verify regulatory requirements
- Review tax and benefit rules
- Coordinate with HR on work authorization and garnishment matters

**Processing Issues** → Payroll Operations Team
- Review retroactive changes
- Manage overtime and wage type rules
- Resolve workflow blockers and calculation issues

**Financial Issues** → Finance & Reconciliation Team
- Verify monetary impact
- Coordinate cost center assignments
- Review GL posting and deduction calculations

### By Complexity

- **Level 1** (Simple): Single data field correction, template-based resolution
- **Level 2** (Standard): Multi-step resolution, requires specialist knowledge
- **Level 3** (Complex): System troubleshooting, regulatory interpretation, escalation

## Workflow

1. **Import**: Load alert export XLSX (5-column standard format)
2. **Context**: Collect payroll deadline from user
3. **Classify**: AI reads Validation Rule names to assign alert domain (Data Quality / Compliance / Processing / Financial)
4. **Score**: Calculate priority (P1-P4) based on rule severity, blocking status, alert volume, and payroll deadline
5. **Group**: Cluster alerts by Validation Rule for root cause analysis
6. **Route**: Recommend team assignment based on domain and complexity
7. **Track**: Generate SLA timeline and escalation path
8. **Batch**: Identify efficiency opportunities for batch resolution
9. **Report**: Create comprehensive triage dashboard

## Output

The skill generates:
- **Triage Summary**: Overview of alert volume, domain distribution, and priority breakdown
- **Priority Dashboard**: Visual distribution across P1-P4 levels
- **Domain Breakdown**: Count of alerts by classification (Data Quality / Compliance / Processing / Financial)
- **SLA Status**: Compliance metrics and escalation triggers
- **Root Cause Analysis**: Grouped alerts with common resolution paths per validation rule
- **Routing Recommendations**: Assignment suggestions by team specialty
- **Batch Processing Plan**: Efficiency opportunities for same-rule alerts
- **Processor Workload**: Current assignment distribution and rebalancing suggestions
- **Multi-sheet XLSX Report**: Dashboard, prioritized alerts, root cause & batch plan, processor workload, routing guide

## Example Scenarios

### Scenario 1: Single Alert
**Input**: "We have an alert for negative net pay for employee John Smith. His payroll runs in 2 days."

**Analysis**:
- Domain: Financial
- Rule: Employees with negative net pay results
- Timeline: 2 days to payroll deadline
- **Priority: P1 Critical** (blocking payment, tight deadline, resolve within 1 hour)
- **Route**: Finance & Reconciliation Team
- **Action**: Investigate deduction/earning calculation, review employee pay records

### Scenario 2: Batch Import
**Input**: Upload pcc_alerts_export.xlsx with 50 alerts. "Payroll deadline is February 15."

**Analysis**:
- 4 alerts: "Employees with missing tax withholding data" → Data Quality, P2
- 7 alerts: "Employees missing cost center assignment" → Data Quality, P3
- 6 alerts: "Employees with duplicate wage type entries" → Processing, P3
- 3 alerts: "Employees with negative net pay results" → Financial, P1
- Remaining alerts distributed across P3/P4
- 15+ alerts with Status "Open" and no Processor — need assignment

**Recommendations**:
- Batch resolve "missing cost center" alerts together (7 employees, same fix)
- Batch resolve "duplicate wage type entries" (6 employees)
- Prioritize negative net pay alerts immediately
- Assign unassigned Open alerts based on domain expertise
- **Total estimated time with batching**: 6 hours vs. 20+ hours individual

### Scenario 3: Deadline Crisis
**Input**: "Payroll freeze in 12 hours. We have 40 Open alerts."

**Analysis**:
- Separate P1 (blocking alerts) — must resolve immediately
- Separate P2 (high-severity alerts) — triage for deadline feasibility
- Recommend P3/P4 alerts be deferred via "Forwarded" status to next cycle
- Identify which P2s can be batch-resolved vs. individual investigation
- **Escalation**: Alert payroll leadership to critical status

## Best Practices

1. **Triage Regularly**: Don't let alerts accumulate. Triage at least daily during payroll cycles.

2. **Act on Root Causes**: Use root cause grouping to fix systematic issues, not just symptoms.

3. **Respect SLAs**: P1 alerts require immediate human attention. Escalate proactively.

4. **Batch for Efficiency**: When possible, group alerts by validation rule and resolve together. Can reduce handling time by 50-70%.

5. **Coordinate Across Teams**: Share routing recommendations with team leads to balance workload.

6. **Track Trends**: Review root cause patterns monthly to identify systemic improvements.

7. **Document Resolutions**: Update alert status to Resolved with resolution notes for audit trail.

8. **Escalate Early**: Don't wait until deadline crisis. Escalate P1/P2 within SLA window.

9. **Plan Ahead**: Run triage on alert exports before payroll freeze period begins.

## References

See the following reference documents:

- **alert-catalog.md**: Complete catalog of 25+ alert types with root causes and resolution steps
- **priority-framework.md**: Detailed priority assignment methodology and examples
- **routing-rules.md**: Team routing logic, expertise mapping, and escalation procedures

---

**Last Updated**: 2026-02-17
**Skill Version**: 1.4.0
**Python Requirements**: 3.8+, openpyxl, pandas, json
