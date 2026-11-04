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
