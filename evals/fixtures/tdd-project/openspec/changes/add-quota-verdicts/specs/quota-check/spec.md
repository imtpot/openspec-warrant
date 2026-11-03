# Spec Delta

## Purpose

Tells whether one quota request fits the free quota, and rejects invalid input.

## ADDED Requirements

### Requirement: Shortfall verdict

WHEN the free amount is less than the needed amount, the quota check SHALL return "short".

#### Scenario: Not enough free
- **WHEN** free is 2 and needed is 4
- **THEN** the result is "short"

### Requirement: Negative input

IF the needed amount is negative, THEN the quota check SHALL raise ValueError.

#### Scenario: Negative request
- **WHEN** needed is -1
- **THEN** the quota check raises ValueError
