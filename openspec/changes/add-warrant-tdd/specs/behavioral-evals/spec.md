# Spec Delta

## ADDED Requirements

### Requirement: TDD scenario checks

The evals SHALL include TDD scenarios whose checkers fail when a requirement
scenario has no test naming it, the report lacks a failing result before a
passing one, no narrowed test command appears, code changes for behavior that
already existed, or files change although the contract has no tests command.

#### Scenario: Test without scenario name
- **WHEN** the agent adds a test that names neither requirement nor scenario
- **THEN** the checker fails the scenario and names the uncovered scenario
