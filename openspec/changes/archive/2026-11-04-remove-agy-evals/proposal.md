# Proposal

## Why

Antigravity CLI (agy) cannot be evaluated headless: it denies commands even
when permission rules allow them, does not name the denied command, and the set
of scenarios it completes changes from run to run (10 of 17 not run in the last
run). Its results say nothing about the skills, and supporting it costs
agy-only code and a requirement.

## What Changes

- Remove agy from the eval runner's agents, with its permission settings and
  the detection of headless permission denials.
- **BREAKING** for eval users: `--agent agy` selects nothing.
- README: drop agy from the results table and note that agy discovers the
  skills and the contract but is not evaluated until its headless permissions
  work.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `behavioral-evals`: three supported agents; the headless-denial requirement is removed.

## Impact

`evals/warrant_evals/runner.py`, `evals/tests/test_runner.py`, `README.md`,
`openspec/config.yaml` (context), the Purpose of
`openspec/specs/behavioral-evals/spec.md`.

## Why code is needed

The runner's agent list and the agy-specific handling are code; configuration
cannot remove them.

## Out of scope

This change removes agy from the evals; it does not change any skill or the schema.

Features and options deliberately left out:

- An opt-in flag that keeps agy runnable.
- Keeping the permission-denial detection for other agents; none of them needs it.

## Assumptions

Confirmed by the requester: remove agy from the evals, as a separate change
after `add-warrant-review`.

None.
