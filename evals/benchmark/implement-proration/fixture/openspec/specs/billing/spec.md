# billing Specification

## Purpose
Monthly subscription prices in integer cents.

## Requirements

### Requirement: Monthly price

The billing module SHALL charge the plan price once per seat per month.

#### Scenario: Three team seats
- **WHEN** the team plan has three seats
- **THEN** the monthly price is 14700 cents
