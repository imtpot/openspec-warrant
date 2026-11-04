# Proposal

## Why

Support refunds unused days by hand and gets different amounts each time.

## What Changes

- `refund_amount(amount, cancel, period_start, period_end)` returns the refund
  for the unused days of a billing period.
- `export_refund(name, cents)` writes a refund note to `exports/`.

## Capabilities

### New Capabilities
- `refund`: refund unused days.

### Modified Capabilities
None.

## Impact

New `app/refund.py` and its tests.

## Why code is needed

No existing tool computes refunds.

## Out of scope

This change computes and exports one refund; it does not pay it out.

Features and options deliberately left out:

- Currencies other than integer cents.

## Assumptions

Confirmed by the requester: unused days are the days from the cancel date to
the period end, both counted from `app/dates.py`; an exact half cent rounds up;
a cancel date not after the period start refunds the whole amount; a cancel
date after the period end refunds nothing. No other
decision is open.
