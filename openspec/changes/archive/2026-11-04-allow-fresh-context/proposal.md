# Proposal

## Why

The kit's agent-neutral principle forbids the word "sub-agent" in skills. All
three supported agents can now start a separate, fresh context (Claude Code's
agents, Copilot CLI's fleet mode, Codex's multi-agent mode). A fresh context
is what makes a review independent of the author's reasoning (mattpocock/skills
review axes, anvil's adversarial review), and forbidding it blocks those ideas
for no remaining reason. Naming a specific agent or its tool stays forbidden.

## What Changes

- Skills may ask for a separate, fresh context (a sub-agent).
- A skill that does so must say what to do when no separate context is
  available.
- `docs/design.md` principle 6 says this; the kit test stops banning the word
  "subagent" and checks for the fallback instead.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `warrant-kit`: a rule for skills that ask for a fresh context.

## Impact

`docs/design.md`, `evals/tests/test_kit.py`.

## Why code is needed

The kit test enforces the principle; documentation alone did not prevent
drift before.

## Out of scope

This change only allows fresh contexts and requires a fallback; no skill uses
one yet, and evals do not prove that an agent started one.

Features and options deliberately left out:

- An eval that proves a sub-agent was started; headless transcripts do not show
  it reliably for all three agents.
- Naming any agent's sub-agent command.

## Assumptions

Confirmed by the requester: all three supported agents have sub-agents, and
skills may use them.

- The fallback sentence is fixed text, "If you cannot start a separate
  context", so the kit test can find it. Owner: requester (decided while the
  requester was away).
- Codex's sub-agent support is taken from community sources and a forum report,
  not from official documentation. Owner: requester.
