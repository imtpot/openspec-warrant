# test-first Specification

## Purpose
Defines the `warrant-tdd` skill: tests first, one requirement scenario at a
time, each test seen failing before code is written and tied to the scenario it
covers.

## Requirements

### Requirement: A test per scenario

WHILE the TDD skill implements a requirement of an OpenSpec change, the TDD
skill SHALL write at least one test for each scenario of that requirement.

#### Scenario: Requirement with two scenarios
- **WHEN** a requirement has the scenarios "Enough free" and "Not enough free"
- **THEN** the diff adds at least one test for each of them

### Requirement: Test names its scenario

The TDD skill SHALL name the requirement and the scenario a test covers in the
test's name or in a one-line comment above it.

#### Scenario: Comment above the test
- **WHEN** a test covers scenario "Not enough free" of requirement "Shortfall verdict"
- **THEN** the test's name or the comment above it contains both names

### Requirement: Red before code

WHEN the TDD skill has written a test, the TDD skill SHALL run it and see it
fail before writing any code that the test exercises.

#### Scenario: Missing behavior
- **WHEN** the function under test does not handle the shortfall yet
- **THEN** the skill runs the new test, sees it fail, and only then edits the function

### Requirement: Fail for the expected reason

IF a new test fails for a reason other than the missing behavior, such as an
import or syntax error, THEN the TDD skill SHALL fix the test until it fails for
the missing behavior.

#### Scenario: Import error
- **WHEN** the new test fails because of a misspelled import
- **THEN** the skill fixes the import and runs the test again before writing code

### Requirement: Behavior already present

IF a new test passes before any code is written for it, THEN the TDD skill SHALL
report that the behavior already exists and write no code for that scenario.

#### Scenario: Existing check
- **WHEN** a test for negative input passes against the unchanged code
- **THEN** the report says the behavior already exists and the code stays unchanged

### Requirement: Green with the least code

WHEN a test fails for the missing behavior, the TDD skill SHALL write the least
code that makes it pass, following warrant-minimal-change, and run it again.

#### Scenario: Shortfall implemented
- **WHEN** the shortfall test fails
- **THEN** the skill adds only the shortfall branch and runs the test again

### Requirement: One scenario at a time

The TDD skill SHALL finish red and green for one scenario before it writes the
test for the next scenario.

#### Scenario: Two scenarios
- **WHEN** two scenarios are to be implemented
- **THEN** the second test is written after the first test passes

### Requirement: Narrowed test command

The TDD skill SHALL run a single test with the contract's tests command narrowed
to that test by the tool's own selection.

#### Scenario: unittest selection
- **WHEN** the contract's tests command is `python3 -m unittest discover -s tests -t .`
- **THEN** a single run looks like `python3 -m unittest tests.test_quota.QuotaTest.test_shortfall`

### Requirement: Red and green evidence

WHEN the TDD skill reports its work, the TDD skill SHALL show for each scenario
the failing result of the red run and the passing result of the green run.

#### Scenario: Report
- **WHEN** two scenarios were implemented
- **THEN** the report shows, per scenario, a failing line and then a passing line

### Requirement: Full verification at the end

WHEN all scenarios pass, the TDD skill SHALL run the contract's verification
following warrant-verify.

#### Scenario: Last step
- **WHEN** the last scenario passes
- **THEN** the report shows the contract's full tests command with its exit code

### Requirement: Scenarios without a change

WHILE no OpenSpec change is active, the TDD skill SHALL state the scenarios it
derives from the request before it writes the first test and then continue
without waiting for an answer.

#### Scenario: Direct request
- **WHEN** the user asks to add a feature and no change is active
- **THEN** the skill lists its scenarios before writing a test

### Requirement: No tests command

IF the contract lists no tests command, THEN the TDD skill SHALL tell the user to
add one with warrant-setup and change no file.

#### Scenario: Contract without tests
- **WHEN** the Verification subsection has no tests entry
- **THEN** the skill names warrant-setup and the workspace is unchanged

### Requirement: No task management

The TDD skill SHALL neither select tasks from `tasks.md` nor mark them complete;
the OpenSpec apply workflow does both.

#### Scenario: Implementing inside apply
- **WHEN** the apply workflow hands the TDD skill a requirement to implement
- **THEN** `tasks.md` is unchanged when the TDD skill finishes

### Requirement: Boundary cases from the requirement text

WHILE the TDD skill implements a requirement of an OpenSpec change, the TDD
skill SHALL write a test for each boundary or condition that the requirement's
text states and none of its scenarios shows.

#### Scenario: Exact half not shown
- **WHEN** a requirement says an exact half cent is rounded up and its only scenario rounds two thirds
- **THEN** the diff adds a test with an exact half cent

#### Scenario: Equality inside "not after"
- **WHEN** a requirement says to raise an error if the end is not after the start and its scenario swaps the dates
- **THEN** the diff adds a test where the end equals the start

### Requirement: Boundary cases in the report

WHEN the TDD skill reports, the TDD skill SHALL list the boundary cases it
tested after the spec's scenarios.

#### Scenario: Report with a boundary case
- **WHEN** the skill tested an exact half cent besides the spec's scenarios
- **THEN** the report lists the exact half cent as a boundary case

### Requirement: Independent expected values

The TDD skill SHALL take each expected value from the spec or from a worked
example computed by hand, never from the code under test or its helpers.

#### Scenario: Sum of line items
- **WHEN** a test checks the total of items priced 10 and 5
- **THEN** the test expects the literal 15, not a sum computed in the test

### Requirement: Mocks only at external boundaries

The TDD skill SHALL replace only external systems, time and randomness with
test doubles, and run the project's own modules for real.

#### Scenario: Module calls a helper of the same project
- **WHEN** the code under test calls `days_between` from the same project
- **THEN** the test runs the real `days_between`

### Requirement: Mutation check

WHEN the TDD skill has finished every scenario and boundary case, the TDD
skill SHALL check each realistic mutation of the changed code against the
tests and add a test, red then green, for each mutation that no test fails on.

#### Scenario: Rounding mutation not caught
- **WHEN** replacing round-half-up with round-half-even fails no test
- **THEN** the skill adds a test that fails on that mutation and passes on the code
