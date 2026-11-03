# Design

## Context

See proposal.md - Why. Requirements are in `specs/`.

- The contract parser in `evals/warrant_evals/contract.py` requires exactly the
  four v1 subsections in order; skills read the contract as Markdown directly.
- `warrant-verify` already defines how verification commands run and how their
  evidence is reported.
- OpenSpec's `openspec-verify-change` skill checks an implementation against a
  change's artifacts, but it does not trace diff lines to requirements, does
  not require a test per requirement and reports in its own format.
- An eval workspace is one commit of its fixture; there is no base branch and no
  `origin`, so review range behavior cannot be exercised yet.

## Goals / Non-Goals

**Goals:**
- One report format with three axes that never mix.
- The skill works on all four agents without sub-agents or agent-specific tools.

**Non-Goals:**
- No new verification logic: evidence comes from `warrant-verify`.

## Decisions

### 1. One skill, two modes

`warrant-review` covers review mode and receive mode. Both use the same three
sources (the OpenSpec change, the Standards files, the contract's verification)
and receive mode ends with the same evidence step. The description names both
triggers: "review this branch" and "address these review comments".

Rejected: two skills. They would duplicate the change selection, the Standards
reading and the evidence step, and their descriptions would compete.

### 2. Spec axis done by the skill, not delegated

Option ladder: an existing tool first. `openspec-verify-change` comes closest
but does not trace lines or demand tests, and the OpenSpec skills are an
optional dependency, so a review would change shape depending on whether they
are installed. Standard tools cannot read requirements. The skill therefore
instructs the agent to: list the change's requirements with
`openspec show <change> --type change --json`; for each requirement, find the
implementing lines and the covering test in the diff or the project; for each
added line in the diff, name the requirement it serves.

### 3. Evidence axis delegated to warrant-verify

The skill says "follow warrant-verify" for running the contract's commands and
formatting evidence. No second copy of those rules.

### 4. Review range commands

- Default: `git merge-base HEAD origin/HEAD`, falling back to
  `git merge-base HEAD origin/main`; the review covers `git diff <base>` (commits
  and uncommitted tracked changes) plus `git ls-files --others --exclude-standard`.
- Named base: `git diff <base>` plus untracked files.
- If no merge-base can be found, the skill asks the user for a base instead of
  guessing.

### 5. Standards subsection is optional in the parser

`SUBSECTIONS` keeps the four required names; `Standards` becomes an optional
fifth that, when present, must come last. `Contract` gains `standards:
list[str]` (empty for `none` or missing). Backticked paths only, like
Destructive actions.

Rejected: making Standards required. Every v1 contract would become invalid.

### 6. Scenario setup script for history

Scenarios gain an optional `setup` field: a script inside the fixture that the
runner executes in the workspace after skills are installed and the fixture is
committed. The review fixture's script creates a bare `origin`, sets
`origin/HEAD`, creates a feature branch and commits the change under review
from a patch file in the fixture. Option ladder: the existing `prepare` step is
shared by all scenarios and cannot hold scenario-specific history; a script is
the least new mechanism.

### 7. Deterministic checkers

- Review: section headings Spec, Standards, Evidence appear in that order; the
  option name appears after "Spec" and before "Standards"; the function name
  appears after "Standards" and before "Evidence"; `git status --porcelain`
  equals its state after setup.
- Receive: the conflicting comment's requested change is absent from the code
  (the exit code stays 2), the valid comment's change is present, and the
  transcript contains the verification command.

## Risks / Trade-offs

- [Section-order checks pass a report that names findings in the wrong section
  by luck] → Checks look for each finding between two specific headings, not
  anywhere in the transcript.
- [Agents skip running verification in review mode to save time] → The
  Evidence section must contain the command and exit code; the review checker
  requires the contract command in the Evidence section.
- [`origin/HEAD` is unset in many clones] → Fallback to `origin/main`, then ask.

## Migration Plan

Existing contracts stay valid (Standards optional). Projects run
`npx skills add imtpot/openspec-warrant` again to get `warrant-review`;
`warrant-setup` proposes the Standards subsection only when it creates a new
contract.
