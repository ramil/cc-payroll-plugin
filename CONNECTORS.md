# SAP PCC Payroll Plugin — Connectors

This plugin works with **file exports** from SAP Payroll Control Center. No direct SAP API connections or MCP servers are required.

## Data Flow

| Step | Source | Method | Format |
|------|--------|--------|--------|
| Export | SAP PCC / SAP GUI | Manual export via ALV grid or PC_PAYRESULT | XLSX |
| Upload | Claude Cowork | Drag-and-drop or file select | XLSX |
| Analysis | Plugin scripts | Automated via Python (openpyxl) | JSON → XLSX |

## Future Connectors (Phase 2+)

| Category | Placeholder | Potential Servers | Status |
|----------|-------------|-------------------|--------|
| ERP | ~~erp | SAP S/4HANA, SAP HCM | Planned |
| HRIS | ~~hris | SuccessFactors, Workday | Planned |
| Chat | ~~chat | Slack, Microsoft Teams | Planned |
| Ticketing | ~~ticketing | ServiceNow, Jira | Planned |
