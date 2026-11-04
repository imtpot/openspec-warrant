# Spec Delta

## ADDED Requirements

### Requirement: Context checks

The setup checker SHALL read `context` as OpenSpec renders it and fail when an
expected term is missing, when it contains a contract verification command, or
when a context expected to stay unchanged differs.

#### Scenario: Drafted context
- **WHEN** the fixture README states a constraint and the context omits it
- **THEN** the checker fails and names the missing term

#### Scenario: Kept context
- **WHEN** the fixture context differs after setup
- **THEN** the checker fails and names the change
