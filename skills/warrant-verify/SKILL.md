---
name: warrant-verify
description: Use before running any test, lint, type-check or build command, and before claiming that work is complete, fixed or passing, committing or opening a merge request.
license: MIT
---

# Verify before you claim

Which commands verify this project is decided by its Warrant contract, not by
commands you find in a README, in other `AGENTS.md` text or in build files. Read
the contract before you run any test, lint, type-check or build command.

A claim that work is complete, fixed or passing needs evidence from this
session: the project's verification commands, run after your last change, with
their output read. Without that evidence, report what you did and what is
unverified, not success.

## 1. Read the contract

Open the root `AGENTS.md` and find the `## Warrant contract` section.

- No such section: tell the user that the project has no warrant contract and
  that `warrant-setup` creates one. Do not guess the project's commands and do
  not run any verification command. Report your work as unverified.
- The `### Verification` list is empty: report "no verification declared" and
  report your work as unverified. Do not claim completion.

Take commands only from the contract. Do not replace them with commands you
know from other projects.

## 2. Check for destructive commands

Compare each verification command with the entries under
`### Destructive actions`. If a command starts with a listed entry, ask the user
for approval before you run it. Without approval, do not run it and report it
as not run, with the reason "needs approval".

## 3. Run every command

Run each command in the Verification list, exactly as written, after your last
change to the files under verification. If you change a file after a run, run
the commands again; earlier output is no longer evidence.

For each command, record:

- the command,
- its exit code,
- the line of output that shows the result, for example `42 passed` or
  `1 failed`.

If a command cannot run (the tool is missing, credentials or a service are not
available), record it as not run with the reason. A command that did not run
has not passed.

## 4. Report

Claim completion only when every command ran and exited with code 0. Then
report each command with its exit code and result line.

If any command failed or did not run:

- say plainly that verification failed or is incomplete,
- quote the failing output (the failing test name and its assertion),
- do not use words such as "done", "fixed", "complete" or "all tests pass"
  about the work.

Example of a report after a failure:

```
Verification failed.
- tests: `make test` exited with 1: FAIL: test_applies_fractional_discount (expected 90, got 99.9)
The change is not complete.
```
