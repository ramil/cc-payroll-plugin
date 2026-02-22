#!/usr/bin/env python3
"""
Generate Test Payroll Data with Deliberate Issues

Creates payroll_data.xlsx with 50 employees containing realistic
SAP payroll results data. Issues are post-processing validation
problems that WOULD appear in payroll results (not SAP hard stops).

SAP Hard Stops (employees would NOT appear in results):
  - Missing infotype 0001 (Org Assignment) / missing cost center
  - Missing infotype 0008 (Basic Pay)
  - Missing infotype 0210 (Tax Data)
  - Invalid bank details (infotype 0009)
  - Payroll area not assigned

Realistic Post-Processing Issues (CAN appear in results):
  - Employee over SS wage base ($176,100)
  - Garnishment exceeding 25% of disposable earnings
  - FICA still withheld after SS wage base exceeded
  - Duplicate employee records in export
  - Unusually high payment (statistical outlier)
  - Missing department in export (org structure gap)
  - Zero net pay (deductions consume entire gross)
  - Overtime calculated at wrong multiplier (1.25x vs 1.5x)
  - Tax withholding rate anomaly

Author: CC Payroll Plugin
License: Proprietary
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


def generate_test_payroll_data(output_file='payroll_data.xlsx'):
    """Generate test payroll data with deliberate compliance issues.

    Data represents a monthly payroll run from SAP with a mix of
    salaried and hourly employees. All employees passed SAP hard stops
    (they have valid org assignment, basic pay, tax data, and bank details).
    """

    np.random.seed(42)

    # SAP employee status codes (infotype 0000)
    # 0 = Active, 1 = Retiree, 2 = Leave of Absence, 3 = Withdrawn/Terminated
    EE_STATUS_ACTIVE = 0
    EE_STATUS_TERMINATED = 3

    departments = ['Sales', 'Engineering', 'HR', 'Finance', 'Operations', 'Manufacturing', 'Legal', 'IT']
    cost_centers = ['CC-1000', 'CC-2000', 'CC-3000', 'CC-4000', 'CC-5000']
    payroll_areas = ['US01', 'US02', 'US03']

    first_names = [
        'James', 'Maria', 'Robert', 'Jennifer', 'Michael', 'Linda', 'David',
        'Patricia', 'William', 'Elizabeth', 'Richard', 'Susan', 'Joseph', 'Karen',
        'Thomas', 'Nancy', 'Christopher', 'Betty', 'Daniel', 'Dorothy',
        'Matthew', 'Sandra', 'Anthony', 'Ashley', 'Mark', 'Kimberly',
        'Steven', 'Donna', 'Andrew', 'Emily', 'Paul', 'Carol', 'Joshua',
        'Michelle', 'Kenneth', 'Amanda', 'Kevin', 'Melissa', 'Brian', 'Deborah',
        'George', 'Stephanie', 'Timothy', 'Rebecca', 'Ronald', 'Sharon',
        'Edward', 'Laura', 'Jason', 'Cynthia'
    ]
    last_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
        'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
        'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
        'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark',
        'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King',
        'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green',
        'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
        'Carter', 'Roberts'
    ]

    # Monthly salary ranges by department (annual / 12)
    salary_ranges = {
        'Sales':         (4000, 8500),     # $48K-$102K annual
        'Engineering':   (5500, 11000),    # $66K-$132K annual
        'HR':            (4200, 7500),     # $50K-$90K annual
        'Finance':       (5000, 10000),    # $60K-$120K annual
        'Operations':    (3500, 6500),     # $42K-$78K annual
        'Manufacturing': (3200, 5500),     # $38K-$66K annual
        'Legal':         (6000, 12000),    # $72K-$144K annual
        'IT':            (5500, 10500),    # $66K-$126K annual
    }

    data = []
    period = '202501'
    period_start = '2025-01-01'
    period_end = '2025-01-31'

    for i in range(50):
        emp_id = f'{10000 + i}'
        dept = np.random.choice(departments)
        cost_center = np.random.choice(cost_centers)
        payroll_area = np.random.choice(payroll_areas)
        first = first_names[i % len(first_names)]
        last = last_names[i % len(last_names)]
        name = f'{first} {last}'

        # 85% active, 8% new hire (still active status), 7% terminated in period
        status_roll = np.random.random()
        if status_roll < 0.85:
            ee_status = EE_STATUS_ACTIVE
            hire_date = (datetime(2025, 1, 31) - timedelta(days=int(np.random.uniform(60, 2000)))).strftime('%Y-%m-%d')
            term_date = ''
        elif status_roll < 0.93:
            ee_status = EE_STATUS_ACTIVE  # new hires are active
            hire_date = (datetime(2025, 1, 1) + timedelta(days=int(np.random.uniform(0, 15)))).strftime('%Y-%m-%d')
            term_date = ''
        else:
            ee_status = EE_STATUS_TERMINATED
            hire_date = (datetime(2025, 1, 31) - timedelta(days=int(np.random.uniform(180, 2000)))).strftime('%Y-%m-%d')
            term_date = (datetime(2025, 1, 15) + timedelta(days=int(np.random.uniform(0, 15)))).strftime('%Y-%m-%d')

        # Monthly salary (wage type 1000)
        sal_min, sal_max = salary_ranges[dept]
        monthly_salary = round(np.random.uniform(sal_min, sal_max), 2)

        # Overtime (20% chance, only for non-exempt roles)
        overtime_pay = 0.0
        if dept in ['Operations', 'Manufacturing'] and np.random.random() < 0.30:
            ot_hours = np.random.uniform(5, 25)
            hourly_equiv = monthly_salary / 173.33  # avg monthly hours
            overtime_pay = round(ot_hours * hourly_equiv * 1.5, 2)

        # Bonus (10% chance)
        bonus = round(monthly_salary * np.random.uniform(0.05, 0.20), 2) if np.random.random() < 0.10 else 0.0

        gross_pay = round(monthly_salary + overtime_pay + bonus, 2)

        # YTD earnings (January = just this period for most, but simulate mid-year for variety)
        ytd_earnings = round(gross_pay * 1, 2)  # January = 1 month

        # Tax calculations
        federal_tax = round(gross_pay * np.random.uniform(0.10, 0.22), 2)
        state_tax = round(gross_pay * np.random.uniform(0.03, 0.07), 2)
        ss_withholding = round(gross_pay * 0.062, 2)
        medicare_withholding = round(gross_pay * 0.0145, 2)

        # Benefits deductions
        medical_deduction = 250.00 if np.random.random() < 0.90 else 0.0
        dental_deduction = 50.00 if np.random.random() < 0.75 else 0.0
        k401_deduction = round(gross_pay * np.random.uniform(0.03, 0.08), 2) if np.random.random() < 0.80 else 0.0

        # Garnishment (5% of employees)
        garnishment = 0.0
        if np.random.random() < 0.05:
            disposable = gross_pay - federal_tax - state_tax - ss_withholding - medicare_withholding
            garnishment = round(disposable * 0.20, 2)  # 20% of disposable (within 25% limit)

        # Net pay
        total_deductions = (federal_tax + state_tax + ss_withholding + medicare_withholding +
                          medical_deduction + dental_deduction + k401_deduction + garnishment)
        net_pay = round(gross_pay - total_deductions, 2)

        data.append({
            'Employee_ID': emp_id,
            'Employee_Name': name,
            'EE_Status': ee_status,
            'Hire_Date': hire_date,
            'Term_Date': term_date,
            'Department': dept,
            'Cost_Center': cost_center,
            'Payroll_Area': payroll_area,
            'Monthly_Salary': monthly_salary,
            'Overtime_Pay': overtime_pay,
            'Bonus': bonus,
            'Gross_Pay': gross_pay,
            'Federal_Tax': federal_tax,
            'State_Tax': state_tax,
            'SS_Withholding': ss_withholding,
            'Medicare_Withholding': medicare_withholding,
            'Medical_Deduction': medical_deduction,
            'Dental_Deduction': dental_deduction,
            '401K_Deduction': k401_deduction,
            'Garnishment': garnishment,
            'Net_Pay': net_pay,
            'YTD_Earnings': ytd_earnings,
            'Period': period,
            'Period_Start': period_start,
            'Period_End': period_end,
        })

    df = pd.DataFrame(data)

    # --- Inject Deliberate Post-Processing Issues ---
    # These are issues that SAP would NOT block but compliance checks should catch

    # Issue 1: Employee over SS wage base of $176,100
    # (High earner whose YTD crossed the limit - SS should have stopped withholding)
    df.loc[20, 'Monthly_Salary'] = 15000.00
    df.loc[20, 'Gross_Pay'] = 15000.00
    df.loc[20, 'YTD_Earnings'] = 180000.00  # Over $176,100 limit
    df.loc[20, 'SS_Withholding'] = round(15000 * 0.062, 2)  # Still withholding SS (error!)

    # Issue 2: Garnishment exceeding 25% of disposable earnings
    gross_25 = df.loc[25, 'Gross_Pay']
    disposable_25 = gross_25 - df.loc[25, 'Federal_Tax'] - df.loc[25, 'State_Tax'] - df.loc[25, 'SS_Withholding'] - df.loc[25, 'Medicare_Withholding']
    df.loc[25, 'Garnishment'] = round(disposable_25 * 0.30, 2)  # 30% of disposable (over 25% limit)
    df.loc[25, 'Net_Pay'] = round(gross_25 - df.loc[25, 'Federal_Tax'] - df.loc[25, 'State_Tax'] -
                                   df.loc[25, 'SS_Withholding'] - df.loc[25, 'Medicare_Withholding'] -
                                   df.loc[25, 'Medical_Deduction'] - df.loc[25, 'Dental_Deduction'] -
                                   df.loc[25, '401K_Deduction'] - df.loc[25, 'Garnishment'], 2)

    # Issue 3: Overtime rate error - calculated at 1.25x instead of 1.5x FLSA requirement
    df.loc[30, 'Department'] = 'Manufacturing'
    hourly_30 = df.loc[30, 'Monthly_Salary'] / 173.33
    df.loc[30, 'Overtime_Pay'] = round(15 * hourly_30 * 1.25, 2)  # Should be 1.5x
    df.loc[30, 'Gross_Pay'] = round(df.loc[30, 'Monthly_Salary'] + df.loc[30, 'Overtime_Pay'] + df.loc[30, 'Bonus'], 2)

    # Issue 4: 2 duplicate employee records in export
    dup_row_1 = df.iloc[5].copy()
    dup_row_2 = df.iloc[12].copy()
    df = pd.concat([df, pd.DataFrame([dup_row_1, dup_row_2])], ignore_index=True)

    # Issue 5: Unusually high payment (>3 std dev from mean) - legitimate but needs review
    mean_pay = df['Gross_Pay'].mean()
    std_pay = df['Gross_Pay'].std()
    df.loc[35, 'Gross_Pay'] = round(mean_pay + (4 * std_pay), 2)
    df.loc[35, 'Monthly_Salary'] = df.loc[35, 'Gross_Pay']  # Keep consistent
    df.loc[35, 'Bonus'] = 0.0
    df.loc[35, 'Overtime_Pay'] = 0.0

    # Issue 6: 3 missing department codes (possible in export if org structure has gaps)
    df.loc[8, 'Department'] = None
    df.loc[18, 'Department'] = None
    df.loc[38, 'Department'] = None

    # Issue 7: Tax withholding anomaly - effective rate suspiciously low for high earner
    df.loc[40, 'Monthly_Salary'] = 12000.00
    df.loc[40, 'Gross_Pay'] = 12000.00
    df.loc[40, 'Federal_Tax'] = round(12000 * 0.03, 2)  # Only 3% effective rate (too low)

    # Issue 8: Zero net pay - deductions consume entire gross (not a hard stop, but a flag)
    gross_45 = df.loc[45, 'Gross_Pay']
    df.loc[45, 'Garnishment'] = round(gross_45 * 0.25, 2)
    df.loc[45, '401K_Deduction'] = round(gross_45 * 0.15, 2)
    df.loc[45, 'Medical_Deduction'] = 500.00
    total_ded_45 = (df.loc[45, 'Federal_Tax'] + df.loc[45, 'State_Tax'] +
                    df.loc[45, 'SS_Withholding'] + df.loc[45, 'Medicare_Withholding'] +
                    df.loc[45, 'Medical_Deduction'] + df.loc[45, 'Dental_Deduction'] +
                    df.loc[45, '401K_Deduction'] + df.loc[45, 'Garnishment'])
    df.loc[45, 'Net_Pay'] = round(gross_45 - total_ded_45, 2)

    # Write to Excel
    output_path = Path(output_file)
    df.to_excel(output_path, sheet_name='Payroll Results', index=False)
    print(f"Test payroll data generated: {output_path}")
    print(f"Total records: {len(df)}")
    print(f"\nInjected Issues (all post-processing, no SAP hard stops):")
    print(f"  - SS wage base exceeded with continued withholding: 1 employee (row 20)")
    print(f"  - Garnishment exceeding 25% disposable: 1 employee (row 25)")
    print(f"  - Overtime rate at 1.25x instead of 1.5x FLSA: 1 employee (row 30)")
    print(f"  - Duplicate records in export: 2 employees (copies of rows 5, 12)")
    print(f"  - Unusually high payment (outlier >3 std dev): 1 employee (row 35)")
    print(f"  - Missing department codes: 3 employees (rows 8, 18, 38)")
    print(f"  - Tax withholding rate anomaly (3% effective): 1 employee (row 40)")
    print(f"  - Zero/negative net pay from deductions: 1 employee (row 45)")
    print(f"\nExpected outcome: Risk score 50-65 (High Risk)")
    print(f"\nTermination detection: Use EE_Status column (0=Active, 3=Withdrawn)")

    return df


if __name__ == '__main__':
    generate_test_payroll_data()
