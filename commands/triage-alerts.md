---
description: Triage and prioritize PCC alerts with routing recommendations
argument-hint: "<optional: deadline date>"
---

# Triage Alerts

## Trigger
User runs `/triage-alerts` or asks to triage payroll control center alerts, prioritize issues, or route alerts to teams.

## Inputs
1. **Alert Export XLSX** — Export from the payroll control center's alert management view (5-column standard format)
2. **Deadline date** (optional) — payroll deadline for SLA calculations (default: 7 days from now)
3. **Team structure** (optional) — assignment of team members to payroll areas or specialties
4. **Escalation rules** (optional) — custom routing rules for specific alert types

## Alert Classifications

### Data Quality Domain
Missing or invalid master data alerts:
- Employees with missing tax withholding data
- Employees with invalid bank account details
- Employees with missing time evaluation results
- Employees missing cost center assignment
- Employees with duplicate employee records
- Employees with missing employee master data

### Compliance Domain
Regulatory and policy violation alerts:
- Employees with garnishment order validation errors
- Employees with missing state tax jurisdiction
- Employees with expired work authorization documents
- Employees with tax reciprocity violation
- Employees with regulatory filing delay
- Employees with benefits compliance gap
- Employees with wage law violation

### Processing Domain
Payroll calculation and workflow alerts:
- Employees exceeding overtime hours threshold
- Employees with retroactive change pending processing
- Employees with unprocessed infotype changes
- Employees with duplicate wage type entries
- Employees with payroll lock condition
- Employees with system validation error
- Employees with batch processing failure

### Financial Domain
Monetary impact alerts:
- Employees with negative net pay results
- Employees with gross pay variance exceeding threshold
- Employees with GL posting variance detected
- Employees with benefit deduction exceeding net pay
- Employees with cost center misallocation
- Employees with budget variance alert

## Workflow

### Step 1: Validate Alert Export
- Confirm XLSX file is uploaded and readable
- Check for required columns: Validation Rule, Employee Name, Personnel Number, Processor, Status
- Report total alert count by status (Open, Solution Applied, Resolved, Forwarded)

### Step 2: Classify and Prioritize
- Use `triage_alerts.py` to classify each alert into domain categories based on the Validation Rule name
- Assign P1-P4 priority based on rule severity, blocking status, alert volume, and days to deadline
- Calculate SLA response and resolution times

### Step 3: Group by Root Cause
- Identify related alerts by Validation Rule name
- Group same-rule alerts for batch resolution (e.g., all "missing tax withholding data" alerts)
- Link employee-specific vs. system-wide issues

### Step 4: Generate Routing Recommendations
- Use `generate_triage_report.py` to create assignment recommendations
- Route by alert domain to team specialty
- Balance workload across available processors
- Flag P1 critical blocking alerts for escalation

## Example Prompts
- "Import and triage the alert export"
- "What are the critical alerts I need to handle before the payroll deadline?"
- "Show me all missing tax data alerts that can be resolved together"
- "Who should handle each alert based on their expertise?"

## Output
- Prioritized alert list with P1-P4 classification
- Natural language summary of critical blocking alerts
- Routing suggestions with assignment recommendations
- SLA tracking timeline and escalation alerts
- Root cause groupings by validation rule with batch resolution strategies
- Alert pattern analysis and prevention recommendations
