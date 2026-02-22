---
description: Reconcile payroll results to GL postings from SAP payroll result exports
argument-hint: "<optional: reconciliation type>"
---

# Reconcile GL

## Trigger
User runs `/reconcile-gl` or asks to reconcile payroll results to GL, validate GL postings, or investigate GL variances.

## Inputs
1. **Payroll Results XLSX** — exported from SAP (wage type level data)
2. **GL Postings XLSX** — GL line items from SAP FI for payroll posting accounts
3. **Reconciliation type** (optional) — one of: all, gross-to-net, employer-costs, tax-liabilities, cost-center-allocation (default: all)
4. **Tolerance thresholds** (optional) — rounding variance tolerance, typically 0.01-1.00 USD

## Reconciliation Types

### Gross-to-Net Reconciliation
- Validates payroll walkdown from gross salary through deductions to net pay
- Matches to GL net pay liability accounts
- Identifies variances at each step

### Employer Cost Reconciliation
- Reconciles employer-paid taxes (FICA, FUTA, SUI) and benefit costs
- Maps to GL expense accounts (6xxx range)
- Validates cost center allocations

### Tax Liability Reconciliation
- Validates federal, state, and local withholding liabilities
- Maps to GL liability accounts (2xxx range)
- Verifies opening balance + accrual - payments = closing balance

### Cost Center Allocation
- Ensures payroll by cost center matches GL distributions
- Identifies cost center mismatches
- Validates GL posting accuracy by organizational unit

## Workflow

### Step 1: Validate Data
- Confirm both files are uploaded and readable
- Check for required columns: Wage_Type, Employee_ID, Amount, GL Account, Cost Center
- Report row counts and data quality issues

### Step 2: Run Reconciliation
- Use the `reconcile_payroll_gl.py` script from the gl-reconciliation skill
- Perform wage type to GL account mapping using symbolic account logic
- Support flexible column name matching across different SAP naming conventions

### Step 3: Generate Report
- Use `generate_recon_report.py` to create multi-sheet XLSX workbook
- Sheets: Summary, Gross-to-Net, Employer Costs, Tax Liabilities, Unmatched Items, Reconciling Items

### Step 4: Provide Commentary
- Summarize match rates and variance totals
- Identify reconciling items by classification (timing, rounding, retroactive)
- Provide resolution steps for unmatched items

## Example Prompts
- "Reconcile this month's payroll to GL postings"
- "Run a gross-to-net reconciliation on these exports"
- "Check if payroll costs by cost center match GL distributions"
- "Investigate the $50K variance in the gross salary GL account"

## Output
- Multi-sheet XLSX reconciliation report (saved to workspace)
- Matched items with cross-references (preliminary)
- Unmatched items detailed list
- Reconciling items with classification and resolution hints
- Match rate percentage and summary statistics
