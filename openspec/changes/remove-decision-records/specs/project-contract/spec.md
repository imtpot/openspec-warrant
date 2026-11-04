# Spec Delta

## MODIFIED Requirements

### Requirement: Contract section and headings

The project contract SHALL be the `## Warrant contract` section of the target
project's root `AGENTS.md`, with the subsections `### Verification`,
`### Destructive actions`, `### Glossary` and the optional `### Standards`, in
that order.

#### Scenario: Contract created by setup
- **WHEN** `warrant-setup` completes in a project
- **THEN** the root `AGENTS.md` contains `## Warrant contract` with the four
  subsections in that order

#### Scenario: Contract without Standards
- **WHEN** a contract has the first three subsections and no `### Standards`
- **THEN** the contract is valid

## REMOVED Requirements

### Requirement: Location entries

**Reason**: The Decision records subsection is removed; the Glossary entry
moves to its own requirement.
**Migration**: See "Glossary entry".

## ADDED Requirements

### Requirement: Glossary entry

The Glossary subsection SHALL contain one relative path or the word `none`.

#### Scenario: No glossary
- **WHEN** a project keeps no glossary
- **THEN** the Glossary subsection contains `none`

### Requirement: Former Decision records subsection

IF a contract contains a `### Decision records` subsection, THEN the warrant
skills SHALL ignore that subsection.

#### Scenario: Contract written by an earlier setup
- **WHEN** a contract has `### Decision records` between Glossary and Standards
- **THEN** the contract is valid and its Standards entries are read
