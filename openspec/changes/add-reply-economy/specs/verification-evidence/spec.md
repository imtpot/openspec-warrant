# Spec Delta

## ADDED Requirements

### Requirement: One line per command

WHEN the agent reports verification, the verify skill SHALL direct the agent to
give one line per verification command with the command, its exit code and its
result line.

#### Scenario: Two commands
- **WHEN** the contract lists tests and lint
- **THEN** the verification part of the report has two lines, one per command

### Requirement: Closing line

WHEN the agent reports verification, the verify skill SHALL direct the agent to
end the report with the line `Not checked: <items or none>; Risks: <items or none>`.

#### Scenario: Nothing skipped
- **WHEN** every command ran and passed and no risk is known
- **THEN** the report ends with `Not checked: none; Risks: none`
