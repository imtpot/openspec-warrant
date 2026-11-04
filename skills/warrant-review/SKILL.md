---
name: warrant-review
description: Use when asked to review a branch, a diff or a merge request before merge, or to address, answer or apply review comments.
license: MIT
---

# Review

Two modes. **Review mode** reports findings and changes no file. **Receive
mode** addresses review comments. Read the `## Warrant contract` section of the
root `AGENTS.md` first; if it is missing, tell the user to run `warrant-setup`
and stop.

## Review mode

Change no file in this mode, not even to fix an obvious problem.

### 1. Find the range

- The user named a base (a commit, tag or branch): review `git diff <base>`.
- Otherwise: base is `git merge-base HEAD origin/HEAD`; if that fails, use
  `git merge-base HEAD origin/main`; if that fails too, ask the user for a base.
- Add untracked files: `git ls-files --others --exclude-standard`.
- If the range has no changes, report "nothing to review" and stop.

### 2. Choose the OpenSpec change

Run `openspec list --json`.

- The user named a change: use it.
- Exactly one active change: use it.
- More than one and none named: ask the user which one, before the Spec axis.
- None: the Spec section reads "no OpenSpec change"; continue with Standards.

### 3. Spec axis

Get the requirements with `openspec show <change> --type change --json`.

- For each requirement, find the lines that implement it. None: blocking
  finding "not implemented".
- For each requirement, find a test that exercises it, in the diff or in the
  project. None: blocking finding "untested".
- For each added line in the diff, name the requirement it serves. None:
  blocking finding "untraced", with file and line. Imports, test code and
  formatting count for the requirement they support.

### 4. Standards axis

Read each file listed under `### Standards`. If the subsection is missing or
reads `none`, write "no standards declared" and check only the minimal-change
rules below.

- A diff part that breaks a rule in a Standards file: blocking. Quote the rule
  and name its file.
- Removed validation at trust boundaries, removed error handling that prevents
  data loss, removed security checks: blocking.
- Speculative generality, an option or parameter nothing uses, a new dependency
  with no stated reason: non-blocking.

### 5. Evidence axis

Run the contract's verification commands following the `warrant-verify` skill.
Report each command with its exit code and result line. A failed command or one
that could not run: blocking.

### 6. Report

Write three sections in this order and never move a finding between them:

```
## Spec
## Standards
## Evidence
```

Each finding: level (blocking or non-blocking), `file:line` where one exists,
and the quoted code, requirement or rule. End with one line per axis: number of
blocking and non-blocking findings. Do not rank the axes against each other.

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

Do not agree with a comment only because a reviewer wrote it, and do not reject
one only because it means more work. The code and the specs decide.
