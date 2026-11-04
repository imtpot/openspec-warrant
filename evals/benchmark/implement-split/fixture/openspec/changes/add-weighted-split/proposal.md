# Proposal

## Why

Finance splits a whole number of budget units between teams by weight. Today
they do it by hand in a spreadsheet, and rounding makes the shares add up to
more or less than the budget.

## What Changes

- A function `split(total, weights)` returns whole-unit shares that add up to
  the total, proportional to the weights, with the remainder assigned by the
  largest remainder method.
- Invalid input raises `ValueError`.

## Capabilities

### New Capabilities
- `weighted-split`: split a whole number by weights.

### Modified Capabilities
None.

## Impact

New `app/split.py` and `tests/test_split.py`.

## Why code is needed

No configuration or existing tool in this project splits budgets; the
standard library has no largest remainder function.

## Out of scope

This change adds the function only; it adds no command line or file output.

Features and options deliberately left out:

- Fractional units.
- Minimum shares per team.

## Assumptions

Confirmed by the requester: whole units only; the largest remainder method;
ties go to the earlier weight; invalid input raises `ValueError`. No other
decision is open.
