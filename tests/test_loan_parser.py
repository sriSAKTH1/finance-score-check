from agents.loan_parser import extract_loan_details


result = extract_loan_details(
    "Can I take a ₹50,000 loan at 12% for 24 months?"
)

print("LOAN PARSER")
print("====================")

print("Loan Amount:", result.loan_amount)
print("Interest Rate:", result.interest_rate)
print("Tenure:", result.tenure_months)
print("Purpose:", result.purpose)