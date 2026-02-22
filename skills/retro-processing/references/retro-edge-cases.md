# Edge Case Catalog for Retroactive Payroll Processing

## Table of Contents
1. [Year-Boundary Crossings](#year-boundary-crossings)
2. [Terminated Employee Retro](#terminated-employee-retro)
3. [Multiple Retro Periods](#multiple-retro-periods)
4. [Tax Jurisdiction Changes](#tax-jurisdiction-changes)
5. [Wage Type Configuration Changes](#wage-type-configuration-changes)
6. [Missing Master Data](#missing-master-data)
7. [Time Evaluation Conflicts](#time-evaluation-conflicts)
8. [Benefit Plan Changes During Retro Period](#benefit-plan-changes-during-retro-period)

---

## Year-Boundary Crossings

### Description

Year-boundary crossing occurs when a retroactive change spans from one calendar year into another. This is complex because tax tables, GL account structures, and payroll configurations often differ between years.

**Example Scenario:**
```
Current Date: March 2024
Retroactive Change Effective: October 2023
Affected Periods: October 2023, November 2023, December 2023, January 2024, February 2024, March 2024
Year Boundary: Between December 2023 and January 2024
```

### Specific Issues

#### Issue 1: Different Tax Tables

**Problem:**
- 2023 tax tables are different from 2024 tax tables
- IRS updates standard deduction, tax brackets, FICA rates annually
- Retro recalculation must use correct table for each period

**Example:**
```
Federal Tax Calculation:
2023 Standards:
  Standard Deduction: $13,850 (single)
  Tax Brackets: 10% on $0-$11,000; 12% on $11,000-$44,725

2024 Standards:
  Standard Deduction: $14,600 (single)
  Tax Brackets: 10% on $0-$11,600; 12% on $11,600-$47,150

Employee paid:
  2023: Based on $13,850 deduction and lower brackets
  2024: Based on $14,600 deduction and higher brackets

Retro change (salary increase):
  Oct-Dec 2023: Use 2023 tax table
  Jan-Mar 2024: Use 2024 tax table

If wrong table used for 2024 periods, tax withholding is incorrect.
```

**SAP Handling:**
- SAP stores tax table versions per calendar year
- Retro processing must reference correct year's table
- PCR wage type calculations must check period date for table selection

#### Issue 2: GL Account Structure Changes

**Problem:**
- Company may reorganize GL accounts between years
- Old GL account 4100 may be retired, replaced with 4110
- Account mapping changes from 2023 to 2024

**Example:**
```
GL Account Changes:
2023: GL 4100 (All Salary Expense)
2024: GL 4110 (Salary - Regular), GL 4115 (Salary - Supplement)

Retro salary change for Oct 2023 - Mar 2024:
  Oct-Dec 2023: Post to GL 4100 (per 2023 structure)
  Jan-Mar 2024: Post to GL 4110 (per 2024 structure)

Without year-aware posting, all postings may go to GL 4100,
leaving GL 4110 undersaturated in 2024 records.
```

**SAP Handling:**
- GL account mapping should be time-effective
- Retro posting engine must check GL mapping date
- May need manual posting adjustments if structure changed

#### Issue 3: Paid Time Off (PTO) Accrual Reset

**Problem:**
- PTO accruals typically reset on calendar year boundary
- Sick leave, vacation days may reset January 1
- Retro changes may affect accrual balances

**Example:**
```
Employee: E001
2023 Balance: 20 vacation days (at start of year)
Used: 15 days
Remaining at 12/31/2023: 5 days
Rollover to 2024: 5 days (per policy)

2024 New Accrual: 20 days
Balance at 1/1/2024: 5 + 20 = 25 days

Retro Change (Nov 2023): Employee status change (part-time to full-time)
Impact: Should have accrued more days in 2023 retroactively

Complication:
- If retro increases 2023 accrual, does it increase 12/31/2023 balance?
- If so, does it increase 2024 rollover?
- System accrual may have already been paid out or scheduled

Resolution:
- Typically, retroactive accrual changes require manual adjustment
- Cannot automatically recalculate accrual for entire year
- May require HR intervention to adjust 2024 balance
```

**SAP Handling:**
- Retro affects wage types (/100, /103, etc.) but not accrual balances
- Accrual changes are separate from payroll retro
- Require manual time management adjustments

#### Issue 4: Payroll Period Definition Changes

**Problem:**
- Payroll period definitions may change year-to-year
- 2023 may have 26 biweekly periods
- 2024 may reorganize into 24 bimonthly periods
- Retro periods don't align with new structure

**Example:**
```
2023 Payroll Structure:
  Period 1: 12/27/2022 - 01/09/2023
  Period 2: 01/10/2023 - 01/23/2023
  ...
  Period 26: 12/12/2023 - 12/25/2023

2024 Payroll Structure:
  Period 1: 01/01/2024 - 01/15/2024
  Period 2: 01/16/2024 - 01/31/2024
  ...

Retro for Oct-Dec 2023 in Jan 2024:
  Must use 2023 period structure for Oct-Dec
  Must use 2024 period structure for Jan-Dec (if affected)
```

**SAP Handling:**
- SAP stores period definitions per year
- Retro must use correct period calendar for each year
- May require manual period mapping if structures differ significantly

### Resolution Procedures

**Before Year-Boundary Retro:**

1. **Audit Tax Tables:**
   - [ ] Verify correct 2023 tax table for Oct-Dec periods
   - [ ] Verify correct 2024 tax table for Jan-Mar periods
   - [ ] If tax tables changed, confirm new rates are in SAP
   - [ ] Run test calculation on sample employee to verify

2. **Audit GL Accounts:**
   - [ ] Verify GL account codes for 2023 posting
   - [ ] Verify GL account codes for 2024 posting
   - [ ] If accounts changed, ensure wage type mapping is updated
   - [ ] Run GL posting simulation to preview accounts

3. **Check Accruals:**
   - [ ] Review accrual rules for Dec 31 year-end cutoff
   - [ ] Check if retro affects accrual balances (usually doesn't)
   - [ ] If affected, plan manual HR adjustment
   - [ ] Notify HR of any accrual impacts

4. **Check Period Structure:**
   - [ ] Verify period calendar is defined for both years
   - [ ] Confirm period dates are continuous across year boundary
   - [ ] Check for any missing or overlapping periods

5. **Simulation:**
   - [ ] Run payroll simulation for Oct 2023 - Mar 2024 (full range)
   - [ ] Check simulation results for both years
   - [ ] Verify tax amounts are reasonable for both years
   - [ ] Review GL posting by account and year

**During Year-Boundary Retro:**

1. **Execute in Correct Sequence:**
   - Process earliest affected period first (Oct 2023)
   - Process through year boundary (Dec 2023 → Jan 2024)
   - Process latest affected period last (Mar 2024)
   - Do NOT skip periods

2. **Validate After Each Period Group:**
   - Validate 2023 periods (Oct-Dec) completely
   - Then validate 2024 periods (Jan-Mar)
   - Check GL accounts for each year separately
   - Verify tax amounts for each year

3. **Monitor GL Postings:**
   - Track GL postings by account AND by year
   - Ensure 2023 postings go to 2023-valid accounts
   - Ensure 2024 postings go to 2024-valid accounts
   - Watch for posting to retired accounts

**After Year-Boundary Retro:**

1. **Reconcile by Year:**
   - [ ] Total 2023 retro amount (Oct-Dec)
   - [ ] Total 2024 retro amount (Jan-Mar)
   - [ ] Verify tax amounts are appropriate for each year
   - [ ] Check GL accounts are correctly coded per year

2. **Validate Tax Compliance:**
   - [ ] Verify 2023 tax liability matches retro postings
   - [ ] Verify 2024 tax liability matches retro postings
   - [ ] Confirm no double-posting of taxes
   - [ ] Ensure year-end 2023 tax totals are correct

3. **Employee Communication:**
   - Explain that retro spans two years
   - Show separate calculations for each year
   - Clarify when payment will be made

---

## Terminated Employee Retro

### Description

Processing retroactive payroll changes for employees who have been terminated is complex and risky. Once an employee is terminated, their payroll is considered final. Retro changes introduce complications with ERD (Employee Retirement Date), final pay, and tax compliance.

### Key Issues

#### Issue 1: ERD (Employee Retirement Date) Restrictions

**Problem:**
- ERD marks the official last day of employment
- SAP typically locks payroll after ERD
- Retro changes for periods after ERD may be blocked by system

**Example:**
```
Employee: E001, John Doe
Hired: 01/01/2020
Terminated: 12/31/2023 (ERD = 12/31/2023)
Last Payroll: December 2023

Scenario 1: Retro for October 2023 (BEFORE ERD)
  Retro Change: Salary increase approved for Oct, but implementation was forgotten
  RRDAT: October 2023
  Status: ALLOWED (Oct 2023 is before ERD)
  Processing: Can be executed normally

Scenario 2: Retro for December 2023 (ON ERD Month)
  Retro Change: Correct error in December final pay
  RRDAT: December 2023
  Status: DEPENDS (policies vary)
  Processing: Some systems allow, some require special override

Scenario 3: Retro for January 2024 (AFTER ERD)
  Retro Change: Trying to correct something in Jan 2024
  Status: BLOCKED (employee already terminated)
  Processing: Cannot be executed without special procedures
```

**SAP Behavior:**
- Transaction PU03 may show warning if RRDAT is after ERD
- Retro recalculation may fail with error "Employee inactive in period"
- Some configurations allow override, but require additional authorization

**Resolution:**
- Retro for periods BEFORE ERD: Standard processing
- Retro for ERD month: May require HR approval override
- Retro for periods AFTER ERD: Requires special reversal and reactivation procedures (see below)

#### Issue 2: Reinstatement vs. New Hire

**Problem:**
- If terminated employee returns, is it a reinstatement or new hire?
- Retro to pre-termination period affects reinstatement date logic
- Benefits and seniority may be impacted

**Example:**
```
Employee: E002, Jane Smith
Original Hire: 01/01/2022
Terminated: 06/30/2023 (ERD = 06/30/2023)

Scenario: Retro adjustment needed for May 2023 (before termination)

If processing as reinstatement:
  Create new hire record with hire date = 07/01/2023
  Process retro for May 2023 as if employee was still active

Issue: System may see May 2023 as "before hire date" for new record
  May 2023 is 2 months before new hire date of 07/01/2023
  System may reject payroll calculation

Resolution:
  Temporarily set hire date to match retro period (back to 01/01/2022)
  Process retro
  Then reset hire date back to 07/01/2023 if needed
```

#### Issue 3: Final Pay Complications

**Problem:**
- Final pay (December 2023 for 12/31 termination) includes special items
  - Payout of unused vacation
  - Payoff of benefits
  - Final bonus or separation package
- Retro to final pay period affects these items

**Example:**
```
December 2023 Final Pay:
  Regular Salary (/100):           5000.00
  Vacation Payout (/110):          3000.00  (10 days × $300)
  Health Insurance Payoff (/200):   -100.00
  Final Check Net:                 7900.00

Retro Scenario:
  Change: Salary increase to $5200 effective Oct 2023

Retro Recalculation of Dec:
  Regular Salary (/100):           5200.00  (increased)
  Vacation Payout (/110):          3000.00  (unchanged)
  Health Insurance Payoff (/200):   -100.00  (unchanged)
  Recalc Total:                    8100.00
  /551 Difference:                  200.00

Issue: Who receives the $200 extra?
  - Already terminated, no future paycheck
  - May need to issue separate check
  - Tax implications (bonus vs. wage payment)
  - Final paystub needs to reflect adjustment
```

**Resolution:**
- Review final pay structure before authorizing retro
- Verify unused vacation and benefits will still be paid correctly
- Plan for separate check if retro affects final pay
- Update final paystub to show /551 adjustment
- Confirm with HR and employee

#### Issue 4: Pension/Benefit Vesting

**Problem:**
- Retro to periods near termination may affect pension contributions
- Vesting may be tied to service calculation
- Retro may retroactively change vesting percentage

**Example:**
```
Employee Pension Vesting:
  Years 0-2: 0%
  Years 2-5: 20% per year
  After 5 years: 100%

Employee E003: Hired 01/01/2019, Terminated 06/30/2023 (4.5 years)
Original Vesting: 80% (4 years × 20%)
Pension Contributions Vested: $80,000 (80% of $100,000)

Retro Scenario:
  Change: Correct hire date from 01/01/2019 to 12/01/2018 (off-by-one error)
  New Tenure: 5 years 7 months
  New Vesting: 100%
  New Vested Amount: $100,000 (full contribution)

Impact:
  Pension plan must be notified
  Vesting percentage is recalculated
  Employee receives additional $20,000 vesting
  May require coordination with pension plan administrator
```

**Resolution:**
- Check if retro affects tenure calculation
- Alert Pension/Benefits team before processing
- May require separate pension plan adjustment
- Coordinate with plan administrator on vesting changes

### Resolution Procedures

**Before Terminated Employee Retro:**

1. **Verify ERD and Status:**
   - [ ] Confirm employee's ERD date
   - [ ] Verify RRDAT is on or before ERD month
   - [ ] Check if employee is rehired (reinstatement scenario)
   - [ ] Confirm employee status in HR system

2. **Review Final Pay:**
   - [ ] Obtain copy of final December payslip
   - [ ] Identify special payments (vacation payout, bonuses, etc.)
   - [ ] Verify benefits were properly paid off
   - [ ] Determine if retro will affect final pay items

3. **Assess Pension/Benefits Impact:**
   - [ ] Check if retro affects vesting calculation
   - [ ] Alert pension plan administrator
   - [ ] Get written approval for vesting changes (if applicable)
   - [ ] Document plan adjustment requirements

4. **HR Coordination:**
   - [ ] Notify HR of retro before processing
   - [ ] Get HR approval for ERD-month retro (if needed)
   - [ ] Coordinate employee communication
   - [ ] Verify employment status is correct in system

5. **Simulation:**
   - [ ] Simulate retro for pre-ERD periods
   - [ ] Review simulation results carefully
   - [ ] Check for system errors or warnings
   - [ ] Validate retro amount calculations

**Handling Post-ERD Retro (Special Procedure):**

If retro MUST be applied to periods after ERD:

1. **Reactivate Employee:**
   - Set new hire date to earliest affected period (if not already rehired)
   - Or temporarily remove ERD restriction (requires system access)
   - Confirm system allows payroll calculation

2. **Process Retro:**
   - Calculate retro for affected periods
   - Generate /551 differences
   - Validate results

3. **Correction Entry:**
   - If reactivation was temporary, re-terminate employee
   - Reset ERD back to original date
   - Document the correction

**After Terminated Employee Retro:**

1. **Employee Communication:**
   - [ ] Notify employee of retro adjustment
   - [ ] Send written explanation with amount
   - [ ] Arrange payment method (check, direct deposit if account still active)
   - [ ] Provide updated final paystub showing /551 adjustment

2. **Tax/Wage Documents:**
   - [ ] Update W-2 (if retro affects taxable income for that year)
   - [ ] Recalculate tax withholding if applicable
   - [ ] Notify tax authorities if adjustments exceed threshold
   - [ ] Keep copy of retro documentation for audit

3. **Reconciliation:**
   - [ ] Verify final payroll GL posting includes retro
   - [ ] Check employee payable account is cleared (including retro payment)
   - [ ] Reconcile tax liability with retro tax changes
   - [ ] Archive all retro documentation

---

## Multiple Retro Periods

### Description

When the same payroll area/employee group has multiple retroactive changes to the same period, the processing becomes increasingly complex.

**Scenario:**
```
Example Timeline:
January 2024: Salary increase approved (RRDAT = 01/01/2024)
  → Retro #1 executed in February for Jan, Dec, Nov, Oct
  → Employees show /551 differences

March 2024: Correction to salary increase (should have been higher)
  → Retro #2 executed in April for Jan, Dec, Nov, Oct (same periods as Retro #1)
  → Employees show /552 differences (NOT /551, because /551 already exists)

May 2024: Tax correction for 2024
  → Retro #3 executed in June for Jan-May 2024
  → For Jan-Apr (already affected by Retro #1 and #2): /552 generated
  → For May (first retro): /551 generated
```

### Issues with Multiple Retros

#### Issue 1: /551 vs /552 Selection

**Problem:**
- First retro of a period generates /551
- Subsequent retros generate /552
- System must correctly identify which is first vs. subsequent
- If incorrectly classified, double-adjustment occurs

**Example:**
```
Correct Sequence:
  Retro #1: /551 = 416.67
  Total: 416.67

  Retro #2: /552 = 83.33 (additional adjustment, not first 416.67 again)
  Total: 416.67 + 83.33 = 500.00

  Payroll after both retros: Total adjustment = 500.00 ✓

Incorrect Sequence (if Retro #1 re-executed):
  Retro #1: /551 = 416.67
  Retro #2: /551 = 416.67 (ERROR - should be /552!)
  Total: 416.67 + 416.67 = 833.34 ✗ (double-payment)

Fix Required:
  - Identify the double-posted /551
  - Create reversal /553 = -416.67 for one of them
  - Document the correction
```

**SAP Handling:**
- SAP maintains flag "retro_processed_this_period" in cluster
- On second retro, system checks flag and generates /552 instead of /551
- If flag is corrupted or cluster is manually edited, system may generate /551 twice

**Prevention:**
- NEVER re-execute Retro #1 after Retro #2 is complete
- If correction needed after Retro #2, process Retro #3 (not re-execute Retro #1)
- Always use simulation to verify /552 is used before committing

#### Issue 2: Cascading Effects Across Multiple Retros

**Problem:**
- Retro #1 changes /551 for wage types A and B
- Retro #2 changes wage types B and C
- Retro #3 changes wage types A and C
- Final result must be correct for ALL three

**Example:**
```
Original (Jan):
  /100: 5000
  /103: 625
  /200: -250
  /560: 4725

Retro #1 (Feb): Salary increase to 5416.67
  /100 /551: +416.67
  /103 /551: +52.08
  /560 /551: +364.59

After Retro #1:
  /100: 5416.67
  /103: 677.08
  /200: -250
  /560: 5089.75

Retro #2 (Mar): Tax correction (filing status change)
  /103 /552: should be based on current 5416.67, not original 5000

Correct calculation:
  Original tax (on 5000): 625.00
  Current tax (on 5416.67): 677.08
  Total difference: 52.08
  Previous /551: 52.08
  /552: 0.00 (no additional change)

Retro #3 (Apr): Salary correction (should have been 5500, not 5416.67)
  /100 /552: (5500 - 5000) - (5416.67 - 5000) = 83.33
  /103 /552: (687.50 - 625.00) - (677.08 - 625.00) = 10.42
  /560 /552: 72.91

Final result after all retros:
  /100: 5500.00 ✓
  /103: 687.50 ✓
  /200: -250.00 ✓
  /560: 5162.66 ✓

Total /551 + /552: 500.00 + 83.33 = 583.33 ✓
```

#### Issue 3: Different Departments/Cost Centers

**Problem:**
- Multiple retros in same period may affect different cost centers
- First retro is for department A (salary)
- Second retro is for department B (org change)
- System must handle both independently

**Example:**
```
Retro #1: Salary increase (affects depts A, B, C equally)
  All employees get 5% raise

Retro #2: Org change (affects dept B only)
  Dept B employees move to cost center 5200

Processing:
  Retro #1: All affected employees → /551 = 416.67 (salary diff)
  Retro #2: Dept B employees → /552 = 0 (cost center change, no amount change)
            BUT GL posting changes (from 4100/5100 to 4100/5200)
```

### Resolution Procedures

**Planning Multiple Retros:**

1. **Sequence Planning:**
   - [ ] Document what each retro will accomplish
   - [ ] Determine if retros must be sequential or can be independent
   - [ ] Identify dependencies between retros
   - [ ] Decide on execution order (usually earliest first)

2. **Stakeholder Communication:**
   - [ ] Notify Finance of multiple retro runs
   - [ ] Explain cascading impacts to GL accounts
   - [ ] Manage expectations (multiple updates to same periods)
   - [ ] Get approval for multiple-retro approach

3. **Documentation:**
   - [ ] Document each retro's business justification
   - [ ] Record RRDAT and affected periods for each
   - [ ] Note affected employees per retro
   - [ ] Identify which retros are dependent on others

**Executing Multiple Retros:**

1. **Execute in Sequence:**
   - Process Retro #1 to completion (including validation)
   - Then execute Retro #2 (do NOT re-execute Retro #1)
   - Then execute Retro #3 (do NOT re-execute #1 or #2)

2. **Validate After Each Retro:**
   - Run full validation on Retro #1 results
   - Check /551 is generated (not /552)
   - Validate GL postings

   Then:
   - Simulate Retro #2 (verify /552 is used, not /551)
   - Execute Retro #2
   - Validate /552 is generated correctly
   - Check GL postings are cumulative (Retro #1 + Retro #2)

   Then:
   - Repeat for Retro #3

3. **GL Reconciliation:**
   - After each retro, reconcile GL accounts
   - Total GL posting should equal SUM(all /551) + SUM(all /552)
   - Track GL posting by cost center and retro number

**After Multiple Retros:**

1. **Final Reconciliation:**
   - [ ] Total retro amount = final wage type value - original value
   - [ ] Should be same regardless of how many retros executed
   - [ ] GL postings should reconcile to final amounts

2. **Employee Communication:**
   - Explain that multiple adjustments were needed
   - Show net effect (final total), not intermediate /551 and /552
   - Clarify total payment amount (single check preferred)

3. **Documentation:**
   - [ ] Archive all three retro execution logs
   - [ ] Keep simulation results for audit trail
   - [ ] Document any issues that arose
   - [ ] Record any manual corrections made

---

## Tax Jurisdiction Changes

### Description

When an employee changes work location or domicile during the retro period, different tax jurisdiction rules apply. This is particularly complex for multi-state companies.

### Issues

#### Issue 1: State Tax Table Changes

**Problem:**
- Employee worked in State A (Jan-Mar)
- Transferred to State B (Apr-Jun)
- Retro salary increase for Jan-Jun
- State A and State B have different tax rates and calculations

**Example:**
```
Employee: E004, Bob Johnson
Work Location: State A (NY) for Jan-Mar, then State B (NJ) for Apr-Jun

Original Calculation (Jan):
  Gross: 5000
  NY State Tax (/104): 375.00 (7.5% - simplified rate)

Original Calculation (Apr, after transfer to NJ):
  Gross: 5000
  NJ State Tax (/104): 285.00 (5.7% - simplified rate)

Retro Change: Salary increase to 5416.67

Retro Recalc (Jan) - still in State A (NY):
  Gross: 5416.67
  NY State Tax: 406.25 (7.5% × 5416.67)
  Tax difference: 31.25

Retro Recalc (Apr) - now in State B (NJ):
  Gross: 5416.67
  NJ State Tax: 309.35 (5.7% × 5416.67)
  Tax difference: 24.35

Each period uses correct tax table for that period's jurisdiction.
BUT system must know employee's jurisdiction for each period.
```

**SAP Handling:**
- Work location/domicile is infotype 0003 (Employee Address) or 0009 (Pensions)
- Tax calculation checks work location effective date
- Retro calculation must apply correct work location for each period

**Issue:**
- If employee's current location is NJ, system may apply NJ tax to all periods
- Retro calculation may not "look back" to Jan when employee was in NY
- Result: NY taxes calculated using NJ table (INCORRECT)

#### Issue 2: Local Tax Considerations

**Problem:**
- Some states/cities have local income taxes
- Employee may have changed cities or counties during retro period
- Local tax rates are different

**Example:**
```
Employee moved from Philadelphia, PA to Pittsburgh, PA on March 31

Philadelphia local tax: 3.8927%
Pittsburgh local tax: 3.0%

Retro salary increase for Jan-May:
- Jan-Mar: Apply Philadelphia 3.8927% local tax
- Apr-May: Apply Pittsburgh 3.0% local tax

If system doesn't track city-level location, may apply wrong rate.
```

#### Issue 3: Multi-State Withholding Rules

**Problem:**
- Multi-state workers have special withholding rules
- Employee may owe taxes to both resident and non-resident states
- Retro changes allocation between state tax liabilities

**Example:**
```
Employee: Works in State B (NJ) but resides in State A (NY)
Withholding rule: Withhold for NJ (work state) + proportional NY (resident state)

If retro changes work state allocation:
- 100% time in NJ → withhold NJ only
- 50% time in NJ, 50% remote → withhold NJ + partial NY

Retro may trigger need to recalculate multi-state withholding formula.
```

### Resolution Procedures

**Before Tax Jurisdiction Retro:**

1. **Identify Jurisdiction Changes:**
   - [ ] Review employee's work location history for retro period
   - [ ] Check for transfers between states/cities
   - [ ] Identify jurisdiction change dates
   - [ ] Determine applicable tax rules for each jurisdiction

2. **Verify Tax Configuration:**
   - [ ] Confirm work location is correctly recorded in SAP for each period
   - [ ] Verify tax table is assigned to each work location
   - [ ] Check local tax codes if applicable
   - [ ] Verify multi-state rules in PCR rules

3. **Calculate Taxes by Period:**
   - [ ] For each period in retro range, identify jurisdiction
   - [ ] Calculate tax using that jurisdiction's table
   - [ ] Document expected tax amounts per period and jurisdiction
   - [ ] Note any multi-state adjustments

4. **Simulation:**
   - [ ] Simulate retro for first period (before any transfers)
   - [ ] Verify correct tax table used
   - [ ] Simulate retro for period after transfer
   - [ ] Verify correct tax table for new jurisdiction used
   - [ ] Compare to manually calculated expectations

**During Jurisdiction Retro:**

1. **Monitor Tax Calculation:**
   - For each affected period, verify correct jurisdiction used
   - Check that tax rate applied is correct for that period
   - Compare to simulation results

2. **Watch for Multi-State Rules:**
   - If multi-state employee, verify both resident and non-resident taxes
   - Check allocation formula is applied correctly
   - Verify total withholding meets both state requirements

**After Jurisdiction Retro:**

1. **Tax Reconciliation:**
   - [ ] Total tax by jurisdiction (sum of /551 for that state)
   - [ ] Verify GL postings are routed to correct state tax accounts
   - [ ] Reconcile to state tax payment schedules

2. **Tax Authority Notification:**
   - [ ] If retro significantly changes taxes owed, notify tax authorities
   - [ ] File amended returns if required (federal, state, local)
   - [ ] Document retro as supporting evidence for amended return
   - [ ] Retain documentation for audit trail

3. **Employee Communication:**
   - Explain jurisdiction changes affected tax calculation
   - Show tax by jurisdiction if multi-state
   - Clarify net withholding vs. filing requirements

---

## Wage Type Configuration Changes

### Description

SAP wage types are configured via PCR (Payroll Control Record) rules. If wage type configuration changes between the original payroll period and the retro period, retroactive recalculation may use different rules.

### Issues

#### Issue 1: Calculation Rule Changes

**Problem:**
- Wage type /100 (Base Salary) was calculated as "gross salary" in Jan
- By Mar, /100 definition changed to "gross + shift premium"
- Retro recalculation in Mar uses new definition (INCORRECT)

**Example:**
```
Original PCR Rule for /100 (Jan 2024):
  /100 = Employee_Salary

Employee: E005
Salary: 5000
Original /100 (Jan): 5000

PCR Rule Update (Feb 2024):
  /100 = Employee_Salary + Shift_Premium

Shift Premium: 200

New /100 (Feb onwards): 5200 (includes shift premium)

Retro Scenario (Mar): Salary increase to 5416.67 (5% of 5000)

Correct Retro Recalculation (Jan, using original rule):
  /100 = 5000 + 5% = 5250  (no shift premium, because rule was different in Jan)
  /551 = 250

Incorrect Retro Recalculation (Mar, using current rule):
  /100 = 5200 + 5% = 5460  (includes shift premium)
  /551 = 460  (WRONG - shift premium wasn't in original Jan calc)
```

**SAP Handling:**
- SAP can reference different PCR rule versions (time-effective)
- Retro should use PCR version that was active in the original period
- System may not automatically select correct version

#### Issue 2: Rounding Rule Changes

**Problem:**
- Rounding rules for tax calculation may change
- Original: round to nearest cent
- New: round down (always)
- Retro may use new rounding, creating small discrepancies

**Example:**
```
Original Tax Calc (Jan):
  Gross: 5000
  Tax rate: 12.3456%
  Tax (round nearest cent): 616.78

Current Tax Calc (Mar):
  Rounding rule changed to "round down"
  Gross: 5416.67
  Tax rate: 12.3456%
  Tax calculation: 668.43... → Round down: 668.43

Retro Recalculation (should use old rounding rule):
  Gross: 5416.67
  Tax rate: 12.3456%
  Tax (round nearest cent): 668.43  ← Happens to be same

But in other scenarios, rounding differences accumulate:
  Multiple employees × multiple periods = material variance
```

#### Issue 3: Valuation Rule Changes

**Problem:**
- Benefit deduction calculation may change
- Health insurance monthly cost may change
- Retro may apply new rate to old periods

**Example:**
```
Employee: E006
Health Insurance Coverage: Family (2 adults + 2 children)

Original Rate (Jan 2024): $450/month
Retro Period: Jan-Mar 2024
Original Deduction (Jan-Mar): $450 × 3 = $1350

Rate Update (Apr 2024): Increased to $475/month (annual increase effective Apr 1)

Retro Scenario (May): Correct coverage from "Single" to "Family"

Correct Retro Calc (Jan, using original rate):
  Deduction: $450/month × 3 = $1350

Incorrect Retro Calc (May, using current rate):
  Deduction: $475/month × 3 = $1425  (WRONG - rate didn't change until Apr)
  /551: -75  (incorrect reduction)
```

### Resolution Procedures

**Before Configuration Change Retro:**

1. **Audit Configuration Versions:**
   - [ ] Identify when PCR rules changed
   - [ ] Document which wage types changed
   - [ ] Determine what changed (formula, rounding, rate, etc.)
   - [ ] Identify which periods used old vs. new rule

2. **Verify SAP Configuration:**
   - [ ] Check if PCR rules are time-effective in SAP
   - [ ] Verify old rule version is still available
   - [ ] Check if retro configuration references correct rule version
   - [ ] Confirm system can apply period-specific rules

3. **Manual Calculation:**
   - [ ] Calculate expected retro amount using original rule
   - [ ] Calculate using new rule
   - [ ] Document expected difference
   - [ ] Note which periods should use which rule

4. **Simulation:**
   - [ ] Run simulation for period before rule change
   - [ ] Verify original rule is applied
   - [ ] Run simulation for period after rule change
   - [ ] Verify new rule is applied
   - [ ] Compare to manual calculations

**During Configuration Change Retro:**

1. **Verify Rule Application:**
   - Monitor which PCR rule version is being applied
   - Check each period is using correct rule version
   - Watch for unexpected calculation differences

**After Configuration Change Retro:**

1. **Variance Analysis:**
   - [ ] Compare retro results to manual calculation
   - [ ] Investigate any unexplained variances
   - [ ] Determine if variance is due to rounding or actual rule mismatch
   - [ ] Correct if necessary

2. **Documentation:**
   - [ ] Document PCR rule versions used
   - [ ] Explain any variances from manual calculation
   - [ ] Archive PCR configuration screenshots
   - [ ] Maintain for audit trail

---

## Missing Master Data

### Description

Master data (employee records, cost centers, GL accounts) may change between the original payroll period and the retro period. If original master data is no longer available, retro recalculation may fail or produce incorrect results.

### Issues

#### Issue 1: Deleted Cost Center

**Problem:**
- Cost center 4500 existed in Jan (where employee was assigned)
- Cost center was deleted in Feb (merged with 4600)
- Retro in Mar tries to assign employee to deleted cost center

**Example:**
```
Original (Jan):
  Employee E007: Cost Center 4500 (Materials Handling)
  Payroll posting: GL 4100 (Salary) to Cost Center 4500

Cost Center Restructuring (Feb):
  Cost Center 4500 merged into 4600 (Warehouse Operations)
  Cost Center 4500 deleted

Retro Scenario (Mar): Salary increase retroactive to Jan

Retro Recalculation (Jan):
  System looks up: Employee E007's cost center in Jan
  Expected: 4500
  Found: 4600 (current cost center, because 4500 deleted)

Result:
  GL posting is to 4600, not original 4500
  Jan retro GL posting doesn't match Jan original posting
  GL reconciliation shows variance
```

**SAP Handling:**
- If cost center is deleted with "no posting to deleted accounts" rule, posting fails
- If cost center is deleted with "remap to new center" rule, posting goes to new center
- Retro calculation may use current cost center instead of original

#### Issue 2: Changed GL Account

**Problem:**
- GL account 4100 was primary salary expense in Jan
- In Feb, company implemented new GL structure
- GL 4100 was retired, split into 4110 (salary) and 4115 (supplement)
- Retro tries to post to deleted GL account 4100

**Example:**
```
Original GL Structure (Jan):
  GL 4100: All Salary Expense
  Employee posted to 4100

GL Restructuring (Feb):
  GL 4100 retired
  GL 4110: Salary - Regular
  GL 4115: Salary - Supplement
  GL 4120: Bonus and Other Compensation

Retro Salary Increase (Mar, retroactive to Jan):

Correct Retro Posting (Jan): Post to GL 4100 (was valid in Jan)
Incorrect Retro Posting: Try to post to GL 4100, fail because deleted

Resolution:
  Must manually remap old GL 4100 to new GL 4110
  Or use GL account mapping table
```

#### Issue 3: Modified Wage Type

**Problem:**
- Wage type /150 (Shift Premium) existed with specific configuration in Jan
- Configuration was changed in Feb
- Retro recalculation uses new configuration (wrong for Jan)

**Example:**
```
Original /150 Configuration (Jan):
  Description: Shift Premium
  Calculation: Base Salary × 0.1 (10% premium)
  Posting: To GL 4120

Configuration Change (Feb):
  Description: Shift Premium (updated)
  Calculation: Changed to Base Salary × 0.15 (15% premium)
  Posting: Changed to GL 4125

Retro Scenario (Mar): Correct misclassification from Jan (was incorrectly classified as 10%)

Retro Recalculation (Jan):
  Original /150: 500 (5000 × 10% correct)
  Retro with new config: 812.50 (5416.67 × 15% wrong - config didn't change until Feb)
  /551: 312.50 (INCORRECT - using wrong rate)

Correct Retro:
  Should use 10% rate (what was in effect in Jan)
  /551: 291.67 (5416.67 × 10%)
```

### Resolution Procedures

**Before Missing Data Retro:**

1. **Audit Master Data Changes:**
   - [ ] Document all cost center changes (deleted, merged, created)
   - [ ] Document all GL account changes (deleted, merged, renumbered)
   - [ ] Document all wage type configuration changes
   - [ ] Identify which changes occurred between original and retro periods

2. **Verify Data Availability:**
   - [ ] Check if deleted cost centers are archived and retrievable
   - [ ] Check if deleted GL accounts are archived
   - [ ] Verify wage type versions are archived
   - [ ] Confirm original configuration can be accessed

3. **Reconstruction Plan:**
   - [ ] For deleted cost centers, identify mapping to new centers (if needed)
   - [ ] For deleted GL accounts, identify remapping rules
   - [ ] For changed wage types, identify which config version applies per period
   - [ ] Document plan for handling missing data

4. **Master Data Restoration:**
   - If master data is missing (truly deleted):
     - [ ] Restore from backup if available
     - [ ] Manually recreate based on original payroll documentation
     - [ ] Verify restored data matches original (e.g., Jan payslips)
   - If master data was reclassified:
     - [ ] Create mapping rules for retro (use original classification for original periods)
     - [ ] Test mapping rules in simulation

**During Missing Data Retro:**

1. **Monitor for Errors:**
   - Watch for "cost center not found" errors
   - Watch for "GL account locked" errors
   - Watch for wage type calculation errors
   - Note any warnings about master data mismatches

2. **Manual Corrections:**
   - If retro fails due to missing cost center, manually remap
   - If retro fails due to missing GL account, use mapping table
   - Rerun retro after corrections

**After Missing Data Retro:**

1. **Verification:**
   - [ ] Verify GL postings are routed to correct accounts (original, not current)
   - [ ] Verify cost centers are assigned correctly per original
   - [ ] Verify wage type calculations use correct configurations per period

2. **Documentation:**
   - [ ] Document any master data restoration
   - [ ] Document any manual mappings used
   - [ ] Explain variances between original and retro calculations (if any)
   - [ ] Archive original master data for audit trail

3. **Prevention:**
   - [ ] Create process to preserve master data before deleting
   - [ ] Implement time-effective master data instead of deleting
   - [ ] Maintain change log of all master data changes
   - [ ] Set archive retention for retro lookup

---

## Time Evaluation Conflicts

### Description

Retroactive payroll changes may trigger conflicts with time evaluation (RPTIME00). If wage types are tied to time entries (hours, overtime), retro changes may require time data to be reevaluated.

### Issues

#### Issue 1: Missing Time Data

**Problem:**
- Hourly employee, retro for period with time entries already evaluated
- Retro is for a wage type that depends on hours (e.g., hourly rate increase)
- Time entries for that period are no longer available or have been locked

**Example:**
```
Employee: E008 (Hourly, $25/hour)
Period: January 2024
Original Time Entry: 160 hours worked
Original Payroll: 160 × $25 = $4000

Retro Scenario (Mar): Hourly rate increase to $27/hour effective retroactively

Retro Recalculation (Jan):
  Need to recalculate: 160 × $27 = $4320
  But time data for Jan may have been:
  - Locked (cannot be modified)
  - Purged (deleted after payroll finalized)
  - Lost (system error)

If time data not available:
  Cannot recalculate hours × new rate
  Retro calculation fails with error "Time data not found"
```

#### Issue 2: Time Rule Changes

**Problem:**
- Time evaluation rules may have changed between original and retro
- Original: Overtime calculated as hours > 40/week
- New: Overtime calculated as hours > 37.5/week
- Retro should use original rule, not current rule

**Example:**
```
Original Time Rule (Jan): Overtime threshold = 40 hours/week
  Employee worked: 45 hours (5 hours OT at 1.5×)
  Calculation: 40 × $25 + 5 × $37.50 = $1187.50

Time Rule Change (Feb): Overtime threshold reduced to 37.5 hours/week
  (Due to labor union agreement)

Retro Scenario (Mar): Hourly rate increase

Correct Retro (Jan, using original rule):
  40 × $27 + 5 × $40.50 = $1282.50
  /551: 95.00

Incorrect Retro (using current rule):
  37.5 × $27 + 7.5 × $40.50 = $1309.88
  /551: 122.38 (WRONG - used wrong OT threshold)
```

#### Issue 3: Attendance Adjustments

**Problem:**
- Employee had attendance adjustments (sick leave, PTO) in retro period
- Adjustments were applied after original payroll
- Retro must consider these adjustments

**Example:**
```
Original Time Entry (Jan): 160 hours worked
Original Payroll (Jan): 160 × $25 = $4000

Post-Payroll Adjustment (late Jan): Employee retroactively approved for 8 sick hours
Adjusted Time (Jan): 160 + 8 = 168 hours
Adjusted Payroll (Jan): 168 × $25 = $4200 (adjustment paid later)

Retro Scenario (Mar): Rate increase to $27

Retro Recalculation (Jan):
  Must include both:
  - Original 160 hours: 160 × $27 = $4320 (diff = $320)
  - Approved 8 hours: 8 × $27 = $216 (diff = $48)

Total /551: 368  (320 + 48)
```

### Resolution Procedures

**Before Time-Dependent Retro:**

1. **Identify Time Dependencies:**
   - [ ] Determine if affected wage types depend on time entries
   - [ ] Identify which employees have time-dependent wage types
   - [ ] Check if time data is available for retro periods
   - [ ] Verify time evaluation rules

2. **Verify Time Data:**
   - [ ] Pull time entries for retro periods
   - [ ] Verify hours are complete and correct
   - [ ] Check for locked or archived time data
   - [ ] Note any post-payroll time adjustments (sick days, PTO approved later)

3. **Audit Time Rules:**
   - [ ] Document time rules in effect for original periods
   - [ ] Compare to current time rules
   - [ ] Identify when rules changed
   - [ ] Verify retro can use period-specific rules

4. **Time Data Reconstruction:**
   - If time data is missing:
     - [ ] Check backup systems
     - [ ] Review original time tracking records
     - [ ] Reconstruct from manual timesheets if necessary
     - [ ] Verify reconstructed data matches original payroll

5. **Simulation:**
   - [ ] Simulate retro for period with time data available
   - [ ] Verify time-dependent wage types are recalculated correctly
   - [ ] Compare to manual calculation
   - [ ] Verify correct time rules are applied

**During Time-Dependent Retro:**

1. **Monitor Time Evaluation:**
   - Track which employees trigger time reevaluation (RPTIME00)
   - Watch for warnings about missing time data
   - Monitor for time rule discrepancies
   - Note any hours-related calculation issues

2. **Error Handling:**
   - If time data is missing, manually reconstruct before retro
   - If time rules changed, verify correct version is applied
   - If RPTIME00 fails, resolve before proceeding with retro

**After Time-Dependent Retro:**

1. **Time Reconciliation:**
   - [ ] Verify hours are correctly applied in retro calc
   - [ ] Reconcile total hours × rate = expected wage amount
   - [ ] Check for gaps where time data was missing
   - [ ] Validate post-payroll time adjustments were included

2. **Overtime Verification:**
   - [ ] Verify overtime thresholds were applied correctly
   - [ ] Check OT rates (1.5×, 2×, etc.) are correct per original rules
   - [ ] Reconcile OT amount per time rule version

3. **Documentation:**
   - [ ] Archive time data used for retro
   - [ ] Document any time data reconstruction
   - [ ] Note time rule versions applied per period
   - [ ] Explain any variances between original and retro time calculations

---

## Benefit Plan Changes During Retro Period

### Description

Benefit plans (health insurance, 401k, FSA) may have undergone changes (rate changes, plan changes, enrollment changes) during the retro period. Retro recalculation must correctly apply the benefit rules that were in effect for each period.

### Issues

#### Issue 1: Benefit Rate Changes

**Problem:**
- Health insurance rate was $450/month in Jan-Feb
- Rate increased to $475/month effective Mar 1
- Retro for Jan-Feb must use $450, not current $475

**Example:**
```
Employee: E009
Benefit: Family Health Insurance

Original (Jan-Feb): $450/month × 2 = $900
Original (Mar): $475/month × 1 = $475
Total Original: $1375

Retro Scenario (Apr): Correct employee classification from "employee" to "employee+spouse"

Correct Retro (using correct rates per period):
  Jan-Feb at $450: Same as original (no change to rate, only classification)
  Mar at $475: Same as original
  Total Retro: $1375 (no /551, classification doesn't change cost)

Incorrect Retro (using current rate everywhere):
  Jan-Feb using $475: -$50 variance
  Mar using $475: $0 variance
  Result: Would create false /551 for Jan-Feb
```

#### Issue 2: Plan Enrollment Changes

**Problem:**
- Employee was not enrolled in 401(k) in Jan-Feb
- Enrolled in Mar (with retroactive effective date)
- Retro recalculation must apply 401(k) deduction for all periods

**Example:**
```
Original Payroll (Jan-Feb):
  /200 (Health Ins): $450 (enrolled)
  /201 (401k): $0 (not enrolled)
  Total Deductions: $450

Plan Enrollment (effective retroactively to Jan):
  401(k) enrollment with 3% contribution

Retro Recalculation (Jan-Feb):
  /200 (Health Ins): $450 (already enrolled)
  /201 (401k): $150 (new 3% deduction, retro to Jan)
  /551 (401k diff): $150
  Total Deductions: $600
  /560 Net Pay: Decreases by $150 (less take-home, 401k deduction)

Complication:
  Employee wasn't expecting Jan-Feb 401(k) deduction
  Only authorized Mar onwards
  But retro applies Jan retroactively
```

#### Issue 3: Plan Termination Midyear

**Problem:**
- Employee terminated plan participation in May
- Retro salary change applies to Jan-May
- Retro must respect May termination (no deduction for June onwards)

**Example:**
```
Employee: E010
FSA Enrollment: Jan-May 2024
FSA Monthly: $300

Termination (May 31): FSA terminated due to separation

Retro Salary Increase (Jun): Retroactive to Jan

Correct Retro:
  Jan-May: Salary increase applies, FSA deduction continues ($300 × 5 = $1500)
  Jun onwards: FSA is terminated, no deduction

Incorrect Retro:
  If system doesn't respect termination date:
  Would apply FSA deduction for Jun-Dec even though terminated
```

### Resolution Procedures

**Before Benefit Change Retro:**

1. **Audit Benefit Changes:**
   - [ ] Document all benefit rate changes during retro period
   - [ ] Identify plan enrollment changes (effective dates)
   - [ ] Identify plan termination changes
   - [ ] Check if changes are time-effective in SAP

2. **Verify Benefit Configuration:**
   - [ ] Confirm employee's benefit status for each month in retro period
   - [ ] Verify rates are assigned for each effective date period
   - [ ] Check benefit deduction formulas (% vs. $, before/after tax)
   - [ ] Verify FSA/HSA special rules if applicable

3. **Manual Calculation:**
   - [ ] Calculate expected benefit deductions per month using period-specific rates
   - [ ] Document expected /551 for each benefit
   - [ ] Total expected /551 across all months

4. **Simulation:**
   - [ ] Simulate retro for earliest period (Jan)
   - [ ] Verify correct benefit rates applied
   - [ ] Simulate for period with rate change (transition month)
   - [ ] Verify old rate used for pre-change, new rate for post-change
   - [ ] Simulate for period with enrollment change
   - [ ] Verify enrollment status is correctly applied

**During Benefit Change Retro:**

1. **Monitor Benefit Calculation:**
   - Watch for warnings about benefit mismatches
   - Verify each month uses correct rates
   - Check enrollment status is applied per period
   - Note any special handling for FSA/HSA

**After Benefit Change Retro:**

1. **Benefit Reconciliation:**
   - [ ] Reconcile benefit deductions to benefit system records
   - [ ] Verify amounts match plan documents (rate letters, enrollment forms)
   - [ ] Check FSA/HSA compliance (contribution limits, rollover rules)
   - [ ] Validate tax treatment (pre-tax vs. post-tax)

2. **Employee Communication:**
   - Explain benefit changes during retro period
   - Show expected deductions per period
   - Clarify retroactive benefit impacts (if any)
   - Provide summary of benefit changes

3. **Plan Administration:**
   - [ ] Notify benefits administrator of retro adjustments
   - [ ] Update benefit system if required
   - [ ] Reconcile with benefits provider (insurance company, 401k plan admin)
   - [ ] Retain documentation for benefits audit

4. **Documentation:**
   - [ ] Archive benefit configuration for each period
   - [ ] Document rate changes with effective dates
   - [ ] Document enrollment/termination changes
   - [ ] Maintain for audit trail

---

**End of Edge Case Catalog**

For additional information, see:
- `retro-processing-guide.md` - Workflow and validation procedures
- `retro-wage-types.md` - Technical details on /551, /552, /553 calculations
