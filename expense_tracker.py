#!/usr/bin/env python3
"""
expense_tracker.py
"""

# --- default budget limits ---
DEFAULT_BUDGETS = {
    'rent': 800,
    'food': 300,
    'transport': 150,
    'entertainment': 100,
    'utilities': 200,
    'other': 200
}

# --- overspending thresholds ---
WARNING_PERCENT = 0.80   # warn at 80% of budget
OVERSPEND_PERCENT = 1.00  # flag at 100% of budget


def get_expense(category):
    """ask how much was spent in a category"""
    while True:
        try:
            amount = float(input(f"  {category}: N"))
            if amount < 0:
                print("    Can't be negative, try again")
                continue
            return amount
        except ValueError:
            print("    That's not a number, try again")


def check_spending(category, spent, budget):
    """check if spending is within budget"""
    percent = spent / budget if budget > 0 else 0
    
    # comparison operators
    is_warning = percent >= WARNING_PERCENT and percent < OVERSPEND_PERCENT
    is_overspent = percent >= OVERSPEND_PERCENT
    is_critical = percent >= 1.20  # 20% over budget
    
    # logical conditions for status
    if is_critical:
        status = "CRITICAL"
        message = f"wayyy over budget! ({percent*100:.0f}%)"
    elif is_overspent:
        status = "OVERSPENT"
        message = f"over budget by N{spent - budget:.2f} ({percent*100:.0f}%)"
    elif is_warning:
        status = "WARNING"
        message = f"Getting close ({percent*100:.0f}%)"
    else:
        status = "OK"
        message = f"On track ({percent*100:.0f}%)"
    
    return status, message, percent


def main():
    print()
    print("-" * 50)
    print("  MONTHLY EXPENSE TRACKER")
    print("-" * 50)
    print()
    print("Enter your spending for each category:")
    print()
    
    expenses = {}
    total_spent = 0
    total_budget = 0
    
    # collect expenses
    for category, budget in DEFAULT_BUDGETS.items():
        print(f"{category} (Budget: N{budget})")
        spent = get_expense(category)
        expenses[category] = {'spent': spent, 'budget': budget}
        total_spent += spent
        total_budget += budget
        print()
    
    # check each category
    print("=" * 50)
    print("  SPENDING REPORT")
    print("=" * 50)
    print()
    
    overspent_categories = []
    warning_categories = []
    
    for category, data in expenses.items():
        spent = data['spent']
        budget = data['budget']
        status, message, percent = check_spending(category, spent, budget)
        
        # track problems
        if status == "OVERSPENT" or status == "CRITICAL":
            overspent_categories.append(category)
        elif status == "WARNING":
            warning_categories.append(category)
        
        # print with emoji indicators
        if status == "OK":
            icon = "  "
        elif status == "WARNING":
            icon = "! "
        else:
            icon = "X "
        
        print(f"  {icon}{category:15s} N{spent:>7.2f} / N{budget:>6.2f}  {message}")
    
    # overall summary
    print()
    print("-" * 50)
    overall_percent = total_spent / total_budget if total_budget > 0 else 0
    print(f"  TOTAL:           N{total_spent:>7.2f} / N{total_budget:>6.2f}  ({overall_percent*100:.0f}%)")
    print("-" * 50)
    print()
    
    # flag overspending alerts
    if overspent_categories:
        print("  OVERSPENDING ALERT!")
        print(f"  {len(overspent_categories)} category(s) Over budget:")
        for cat in overspent_categories:
            over = expenses[cat]['spent'] - expenses[cat]['budget']
            print(f"    - {cat}: N{over:.2f} Over")
        print()
    
    if warning_categories:
        print("  WARNING: Getting close to budget:")
        for cat in warning_categories:
            left = expenses[cat]['budget'] - expenses[cat]['spent']
            print(f"    - {cat}: only N{left:.2f} left")
        print()
    
    if not overspent_categories and not warning_categories:
        print("  All good! No overspending this Month.")
        print()
    
    print("=" * 50)


if __name__ == "__main__":
    main()
