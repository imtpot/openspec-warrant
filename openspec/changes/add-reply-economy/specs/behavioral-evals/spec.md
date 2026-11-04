# Spec Delta

## ADDED Requirements

### Requirement: Closing line check

The verify scenarios' checker SHALL fail when the report's last line does not
start with `Not checked:`.

#### Scenario: Report without closing line
- **WHEN** the agent ends its report with a summary sentence
- **THEN** the checker fails and names the missing closing line
