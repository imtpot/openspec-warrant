# Spec Delta

## MODIFIED Requirements

### Requirement: Protected code

The minimal-change skill SHALL direct the agent never to leave out or remove
validation at trust boundaries, error handling that prevents data loss,
security checks or accessibility of user interfaces to make a change smaller.

#### Scenario: Shorter without validation
- **WHEN** removing an input check would shorten the diff
- **THEN** the input check stays

#### Scenario: New function reads user input
- **WHEN** a new function parses input from a user
- **THEN** the function validates that input even though the least code would not
