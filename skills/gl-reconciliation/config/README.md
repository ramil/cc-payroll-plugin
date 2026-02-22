# Wage Type GL Mapping Configuration

## Overview

The `wage_type_mapping.json` file defines how SAP payroll wage types map to general ledger accounts. This is the file you customize to match your SAP backend configuration (T52EK/T52EL tables). You do not need to modify any Python code.

## How to Find Your Mappings in SAP

1. **T52EK** (Wage Type Table): Shows each wage type's symbolic account assignment
2. **T52EL** (GL Account Determination): Shows how symbolic accounts resolve to GL accounts
3. **RPCPRRU0** (Payroll Reconciliation Report): Shows actual postings with GL accounts

Run SE16 on these tables, or export a reconciliation report (RPCPRRU0) to see the wage type to GL account relationships your system uses.

## Editing the Mapping

Open `wage_type_mapping.json` in any text editor. Each entry under `"mappings"` follows this structure:

```json
"1000": {
  "description": "Regular Salary",
  "gl_account": "6100",
  "category": "gross",
  "type": "income"
}
```

**Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Human-readable label for the wage type |
| `gl_account` | Yes | Target GL account number from your chart of accounts |
| `category` | Yes | One of: `gross`, `deduction_pretax`, `deduction_posttax`, `tax_withholding`, `employer_tax`, `benefit_cost`, `net_pay` |
| `type` | Yes | One of: `income`, `expense`, `liability` |

## Common Customizations

### Changing a GL Account

If your company posts regular salary to GL 510000 instead of 6100:

```json
"1000": {
  "description": "Regular Salary",
  "gl_account": "510000",
  "category": "gross",
  "type": "income"
}
```

### Adding a New Wage Type

To add commissions (wage type 1040):

```json
"1040": {
  "description": "Commission",
  "gl_account": "6140",
  "category": "gross",
  "type": "income"
}
```

### Removing a Wage Type

Delete the entire entry block for that wage type code.

## Fallback Behavior

If this config file is missing or unreadable, the reconciliation script falls back to built-in US payroll defaults. Your reconciliation will still run, but the mapping may not match your SAP configuration.

## Validation

When the script loads the config, it checks for:
- Valid JSON syntax
- Required fields on each mapping entry (description, gl_account, category, type)
- Known category and type values

Warnings are printed for any issues, but reconciliation continues with available mappings.
