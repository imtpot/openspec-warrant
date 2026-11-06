---
name: warrant-tdd
description: Use when implementing a requirement, an OpenSpec task or a bug fix with tests; not for choosing or checking off tasks.
license: MIT
---

# Test first

A test written before the code shows what the requirement asks. A test written
after it shows what the code happens to do. Work one scenario at a time, red
then green.

Read the `## Warrant contract` section of the root `AGENTS.md`. Find the command
under `### Verification` that runs the tests. If there is none, tell the user to
add it with `warrant-setup`, and stop without changing any file.

Implement only the requirement you were given. The OpenSpec apply workflow
picks the tasks in `tasks.md` and checks them off.

## 1. List the scenarios

- Inside an OpenSpec change: take the scenarios of the requirement you were
  given from its spec. Then read the requirement's text and add one boundary
  case for each condition it states that no scenario shows: each side of a
  comparison ("before", "after", "not after", "at least"), an exact rounding
  point, an empty or zero input, and the case just outside a stated condition.
  Example: "an exact half cent is rounded up" with only a two-thirds scenario
  needs a case with exactly half a cent. "Not after" needs the equal case.
  Treat each boundary case as a scenario in step 2.
- Without a change: derive the scenarios from the request, list them to the
  user before you write the first test, and continue without waiting for an
  answer.

## 2. For each scenario, in order

### Red

1. Write one test for this scenario only:
   - First name one wrong implementation that this test will catch.
   - Test through the interface the requirement describes.
   - Put a one-line comment above the test, `<Requirement>: <Scenario>` in the
     test language's comment syntax, or name the test after the scenario.
   - Take the expected value from the spec or work it out by hand, never from
     the code under test or its helpers.
   - Replace only external systems, time and randomness with test doubles. Run
     the project's own modules for real.
2. Run only this test. Narrow the contract's tests command with the tool's own
   selection (a file path, a test id, `-k`, `--grep`, `-run`). Example: the
   contract says `python3 -m unittest discover -s tests -t .`, so run
   `python3 -m unittest tests.test_quota.QuotaTest.test_not_enough_free`.
   This run shows this scenario only and is not evidence that the work is
   complete. Check the narrowed command against Destructive actions as
   `warrant-verify` step 2 says.
3. Read the result:
   - It fails because the behavior, or the function, module or attribute under
     test, does not exist yet: go to Green.
   - It fails because of an error in the test (import, syntax, wrong fixture):
     fix the test and run it again. Production code changes only in Green.
   - It passes: the behavior already exists. Keep the test, write no code for
     this scenario, and say so in the report.

### Green

4. Write the least code that makes this test pass, following
   `warrant-minimal-change`.
5. Run the same narrowed command. If it still fails, fix the code, not the test,
   unless the test contradicts the requirement.
6. Only then write the test for the next scenario.

## 3. Finish

List the realistic mutations of the code you changed: a wrong constant or
comparison (`<` for `<=`), the other branch, a missing check for zero, empty or
invalid input, a missing side effect, an empty or default return. For each
mutation, apply it, run the tests, and revert it. If no test fails on the
mutation, write one, run it on the mutated code (red), revert, and run it again
(green). Leave no mutation in the code.

Then run the contract's verification following `warrant-verify`.

## Report

Start with the list of scenarios: the spec's, or the ones you derived from the
request. Then list the boundary cases. Then, for each scenario and boundary
case: the narrowed command, the failing result line of the red run and the
passing result line of the green run, or "already exists" with the passing
line. Then the verification commands with their exit codes.

```
Scenarios: Not enough free; Negative request
Boundary cases: free equals needed
Not enough free: `python3 -m unittest tests.test_quota.QuotaTest.test_not_enough_free`
  red: FAIL - AssertionError: None != 'short'
  green: OK
Negative request: already exists - the new test passed before any change (OK)
Verification: `python3 -m unittest discover -s tests -t .` exited 0 (OK)
```
