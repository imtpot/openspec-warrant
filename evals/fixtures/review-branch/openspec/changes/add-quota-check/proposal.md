# Proposal

## Why

Operators need to know whether a request fits the free quota.

## What Changes

- `check()` returns a verdict for a quota request.

## Capabilities

### New Capabilities
- `quota-check`: the verdict for one quota request.

## Impact

`app/quota.py`, `tests/test_quota.py`.
