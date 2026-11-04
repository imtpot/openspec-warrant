# Spec Delta

## ADDED Requirements

### Requirement: Arm filter

WHERE the user passes `--arm`, the benchmark SHALL run only the named arms.

#### Scenario: Warrant only
- **WHEN** the benchmark runs with `--arm warrant`
- **THEN** every run in the table is in the `warrant` arm
