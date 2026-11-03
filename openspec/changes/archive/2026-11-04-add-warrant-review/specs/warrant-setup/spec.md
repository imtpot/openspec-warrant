# Spec Delta

## MODIFIED Requirements

### Requirement: Create the contract skeleton

WHEN the root `AGENTS.md` has no warrant contract, the setup skill SHALL append
the contract section with all five subsections.

#### Scenario: AGENTS.md without contract
- **WHEN** `AGENTS.md` exists without `## Warrant contract`
- **THEN** setup appends the section and leaves the existing content unchanged

#### Scenario: Standards found
- **WHEN** the project has a `CONTRIBUTING.md` with coding rules
- **THEN** setup proposes it under `### Standards` and writes it after the user confirms
