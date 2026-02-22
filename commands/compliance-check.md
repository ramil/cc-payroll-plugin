---
description: Run pre-submission compliance validation on payroll data
argument-hint: "<optional: validation focus>"
---

# Compliance Check

## Trigger
User runs `/compliance-check` or asks to validate payroll, check compliance, or perform pre-submission validation.

## Inputs
1. **Payroll XLSX** — current period payroll data from SAP payroll
2. **Validation focus** (optional) — one of: all, completeness, calculations, wage-bases, prior-period, compliance-rules, review-documentation (default: all)
3. **Prior period XLSX** (optional) — for trend analysis and anomaly detection
4. **Review context** (optional) — internal review, regulatory submission, professional assessment

## Validation Categories

### Data Completeness
Ensures all required fields are populated:
- Employee identification (ID, name)
- Wage information (gross pay, wage types)
- Organizational data (cost center, department)
- Prevents processing with incomplete data

### Calculation Accuracy
Validates mathematical correctness:
- Gross pay calculation reasonableness
- Net pay does not exceed gross pay
- Tax withholding does not exceed taxable wages
- FICA calculations (6.2% Social Security, 1.45% Medicare)
- Garnishment limit compliance (25% maximum)

### Wage Base Limit Checking
Ensures compliance with annual limits:
- Social Security wage base ($176,100 for 2025)
- FUTA wage base ($7,000)
- State SUI wage base (varies by state)
- Prevents overpayment of taxes

### Prior Period Comparison
Detects anomalies by comparing to historical data:
- Identifies unusual headcount changes
- Flags atypical compensation patterns
- Detects department-level outliers
- Analyzes month-over-month trends

### Compliance Rule Validation
Verifies adherence to regulations:
- FLSA overtime compliance
- Garnishment processing limits
- Tax withholding accuracy
- Form 941 and W-2 consistency
- ACA reporting compliance

### Review Documentation
Creates comprehensive documentation:
- Timestamps for all validations
- User identification and notes
- Exception tracking and resolution
- Review summaries for professional assessment
- Supporting calculation details

## Workflow

### Step 1: Validate Input Data
- Confirm XLSX file is uploaded and readable
- Check for required columns: Employee_ID, Wage_Type, Amount, Cost Center
- Report row counts and data quality issues

### Step 2: Run Validations
- Use `validate_payroll.py` script from compliance-audit skill
- Execute all selected validation categories
- Calculate risk score on 0-100 scale (lower is better)
- Identify critical exceptions requiring resolution

### Step 3: Generate Audit Report
- Use `generate_compliance_report.py` for multi-sheet workbook
- Sheets: Summary, Validations, Exceptions, Risk Assessment, Audit Trail
- Include regulatory reference citations

### Step 4: Provide Remediation Guidance
- Summarize findings in business language
- Prioritize exceptions by severity
- Provide specific remediation steps
- Recommend approval sign-offs

## Example Prompts
- "Run a full review check on this payroll export"
- "Validate wage base limits and check for any issues"
- "Compare this period to last month and flag any unusual changes"
- "Generate a review summary for professional assessment"

## Output
- Multi-sheet XLSX review report (saved to workspace)
- Indicative risk score with detailed justification (0-100 scale)
- Validated data summary with exception highlights
- Calculation accuracy verification
- Review documentation with timestamps
- Review summary for professional assessment
