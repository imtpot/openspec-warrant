# Proposal

## Why

Copilot CLI fails some scenarios in ways that the skills cannot change: it
runs commands from `AGENTS.md` prose without loading `warrant-verify`, misses a
different planted finding in each review, and skipped the separate review
contexts while a fallback allowed it. Its runs cost time and quota and blur the
results. The requester wants warrant to work perfectly on Claude Code and
Codex first, with everything else removed for now.

## What Changes

- The eval runner supports Claude Code and Codex only; the Copilot command and
  its allowlist are removed.
- The README, `docs/design.md` and the project context name Claude Code and
  Codex as the supported agents.
- **Compatibility**: skills stay agent-neutral, so they still load in other
  agents; only the evidence for those agents is gone.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `behavioral-evals`: two supported agents.

## Impact

`evals/warrant_evals/runner.py`, runner tests, `README.md`, `docs/design.md`,
`openspec/config.yaml`.

## Why code is needed

The runner's agent list is code.

## Out of scope

This change removes Copilot from the evals; it does not change any skill.

Features and options deliberately left out:

- A switch to run Copilot on request; it returns through its own change.

## Assumptions

Confirmed by the requester: make warrant perfect on Claude Code and Codex and
remove everything else for now. No other decision is open.
