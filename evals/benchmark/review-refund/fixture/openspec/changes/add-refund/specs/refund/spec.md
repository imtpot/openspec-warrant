# Spec Delta

## ADDED Requirements

### Requirement: Refund amount

WHEN `refund_amount` is called, the refund module SHALL return `amount`
multiplied by the unused days and divided by the days of the period, with an
exact half cent rounded up.

#### Scenario: Half of April
- **WHEN** `refund_amount(3000, date(2026, 4, 16), date(2026, 4, 1), date(2026, 5, 1))` is called
- **THEN** the result is 1500

### Requirement: Cancel at the start

IF the cancel date is not after the period start, THEN the refund module SHALL
return the whole amount.

#### Scenario: Cancelled before the period
- **WHEN** `refund_amount(3000, date(2026, 3, 20), date(2026, 4, 1), date(2026, 5, 1))` is called
- **THEN** the result is 3000

### Requirement: Cancel after the end

IF the cancel date is after the period end, THEN the refund module SHALL
return 0.

#### Scenario: Cancelled after the period
- **WHEN** `refund_amount(3000, date(2026, 5, 10), date(2026, 4, 1), date(2026, 5, 1))` is called
- **THEN** the result is 0

### Requirement: Refund note

WHEN `export_refund` is called, the refund module SHALL write the refund in
cents to a file of that name in `exports/`.

#### Scenario: Note written
- **WHEN** `export_refund('alice.txt', 1500)` is called
- **THEN** `exports/alice.txt` contains `1500`
