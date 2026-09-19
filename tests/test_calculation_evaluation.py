from tools.debt import (
    calculate_emi,
    calculate_total_repayment,
    calculate_total_interest,
)


def check_close(actual, expected, tolerance=0.01):
    return abs(actual - expected) <= tolerance


print("=" * 70)
print("CALCULATION EVALUATION")
print("=" * 70)


# --------------------------------------------------
# EMI
# --------------------------------------------------

emi = calculate_emi(
    principal=100000,
    annual_rate=10,
    tenure_months=36,
)

expected_emi = 3226.72

print("\nEMI")
print("Expected:", expected_emi)
print("Actual  :", round(emi, 2))

assert check_close(
    emi,
    expected_emi,
    0.05
)

print("PASS")


# --------------------------------------------------
# TOTAL REPAYMENT
# --------------------------------------------------

repayment = calculate_total_repayment(
    principal=100000,
    annual_rate=10,
    tenure_months=36,
)

expected_repayment = emi * 36

print("\nTOTAL REPAYMENT")
print("Expected:", round(expected_repayment, 2))
print("Actual  :", round(repayment, 2))

assert check_close(
    repayment,
    expected_repayment,
    0.05
)

print("PASS")


# --------------------------------------------------
# TOTAL INTEREST
# --------------------------------------------------

interest = calculate_total_interest(
    principal=100000,
    annual_rate=10,
    tenure_months=36,
)

expected_interest = repayment - 100000

print("\nTOTAL INTEREST")
print("Expected:", round(expected_interest, 2))
print("Actual  :", round(interest, 2))

assert check_close(
    interest,
    expected_interest,
    0.05
)

print("PASS")


print("\n" + "=" * 70)
print("ALL CALCULATION TESTS PASSED")
print("=" * 70)