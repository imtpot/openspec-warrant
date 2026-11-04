# project-contract Specification

## Purpose
Defines the warrant contract section that a target project declares in its
`AGENTS.md`, and how warrant skills read project specifics from it instead of
assuming a language, tool or layout.

## Requirements

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

### Requirement: Verification entries

The Verification subsection SHALL list each verification as one bullet with a
name and an exact shell command in backticks.

#### Scenario: Test command
- **WHEN** a project runs its tests with `uv run pytest`
- **THEN** the subsection contains a bullet such as ``- tests: `uv run pytest` ``

### Requirement: Destructive action entries

The Destructive actions subsection SHALL list commands or command prefixes that
an agent must not run without explicit user approval.

#### Scenario: Deployment command
- **WHEN** a project lists `pulumi up` as destructive
- **THEN** warrant skills ask the user before running any command that starts
  with `pulumi up`

### Requirement: Skills read only the contract

The warrant skills SHALL take verification commands, destructive actions and
document locations only from the contract.

#### Scenario: Project with a glossary
- **WHEN** the contract names `docs/glossary.md` as the glossary
- **THEN** warrant skills read terms from `docs/glossary.md` and do not look for
  `GLOSSARY.md`

### Requirement: Missing contract

IF a warrant skill runs in a project whose `AGENTS.md` has no warrant contract,
THEN the skill SHALL tell the user to run `warrant-setup`.

#### Scenario: Verify without contract
- **WHEN** `warrant-verify` runs in a project without the contract
- **THEN** it reports that the contract is missing and names `warrant-setup`

### Requirement: No guessed commands

IF a warrant skill runs in a project whose `AGENTS.md` has no warrant contract,
THEN the skill SHALL run no command that the contract would declare.

#### Scenario: Verify without contract runs nothing
- **WHEN** `warrant-verify` runs in a project without the contract
- **THEN** it runs no verification command

### Requirement: Empty verification list

IF the Verification subsection lists no command, THEN warrant skills SHALL
report that no verification is declared instead of reporting success.

#### Scenario: Contract without commands
- **WHEN** `warrant-verify` runs and the Verification subsection is empty
- **THEN** it reports "no verification declared" and does not claim completion

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
