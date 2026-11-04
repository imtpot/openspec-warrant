# Proposal

## Why

Verification results in `tasks.md` are free text, so neither a reader nor CI
can check them without interpretation. anvil's `DECISION:` line shows the
value of one fixed line; warrant's artifact review already ends with one.

## What Changes

- A `[warrant]` tasks rule fixes the verification result format on the task's
  own line: `Result: exit <code>, <result line>` or `Result: not run, <reason>`.
- The archive guidance asks for a `Result:` line on every verification task.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `warrant-rules`: verification result format.

## Impact

`skills/warrant-setup/rules.yaml` and its copies, `evals/tests/test_kit.py`,
`docs/design.md`.

## Why code is needed

The rules carry the change; a kit test keeps the format in the shipped rules.

## Out of scope

This change fixes the format of verification results; it does not add a CI job.

Features and options deliberately left out:

- A brevity rule and a closing "Not checked / Risks" line; tried in
  `warrant-verify` and dropped so that no skill is an exception.
- A machine-readable summary file.

## Assumptions

Confirmed by the requester: take anvil's CI-parsable result idea; no brevity
rule in any skill.

- The result format is `Result: exit <code>, <result line>` or
  `Result: not run, <reason>`, on the verification task's own line.
  Owner: requester (decided while the requester was away).
