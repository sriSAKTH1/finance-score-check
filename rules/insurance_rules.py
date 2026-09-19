def check_life_cover_gap(required_cover: float, existing_cover: float):
    gap = max(required_cover - existing_cover, 0.0)

    if gap > 0:
        return {
            "rule": "life_cover_gap",
            "status": "attention",
            "message": f"Life insurance gap identified: ₹{gap:,.2f}.",
            "gap": gap,
        }

    return {
        "rule": "life_cover_gap",
        "status": "informational",
        "message": "No life insurance gap based on the supplied required-cover assumption.",
        "gap": 0.0,
    }


def check_health_cover(health_cover: float):
    if health_cover <= 0:
        return {
            "rule": "health_cover",
            "status": "attention",
            "message": "No health insurance cover is recorded.",
        }

    return {
        "rule": "health_cover",
        "status": "informational",
        "message": f"Recorded health insurance cover: ₹{health_cover:,.2f}.",
    }


def check_dependents_coverage(health_cover: float, dependents: int):
    if dependents <= 0:
        return {
            "rule": "dependent_coverage",
            "status": "informational",
            "message": "No dependents are recorded.",
        }

    if health_cover <= 0:
        return {
            "rule": "dependent_coverage",
            "status": "attention",
            "message": "Dependents are recorded but no health cover is available.",
        }

    return {
        "rule": "dependent_coverage",
        "status": "informational",
        "message": (
            f"Health cover is recorded for {dependents} dependent(s). "
            "Review adequacy based on actual healthcare costs and policy terms."
        ),
    }


def evaluate_insurance(
    required_life_cover: float,
    existing_life_cover: float,
    health_cover: float,
    dependents: int,
):
    return {
        "life_cover": check_life_cover_gap(
            required_life_cover,
            existing_life_cover,
        ),
        "health_cover": check_health_cover(
            health_cover,
        ),
        "dependent_coverage": check_dependents_coverage(
            health_cover,
            dependents,
        ),
    }