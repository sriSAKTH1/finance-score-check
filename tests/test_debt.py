from tools.debt import (
    calculate_emi,
    calculate_total_interest,
    calculate_total_repayment,
    calculate_existing_emi,
    calculate_debt_burden,
    calculate_post_loan_cashflow,
)


USER_ID = "demo_user_001"

LOAN_AMOUNT = 50000
INTEREST_RATE = 12
TENURE = 24


emi = calculate_emi(
    LOAN_AMOUNT,
    INTEREST_RATE,
    TENURE,
)

interest = calculate_total_interest(
    LOAN_AMOUNT,
    INTEREST_RATE,
    TENURE,
)

repayment = calculate_total_repayment(
    LOAN_AMOUNT,
    INTEREST_RATE,
    TENURE,
)

existing_emi = calculate_existing_emi(USER_ID)

debt_burden = calculate_debt_burden(USER_ID)

post_loan_cashflow = calculate_post_loan_cashflow(
    USER_ID,
    emi,
)


print("DEBT CALCULATION")
print("=================")

print(f"Loan Amount          : ₹{LOAN_AMOUNT:,.2f}")
print(f"Interest Rate        : {INTEREST_RATE}%")
print(f"Tenure               : {TENURE} months")
print(f"New Loan EMI         : ₹{emi:,.2f}")
print(f"Total Interest       : ₹{interest:,.2f}")
print(f"Total Repayment      : ₹{repayment:,.2f}")

print("\nEXISTING DEBT")
print("=============")

print(f"Existing EMI         : ₹{existing_emi:,.2f}")
print(f"Existing Debt Burden : {debt_burden:.2f}%")

print("\nAFTER NEW LOAN")
print("==============")

print(
    f"Post Loan Cashflow   : ₹{post_loan_cashflow:,.2f}"
)