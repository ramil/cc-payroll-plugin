---
name: variance-analyzer
description: Automated period-over-period payroll variance analysis for SAP payroll result exports. Identifies significant wage type changes, cost center variances, anomalies, and generates executive-ready reports. Triggers on payroll variance requests, payroll result comparison, period comparison, wage type changes, cost center variance, gross-to-net comparison, payroll simulation vs production comparison, and payroll anomaly detection.
---

# Variance Analyzer

## Overview

The Variance Analyzer skill performs automated period-over-period analysis of SAP payroll result exports. It calculates variances at multiple levels (employee, wage type, cost center), flags trends and anomalies, generates natural language commentary explaining significant changes, and produces formatted Excel workbooks and draft summaries for management review.

**Data source:** This skill works with payroll result exports from SAP — typically generated via Wage Type Reporter (PC00_M99_CWTR), payroll journal reports, or custom ALV exports. It does NOT require direct SAP system access; it analyzes file exports directly.

**What SAP already provides natively:**
- **Wage Type Reporter** (PC00_M99_CWTR): Can compare two periods side by side and display dollar/percentage differences in tabular ALV format
- **PCC Monitoring Dashboard**: Real-time KPIs showing payroll status and highlighted anomalies

**What this skill adds:**
- **AI-driven anomaly flagging** — automatically flags unusual patterns (new hires, terminations, wage type changes, gross pay spikes) with AI-suggested root cause hypotheses. The Wage Type Reporter shows numbers but doesn't tell you *why* something changed.
- **Natural language commentary** — generates draft narrative explaining each significant variance in business terms, not just SAP codes
- **Multi-dimensional analysis** in a single pass — by wage type, cost center, payroll area, and individual employee. WTR requires separate runs for each view.
- **Formatted multi-sheet Excel workbook** — for review purposes, with conditional formatting and summary dashboards. WTR outputs a flat ALV grid.
- **Configurable thresholds** — flag variances by both percentage AND absolute amount to surface material changes for review

**Why this matters:** Manual spreadsheet analysis of WTR exports is error-prone and time-consuming; this skill automates the entire analysis-to-report workflow.

## When to Use This Skill

Use Variance Analyzer when you need to:
- Compare payroll results across two periods (current vs. prior month)
- Analyze payroll simulation/test results against production results before go-live
- Investigate why specific wage types or cost centers changed
- Identify new employees, terminated employees, or wage type anomalies
- Generate variance reports for client communication or executive review
- Detect payroll processing errors before production run finalization
- Explain cost changes to stakeholders with data-backed natural language commentary

## Core Capabilities

### 1. Multi-Format Data Ingestion

**Accept XLSX payroll result exports from SAP (Wage Type Reporter, ALV, or custom reports):**

```
Standard Columns (any order — column name variations accepted):
- Personnel Number   (or PERNR, Employee_ID, emp_id, ID)
- Employee Name      (or ENAME, Employee_Name, name)
- Payroll Area       (or ABKRS, Payroll_Area — 2-char pay schedule code: BW=biweekly, SM=semi-monthly, MO=monthly)
- Payroll Period     (or FPPER, Period — YYYYMM format, e.g., 202602)
- Cost Center        (or KOSTL, Cost_Center, cc)
- Wage Type          (or LGART, Wage_Type, wage_code — 4-digit customer wage type code)
- Wage Type Text     (or LGTXT, Wage_Type_Description, description)
- Amount             (or BETRG — positive for earnings/employer costs, negative for deductions)
- Currency           (or WAERS — optional, defaults to USD)
```

**Optional columns (used for additional analysis if present):**
- Prior Amount (for combined format — alternative to separate prior period file)
- Personnel Area (or PERSA — for organizational grouping)
- Company Code (or BUKRS — for multi-company analysis)

**Two input modes:**

1. **Separate Files:** `payroll_current.xlsx` and `payroll_prior.xlsx` with same structure
2. **Combined File:** Single file with `Current Amount` and `Prior Amount` columns side-by-side

The skill merges on `Personnel Number + Wage Type` to match records across periods.

**Sign convention:** Earnings and employer costs are positive amounts. Employee deductions (taxes, benefits, 401k) are negative amounts. This follows standard SAP payroll result sign convention.

### 2. Variance Calculation & Flagging

For each record, calculate:
- **Absolute Variance:** `Current - Prior` (dollar amount)
- **Percentage Variance:** `(Current - Prior) / |Prior| * 100` (percent change, handles zero denominators)
- **Flag Threshold:** Default: >5% AND >$500 absolute (configurable via `--threshold-pct`, `--threshold-abs`, `--threshold-logic`)
- **Threshold Logic:**
  - Use `--threshold-logic AND` (default) when the user specifies custom thresholds or asks for a focused review — this is stricter and reduces noise
  - Use `--threshold-logic OR` when doing broad monitoring sweeps — this surfaces more items for broader review
  - When the user says "flag anything over X% or $Y", use AND logic (they want items that are both materially large AND percentage-significant)
- **Direction:** Label as "increase" (favorable for earnings, unfavorable for deductions) or "decrease"

**Why:** Percentage alone misses large changes on small values; absolute amount alone misses percentage changes on large values. AND logic (default) helps surface only truly material variances, keeping reports focused. OR logic surfaces more edge cases for broader monitoring.

### 3. Multi-Dimensional Analysis & Summarization

Group and summarize variances by:
- **Wage Type** (Basic Pay, Overtime, Bonuses, Federal Tax, State Tax, 401K, Medical, Employer FICA, etc.)
- **Cost Center** (organizational cost codes — primary grouping dimension from SAP)
- **Payroll Area** (pay schedule group: biweekly, semi-monthly, monthly — for period normalization)
- **Employee** (individual-level when flagged for large variances)

**Why:** Payroll costs are managed at multiple levels—CFOs care about cost center totals, operations managers track specific wage type trends, and HR must investigate individual anomalies. Each view answers different business questions.

### 4. Natural Language Commentary Generation

For each significant variance, generate human-readable explanations following templates organized by variance type:

**Examples:**
- "Overtime in Cost Center 4500 increased 23% ($12,450)—likely driven by 3 new hires still ramping and unfilled positions. Recommend monitoring next period."
- "Federal tax withholding decreased 4.2% across all departments, consistent with 8 employees submitting updated W-4 forms this period."
- "Shift differential pay (Wage Type 1200) is zero this period; 5 employees who earned this last month are no longer in overnight rotation."

**Why:** Numbers alone don't explain context. Natural language commentary helps stakeholders understand root causes, assess whether changes are expected, and decide if further investigation is needed.

### 5. Anomaly Detection & Risk Flagging

Automatically detects and flags six categories of anomalies (all implemented in `analyze_variance.py`):

- **New Employees:** Present in current period, absent in prior — flags as MEDIUM risk with gross pay impact and investigation checklist (verify hire date, benefits, W-4/I-9, cost center)
- **Terminated Employees:** Present in prior, absent in current — flags as MEDIUM risk with prior gross pay impact and investigation checklist (verify termination, final pay, COBRA, benefits termination)
- **Gross Pay Anomalies:** Employees with >30% change in total gross pay (excluding new hires/terminations) — flags as HIGH risk. Suggests investigation for undocumented salary change, job code change, shift change, unpaid leave, overpayment correction, or data entry error
- **Wage Type Appearance/Disappearance:** Wage types that appear or disappear for continuing employees between periods — flags as MEDIUM risk. Appearance suggests new benefit enrollment, bonus plan, or payroll condition; disappearance suggests benefit termination or plan drop
- **Cost Center Shifts:** Employees whose cost center assignment changed between periods — flags as LOW risk with transfer verification checklist
- **Z-Score Statistical Outliers:** For each wage type with 5+ employees, calculates z-scores on percentage variance; flags employees >2σ from mean as MEDIUM, >3σ as HIGH. Identifies individual employees whose variance for a specific wage type is statistically unusual compared to their peer group

Each anomaly record includes: anomaly type, risk level, employee details, descriptive detail text, dollar impact, and investigation notes.

**Risk Categorization:** Every variance record is classified as HIGH (>10% and >$2,000), MEDIUM (>5% or >$500), LOW (>2% or >$100), or NONE. The Summary sheet shows the risk distribution and the Detail sheet color-codes risk levels (red=HIGH, amber=MEDIUM, green=LOW).

**Why:** Most payroll errors manifest as anomalies. Flagging these items helps identify potential issues for professional review.

### 6. Output Generation

**Excel Workbook** with 6 formatted sheets:
- **Summary:** Top-level metrics (total payroll, change, % change), risk distribution (HIGH/MEDIUM/LOW counts), anomaly summary by type, top 20 variances by impact with risk column
- **By Wage Type:** Subtotals and variances grouped by wage type category across all employees, with variance percentages
- **By Cost Center:** Cost center-level summary with largest variances highlighted, supporting employee details
- **By Department:** Department-level rollup with flagged item counts
- **Detail:** Full employee-level variance data, all wage types, with risk level column (color-coded) and flagged indicator — sortable and filterable
- **Anomalies:** Dedicated sheet with anomaly summary table (type, count, highest risk) followed by full anomaly details sorted by risk (HIGH first), including investigation notes and dollar impact. Color-coded by risk level (red=HIGH, amber=MEDIUM, green=LOW)

**Optional Text Summary:** Draft summary with key findings, suggested root cause hypotheses, and recommendations for review.

**Why:** Excel enables sorting, filtering, and further analysis by downstream users. Multiple sheets serve different stakeholder needs. Conditional formatting (red/yellow/green based on variance magnitude) enables at-a-glance assessment.

### 7. Configurable Tolerance Thresholds

Set tolerances independently:
- **Percentage Threshold:** Default 5% (flag variances >5% change)
- **Absolute Threshold:** Default $500 (flag variances >$500 dollar amount)
- **Logic:** Flag if **either** threshold is exceeded (OR logic)

Override via command-line or interactive configuration to match organizational risk tolerance.

### 8. Trend Detection (Multi-Period)

When 3+ periods of data are available:
- Detect trend direction (increasing, decreasing, stable)
- Flag anomalous spikes or dips
- Calculate moving averages for smoothing seasonal patterns
- Identify cyclical patterns (e.g., seasonal overtime)

**Why:** Single-period variances may be normal; trends reveal processing changes or structural shifts.

## Workflow: Running Variance Analysis

### Step 1: Prepare & Upload Files

Upload two XLSX files:
1. `payroll_current.xlsx` — Current period payroll result export from SAP
2. `payroll_prior.xlsx` — Prior period payroll result export from SAP

Both files should contain the standard column structure described above. Exports can be generated from SAP Wage Type Reporter (PC00_M99_CWTR), payroll journal reports, or custom ALV queries.

**User-provided context:** When uploading files, provide the payroll area (e.g., "BW - Biweekly") and period (e.g., "January vs February 2026") if not already in the file columns. This helps the skill normalize comparisons and frame commentary correctly.

### Step 2: Run Analysis

Execute the analysis with optional threshold overrides:

```bash
python scripts/analyze_variance.py current_period.xlsx prior_period.xlsx \
  --threshold-pct 5 \
  --threshold-abs 500 \
  --output variance_results.json
```

### Step 3: Generate Report

Create formatted Excel and text outputs from analysis results:

```bash
python scripts/generate_variance_report.py variance_results.json \
  --output variance_report.xlsx
```

### Step 4: Review Output

- Open the Excel workbook
- Start with **Summary** sheet for high-level findings and risk assessment
- Dive into specific sheets (by wage type, cost center, etc.) as needed for detailed investigation
- Review **Anomalies** sheet and investigate flagged items before payroll go-live
- Use natural language commentary to inform stakeholder communication

## Configuration & Customization

**Tolerance Framework:**
- Default: Flag variances >5% OR >$500 absolute
- Organizational: Adjust to match risk tolerance (e.g., stricter for pre-production: 2% / $250, looser for routine reviews: 10% / $1000)
- Category-specific: Apply tighter thresholds to deductions (0.5%, $100) vs. earnings (5%, $500)

**Wage Type Categorization:**
Uses standard SAP US wage type ranges—see `references/wage-type-categories.md` for full catalog and typical variance explanations.

**Analysis Methodology:**
See `references/analysis-methodology.md` for detailed explanation of variance formulas, anomaly detection algorithms, trend analysis methods, and commentary template patterns.

## Example Scenarios

**Scenario 1: Post-Period Variance Review**
*User:* "I've got January and December payroll exports from SAP. Compare them and flag anything unusual."
*Output:* Complete variance workbook with all sheets populated, anomalies highlighted, natural language summaries, ready for executive review.

**Scenario 2: Cost Center Investigation**
*User:* "Why did labor costs jump in cost center 4500 this month? I need something I can send to the CFO."
*Output:* Focused analysis on cost center 4500, drill-down by wage type and employee, executive-ready summary document highlighting root causes.

**Scenario 3: Pre-Production Validation**
*User:* "We're about to go live with production payroll. Please compare these test results against last month's actual and flag anything that looks wrong before we finalize."
*Output:* Comparison report with HIGH/MEDIUM/LOW risk flags, go/no-go recommendation, employee-level anomalies requiring sign-off before go-live.

**Scenario 4: Custom Threshold Review**
*User:* "Compare these two payroll runs and flag anything over 10% change or more than $1000 difference. I need to review before we release tomorrow."
*Output:* Variance analysis using custom thresholds (10% / $1000), focused on high-impact items, urgency-appropriate formatting suitable for pre-production check.

## Technical Notes

- **Language:** Python 3.7+
- **Dependencies:** openpyxl (Excel I/O), json (data serialization)
- **Input:** XLSX format only (SAP payroll result export via Wage Type Reporter, ALV, or custom reports)
- **Output:** XLSX workbook + JSON intermediate data + optional Markdown summary
- **Edge Cases Handled:** Missing columns, empty cells, different column orderings, duplicate employees, zero prior amounts (division by zero), different currency codes

## References

Detailed methodology and reference materials:
- `references/wage-type-categories.md` — US payroll wage type catalog with typical SAP wage type codes, descriptions, and variance explanations
- `references/analysis-methodology.md` — Variance formulas, tolerance framework, threshold configuration, trend detection, root cause patterns, statistical anomaly detection

Scripts and execution:
- `scripts/analyze_variance.py` — Main analysis engine
- `scripts/generate_variance_report.py` — Report generation engine

Test data:
- `evals/files/payroll_current.xlsx` — Sample current period export (Feb 2026, 38 employees)
- `evals/files/payroll_prior.xlsx` — Sample prior period export (Jan 2026, 38 employees)
- `evals/files/payroll_combined.xlsx` — Combined format sample (10 employees)
- `evals/files/simulation_results.xlsx` — Simulation run sample (5 employees)
- `evals/files/prior_production.xlsx` — Production run sample (5 employees)

---

**Status:** Proof-of-Concept (Alpha 0.1.0) — This skill demonstrates variance analysis concepts and aims to assist with payroll review. All analysis outputs should be reviewed by qualified payroll professionals before use in production or for formal reporting.

**Last Updated:** 2026-02-17
**Version:** 1.2.0 — Implemented full anomaly detection suite: gross pay anomalies (>30% change), wage type appearance/disappearance, cost center shift detection, z-score statistical outlier detection. Added risk categorization (HIGH/MEDIUM/LOW) to all variance records. Added dedicated Anomalies sheet to Excel report with summary table, risk-colored detail rows, investigation notes, and dollar impact. Summary sheet now includes risk distribution and anomaly counts.
