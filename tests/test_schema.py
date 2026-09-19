from context.financial_context import FinancialContext


context = FinancialContext()

user = context.get_user("demo_user_001")

print("USER")
print("======")

print("Name:", user.profile.name)
print("Age:", user.profile.age)

print("\nINCOME")
print("======")

print("Salary:", user.income.monthly_salary)
print("Other Income:", user.income.other_income)

print("\nASSETS")
print("======")

print("Bank:", user.assets.bank_savings)
print("Mutual Funds:", user.assets.mutual_funds)
print("Gold:", user.assets.gold)

print("\nRISK")
print("======")

print("Risk Profile:", user.risk_profile.category)

print("\nGOALS")
print("======")

for goal in user.goals:
    print(goal.name)
    print("Target:", goal.target_amount)
    print("Years:", goal.years)