from tools.insurance import (
    calculate_insurance_gap,
    calculate_life_cover_multiple,
    calculate_health_cover_per_dependent,
    calculate_total_insurance_cover,
)


existing_life_cover = 1000000
required_life_cover = 3000000

existing_health_cover = 500000
dependents = 2

life_gap = calculate_insurance_gap(
    required_cover=required_life_cover,
    existing_cover=existing_life_cover,
)

life_multiple = calculate_life_cover_multiple(
    annual_income=80000 * 12,
    life_cover=existing_life_cover,
)

health_per_dependent = calculate_health_cover_per_dependent(
    health_cover=existing_health_cover,
    dependents=dependents,
)

total_cover = calculate_total_insurance_cover(
    life_cover=existing_life_cover,
    health_cover=existing_health_cover,
)


print("\nINSURANCE TOOL TEST")
print("===================")

print(f"Life insurance gap: ₹{life_gap:,.2f}")
print(f"Life cover / annual income: {life_multiple:.2f}x")
print(
    f"Health cover per dependent: "
    f"₹{health_per_dependent:,.2f}"
)
print(f"Total recorded insurance cover: ₹{total_cover:,.2f}")