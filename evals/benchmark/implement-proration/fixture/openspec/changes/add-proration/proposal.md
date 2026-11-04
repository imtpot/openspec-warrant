# Proposal

## Why

Customers who start or cancel in the middle of a billing period are charged a
full month. Support refunds the difference by hand, and the refunds disagree
with each other by a cent or more.

## What Changes

- A function `prorate(amount, start, end, period_start, period_end)` returns
  the part of `amount` that falls on the days of `[start, end)` inside the
  billing period `[period_start, period_end)`.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `billing`: prorated charges.

## Impact

`app/billing.py` and its tests.

## Why code is needed

No configuration setting or existing tool computes prorated charges, and a
documentation change cannot compute a charge: support already has written
rules and still gets different results by hand. `days_between` in
`app/billing.py` counts days and stays the only day counter.

## Out of scope

This change computes one prorated amount; it does not create invoices or
refunds.

Features and options deliberately left out:

- Proration by hour.
- Currencies other than integer cents.

## Assumptions

Confirmed by the requester: every rule in the spec, including rounding half
up and clamping to the period; `prorate` lives in `app/billing.py` next to
`days_between` and counts every day with it; rounding uses the standard
library's `decimal` module; the terms "billing period" (the days of
`[period_start, period_end)`) and "used days" (the days of `[start, end)`
inside the billing period). No other decision is open.
