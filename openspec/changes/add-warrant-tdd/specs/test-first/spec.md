# Spec Delta

## Purpose

Defines the `warrant-tdd` skill: tests first, one requirement scenario at a
time, each test seen failing before code is written and tied to the scenario it
covers.

## ADDED Requirements

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
derives from the request before it writes the first test.

#### Scenario: Direct request
- **WHEN** the user asks to add a feature and no change is active
- **THEN** the skill lists its scenarios before writing a test

### Requirement: No tests command

IF the contract lists no tests command, THEN the TDD skill SHALL tell the user to
add one with warrant-setup and change no file.

#### Scenario: Contract without tests
- **WHEN** the Verification subsection has no tests entry
- **THEN** the skill names warrant-setup and the workspace is unchanged
