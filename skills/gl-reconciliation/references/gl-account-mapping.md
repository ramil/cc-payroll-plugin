# GL Account Mapping Reference

## Overview

This document provides comprehensive guidance on mapping SAP payroll wage types to general ledger
accounts. Payroll-to-GL mapping is a critical control point ensuring that all payroll calculations
are accurately reflected in the financial records.

## Standard US Payroll GL Account Structure

### Expense Accounts (6xxx series)

**Salary & Wage Expenses (61xx)**
- 6100: Regular Salary Expense
- 6110: Overtime Expense
- 6120: Shift Differential Expense
- 6130: Bonus Expense
- 6140: Commission Expense
- 6150: Severance Expense

**Payroll Tax Expenses (62xx)**
- 6200: FICA Social Security Expense (Employer)
- 6201: FICA Medicare Expense (Employer)
- 6202: FUTA Expense (Employer)
- 6203: SUI Expense (Employer)
- 6204: Workers Compensation Insurance Expense
- 6205: Unemployment Insurance Expense

**Benefit Expenses (62xx continued)**
- 6210: Health Insurance - Employer Contribution
- 6211: Dental Insurance - Employer Contribution
- 6212: Vision Insurance - Employer Contribution
- 6213: Life Insurance - Employer Contribution
- 6214: Disability Insurance - Employer Contribution
- 6215: 401k Employer Match
- 6216: Pension Expense
- 6217: Stock Purchase Plan - Employer

**Payroll Processing & Admin (63xx)**
- 6300: Payroll Processing Fees
- 6310: Background Check Fees
- 6320: Drug Testing Fees
- 6330: Training Expense - Payroll Related

### Liability Accounts (2xxx series)

**Income Tax Payable (21xx)**
- 2100: Federal Income Tax Payable
- 2110: Federal Income Tax - Employee Withholding
- 2111: Federal Income Tax - Backup Withholding
- 2120: State Income Tax Payable
- 2125: State Disability Insurance Payable
- 2130: Local Income Tax Payable

**Payroll Tax Payable (21xx continued)**
- 2140: FICA Social Security - Employee Withholding Payable
- 2141: FICA Medicare - Employee Withholding Payable
- 2142: FICA Social Security - Employer Payable
- 2143: FICA Medicare - Employer Payable
- 2144: FUTA Payable
- 2145: SUI Payable

**Benefit Payables (22xx)**
- 2210: Health Insurance Premium Payable - Employee
- 2211: Dental Insurance Premium Payable - Employee
- 2212: Vision Insurance Premium Payable - Employee
- 2213: Life Insurance Premium Payable - Employee
- 2214: Disability Insurance Premium Payable - Employee
- 2215: FSA Premium Payable
- 2216: HSA Premium Payable

**Deferred Compensation (23xx)**
- 2310: 401k Deferral Payable
- 2311: 403b Deferral Payable
- 2312: 457 Plan Deferral Payable
- 2313: 401k Loan Payable
- 2314: Pension Plan Payable
- 2315: Deferred Compensation Plan Payable

**Net Pay Liability (20xx)**
- 2000: Net Pay Payable
- 2001: Accrued Payroll - Regular Employees
- 2002: Accrued Payroll - Part-Time Employees
- 2003: Accrued Payroll - Contractors
- 2010: Paycheck Clearing Account (temporary)

### Clearing Accounts (9xxx series)

**Payroll Clearing (91xx)**
- 9100: Payroll Accrual/Reversal Clearing
- 9110: Retroactive Adjustment Clearing
- 9120: Off-Cycle Payroll Clearing
- 9130: Payroll Manual Entry Clearing

## Wage Type Mapping Framework

### Editable Configuration File

The wage type to GL account mapping used by the reconciliation scripts is stored in:

```
config/wage_type_mapping.json
```

This file ships with standard US payroll defaults. To match your SAP backend configuration, edit this JSON file with your actual wage type codes and GL account numbers. The tables below document the default mapping structure. See `config/README.md` for editing instructions.

### Wage Type Hierarchy

SAP Payroll uses a hierarchical wage type structure:

1. **Wage Type**: Basic code identifying the compensation element (1000, 1010, etc.)
2. **Symbolic Account**: Intermediate accounting classification (e.g., GROSS, FEDTAX, FICA_SS)
3. **GL Account**: Final general ledger posting account (6100, 2100, etc.)

### Core Wage Type Categories

#### Category: GROSS (Income)

| Wage Type | Description | Symbolic Account | GL Account | Notes |
|-----------|-------------|-----------------|-----------|-------|
| 1000 | Regular Salary | GROSS_SALARY | 6100 | Base hourly/salaried wages |
| 1010 | Overtime | GROSS_OT | 6110 | Hours > 40/week at 1.5x rate |
| 1020 | Shift Differential | GROSS_DIFF | 6120 | Premium for off-shift hours |
| 1030 | Bonus | GROSS_BONUS | 6130 | One-time or periodic bonus |
| 1040 | Commission | GROSS_COMM | 6140 | Sales commission |
| 1050 | Severance | GROSS_SEV | 6150 | Termination-related payment |

#### Category: DEDUCTION_PRETAX (Pre-tax deductions)

| Wage Type | Description | Symbolic Account | GL Account | Notes |
|-----------|-------------|-----------------|-----------|-------|
| 201 | Health Insurance - EE | BENEFIT_HEALTH_EE | 2210 | Employee portion of premiums |
| 202 | Dental Insurance - EE | BENEFIT_DENTAL_EE | 2211 | Employee portion of premiums |
| 203 | Vision Insurance - EE | BENEFIT_VISION_EE | 2212 | Employee portion of premiums |
| 204 | Life Insurance - EE | BENEFIT_LIFE_EE | 2213 | Employee portion of premiums |
| 205 | Disability Insurance - EE | BENEFIT_DIS_EE | 2214 | Employee portion of premiums |
| 301 | 401k Deferral | DEFERRED_401K | 2310 | Elective deferral under IRC 401(k) |
| 302 | FSA Deduction | DEFERRED_FSA | 2311 | Health Flexible Spending Account |
| 303 | HSA Deduction | DEFERRED_HSA | 2312 | Health Savings Account |
| 304 | 403b Deferral | DEFERRED_403B | 2311 | Tax-sheltered annuity deferral |

#### Category: TAX_WITHHOLDING (Taxes withheld)

| Wage Type | Description | Symbolic Account | GL Account | Notes |
|-----------|-------------|-----------------|-----------|-------|
| 101 | Federal Income Tax | FIT_WH | 2100 | Calculated via IRS tables |
| 102 | State Income Tax | SIT_WH | 2120 | Varies by employee home state |
| 103 | Local Income Tax | LIT_WH | 2130 | City/county level taxes |
| 104 | DC Commuter Tax | DCT_WH | 2131 | DC metro area commuter tax |
| 110 | FICA-SS Employee | FICA_SS_EE | 2140 | 6.2% of gross |
| 111 | FICA-Medicare Employee | FICA_MED_EE | 2141 | 1.45% of gross |
| 112 | FICA-Additional Medicare | FICA_ADDL_MED | 2142 | 0.9% of wages > threshold |

#### Category: EMPLOYER_TAX (Employer taxes)

| Wage Type | Description | Symbolic Account | GL Account | Notes |
|-----------|-------------|-----------------|-----------|-------|
| 401 | FICA-SS Employer | FICA_SS_ER | 6200 | 6.2% match to employee |
| 402 | FICA-Medicare Employer | FICA_MED_ER | 6201 | 1.45% match to employee |
| 403 | FUTA | FUTA_PAYABLE | 6202 | Federal unemployment tax |
| 404 | SUI | SUI_PAYABLE | 6203 | State unemployment insurance |
| 405 | Health Insurance - ER | BENEFIT_HEALTH_ER | 6210 | Employer contribution to premiums |
| 406 | Dental Insurance - ER | BENEFIT_DENTAL_ER | 6211 | Employer contribution to premiums |
| 407 | Vision Insurance - ER | BENEFIT_VISION_ER | 6212 | Employer contribution to premiums |
| 408 | Life Insurance - ER | BENEFIT_LIFE_ER | 6213 | Employer-paid life coverage |

#### Category: NET_PAY (Payment)

| Wage Type | Description | Symbolic Account | GL Account | Notes |
|-----------|-------------|-----------------|-----------|-------|
| 501 | Net Pay | NET_PAY | 2000 | Gross less all deductions |

### Symbolic Account Determination

Symbolic accounts provide an intermediate layer of abstraction. The mapping from wage type to
symbolic account is configured in SAP table **T52EK** (Wage Type Table).

**Table T52EK Key Fields:**
- LGART: Wage Type
- KALSF: Calculation Rule
- MCTCH: Accounting Class
- GEWK: Valuation Class (determines posting logic)

**Table T52EL: GL Account Determination**
- KALSF: Calculation Rule
- KTOPL: Chart of Accounts
- KONTO: GL Account
- KSTAT: Account Status
- KOART: Account Type (S=Salary, T=Tax, V=Deduction, E=Employer)

Example mapping chain:
```
Wage Type 1000 (Regular Salary)
  ↓
Symbolic Account GROSS_SALARY (T52EK)
  ↓
GL Account 6100 (T52EL, based on KALSF + Org Assignment)
```

### Employee Grouping & Account Determination

SAP Payroll supports employee grouping schemes to apply different GL accounts based on organizational
attributes. This is configured in table **T52EM** (Grouping Factor).

**Common Grouping Factors:**
- PERSG: Employee Group (active, contractor, temporary)
- PERSK: Employee Subgroup (management, hourly, salaried)
- KTABL: Costing Table (cost center, company code, plant)
- GSBER: Business Area (division, profit center)

Example: Health insurance may post to:
- 6210 for salaried employees (PERSK = 01)
- 6215 for hourly employees (PERSK = 02)
- 6220 for contractors (PERSK = 03)

## Cost Center Assignment

### Payroll Cost Center Assignment

Employee cost center assignment in payroll determines where costs are allocated. Key SAP tables:
- **PA0001**: Employee Master (KOSTL field = cost center)
- **PA0027**: Cost Center Assignment (time-dependent records)

The cost center can be overridden at the wage type level via table **T52AB** (Wage Type Cost Center).

### GL Cost Center Assignment

GL postings must match the cost center assignment in payroll. Validation points:

1. **GL Posting Rule**: Verify cost center derivation rules in payroll customization
2. **Batch GL Posting**: Check posting variant (RPCPRRU0) for cost center override logic
3. **Offset Account**: Verify that offsetting journal entries maintain cost center consistency

**Common Timing Issue**: Payroll calculates on PA0001 KOSTL at pay period end, but PA0027
may have effective-dated changes. GL posting uses PA0027 which may be different.

## Configuration Tables

### T52EK: Wage Type Definition

Controls wage type properties and symbolic account determination.

```
LGART = Wage Type (1000, 101, 401, etc.)
GEWK = Valuation Class (determines posting logic)
MCTCH = Accounting Class
NTAV = Net Wage Processing (X = include in net, blank = exclude)
```

### T52EL: Symbolic Account GL Account Link

Maps symbolic accounts to GL accounts by chart of accounts.

```
KALSF = Calculation Rule / Symbolic Account
KTOPL = Chart of Accounts (chart ID, e.g., 1000, 2000)
KONTO = GL Account (6100, 2100, etc.)
KSTAT = Account Status
KOART = Account Type (S/T/V/E)
```

### T52EM: Employee Grouping

Defines grouping factors for account determination variations.

```
GTMPL = Grouping Template
GTFLD = Grouping Field (PERSG, PERSK, GSBER)
GTVAL = Grouping Value
KONTO = GL Account for this group
```

### OBYE: GL Account Master

Standard SAP GL account master data.

```
SAKNR = GL Account (6100, 2100, etc.)
XALIN = Post automatically X
XOPEN = Account open X
MWSKZ = Tax Code
KNSM = Cost element
```

## Country-Specific Variations

### United States

- Tax calculation follows IRS withholding tables (updated annually)
- FICA Social Security: 6.2% employee, 6.2% employer (capped at $168,600 annually for 2024)
- FICA Medicare: 1.45% both, plus 0.9% employee only on wages > $200K
- FUTA: Federal unemployment, 0.6% after state credit (max $756 per employee annually)
- SUI: State unemployment, rate varies by state (0.5% - 5.4%) and industry experience rating

### Other Countries

Different countries have different tax structures. This document focuses on US configuration.
For other countries, refer to country-specific payroll documentation:
- Germany: RPRGLAC0 report, German payroll accounting tables
- UK: Tax Year in PLC, National Insurance tables
- Canada: Provincial tax codes, CPP/EI withholding

## Reconciliation Mapping Validation

### Pre-Reconciliation Checks

Before running reconciliation, validate the mapping configuration:

1. **Wage Type Configuration**
   - Verify T52EK entries for all active wage types
   - Check GEWK (valuation class) is set correctly
   - Confirm MCTCH (accounting class) matches your GL structure

2. **GL Account Mapping**
   - Verify T52EL entries for all calculation rules
   - Confirm GL account numbers are valid (OBYE)
   - Check account type (S/T/V/E) consistency

3. **Employee Grouping**
   - Verify T52EM grouping factors if used
   - Confirm grouping field values in employee master
   - Test account determination with sample employees

4. **Cost Center Configuration**
   - Verify cost center validity in CSKS/CSKA
   - Check PA0001 KOSTL assignments
   - Validate PA0027 time-dependent assignments

### Reconciliation Variance Investigation

When reconciliation variance is detected:

1. **Symbolic Account Check**
   - Query T52EK for wage type symbolic account
   - Verify calculation rule (KALSF) is assigned

2. **GL Account Lookup**
   - Query T52EL for symbolic account GL mapping
   - Verify GL account is open and posting enabled (OBYE)

3. **Cost Center Validation**
   - Compare payroll cost center to GL cost center posting
   - Check for overrides in T52AB
   - Verify PA0027 effective date vs payroll period

4. **Amount Verification**
   - Compare payroll wage type total to GL posting total
   - Check for multiple GL postings to same account (different cost centers)
   - Verify no amount rounding issues

## Common Mapping Issues & Solutions

### Issue 1: GL Account Not Found

**Symptom**: Reconciliation shows GL posting to account 0000 or blank

**Root Cause**: T52EL entry missing for symbolic account + chart of accounts combination

**Solution**:
1. Identify wage type and its symbolic account (T52EK, KALSF)
2. Query T52EL for missing KALSF + KTOPL entry
3. Create entry with appropriate GL account
4. Re-run reconciliation

### Issue 2: Amount Mismatch Between Payroll & GL

**Symptom**: Payroll shows $100K, GL shows $99.5K (consistent variance)

**Root Cause**: Payroll calculation includes certain wage types that GL posting excludes

**Solution**:
1. Verify which wage types are included in gross (T52EK, GEWK)
2. Check if wage type is excluded from GL posting (NTAV field)
3. Verify calculation rule cumulation logic (KALSF)
4. Update T52EK if necessary to include/exclude wage type from GL

### Issue 3: Cost Center Mismatch

**Symptom**: Payroll shows cost center 1000, GL posts to cost center 2000

**Root Cause**: Payroll cost center assignment differs from GL posting cost center

**Solution**:
1. Check PA0001 KOSTL for employee vs payroll date
2. Verify PA0027 effective dates span payroll period
3. Check T52AB for wage type-level cost center overrides
4. Check RPCPRRU0 posting variant for cost center derivation rules
5. If configured, verify grouping factor application

## Best Practices

1. **Annual Review**: Review and validate all GL account mappings at least annually
2. **Change Control**: Document any changes to T52EK, T52EL, T52EM configurations
3. **Test After Changes**: Run reconciliation on trial period before production use
4. **Audit Trail**: Maintain documentation of mapping decisions and rationale
5. **Reconciliation Documentation**: Store reconciliation reports and variance analysis with financial records
6. **Symbolic Account Consistency**: Use standardized symbolic account naming convention across all wage types
7. **GL Account Segregation**: Separate employee and employer tax accounts for clear GL reporting
8. **Cost Center Validation**: Validate cost center assignments quarterly, especially after organizational changes

## References

- SAP Payroll Configuration Guide
- SAP HR Module Documentation (PA, PY, PT modules)
- IRS Publication 15 (Circular E) - Employment Tax Guide
- SAP Tables: T52EK, T52EL, T52EM, T52AB, OBYE, PA0001, PA0027
- Related SAP Reports: RPCPRRU0, RPDKON00, PC00_M99_CIPE, RPCLSTB0
