---
name: warrant-review
description: Use when asked to review a branch, a diff or a merge request before merge, to review a change's planning artifacts before implementation, or to address, answer or apply review comments.
license: MIT
---

# Review

Three modes. **Review mode** reports findings on a diff. **Artifact mode**
reviews a change's planning artifacts before code. **Receive mode** addresses
review comments. Read the `## Warrant contract` section of the root `AGENTS.md`
first. If it is missing, tell the user to run `warrant-setup` and stop.

## Review mode

Change no file in this mode, not even to fix an obvious problem.

### 1. Find the range

- The user named a base (a commit, tag or branch): review `git diff <base>`.
- Otherwise, take the first base that works:
  1. `git merge-base HEAD origin/HEAD`
  2. `git merge-base HEAD origin/main`
  3. a base you ask the user for
- Add untracked files: `git ls-files --others --exclude-standard`.
- If the range has no changes, write the line `nothing to review` and stop.

### 2. Choose the OpenSpec change

Run `openspec list --json`.

- The user named a change: use it.
- Exactly one active change: use it.
- More than one and none named: ask the user which one, before the Spec axis.
- None: the Spec section reads "no OpenSpec change"; continue with Standards.

Run steps 3 and 4 each in a separate, fresh context (a sub-agent), so that one
axis does not shape the other. Give each context the range, the change and
only its own step.

### 3. Spec axis

Run the `openspec-verify-change` workflow for the change and report its
findings here with their own severities (CRITICAL, WARNING, SUGGESTION). If
that skill is not installed, write "Spec axis not run" and give the command
`npx skills add https://github.com/Fission-AI/OpenSpec/tree/v<installed version>/skills`.

Then add what that workflow does not check: trace each added line of the diff
as `warrant-minimal-change` describes under "Trace lines to requirements". A
line that serves no requirement is a blocking finding "untraced", with file and
line.

### 4. Standards axis

Read each file listed under `### Standards`. If the subsection is missing or
reads `none`, write "no standards declared" and check only the rules below.

- A diff part that breaks a rule in a Standards file: blocking. Quote the rule
  and name its file.
- Read the code connected to the diff, not only the diff: every caller of a
  changed or added function and every function the diff calls. A bug there
  (wrong arguments, wrong order, an unhandled error, a broken contract) or a
  security problem (injection, exposed secrets, missing authorization):
  blocking, with file and line.
- Removed code from the "Protected code" list of `warrant-minimal-change`:
  blocking.
- Speculative generality, an option or parameter nothing uses, a new dependency
  with no stated reason: non-blocking.

### 5. Evidence axis

Run the contract's verification commands following the `warrant-verify` skill.
Report each command with its exit code and result line. A failed command or one
that could not run: blocking.

### 6. Report

Write three sections in this order. Put each finding under the axis that found
it:

```
## Spec
## Standards
## Evidence
```

Each finding: level (blocking or non-blocking, or verify-change's severity on
the Spec axis), `file:line` where one exists,
and the quoted code, requirement or rule. End with one line per axis: number of
blocking and non-blocking findings. Do not rank the axes against each other.

## Artifact mode

Use this mode for a change's `proposal.md`, `specs/`, `design.md` and
`tasks.md` before its first task is implemented. Change no file.

Review in a separate, fresh context (a sub-agent) that gets the artifact
files, the contract and the `design.md` files of archived changes
(`openspec/changes/archive/`), not the conversation that wrote the artifacts.

Report as blocking:

- a requirement with more than one `SHALL`, or one not written in an EARS
  pattern (the `[warrant]` rules for specs in `openspec/config.yaml` list the
  patterns),
- a requirement for which `tasks.md` has no test task,
- a task list without a verification group,
- a design decision that contradicts a decision in the `design.md` of an
  archived change, with both decisions quoted,
- a decision the specs or design present as settled that the proposal lists
  neither as confirmed nor under Assumptions.

End the report with exactly one of these lines, as its last line:

```
Artifact review: REVISE
Artifact review: PASS
```

`REVISE` when any blocking finding exists, `PASS` otherwise.

## Receive mode

Use this mode when the user gives you review comments to address.

1. **Classify every comment before you edit anything.** For each comment, read
   the code it refers to and the requirements of the OpenSpec change, then mark
   it accepted or rejected with a reason:
   - It asks for behavior that conflicts with a requirement: reject it and quote
     the requirement.
   - It states something about the code that the code contradicts: reject it
     and quote the code that contradicts it.
   - It does not say what to change: ask the user, and leave that code alone.
   - Otherwise: accept it.
2. List the classifications to the user.
3. Apply the accepted comments, following `warrant-minimal-change`.
4. Run the contract's verification following `warrant-verify` before you report
   the comments as addressed. If verification fails, report that instead.

Decide each comment by the code and the specs alone: who wrote it and how much
work it causes do not count.
