---
name: payroll-reporting
description: "Generate professional stakeholder payroll reports from SAP payroll result XLSX exports. Creates executive summaries, HR operations reports, finance reports, BPO client deliverables, and ad-hoc payroll analysis. Auto-detects report type and generates formatted DOCX/XLSX outputs with AI-generated narrative commentary. Triggers: payroll reporting, payroll summary, executive payroll report, period-end report, payroll metrics, payroll dashboard, client payroll report, stakeholder payroll update, headcount report, labor cost report."
---

# Payroll Reporting Skill

## Overview

This skill demonstrates AI-assisted payroll analysis, generating draft reports from SAP payroll result XLSX data exports. Reports are intended for review purposes and combine fact-based data with AI-generated commentary for stakeholder discussion.

**What SAP already provides natively:**
- **Payroll Journal**: Detailed per-employee payroll register (tabular, operational)
- **Remuneration Statement**: Individual employee pay slip
- **Wage Type Reporter** (PC00_M99_CWTR): Flexible analytical report by wage type, cost center, or employee (tabular ALV output)
- **PCC Dashboard**: Real-time processing KPIs and monitoring metrics

**What this skill adds:**
- **AI-generated draft commentary** — SAP reports are tabular data; this skill generates suggested narratives explaining observations for professional review
- **Stakeholder-specific formatting** — Draft summaries for executives, HR teams, finance teams, and client stakeholders — each with different tone, depth, and metrics. SAP reports are one-size-fits-all.
- **Formatted DOCX/XLSX output** — structured for review and discussion, not SAP ALV grids that need post-processing
- Works from **XLSX exports** — no SAP access required for report generation

**Important:** All generated reports are draft materials and require professional review and verification before distribution or formal use. AI-generated commentary should be validated and edited by subject matter experts.

## Supported Report Types

### Executive Summary
**Audience:** CEO, CFO, board-level stakeholders, VP Finance

**Purpose:** High-level payroll health, KPIs, risks, and trends

**Key Content:**
- Total payroll cost and headcount metrics
- Period-over-period comparison
- Top 5 cost centers by labor cost
- Key metrics dashboard (gross pay, net pay, taxes, benefits, employer costs)
- Notable items (significant changes, exceptions)
- AI-generated draft narrative for review explaining trends and highlighting potential items

**Output Format:** Draft DOCX report (1-2 pages)

### HR Operations Report
**Audience:** HR managers, CHRO, payroll operations team

**Purpose:** Workforce changes, headcount impact, compliance tracking

**Key Content:**
- Headcount by department and cost center
- New hires list with start dates
- Terminations list
- Overtime analysis and trends
- Benefits enrollment summary
- Action items and follow-ups

**Output Format:** Draft DOCX report (2-3 pages)

### Finance Report
**Audience:** Controller, financial analyst, CFO

**Purpose:** Cost impact, GL reconciliation, accrual accuracy

**Key Content:**
- Payroll register summary by wage type category
- Cost center allocation and labor distribution
- Posting summary (gross payroll, taxes, benefits, employer contributions)
- Reconciliation data points
- Tax liability and deduction accuracy
- Period-over-period cost comparison

**Output Format:** Formatted XLSX workbook with multiple sheets (summary, cost center detail, wage type detail, employee detail)

### Client Report (BPO)
**Audience:** External BPO client, account management

**Purpose:** Demonstrate service delivery, SLA performance, value

**Key Content:**
- Client branding header
- Processing summary (period dates, volumes, status)
- SLA compliance metrics
- Headcount and cost summary by department
- Exception and issue resolution log
- Next period calendar and upcoming actions

**Output Format:** Draft DOCX report (2-3 pages, client-branded)

### Ad-hoc Query
**Audience:** Varies (usually finance analyst, manager, consultant)

**Purpose:** Answer specific one-off questions about payroll data

**Key Content:** Focused answer with relevant data tables and explanations

**Output Format:** Varies (direct answer, formatted table, brief report as needed)

## Input Data Format

The skill accepts XLSX files from SAP payroll result exports with the following column structure:

| Column | Description | Example |
|--------|-------------|---------|
| Employee ID | Unique employee identifier | EMP001234 |
| Employee Name | Employee full name | John Smith |
| Payroll Area | SAP payroll area code | P1 |
| Cost Center | Department cost center | 4100 |
| Department | Department name or code | Sales |
| Wage Type | 4-digit wage type code | 1000 |
| Wage Type Description | Human-readable wage type | Basic Pay |
| Amount | Wage amount (in currency) | 5500.00 |
| Currency | ISO currency code | USD |
| Pay Date | End of pay period | 2026-01-31 |
| Status | Processing status | Completed |

**Wage Type Convention:**
- **1000-1999:** Earnings (Basic Pay, Overtime, Bonus, Commissions)
- **2000-2999:** Deductions (Taxes, Benefits, Garnishments)
- **3000-3999:** Employer Contributions (FICA, Health Insurance, 401k Match)
- **4000+:** Informational (FTE counts, benefit statuses)

## How to Use This Skill

### Step 1: Accept and Parse Payroll Data

When a user provides an XLSX payroll export:

1. **Verify the data structure** matches the expected columns above
2. **Note the payroll period** (from Pay Date column)
3. **Identify if prior period data** is available for comparison
4. **Check the status** of records (Completed/Pending/Error)
5. **Flag any data quality issues** (missing fields, unusual values)

### Step 2: Auto-detect or Confirm Report Type

Analyze the user's request to determine the intended report:

- **Executive Summary keywords:** "executive," "VP," "CFO," "summary," "dashboard," "key metrics," "board," "high-level"
- **HR Operations keywords:** "HR," "headcount," "movement," "new hires," "terminations," "department," "operations"
- **Finance keywords:** "GL," "cost center," "accounting," "posting," "reconciliation," "finance," "cost allocation"
- **Client Report keywords:** "client," "BPO," "deliverable," "external," "Acme," "customer," "account"
- **Ad-hoc Query keywords:** Specific questions like "how many," "what's the total," "breakdown," "compare"

**If ambiguous:** Ask clarifying question: "Are you looking for an executive summary, detailed HR operations report, or finance report?"

**Default:** If the user says "report" without specifying type, default to **Executive Summary**

### Step 3: Extract and Calculate Payroll Metrics

Run the extraction script to process the XLSX data:

```bash
python scripts/extract_payroll_metrics.py <payroll_file.xlsx> \
  --output metrics.json \
  [--prior <prior_period_file.xlsx>]
```

This script:
- Reads the XLSX file with openpyxl
- Calculates all key payroll metrics (totals, averages, ratios)
- Aggregates by cost center, department, wage type category
- Identifies notable items (highest paid employees, overtime concentration, etc.)
- Outputs structured JSON for report generation
- Automatically categorizes wage types by the 1000-4000 convention

### Step 4: Generate the Report

For **Executive, HR Operations, or Client Reports:**

Create a formatted DOCX using Python (python-docx library):

1. Use the appropriate template from `references/report-templates.md`
2. Structure: Title page → Key findings → Tables/data → Commentary → Appendix
3. Professional formatting:
   - Consistent heading styles (Heading 1, Heading 2, Heading 3)
   - Styled table headers with light background
   - Currency formatting ($X,XXX.XX)
   - Percentage formatting (X.X%)
   - Page numbers and confidentiality markers
   - 1-inch margins, 11pt body font

For **Finance Reports:**

Generate a formatted XLSX using openpyxl:

1. Summary sheet with key metrics dashboard
2. Cost Center sheet with department-level breakdown
3. Wage Type sheet with earnings/deductions/contributions summary
4. Employee Detail sheet with sortable data
5. Charts sheet with visualization data (top cost centers bar chart data)
6. Professional formatting: header styling, number formats, column widths, borders

### Step 5: Generate AI-written Draft Commentary

For each report section, generate narrative that follows this pattern:

**State the Fact:** What is the data showing?
```
"Total gross payroll for January increased to $2.4M from $2.3M in December,
representing a 4.2% increase driven primarily by new hire onboarding."
```

**Provide Context:** How does this compare to expectations, prior periods, or benchmarks?
```
"This aligns with our forecasted headcount growth of 8 FTE this period.
The increase is consistent with our Q1 hiring plan that called for 15 new hires
across Operations and Customer Success."
```

**Highlight Items for Review:** What should the reader consider?
```
"Review overtime trends in the Operations department—it increased to 12%
of regular pay this period, up from 7% in December. This may warrant discussion
regarding staffing plans for Q2."
```

**Tone by Audience:**
- **Executive:** Business impact, key observations, bottom-line numbers for review
- **HR:** People movement, observations, operational metrics
- **Finance:** GL mapping, data points, suggested reconciliation items
- **Client:** Processing status, items for discussion, observations on delivery

### Step 6: Deliver Output

Return to the user:
- **Primary output:** Formatted DOCX (for executive/HR/client reports) or XLSX (for finance reports)
- **Secondary output:** If requested, also provide the JSON metrics file for further analysis
- **Brief summary:** "Draft report generated: [ReportType] for [Period]. X employees, $Y total payroll, Z items flagged for review. Please verify and edit as needed before distribution. See attached."

## Key Payroll Metrics Reference

Detailed metric definitions and calculations are in `references/payroll-metrics.md`. Common metrics:

- **Total Payroll Cost** = Gross Pay + Employer Contributions
- **Effective Tax Rate** = Total Taxes / Gross Pay
- **Benefits Load Rate** = Total Benefits / Gross Pay
- **Cost per Employee** = Total Payroll Cost / Active Headcount
- **Overtime Ratio** = Overtime Pay / Regular Pay
- **Turnover Indicators** = New Hires + Terminations / Average Headcount

## Report Templates

Standard report structures for each report type are documented in `references/report-templates.md`:

- **Executive Summary Template:** Period ID, Key Metrics Dashboard, Period-over-Period Comparison, Top 5 Cost Centers, Notable Items, Commentary
- **HR Operations Template:** Headcount by Department, New Hires, Terminations, Overtime Analysis, Benefits Summary, Action Items
- **Finance Template:** Payroll Register Summary, Cost Center Allocation, Posting Summary, Reconciliation, Tax Liability
- **Client Report Template:** Header, Processing Summary, SLA Metrics, Exception Log, Next Period Calendar

## Scripts and Tools

### extract_payroll_metrics.py
Extracts metrics from XLSX payroll exports and outputs structured JSON.

**Usage:**
```bash
python scripts/extract_payroll_metrics.py payroll_data.xlsx \
  --output metrics.json
```

**Features:**
- Reads XLSX with openpyxl
- Calculates all key metrics
- Aggregates by cost center and department
- Identifies notable items
- Outputs structured JSON

### generate_payroll_report.py
Generates formatted XLSX reports from metrics JSON.

**Usage:**
```bash
python scripts/generate_payroll_report.py metrics.json \
  --output payroll_report.xlsx \
  --type executive
```

**Outputs:**
- Summary sheet with KPI dashboard
- Cost Center sheet with breakdown
- Wage Type sheet with category summary
- Employee Detail sheet with sortable data
- Charts sheet with visualization data

## Best Practices

**Be Clear About Limitations**
These are draft reports with AI-generated commentary. Always note assumptions and limitations. Flag areas requiring professional verification. A user can read raw data themselves; your role is to suggest interpretations for professional review.

**Match Tone to Audience**
Draft reports should be appropriately detailed for each audience. Executive drafts need clarity. Finance drafts need documentation. Client drafts need appropriate context.

**Flag Items for Professional Review**
Connect observations to areas requiring verification. "X changed" is data. "X changed, which may indicate Y—recommend review" is appropriate draft commentary.

**Handle Missing Data Gracefully**
Real payroll data often has gaps. If a metric can't be calculated, note it. Don't make up numbers. Flag limitations clearly.

**Verify Before Distribution**
These draft reports should be reviewed and edited by qualified payroll professionals before sharing externally. All calculations and conclusions should be validated.

**Professional Presentation**
Reports should look organized and clean. Use clear formatting, structured tables, and readable text—but mark clearly as drafts for review.

## Success Criteria

A draft payroll report is successful if:
- ✓ It addresses the user's specific question or need
- ✓ It uses data accurately and highlights limitations clearly
- ✓ It provides observations beyond raw numbers
- ✓ It's professionally formatted and easy to read
- ✓ It's appropriately scoped for the audience
- ✓ Key observations are clear and documented
- ✓ The user can review, edit, and finalize it for stakeholder use

---

**Status:** Proof-of-Concept (Alpha 0.1.0) — This skill demonstrates AI-assisted payroll reporting. All generated reports are draft materials and require professional review and verification before distribution.

Built for SAP payroll users in BPO, shared services, and enterprise payroll operations.
