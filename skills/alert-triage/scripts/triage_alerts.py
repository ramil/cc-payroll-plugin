#!/usr/bin/env python3
"""
SAP PCC Payroll Alert Triage Script

Analyzes PCC alert exports using the standard 5-column format and provides
intelligent categorization, priority assignment, and routing recommendations.

Input columns (standard PCC export from Alert Management / HRPY_PCC_ERRM):
    Validation Rule | Employee Name | Personnel Number | Processor | Status

Usage:
    python triage_alerts.py alerts.xlsx --deadline "2026-02-15" --output triage_results.json

"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter, defaultdict

import pandas as pd


class AlertTriageEngine:
    """Main alert triage analysis engine for PCC alert exports."""

    # ── Validation Rule → Classification Mapping ──
    # Maps human-readable validation rule names from PCC Manage Configuration
    # to alert domain, canonical type, blocking status, severity, and complexity.

    RULE_CLASSIFICATION = {
        # Data Quality domain
        "Employees with missing tax withholding data": {
            "category": "Data Quality",
            "alert_type": "Missing Tax Data",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 2 (Standard)",
        },
        "Employees with invalid bank account details": {
            "category": "Data Quality",
            "alert_type": "Invalid Bank Details",
            "blocking": True,
            "base_severity": "Medium",
            "complexity": "Level 2 (Standard)",
        },
        "Employees with missing time evaluation results": {
            "category": "Data Quality",
            "alert_type": "Time Data Discrepancies",
            "blocking": False,
            "base_severity": "Medium",
            "complexity": "Level 2 (Standard)",
        },
        "Employees missing cost center assignment": {
            "category": "Data Quality",
            "alert_type": "Cost Center Missing",
            "blocking": True,
            "base_severity": "Medium",
            "complexity": "Level 2 (Standard)",
        },
        "Employees with duplicate employee records": {
            "category": "Data Quality",
            "alert_type": "Duplicate Employee Records",
            "blocking": False,
            "base_severity": "Medium",
            "complexity": "Level 2 (Standard)",
        },
        "Employees with missing employee master data": {
            "category": "Data Quality",
            "alert_type": "Missing Employee Data",
            "blocking": False,
            "base_severity": "Low",
            "complexity": "Level 1 (Simple)",
        },
        # Compliance domain
        "Employees with garnishment order validation errors": {
            "category": "Compliance",
            "alert_type": "Garnishment Error",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with missing state tax jurisdiction": {
            "category": "Compliance",
            "alert_type": "Tax Reciprocity Violation",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with expired work authorization documents": {
            "category": "Compliance",
            "alert_type": "Benefits Compliance Gap",
            "blocking": False,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with tax reciprocity violation": {
            "category": "Compliance",
            "alert_type": "Tax Reciprocity Violation",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with regulatory filing delay": {
            "category": "Compliance",
            "alert_type": "Regulatory Filing Delay",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with benefits compliance gap": {
            "category": "Compliance",
            "alert_type": "Benefits Compliance Gap",
            "blocking": False,
            "base_severity": "Medium",
            "complexity": "Level 2 (Standard)",
        },
        "Employees with wage law violation": {
            "category": "Compliance",
            "alert_type": "Wage Law Violation",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        # Processing domain
        "Employees exceeding overtime hours threshold": {
            "category": "Processing",
            "alert_type": "Overtime Threshold Exceeded",
            "blocking": False,
            "base_severity": "Low",
            "complexity": "Level 1 (Simple)",
        },
        "Employees with retroactive change pending processing": {
            "category": "Processing",
            "alert_type": "Retroactive Change",
            "blocking": False,
            "base_severity": "Medium",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with unprocessed infotype changes": {
            "category": "Processing",
            "alert_type": "Retroactive Change",
            "blocking": False,
            "base_severity": "Medium",
            "complexity": "Level 2 (Standard)",
        },
        "Employees with duplicate wage type entries": {
            "category": "Processing",
            "alert_type": "Wage Type Collision",
            "blocking": False,
            "base_severity": "Medium",
            "complexity": "Level 2 (Standard)",
        },
        "Employees with payroll lock condition": {
            "category": "Processing",
            "alert_type": "Payroll Lock Condition",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with system validation error": {
            "category": "Processing",
            "alert_type": "System Validation Error",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with batch processing failure": {
            "category": "Processing",
            "alert_type": "Batch Processing Failure",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        # Financial domain
        "Employees with negative net pay results": {
            "category": "Financial",
            "alert_type": "Negative Net Pay",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with gross pay variance exceeding threshold": {
            "category": "Financial",
            "alert_type": "Payroll Accrual Variance",
            "blocking": False,
            "base_severity": "Medium",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with GL posting variance detected": {
            "category": "Financial",
            "alert_type": "GL Posting Error",
            "blocking": False,
            "base_severity": "Medium",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with benefit deduction exceeding net pay": {
            "category": "Financial",
            "alert_type": "Benefit Calculation Error",
            "blocking": True,
            "base_severity": "High",
            "complexity": "Level 3 (Complex)",
        },
        "Employees with cost center misallocation": {
            "category": "Financial",
            "alert_type": "Cost Center Misallocation",
            "blocking": False,
            "base_severity": "Medium",
            "complexity": "Level 2 (Standard)",
        },
        "Employees with budget variance alert": {
            "category": "Financial",
            "alert_type": "Budget Variance Alert",
            "blocking": False,
            "base_severity": "Low",
            "complexity": "Level 1 (Simple)",
        },
    }

    # Default classification for unrecognized validation rules
    DEFAULT_CLASSIFICATION = {
        "category": "Processing",
        "alert_type": "Unknown",
        "blocking": False,
        "base_severity": "Medium",
        "complexity": "Level 2 (Standard)",
    }

    # Fuzzy keyword → canonical rule name for partial matching
    FUZZY_KEYWORDS = {
        "missing tax": "Employees with missing tax withholding data",
        "tax withholding": "Employees with missing tax withholding data",
        "bank account": "Employees with invalid bank account details",
        "bank detail": "Employees with invalid bank account details",
        "time evaluation": "Employees with missing time evaluation results",
        "time data": "Employees with missing time evaluation results",
        "cost center missing": "Employees missing cost center assignment",
        "missing cost center": "Employees missing cost center assignment",
        "garnishment": "Employees with garnishment order validation errors",
        "state tax": "Employees with missing state tax jurisdiction",
        "tax jurisdiction": "Employees with missing state tax jurisdiction",
        "work authorization": "Employees with expired work authorization documents",
        "overtime": "Employees exceeding overtime hours threshold",
        "retroactive change": "Employees with retroactive change pending processing",
        "infotype change": "Employees with unprocessed infotype changes",
        "wage type": "Employees with duplicate wage type entries",
        "negative net pay": "Employees with negative net pay results",
        "gross pay variance": "Employees with gross pay variance exceeding threshold",
        "gl posting": "Employees with GL posting variance detected",
        "benefit deduction": "Employees with benefit deduction exceeding net pay",
        "duplicate employee": "Employees with duplicate employee records",
        "payroll lock": "Employees with payroll lock condition",
        "system validation": "Employees with system validation error",
        "batch processing": "Employees with batch processing failure",
        "regulatory filing": "Employees with regulatory filing delay",
        "wage law": "Employees with wage law violation",
        "tax reciprocity": "Employees with tax reciprocity violation",
        "budget variance": "Employees with budget variance alert",
        "cost center misallocation": "Employees with cost center misallocation",
    }

    # SLA timelines (minutes)
    SLA_TIMELINES = {
        "P1": {"response": 15, "resolution": 60},
        "P2": {"response": 60, "resolution": 240},
        "P3": {"response": 240, "resolution": 1440},
        "P4": {"response": 1440, "resolution": 2880},
    }

    # Domain → team routing
    ROUTING_MAP = {
        "Data Quality": "Data Operations Team",
        "Compliance": "Compliance & Legal Team",
        "Processing": "Payroll Operations Team",
        "Financial": "Finance & Reconciliation Team",
    }

    # Severity → base priority score
    SEVERITY_SCORES = {"High": 35, "Medium": 20, "Low": 10}

    # Required PCC export columns
    REQUIRED_COLUMNS = [
        "Validation Rule",
        "Employee Name",
        "Personnel Number",
        "Processor",
        "Status",
    ]

    # Flexible column name aliases for normalizing non-standard exports
    COLUMN_ALIASES = {
        "validation rule": "Validation Rule",
        "rule": "Validation Rule",
        "validation_rule": "Validation Rule",
        "alert_type": "Validation Rule",
        "alert type": "Validation Rule",
        "employee name": "Employee Name",
        "employee_name": "Employee Name",
        "emp_name": "Employee Name",
        "name": "Employee Name",
        "personnel number": "Personnel Number",
        "personnel_number": "Personnel Number",
        "pernr": "Personnel Number",
        "emp_id": "Personnel Number",
        "employee_id": "Personnel Number",
        "employee id": "Personnel Number",
        "processor": "Processor",
        "assigned_to": "Processor",
        "assigned to": "Processor",
        "assignee": "Processor",
        "owner": "Processor",
        "status": "Status",
        "alert_status": "Status",
        "alert status": "Status",
        "workflow_status": "Status",
        "workflow status": "Status",
    }

    def __init__(self, deadline: datetime = None):
        self.deadline = deadline or (datetime.now() + timedelta(days=7))
        self.alerts = []
        self.triaged_alerts = []
        self.root_cause_groups = {}

    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names to standard PCC export format using aliases."""
        rename_map = {}
        for col in df.columns:
            key = col.lower().strip()
            canonical = self.COLUMN_ALIASES.get(key)
            if canonical and col != canonical:
                rename_map[col] = canonical
        if rename_map:
            df = df.rename(columns=rename_map)
        return df

    def load_alerts_from_excel(self, filepath: str) -> int:
        """Load alerts from PCC export XLSX (5-column format).

        Expected columns:
            Validation Rule | Employee Name | Personnel Number | Processor | Status

        Returns:
            Number of alerts loaded
        """
        try:
            df = pd.read_excel(filepath)
        except Exception as e:
            print(f"Error reading Excel file: {e}", file=sys.stderr)
            sys.exit(1)

        df = self._normalize_columns(df)

        missing = [c for c in self.REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            print(
                f"Error: Missing required columns: {missing}\n"
                f"Found columns: {list(df.columns)}\n"
                f"Expected: {self.REQUIRED_COLUMNS}",
                file=sys.stderr,
            )
            sys.exit(1)

        for idx, row in df.iterrows():
            validation_rule = str(row["Validation Rule"]).strip()
            processor = (
                str(row["Processor"]).strip()
                if pd.notna(row["Processor"]) else ""
            )
            status = (
                str(row["Status"]).strip()
                if pd.notna(row["Status"]) else "Open"
            )

            self.alerts.append({
                "id": f"ALR{idx + 1:06d}",
                "validation_rule": validation_rule,
                "employee_name": (
                    str(row["Employee Name"]).strip()
                    if pd.notna(row["Employee Name"]) else ""
                ),
                "personnel_number": (
                    str(row["Personnel Number"]).strip()
                    if pd.notna(row["Personnel Number"]) else ""
                ),
                "processor": processor,
                "status": status,
            })

        return len(self.alerts)

    def _classify_alert(self, validation_rule: str) -> Dict[str, Any]:
        """Classify an alert by its validation rule name.

        First tries exact match, then fuzzy keyword match.
        Falls back to DEFAULT_CLASSIFICATION if no match found.
        """
        if validation_rule in self.RULE_CLASSIFICATION:
            return self.RULE_CLASSIFICATION[validation_rule]

        rule_lower = validation_rule.lower()
        for keyword, canonical_rule in self.FUZZY_KEYWORDS.items():
            if keyword in rule_lower:
                return self.RULE_CLASSIFICATION[canonical_rule]

        return self.DEFAULT_CLASSIFICATION.copy()

    def _calculate_priority(
        self, classification: Dict, alert: Dict, rule_count: int
    ) -> str:
        """Calculate priority (P1-P4) based on multiple factors.

        Scoring:
            Severity:           0-35 pts (High=35, Medium=20, Low=10)
            Blocking status:    0-15 pts
            Deadline proximity: 0-30 pts
            Volume (same rule): 0-20 pts
            Unassigned+Open:    0-5  pts
        """
        score = 0

        score += self.SEVERITY_SCORES.get(classification["base_severity"], 20)

        if classification["blocking"]:
            score += 15

        days_to_deadline = (self.deadline - datetime.now()).days
        if days_to_deadline < 1:
            score += 30
        elif days_to_deadline < 2:
            score += 25
        elif days_to_deadline < 7:
            score += 15
        elif days_to_deadline < 14:
            score += 5

        if rule_count >= 10:
            score += 20
        elif rule_count >= 5:
            score += 15
        elif rule_count >= 3:
            score += 10

        if alert["status"] == "Open" and not alert["processor"]:
            score += 5

        if score >= 65:
            return "P1"
        elif score >= 50:
            return "P2"
        elif score >= 35:
            return "P3"
        else:
            return "P4"

    def triage(self) -> Dict[str, Any]:
        """Execute triage on all loaded alerts.

        Returns:
            Complete triage results dictionary
        """
        rule_counts = Counter(a["validation_rule"] for a in self.alerts)

        for alert in self.alerts:
            classification = self._classify_alert(alert["validation_rule"])
            priority = self._calculate_priority(
                classification, alert, rule_counts[alert["validation_rule"]]
            )
            primary_team = self.ROUTING_MAP.get(
                classification["category"], "Payroll Operations Team"
            )
            sla = self.SLA_TIMELINES[priority]
            sla_deadline = (
                datetime.now() + timedelta(minutes=sla["resolution"])
            ).strftime("%Y-%m-%d %H:%M")

            self.triaged_alerts.append({
                "id": alert["id"],
                "validation_rule": alert["validation_rule"],
                "alert_type": classification["alert_type"],
                "category": classification["category"],
                "priority": priority,
                "severity": classification["base_severity"],
                "blocking": classification["blocking"],
                "employee_name": alert["employee_name"],
                "personnel_number": alert["personnel_number"],
                "processor": alert["processor"],
                "status": alert["status"],
                "primary_team": primary_team,
                "complexity": classification["complexity"],
                "sla_response_min": sla["response"],
                "sla_resolution_min": sla["resolution"],
                "sla_deadline": sla_deadline,
            })

        self._group_by_root_cause()
        return self._generate_results()

    def _group_by_root_cause(self):
        """Group triaged alerts by validation rule for batch processing."""
        groups = defaultdict(list)
        for alert in self.triaged_alerts:
            groups[alert["validation_rule"]].append(alert)

        self.root_cause_groups = {}
        for rule, alerts in groups.items():
            count = len(alerts)
            individual_time = count * 30
            if count >= 3:
                batch_time = 30 + (count - 1) * 5
                savings_pct = int(
                    ((individual_time - batch_time) / individual_time) * 100
                )
                batch_eligible = True
            else:
                batch_time = individual_time
                savings_pct = 0
                batch_eligible = False

            self.root_cause_groups[rule] = {
                "count": count,
                "alert_ids": [a["id"] for a in alerts],
                "batch_eligible": batch_eligible,
                "individual_time_min": individual_time,
                "batch_time_min": batch_time,
                "savings_pct": savings_pct,
                "category": alerts[0]["category"],
                "alert_type": alerts[0]["alert_type"],
            }

    def _generate_results(self) -> Dict[str, Any]:
        """Generate complete triage results."""
        priority_counts = Counter(a["priority"] for a in self.triaged_alerts)
        category_counts = Counter(a["category"] for a in self.triaged_alerts)
        status_counts = Counter(a["status"] for a in self.triaged_alerts)
        team_counts = Counter(a["primary_team"] for a in self.triaged_alerts)
        blocking_count = sum(1 for a in self.triaged_alerts if a["blocking"])
        open_unassigned = sum(
            1 for a in self.triaged_alerts
            if a["status"] == "Open" and not a["processor"]
        )

        proc_workload = defaultdict(
            lambda: {"total": 0, "p1": 0, "p2": 0, "p3": 0, "p4": 0, "open": 0}
        )
        for a in self.triaged_alerts:
            proc = a["processor"] if a["processor"] else "(Unassigned)"
            proc_workload[proc]["total"] += 1
            proc_workload[proc][a["priority"].lower()] += 1
            if a["status"] == "Open":
                proc_workload[proc]["open"] += 1

        batch_opportunities = sorted(
            [
                {
                    "root_cause": rule,
                    "count": g["count"],
                    "alert_ids": g["alert_ids"],
                    "individual_time_min": g["individual_time_min"],
                    "batch_time_min": g["batch_time_min"],
                    "savings_pct": g["savings_pct"],
                }
                for rule, g in self.root_cause_groups.items()
                if g["batch_eligible"]
            ],
            key=lambda x: x["count"],
            reverse=True,
        )

        return {
            "summary": {
                "total_alerts": len(self.triaged_alerts),
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "payroll_deadline": self.deadline.strftime("%Y-%m-%d"),
                "days_to_deadline": (self.deadline - datetime.now()).days,
                "blocking_alerts": blocking_count,
                "open_unassigned": open_unassigned,
            },
            "priority_counts": dict(priority_counts),
            "category_counts": dict(category_counts),
            "status_counts": dict(status_counts),
            "team_counts": dict(team_counts),
            "triaged": self.triaged_alerts,
            "root_cause_groups": {
                k: dict(v) for k, v in self.root_cause_groups.items()
            },
            "batch_opportunities": batch_opportunities,
            "processor_workload": dict(proc_workload),
            "sla_reference": self.SLA_TIMELINES,
        }


def main():
    parser = argparse.ArgumentParser(
        description="Triage SAP PCC alert exports (standard 5-column format)"
    )
    parser.add_argument("input_file", help="Path to PCC alert export XLSX")
    parser.add_argument(
        "--deadline",
        default=None,
        help="Payroll deadline date (YYYY-MM-DD). Default: 7 days from now",
    )
    parser.add_argument(
        "--output",
        default="triage_results.json",
        help="Output file for triage results (JSON)",
    )

    args = parser.parse_args()

    if not Path(args.input_file).exists():
        print(f"Error: Input file not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    deadline = None
    if args.deadline:
        try:
            deadline = datetime.strptime(args.deadline, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid deadline format. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    engine = AlertTriageEngine(deadline=deadline)

    print(f"Loading alerts from {args.input_file}...", file=sys.stderr)
    count = engine.load_alerts_from_excel(args.input_file)
    print(f"Loaded {count} alerts", file=sys.stderr)

    print("Executing triage analysis...", file=sys.stderr)
    results = engine.triage()

    with open(Path(args.output), "w") as f:
        json.dump(results, f, indent=2)

    print(f"Triage results written to {args.output}", file=sys.stderr)

    print("\n=== TRIAGE SUMMARY ===", file=sys.stderr)
    s = results["summary"]
    print(f"Total Alerts: {s['total_alerts']}", file=sys.stderr)
    print(f"Blocking Alerts: {s['blocking_alerts']}", file=sys.stderr)
    print(f"Open & Unassigned: {s['open_unassigned']}", file=sys.stderr)
    print(f"Days to Deadline: {s['days_to_deadline']}", file=sys.stderr)
    print("\nPriority Distribution:", file=sys.stderr)
    for p in ["P1", "P2", "P3", "P4"]:
        print(f"  {p}: {results['priority_counts'].get(p, 0)}", file=sys.stderr)
    print("\nCategory Breakdown:", file=sys.stderr)
    for cat, cnt in results["category_counts"].items():
        print(f"  {cat}: {cnt}", file=sys.stderr)
    print("\nRouting Distribution:", file=sys.stderr)
    for team, cnt in results["team_counts"].items():
        print(f"  {team}: {cnt}", file=sys.stderr)
    if results["batch_opportunities"]:
        print(
            f"\nBatch Opportunities: {len(results['batch_opportunities'])}",
            file=sys.stderr,
        )
        for opp in results["batch_opportunities"]:
            print(
                f"  {opp['root_cause']}: {opp['count']} alerts, "
                f"{opp['savings_pct']}% savings",
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
