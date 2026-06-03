#!/usr/bin/env python3
"""
loan_checker.py
"""

# --- loan rules ---
MIN_AGE = 18
MAX_AGE = 65
MIN_INCOME = 250000      # yearly income in Naira
MIN_CREDIT_SCORE = 6000
MAX_DEBT_RATIO = 0.40   # debt can't exceed 40% of income


def get_number(prompt, min_val=None, max_val=None):
    """ask for a number and validate it"""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  Must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"  Must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("  That's not a number, try again")


def check_eligibility(age, income, credit_score, monthly_debt):
    """check if applicant qualifies for the loan"""
    
    # calculate debt-to-income ratio
    yearly_debt = monthly_debt * 12
    debt_ratio = yearly_debt / income if income > 0 else 1
    
    # --- comparison operators ---
    old_enough = age >= MIN_AGE
    not_too_old = age <= MAX_AGE
    income_ok = income >= MIN_INCOME
    credit_ok = credit_score >= MIN_CREDIT_SCORE
    debt_ok = debt_ratio <= MAX_DEBT_RATIO
    
    # --- logical operators ---
    age_ok = old_enough and not_too_old          # must be 18-65
    financially_ok = income_ok and credit_ok     # must have income and credit
    debt_clean = debt_ok                         # debt ratio must be good
    
    # overall eligibility
    eligible = age_ok and financially_ok and debt_clean
    
    return eligible, {
        'age_ok': age_ok,
        'financially_ok': financially_ok,
        'debt_ok': debt_clean,
        'debt_ratio': debt_ratio
    }


def main():
    print()
    print("-" * 50)
    print("  LOAN ELIGIBILITY CHECKER")
    print("-" * 50)
    print()
    print(f"Rules: Age {MIN_AGE}-{MAX_AGE}, Income >= N{MIN_INCOME:,}")
    print(f"       Credit Ccore >= {MIN_CREDIT_SCORE}")
    print(f"       Debt Ratio <= {MAX_DEBT_RATIO*100:.0f}%")
    print()
    
    # collect inputs
    name = input("Applicant Name: ").strip()
    
    print()
    age = get_number("Age: ", min_val=16, max_val=100)
    income = get_number("Yearly Income (N): ", min_val=0)
    credit_score = get_number("Credit Score (3000-8500): ", min_val=3000, max_val=8500)
    monthly_debt = get_number("Monthly Debt Payments (N): ", min_val=0)
    
    # check eligibility
    eligible, checks = check_eligibility(age, income, credit_score, monthly_debt)
    
    # show results
    print()
    print("=" * 50)
    print(f"  RESULTS FOR {name.upper()}")
    print("=" * 50)
    print()
    
    print(f"  Age:           {age:.0f} years")
    print(f"  Income:        N{income:,.0f}/year")
    print(f"  Credit Score:  {credit_score:.0f}")
    print(f"  Debt Ratio:    {checks['debt_ratio']*100:.1f}%")
    print()
    print("-" * 50)
    
    # breakdown with checkmarks
    status_age = "PASS" if checks['age_ok'] else "FAIL"
    status_fin = "PASS" if checks['financially_ok'] else "FAIL"
    status_debt = "PASS" if checks['debt_ok'] else "FAIL"
    
    print(f"  Age Check:       {status_age}")
    print(f"  Financial Check: {status_fin}")
    print(f"  Debt Check:      {status_debt}")
    print("-" * 50)
    print()
    
    if eligible:
        print("  STATUS: APPROVED  :)")
        print("  You qualify for the loan!")
    else:
        print("  STATUS: DENIED  :(")
        print("  You don't meet all Requirements.")
        
        # tell them why
        if not checks['age_ok']:
            if age < MIN_AGE:
                print(f"  -> Too young. need to be at least {MIN_AGE}.")
            else:
                print(f"  -> Too old. max age is {MAX_AGE}.")
        if not checks['financially_ok']:
            if income < MIN_INCOME:
                print(f"  -> Income too Low. Need atleast N{MIN_INCOME:,}+.")
            if credit_score < MIN_CREDIT_SCORE:
                print(f"  -> Credit Score too Low. need {MIN_CREDIT_SCORE}+.")
        if not checks['debt_ok']:
            print(f"  -> Debt Ratio too High ({checks['debt_ratio']*100:.1f}%).")
            print(f"     Must be under {MAX_DEBT_RATIO*100:.0f}%.")
    
    print()
    print("=" * 50)


if __name__ == "__main__":
    main()
