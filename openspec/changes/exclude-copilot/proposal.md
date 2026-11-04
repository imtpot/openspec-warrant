# Proposal

## Why

Copilot CLI fails some scenarios in ways that the skills cannot change: it
runs commands from `AGENTS.md` prose without loading `warrant-verify`, misses a
different planted finding in each review, and skipped the separate review
contexts while a fallback allowed it. Its runs cost time and quota and blur
the results of the other agents. The requester wants it out of the evals for
now.

## What Changes

- Evals and the benchmark run Claude Code and Codex by default.
- `--agent copilot` still runs Copilot, so it can come back without code.
- The README, `docs/design.md` and the project context name Claude Code and
  Codex as evaluated agents.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `behavioral-evals`: default agents.

## Impact

`evals/warrant_evals/runner.py`, `evals/warrant_evals/__main__.py`, runner and
CLI tests, `README.md`, `docs/design.md`, `openspec/config.yaml`.

## Why code is needed

The runner's default agent list is code.

## Out of scope

This change stops running Copilot by default; it does not remove its command
or claim the skills do not work in Copilot.

Features and options deliberately left out:

- Deleting the Copilot command line from the runner.

## Assumptions

Confirmed by the requester: exclude Copilot for now.

- Keep Copilot selectable with `--agent copilot` instead of deleting it.
  Owner: requester (decided while the requester was away).
