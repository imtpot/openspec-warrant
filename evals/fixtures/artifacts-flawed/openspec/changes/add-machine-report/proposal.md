# Proposal

## Why

CI needs the report in a machine-readable form.

## What Changes

- `report()` gains a machine-readable mode.

## Capabilities

### New Capabilities
- `machine-report`: the machine-readable report.

## Impact

`app/report.py`.

## Why code is needed

No existing option prints the rows in a machine format.

## Out of scope

This change adds one machine format; it does not change the text output.

## Assumptions

None.
