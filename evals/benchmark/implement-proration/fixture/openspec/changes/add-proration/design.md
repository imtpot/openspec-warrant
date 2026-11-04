# Design

## Decisions

Each part records the first option of the option ladder that fully works:
no change, existing project code, standard library or platform, an installed
dependency, new code.

### 1. Interface

`prorate(amount: int, start: date, end: date, period_start: date,
period_end: date) -> int` in `app/billing.py`, next to `days_between`.
No change does not work: no function prorates today.

### 2. Day count

Existing project code: `days_between` counts days from a start to an excluded
end, so it counts both the used days and the period length (28 to 31 days for
a month). No change does not work: nothing counts used days.

### 3. Clamping to the period

Standard library: the built-in `max` of the starts and `min` of the ends give
the overlap. No change and existing project code do not work: nothing clamps
dates today.

### 4. Rounding

Standard library: `decimal` with `ROUND_HALF_UP` rounds an exact half cent up.
The built-in `round()` does not work: it rounds half to even.

### 5. Validation

New code: two checks raise `ValueError` for a negative amount and for a period
whose end is not after its start. No earlier option validates these inputs.
