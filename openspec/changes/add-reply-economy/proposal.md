# Proposal

## Why

The kit's fifth principle asks to spend the reader's tokens carefully, and
Ponytail shows how: a reply a busy person understands in one read, ending with
one or two lines on what was skipped or not checked and any risk. warrant has
no such rule yet; reports grew long in the eval transcripts, and a reader has
to dig for what was not verified. Separately, verification results in
`tasks.md` are free text, so CI cannot check them; anvil's `DECISION:` line
shows the value of one fixed line.

## What Changes

- `warrant-verify`, which every completion claim passes through, asks for a
  short report: one line per verification command, then a closing line
  `Not checked: <...>; Risks: <...>` (`none` allowed).
- A `[warrant]` tasks rule fixes the verification result format on the task
  line: `Result: exit <code>, <result line>` or `Result: not run, <reason>`.
- The archive guidance asks for that line on every verification task.
- The verify scenarios check the closing line.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `verification-evidence`: short report with a closing line.
- `warrant-rules`: verification result format.
- `behavioral-evals`: closing-line check.

## Impact

`skills/warrant-verify/SKILL.md`, `skills/warrant-setup/rules.yaml` and its
copies, `evals/scenarios/verify*.toml`, `evals/warrant_evals/checks.py`,
`docs/design.md`.

## Why code is needed

The rules and the skill text carry the change; the checker must read the
closing line.

## Out of scope

This change shapes verification reports and results; it does not shorten other
skills' text or add a CI job.

Features and options deliberately left out:

- A brevity rule in every skill; the closing line lives in `warrant-verify`
  only, because every completion claim passes through it.
- A machine-readable summary file.

## Assumptions

Confirmed by the requester: follow Ponytail's reply economy; take anvil's
CI-parsable result idea.

- The closing line reads `Not checked: <items or none>; Risks: <items or none>`.
  Owner: requester (decided while the requester was away).
- The result format is `Result: exit <code>, <result line>` or
  `Result: not run, <reason>`, on the verification task's own line.
  Owner: requester (decided while the requester was away).
