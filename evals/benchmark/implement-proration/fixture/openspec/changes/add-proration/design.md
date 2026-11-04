# Design

## Decisions

### 1. Interface

`prorate(amount: int, start: date, end: date, period_start: date,
period_end: date) -> int` in `app/billing.py`, next to `days_between`.

### 2. Day count

Use `days_between` for every day count, so the period length is the real
number of days in the period (28 to 31 for a month).

### 3. Integer rounding

Compute `amount * used_days / period_days` with integers, rounding half up,
so that no floating point error changes a cent.
