## Why

Two skill texts conflict with each other.

- `warrant-verify` triggers before any test command and says to run each
  contract command "exactly as written". `warrant-tdd` tells the agent to run a
  single test with a narrowed command for each red and green step. An agent
  that follows both either runs the full suite at every step or treats a
  narrowed run as a breach. Neither skill says that a narrowed run is allowed
  but proves nothing about completion.
- `warrant-minimal-change` lists Protected code (validation at trust
  boundaries, error handling that prevents data loss, security checks,
  accessibility) that must stay even when the change would be smaller without
  it. Its "Trace lines to requirements" section then tells the agent to stop
  at any line that no requirement covers, and `warrant-review` reports such a
  line as a blocking "untraced" finding. A required input check that no spec
  names is therefore both mandatory and blocking. The same holds for a line
  that a rule in a declared Standards file requires.

## Why code is needed

The behavior lives in skill text under `skills/`; only an edit of that text
changes it. The review eval cannot tell a protected line from an untraced one
today, so the review checker and the review fixture need code too.

## What Changes

- `warrant-verify` says that a narrowed or diagnostic run (one test, one file,
  extra flags) is allowed while the agent works, and that only the contract
  commands, run exactly as written after the last change, are evidence.
- `warrant-tdd` says that its narrowed red and green runs are not evidence of
  completion; its final step stays the full verification.
- `warrant-minimal-change` lets an added line trace to one of three bases: a
  requirement of the change, an item of the Protected code list, or a rule in a
  file under `### Standards` of the contract. The agent names the basis. A line
  with none of the three is removed, or the agent stops and reports the missing
  requirement, as before.
- `warrant-review` reports a line as untraced only when it has none of the
  three bases. Its Spec-axis context also gets the Protected code list and the
  Standards files, so it can check a `protected:` or `standard:` basis.
- A new review eval scenario, `review-protected`, adds an input check that no
  requirement names to the review fixture; its checker fails when the Spec
  section reports that check as untraced.

## Out of scope

This change resolves the two conflicts only; it does not change when the skills
trigger or what counts as evidence for a completion claim.

- The descriptions (trigger text) of `warrant-verify` and `warrant-tdd`.
- Reusing an earlier full verification result instead of running it again.
- The orchestrator's verification after each sub-agent in the apply guidance.
- Narrowing the proposal's Assumptions rule.
- Recording real command runs in the eval harness.
- Running the agent eval scenarios of the four skills on Codex, which AGENTS.md
  asks for after a wording change. The requester runs them on Claude only in
  this change; Codex is deferred.

## Assumptions

- "Anything the requester asked for", the last Protected code item, is not a
  separate basis: a request that a line serves is already a requirement or
  belongs in the specs. Owner: requester.
- The agent names the basis per line in its trace as `requirement: <name>`,
  `protected: <item>` or `standard: <file>`. Owner: requester.
- A line traced to Protected code or a standard is not reported to the
  requester as a missing requirement. Owner: requester.
- The minimal-change section "Trace lines to requirements" is renamed "Trace
  every line", and `warrant-review` cites the new name. Owner: requester.
- "Only the specs define what is required" in `warrant-minimal-change` becomes:
  the specs define the required behavior; Protected code and declared standards
  add what every change keeps. Owner: requester.
- The new scenario reuses the `review-branch` fixture with a new setup
  variant, and the review checker gets a way to fail when a term appears on an
  untraced finding. Owner: requester.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `verification-evidence`: narrowed runs during development are allowed and are
  not evidence.
- `test-first`: narrowed red and green runs are not evidence of completion.
- `minimal-change`: a line traces to a requirement, a Protected code item or a
  declared standard.
- `code-review`: an untraced line has none of the three bases.
- `behavioral-evals`: a review scenario with a protected line that no
  requirement names.

## Impact

- `skills/warrant-verify/SKILL.md`, `skills/warrant-tdd/SKILL.md`,
  `skills/warrant-minimal-change/SKILL.md`, `skills/warrant-review/SKILL.md`.
- `evals/warrant_evals/checks.py` (review checker),
  `evals/fixtures/review-branch/` (new setup variant),
  `evals/scenarios/review-protected.toml`, tests in `evals/tests/`.
- The eval scenarios of the four skills run on Claude only.
