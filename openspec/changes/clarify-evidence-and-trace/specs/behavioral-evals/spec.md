## ADDED Requirements

### Requirement: Protected line review scenario

The evals SHALL include a review scenario whose fixture diff adds an input check
that no requirement names, and whose checker fails when a Spec finding marks
that check as untraced.

#### Scenario: Protected check reported as untraced
- **WHEN** a line of the Spec section contains "untraced" and names the input check
- **THEN** the checker fails the scenario and names the check
