# billing Specification

## Purpose
Prices and charges of monthly subscriptions, in integer cents per seat and month.

## Requirements

### Requirement: Monthly price

The billing module SHALL charge the plan price once per seat per month.

#### Scenario: Three team seats
- **WHEN** the team plan has three seats
- **THEN** the monthly price is 14700 cents
