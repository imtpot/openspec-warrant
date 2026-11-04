# Spec Delta

## ADDED Requirements

### Requirement: Shares add up

WHEN `split` is called with valid input, the split function SHALL return one
share per weight with shares that add up to the total.

#### Scenario: Three equal weights
- **WHEN** `split(10, [1, 1, 1])` is called
- **THEN** the result has three shares that add up to 10

### Requirement: Proportional base shares

The split function SHALL give each weight at least `total * weight // sum(weights)` units.

#### Scenario: Exact split
- **WHEN** `split(6, [1, 2])` is called
- **THEN** the result is `[2, 4]`

### Requirement: Largest remainder

The split function SHALL give the units left after the base shares, one each,
to the weights with the largest remainders `total * weight % sum(weights)`.

#### Scenario: Larger remainder wins over larger weight
- **WHEN** `split(3, [5, 2])` is called
- **THEN** the result is `[2, 1]`

### Requirement: Ties

IF two weights have equal remainders, THEN the split function SHALL give the
extra unit to the earlier weight.

#### Scenario: Equal weights
- **WHEN** `split(2, [1, 1, 1])` is called
- **THEN** the result is `[1, 1, 0]`

### Requirement: Empty weights

IF the weights list is empty, THEN the split function SHALL raise `ValueError`.

#### Scenario: No teams
- **WHEN** `split(10, [])` is called
- **THEN** `ValueError` is raised

### Requirement: Negative weight

IF a weight is negative, THEN the split function SHALL raise `ValueError`.

#### Scenario: One negative weight
- **WHEN** `split(10, [2, -1])` is called
- **THEN** `ValueError` is raised

### Requirement: Zero weights

IF every weight is zero, THEN the split function SHALL raise `ValueError`.

#### Scenario: All zero
- **WHEN** `split(10, [0, 0])` is called
- **THEN** `ValueError` is raised

### Requirement: Negative total

IF the total is negative, THEN the split function SHALL raise `ValueError`.

#### Scenario: Negative budget
- **WHEN** `split(-1, [1])` is called
- **THEN** `ValueError` is raised
