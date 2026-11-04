# Proposal

## Why

Two gaps against the kit's purpose. First, `warrant-minimal-change` forbids
removing validation, error handling and security checks, but says nothing
about leaving them out of new code, so its option ladder ("the least code that
works") can read as permission to skip an input check in a new function.
Ponytail, where the ladder comes from, never cuts validation, error handling,
security or accessibility, in old or new code. Second, outside OpenSpec and
TDD the skill loads only through its description, and no eval checks that:
every minimal-change scenario names the skill in its prompt.

## What Changes

- The protected list applies to new code as well: never leave out or remove
  validation at trust boundaries, error handling that prevents data loss,
  security checks, accessibility of user interfaces, or anything requested.
- A new scenario `minimal-change-implicit` gives the minimal-change task
  without naming any skill.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `minimal-change`: protected code covers new code and accessibility.
- `behavioral-evals`: a scenario that does not name the skill.

## Impact

`skills/warrant-minimal-change/SKILL.md`,
`evals/scenarios/minimal-change-implicit.toml`.

## Why code is needed

Only the skill text and a scenario file change.

## Out of scope

This change closes the two gaps; it does not change the option ladder.

Features and options deliberately left out:

- Implicit-trigger scenarios for the other skills; `warrant-verify` already has
  one (`verify-no-contract`).

## Assumptions

Confirmed by the requester: never leave out validation, error handling,
security or accessibility; add a scenario that does not name the skill.
No other decision is open.
