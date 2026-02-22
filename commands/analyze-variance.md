---
description: Run a period-over-period payroll variance analysis on SAP payroll result exports
argument-hint: "<optional: threshold or focus area>"
---

# Analyze Variance

## Trigger
User runs `/analyze-variance` or asks to compare payroll periods, find variances, or investigate payroll changes.

## Inputs
1. **Current period XLSX** — exported from SAP payroll (Wage Type Reporter, PC_PAYRESULT, ALV export, or PCC)
2. **Prior period XLSX** — the comparison period
3. **Thresholds** (optional) — percentage and absolute dollar thresholds for flagging
4. **Focus area** (optional) — specific cost center, department, or wage type to investigate

## Workflow

### Step 1: Validate Data
- Confirm both files are uploaded and readable
- Check for required columns: Personnel Number, Wage Type, Amount (flexible column name matching)
- Report row counts and any data quality issues

### Step 2: Run Analysis
- Use the `analyze_variance.py` script from the variance-analyzer skill
- Default thresholds: >5% AND >$500 (configurable via user prompt)
- Support AND logic (both must exceed) or OR logic (either triggers flag)

### Step 3: Generate Report
- Use `generate_variance_report.py` to create multi-sheet XLSX workbook
- Sheets: Summary, By Wage Type, By Cost Center, By Department, Detail

### Step 4: Provide Commentary
- Summarize top variance drivers in natural language
- Identify anomalies (new hires, terminations, large one-time payments)
- Categorize risk levels: Critical (>25%), High (>15%), Medium (>5%)

## Example Prompts
- "Compare these two payroll exports and tell me what changed"
- "Flag anything over 10% change or more than $1000 difference"
- "What's driving the cost increase in cost center 4500?"
- "Use strict thresholds — only show variances above 15% AND $2000"

## Output
- Multi-sheet XLSX variance report (saved to workspace)
- Natural language executive summary
- Preliminary risk categorization with recommended actions
