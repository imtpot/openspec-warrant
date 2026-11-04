# Spec Delta

## ADDED Requirements

### Requirement: Prorated amount

WHEN `prorate` is called, the billing module SHALL return `amount` multiplied by
the used days and divided by the days of the billing period, where the used
days are the days of `[start, end)` inside `[period_start, period_end)`.

#### Scenario: Half of a 30-day period
- **WHEN** `prorate(3000, date(2026, 4, 16), date(2026, 5, 1), date(2026, 4, 1), date(2026, 5, 1))` is called
- **THEN** the result is 1500

### Requirement: Real period length

The billing module SHALL count the days of the billing period from its dates,
so that a period has between 28 and 31 days.

#### Scenario: February
- **WHEN** `prorate(2800, date(2026, 2, 1), date(2026, 2, 15), date(2026, 2, 1), date(2026, 3, 1))` is called
- **THEN** the result is 1400

### Requirement: Rounding

The billing module SHALL round the prorated amount to whole cents, with an
exact half cent rounded up.

#### Scenario: Two thirds
- **WHEN** `prorate(1000, date(2026, 4, 11), date(2026, 5, 1), date(2026, 4, 1), date(2026, 5, 1))` is called
- **THEN** the result is 667

### Requirement: Start before the period

IF `start` is before `period_start`, THEN the billing module SHALL count the
used days from `period_start`.

#### Scenario: Started last month
- **WHEN** `prorate(3000, date(2026, 3, 20), date(2026, 4, 16), date(2026, 4, 1), date(2026, 5, 1))` is called
- **THEN** the result is 1500

### Requirement: End after the period

IF `end` is after `period_end`, THEN the billing module SHALL count the used
days up to `period_end`.

#### Scenario: Ends next month
- **WHEN** `prorate(3000, date(2026, 4, 16), date(2026, 6, 1), date(2026, 4, 1), date(2026, 5, 1))` is called
- **THEN** the result is 1500

### Requirement: No overlap

IF `[start, end)` has no day inside the billing period, THEN the billing module
SHALL return 0.

#### Scenario: Cancelled before the period
- **WHEN** `prorate(3000, date(2026, 3, 1), date(2026, 3, 10), date(2026, 4, 1), date(2026, 5, 1))` is called
- **THEN** the result is 0

### Requirement: Negative amount

IF `amount` is negative, THEN the billing module SHALL raise `ValueError`.

#### Scenario: Refund passed as amount
- **WHEN** `prorate(-100, date(2026, 4, 1), date(2026, 5, 1), date(2026, 4, 1), date(2026, 5, 1))` is called
- **THEN** `ValueError` is raised

### Requirement: Empty period

IF `period_end` is not after `period_start`, THEN the billing module SHALL
raise `ValueError`.

#### Scenario: Swapped period dates
- **WHEN** `prorate(3000, date(2026, 4, 1), date(2026, 5, 1), date(2026, 5, 1), date(2026, 4, 1))` is called
- **THEN** `ValueError` is raised
