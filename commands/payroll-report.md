---
description: Generate a professional stakeholder payroll report from SAP payroll result export data
argument-hint: "<report type: executive | hr | finance | client | ad-hoc>"
---

# Payroll Report

## Trigger
User runs `/payroll-report` or asks to create a payroll summary, report, or analysis for a specific audience.

## Inputs
1. **Payroll XLSX** — current period export from SAP payroll result
2. **Report type** — one of: Executive Summary, HR Operations, Finance, Client/BPO, Ad-hoc Query
3. **Audience** (optional) — who the report is for (e.g., "CFO", "HR Director", "Acme Corp client")
4. **Prior period XLSX** (optional) — for period-over-period comparison
5. **Specific focus** (optional) — department, cost center, or metric to emphasize

## Report Types

### Executive Summary
- **Audience:** CFO, VP Finance, Senior Leadership
- **Contents:** Total payroll cost, headcount, key variances, trend commentary
- **Tone:** Strategic, concise, decision-oriented

### HR Operations
- **Audience:** HR Directors, HR Business Partners
- **Contents:** Headcount by department, new hires, terminations, overtime analysis
- **Tone:** Operational, detail-oriented

### Finance Report
- **Audience:** Controllers, Accounting Team
- **Contents:** Cost center breakdown, GL summary, reconciliation data, accruals
- **Tone:** Technical, precise, for review purposes

### Client Report (BPO)
- **Audience:** External Client Stakeholders
- **Contents:** Processing summary, SLA metrics, exceptions, recommendations
- **Tone:** Professional, service-oriented, white-glove

### Ad-hoc Query
- **Audience:** Any stakeholder
- **Contents:** Direct answer to specific data questions in conversational format
- **Tone:** Responsive, focused on the specific question

## Workflow

### Step 1: Extract Metrics
- Use `extract_payroll_metrics.py` to calculate 30+ KPIs
- Categories: Headcount, Compensation, Deductions, Employer Costs, Breakdowns, Ratios

### Step 2: Generate Report
- Use `generate_payroll_report.py` to create formatted XLSX
- Apply template matching the selected report type

### Step 3: Add Commentary
- Generate AI narrative explaining key metrics in business context
- Highlight notable trends, outliers, and action items

## Example Prompts
- "Create an executive payroll summary for our VP of Finance"
- "Generate the period-end client report for Acme Corp"
- "How many people are in department 200 and what's their total cost?"
- "Break down overtime costs by cost center for the HR director"

## Output
- Formatted multi-sheet XLSX report (saved to workspace)
- AI-generated draft narrative commentary
- Key metrics highlighted with business context
