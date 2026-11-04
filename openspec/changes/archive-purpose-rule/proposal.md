# Proposal

## Why

When `openspec archive` creates a capability, it writes a placeholder Purpose
("TBD - created by archiving change ...") into the new main spec, and
`openspec validate --strict` then fails on that spec. In this repository it
happened after archiving `add-benchmark`: the strict validation failed until
the Purpose was written by hand, after the push.

## What Changes

- A `[warrant]` archive guidance entry: after archiving a change that creates a
  capability, replace the placeholder Purpose of each new main spec with what
  the capability is for, then run the contract's verification.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `warrant-rules`: Purpose after archive.

## Impact

`skills/warrant-setup/rules.yaml` and its copies, kit tests.

## Why code is needed

Only a rule changes; a kit test keeps it in the shipped rules.

## Out of scope

This change adds guidance; it does not edit specs that OpenSpec writes.

Features and options deliberately left out:

- A check that blocks archiving.

## Assumptions

Confirmed by the requester: add the Purpose reminder. No other decision is open.
