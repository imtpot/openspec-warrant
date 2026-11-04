# Proposal

## Why

Evals see an agent's final report only. A scenario whose prompt names no skill
passes when the agent behaves well, whether or not it loaded the skill:
`minimal-change-implicit` passed on Claude without showing that
`warrant-minimal-change` loaded. Sub-agents and their models are invisible the
same way. Claude Code can stream its tool calls, and Codex prints the commands
it runs, so evals can see both.

## What Changes

- Claude runs with `--output-format stream-json --verbose`; the runner takes
  the final text for checkers and records skill loads and sub-agent starts.
- For Codex, the runner records a skill as loaded when the output shows a read
  of `.agents/skills/<name>/SKILL.md`.
- A scenario may list `loaded` skills; a run that loads none of them fails with
  a message that names the skill.
- The eval report lists the skills each run loaded.
- `minimal-change-implicit` and `verify-no-contract` require their skill.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `behavioral-evals`: loaded skills.

## Impact

`evals/warrant_evals/runner.py`, `evals/warrant_evals/scenarios.py`,
`evals/warrant_evals/benchmark.py`, their tests, two scenario files.

## Why code is needed

The runner parses agent output in code.

## Out of scope

This change records skill loads and sub-agents; it does not grade how a skill
was followed.

Features and options deliberately left out:

- Sub-agent detection for Codex; its output format for sub-agents was not
  checked.

## Assumptions

Confirmed by the requester: show in evals whether a skill loaded and whether a
sub-agent ran.

- Reading a skill's `SKILL.md` counts as loading it. Owner: requester (decided
  while the requester was away).
