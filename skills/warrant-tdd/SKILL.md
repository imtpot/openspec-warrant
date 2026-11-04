---
name: warrant-tdd
description: Use when implementing a requirement, an OpenSpec task or a bug fix with tests; not for choosing or checking off tasks.
license: MIT
---

# Test first

A test written before the code shows what the requirement asks; a test written
after it shows what the code happens to do. Work one scenario at a time, red
then green.

Read the `## Warrant contract` section of the root `AGENTS.md`. Find the tests
command under `### Verification`. If there is none, tell the user to add it with
`warrant-setup`, and stop without changing any file.

This skill works on the requirement it is given. Do not pick tasks from
`tasks.md` and do not check them off; the OpenSpec apply workflow does that.

## 1. List the scenarios

- Inside an OpenSpec change: take the scenarios of the requirement you were
  given from its spec.
- Without a change: derive the scenarios from the request and list them to the
  user before you write the first test.

## 2. For each scenario, in order

### Red

1. Write one test for this scenario only, through the interface the
   requirement describes. Put a one-line comment above it:
   `<Requirement>: <Scenario>` (in the test language's comment syntax), or name
   the test after the scenario.
2. Run only this test. Narrow the contract's tests command with the tool's own
   selection (a file path, a test id, `-k`, `--grep`, `-run`). Example: the
   contract says `python3 -m unittest discover -s tests -t .`; run
   `python3 -m unittest tests.test_quota.QuotaTest.test_not_enough_free`.
3. Read the result:
   - It fails because the behavior is missing: go to Green.
   - It fails for another reason (import, syntax, wrong fixture): fix the test
     and run it again. Do not write production code to fix a broken test.
   - It passes: the behavior already exists. Keep the test, write no code for
     this scenario, and say so in the report.

### Green

4. Write the least code that makes this test pass, following
   `warrant-minimal-change`.
5. Run the same narrowed command. If it still fails, fix the code, not the test,
   unless the test contradicts the requirement.
6. Only then write the test for the next scenario.

## 3. Finish

Run the contract's verification following `warrant-verify`.

## Report

Start with the list of scenarios: the spec's, or the ones you derived from the
request. Then, for each scenario: the narrowed command, the failing result line of the red run
and the passing result line of the green run, or "already exists" with the
passing line. Then the verification commands with their exit codes.

```
Scenarios: Not enough free; Negative request
Not enough free: `python3 -m unittest tests.test_quota.QuotaTest.test_not_enough_free`
  red: FAIL - AssertionError: None != 'short'
  green: OK
Negative request: already exists - the new test passed before any change (OK)
Verification: `python3 -m unittest discover -s tests -t .` exited 0 (OK)
```
