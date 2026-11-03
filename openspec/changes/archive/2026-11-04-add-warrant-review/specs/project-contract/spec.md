# Spec Delta

## MODIFIED Requirements

### Requirement: Contract section and headings

The project contract SHALL be the `## Warrant contract` section of the target
project's root `AGENTS.md`, with the subsections `### Verification`,
`### Destructive actions`, `### Glossary`, `### Decision records` and the
optional `### Standards`, in that order.

#### Scenario: Contract created by setup
- **WHEN** `warrant-setup` completes in a project
- **THEN** the root `AGENTS.md` contains `## Warrant contract` with the five
  subsections in that order

#### Scenario: Contract without Standards
- **WHEN** a contract has the first four subsections and no `### Standards`
- **THEN** the contract is valid

## ADDED Requirements

### Requirement: Standards entries

The Standards subsection SHALL list each file that holds coding standards as one
bullet with a relative path in backticks, or contain the word `none`.

#### Scenario: Two standards files
- **WHEN** a project keeps its rules in `docs/standards.md` and `CONTRIBUTING.md`
- **THEN** the subsection contains ``- `docs/standards.md` `` and ``- `CONTRIBUTING.md` ``

### Requirement: Missing Standards subsection

WHILE a contract has no Standards subsection, the warrant skills SHALL read the
standards as `none`.

#### Scenario: Contract from warrant v1
- **WHEN** a contract written by warrant v1 has no Standards subsection
- **THEN** `warrant-review` reports "no standards declared"
