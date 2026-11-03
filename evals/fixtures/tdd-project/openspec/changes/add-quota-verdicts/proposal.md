# Proposal

## Why

Operators need the shortfall verdict and safe input handling.

## What Changes

- `check()` returns "short" and rejects negative input.

## Capabilities

### New Capabilities
- `quota-check`: the verdict for one quota request.

## Impact

`app/quota.py`.
