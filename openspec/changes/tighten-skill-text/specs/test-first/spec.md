# Spec Delta

## MODIFIED Requirements

### Requirement: Scenarios without a change

WHILE no OpenSpec change is active, the TDD skill SHALL state the scenarios it
derives from the request before it writes the first test and then continue
without waiting for an answer.

#### Scenario: Direct request
- **WHEN** the user asks to add a feature and no change is active
- **THEN** the skill lists its scenarios before writing a test
