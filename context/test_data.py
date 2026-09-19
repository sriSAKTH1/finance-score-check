from demo_data_provider import load_user


user = load_user("demo_user_001")

print("User ID:", user["user_id"])
print("Age:", user["profile"]["age"])
print("Monthly Salary:", user["income"]["monthly_salary"])
print("Bank Savings:", user["assets"]["bank_savings"])
print("Risk Profile:", user["risk_profile"]["category"])