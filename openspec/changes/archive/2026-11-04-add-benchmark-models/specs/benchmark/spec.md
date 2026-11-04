# Spec Delta

## ADDED Requirements

### Requirement: Model selection

WHERE the user passes `--model <agent>=<model>`, the benchmark SHALL run that
agent with the named model and label its rows `<agent>:<model>`.

#### Scenario: Claude Sonnet
- **WHEN** the benchmark runs with `--model claude=sonnet`
- **THEN** the Claude command contains `--model sonnet` and the table rows read `claude:sonnet`
