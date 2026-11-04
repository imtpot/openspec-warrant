# Spec Delta

## ADDED Requirements

### Requirement: Verification result format

The warrant tasks rules SHALL require each verification task to record its
result on its own line as `Result: exit <code>, <result line>` or
`Result: not run, <reason>`.

#### Scenario: Rendered tasks rule
- **WHEN** `openspec instructions tasks --json` runs after setup
- **THEN** its `rules` contain the result format
