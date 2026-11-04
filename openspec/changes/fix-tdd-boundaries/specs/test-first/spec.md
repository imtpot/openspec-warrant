# Spec Delta

## ADDED Requirements

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
