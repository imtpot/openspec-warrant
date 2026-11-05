## ADDED Requirements

### Requirement: Narrowed runs are not evidence

The TDD skill SHALL state that its narrowed red and green runs show one
scenario's behavior and are not evidence that the work is complete.

#### Scenario: All scenarios green
- **WHEN** every narrowed green run passes
- **THEN** the agent still runs the contract's verification before it reports the work as complete
