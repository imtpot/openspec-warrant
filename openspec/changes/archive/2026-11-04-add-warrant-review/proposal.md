# Proposal

## Why

warrant v1 makes every requirement unambiguous, every changed line warranted
and every completion claim backed by evidence, but nothing checks the result as
a whole before merge. Agents and people review diffs ad hoc: they mix "does it
do what the change asked" with "does it follow our conventions", they rarely
trace lines back to requirements, and when they receive review comments they
tend to apply them without checking them. A review skill closes the chain
request → requirement → line → evidence.

## What Changes

- Add the `warrant-review` skill with two modes:
  - **Review**: review a diff along three separate axes and report findings
    without changing files. Spec: every requirement of the active OpenSpec
    change is implemented and tested, and every changed line traces to a
    requirement. Standards: the diff follows the project's declared standards
    and the minimal-change rules. Evidence: the contract's verification
    commands pass.
  - **Receive**: address review comments by checking each one against the code
    and the specs before acting, accepting or rejecting it with a reason, and
    finishing with verification.
- Extend the project contract with an optional `### Standards` subsection that
  lists the files holding the project's coding standards, or `none`. A contract
  without the subsection reads as `none`.
- `warrant-setup` writes the Standards subsection when it creates a contract.
- Add review and receive eval scenarios.

## Capabilities

### New Capabilities
- `code-review`: the behavior of the `warrant-review` skill in review and
  receive mode.

### Modified Capabilities
- `project-contract`: the contract gains the optional Standards subsection.
- `warrant-setup`: the contract skeleton includes the Standards subsection.
- `behavioral-evals`: review and receive scenarios join the eval set.

## Impact

- New `skills/warrant-review/SKILL.md`.
- `skills/warrant-setup/SKILL.md` (contract skeleton).
- `evals/warrant_evals/contract.py` (Standards subsection), new checkers,
  fixtures and scenarios; the copy of the contract format in `README.md`.
- No change to the warrant schema.

## Why code is needed

No configuration or existing tool reviews a diff against an OpenSpec change and
a project contract; generic review tools know neither. Documentation alone
cannot make an agent separate the axes or verify comments before applying them.

## Out of scope

This change adds review and comment handling; it does not post comments to
GitHub or GitLab, block merges, or fix the findings it reports.

Features and options deliberately left out:

- Posting findings to a merge request or pull request.
- Automatic fixing of findings in review mode.
- Parallel sub-agents per axis; the skill must work on agents without them.
- Severity levels beyond "blocking" and "non-blocking".
- Reviewing changes from more than one OpenSpec change at once.

## Assumptions

Confirmed by the requester: one change per skill, starting with
`warrant-review`; project standards come from a new `### Standards` contract
subsection, and a contract without it reads as `none`; review mode defaults to
the commits since the merge-base with the default branch of `origin` plus
uncommitted changes; review mode runs the contract's verification itself;
findings are blocking or non-blocking; a comment that conflicts with the specs
is rejected with the requirement quoted.

None.
