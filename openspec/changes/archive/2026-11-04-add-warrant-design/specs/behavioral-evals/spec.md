# Spec Delta

## ADDED Requirements

### Requirement: Design scenario checks

The evals SHALL include design scenarios whose checkers fail when the first
message asks more than one question or none, asks for a fact the fixture's
configuration states, misses a recommended option, does not record agreed terms
and decisions in the contract's locations, creates a file for a location the
contract declares as `none`, or creates an OpenSpec change.

#### Scenario: Two questions in one message
- **WHEN** the agent's first message contains two questions
- **THEN** the checker fails the scenario
