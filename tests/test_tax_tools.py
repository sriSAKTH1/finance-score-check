from tools.tax import (
    calculate_taxable_income,
    calculate_tax_saving,
    calculate_post_tax_return,
    calculate_tax_impact,
)


income = 1_200_000
deductions = 150_000
tax_rate = 20


taxable_income = calculate_taxable_income(
    gross_income=income,
    deductions=deductions,
)


tax_saving = calculate_tax_saving(
    deduction_amount=deductions,
    applicable_tax_rate=tax_rate,
)


post_tax_return = calculate_post_tax_return(
    pre_tax_return=10,
    tax_rate=tax_rate,
)


impact = calculate_tax_impact(
    income=income,
    deductions=deductions,
    tax_rate=tax_rate,
)


print("\nTAX TOOL TEST")
print("=============")

print(
    f"Taxable income: "
    f"₹{taxable_income:,.2f}"
)

print(
    f"Estimated tax saving: "
    f"₹{tax_saving:,.2f}"
)

print(
    f"Post-tax return assumption: "
    f"{post_tax_return:.2f}%"
)

print("\nTax impact:")
print(impact)