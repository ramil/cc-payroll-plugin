---
description: Analyze retroactive payroll adjustment impact and GL effects
argument-hint: "<optional: retro type>"
---

# Analyze Retro

## Trigger
User runs `/analyze-retro` or asks to analyze retroactive payroll changes, retro impact, or retro processing effects.

## Inputs
1. **Current Results XLSX** — payroll data after retroactive adjustment (post-retro)
2. **Prior Results XLSX** — payroll data before retroactive adjustment (pre-retro)
3. **Retro type** (optional) — one of: all, pay-rate, organizational, tax-correction, benefit, termination-reversal, time-entry
4. **Risk tolerance** (optional) — threshold for flagging high-impact changes

## Retro Types

### Pay Rate Change
Salary or hourly rate adjustments:
- Retroactive salary increase/decrease
- Hourly rate adjustments
- Effective date adjustments

### Organizational Reassignment
Structural changes affecting pay:
- Cost center reassignment
- Department transfer
- Company code change

### Tax Correction
Tax-related changes:
- Filing status changes
- Exemption adjustments
- Tax jurisdiction changes

### Benefit Change
Benefit plan adjustments:
- Enrollment or plan election changes
- Deduction amount changes
- Coverage modifications

### Termination Reversal
Re-hiring of separated employees:
- Employee reinstatement
- Correction of incorrect terminations
- Effect reversal for terminated period

### Late Time Entry
Retroactive time tickets:
- Delayed overtime entry
- Bonus or incentive payment
- Off-cycle adjustments

## Workflow

### Step 1: Validate Input Files
- Confirm both XLSX files are uploaded and readable
- Check for required columns: Employee_ID, Wage_Type, Amount
- Identify common employees across both periods
- Report period information and scope

### Step 2: Analyze Retro Impact
- Use `analyze_retro_impact.py` to identify all affected employees
- Calculate wage type breakdown showing changes
- Estimate employee net pay impact (/551 equivalent)
- Project tax impact (federal, state, FICA)

### Step 3: Classify and Preliminary Risk Assessment
- Use `classify_retro.py` to categorize retro change type
- Classify financial risk indicators: Low, Medium, High, Critical
- Identify edge cases requiring manual review
- Flag data quality issues

### Step 4: Generate Impact Report
- Use `generate_retro_report.py` for multi-sheet workbook
- Sheets: Summary, Impact Analysis, Affected Employees, GL Projection, Risk Assessment
- Include year-boundary and terminated employee edge cases

## Example Prompts
- "Analyze the impact of this retroactive salary increase"
- "Show me all employees affected by this retro change and the total cost"
- "What's the GL impact of these retroactive adjustments?"
- "Flag any risky or unusual aspects of this retro processing scenario"

## Output
- Multi-sheet XLSX retro analysis report (saved to workspace)
- Affected employee count and list with impact amounts
- Wage type breakdown showing exactly what changed
- Net pay impact per employee with total cost
- Tax impact estimation by jurisdiction (preliminary)
- GL posting impact projection
- Preliminary risk indicators with edge case warnings
- Natural language summary and remediation guidance
