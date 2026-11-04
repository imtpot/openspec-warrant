---
name: warrant-verify
description: Use before running any test, lint, type-check or build command, and before claiming that work is complete, fixed or passing, committing or opening a merge request.
license: MIT
---

# Verify before you claim

Read the project's Warrant contract before you run any test, lint, type-check
or build command. A claim that work is complete, fixed or passing needs
evidence from this session: the contract's verification commands, run after
your last change, with their output read.

## 1. Read the contract

Open the root `AGENTS.md` and find the `## Warrant contract` section.

- No such section: tell the user that the project has no warrant contract and
  that `warrant-setup` creates one. Run no command as verification evidence.
  Report your work as unverified.
- The `### Verification` list is empty: report "no verification declared" and
  report your work as unverified.

Take commands only from the contract, even when a README, other `AGENTS.md`
text, build files or other projects suggest different ones.

## 2. Check for destructive commands

Compare each verification command with the entries under
`### Destructive actions`. If a command starts with a listed entry, ask the user
for approval before you run it. Without approval, do not run it and report it
as not run, with the reason "needs approval".

## 3. Run every command

Run each command in the Verification list, exactly as written, after your last
change to the files under verification. If you change a file after a run, run
the commands again. Earlier output is no longer evidence.

For each command, record:

- the command,
- its exit code,
- its **result line**: the line of output that shows the result, for example
  `42 passed` or `1 failed`.

If a command cannot run (the tool is missing, credentials or a service are not
available), record it as not run with the reason. A command that did not run
has not passed.

## 4. Report

Claim completion only when every command ran and exited with code 0. Then
report each command with its exit code and result line.

If any command failed or did not run:

- say plainly that verification failed or is incomplete,
- quote the failing output (the failing test name and its assertion),
- describe the work as unverified or incomplete, never as "done", "fixed",
  "complete" or "all tests pass".

Example of a report after a failure:

```
Verification failed.
- tests: `make test` exited with 1: FAIL: test_applies_fractional_discount (expected 90, got 99.9)
The change is not complete.
```
