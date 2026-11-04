"""Monthly subscription billing. Amounts are integer cents."""

from datetime import date

PLANS = {'basic': 900, 'team': 4900}


def days_between(start: date, end: date) -> int:
    """Days from `start` (included) to `end` (excluded)."""
    return (end - start).days


def monthly_price(plan: str, seats: int = 1) -> int:
    if plan not in PLANS:
        raise ValueError(f'unknown plan: {plan}')
    if seats < 1:
        raise ValueError('seats must be at least 1')
    return PLANS[plan] * seats
