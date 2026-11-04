# Spec Delta

## Purpose

Defines the artifact rules and operation guidance that warrant adds to a
project's `openspec/config.yaml`, on top of OpenSpec's own `spec-driven` schema.

## ADDED Requirements

### Requirement: Marked entries

The warrant rules and guidance SHALL start each of their entries with `[warrant] `.

#### Scenario: Project config after setup
- **WHEN** setup has written the rules
- **THEN** every entry that warrant added starts with `[warrant] `

### Requirement: Assumptions in the proposal

The warrant proposal rules SHALL require an Assumptions section that lists each
decision the requester has not confirmed, with an owner.

#### Scenario: Rendered proposal instructions
- **WHEN** `openspec instructions proposal --json` runs in a project after setup
- **THEN** its `rules` contain the Assumptions rule

### Requirement: Why code is needed

The warrant proposal rules SHALL require a statement of why configuration, an
existing tool or a documentation change cannot meet the need.

#### Scenario: Rendered proposal rule
- **WHEN** `openspec instructions proposal --json` runs after setup
- **THEN** its `rules` contain the "why code is needed" rule

### Requirement: EARS requirements

The warrant specs rules SHALL require one EARS pattern and one `SHALL` per
requirement, WHERE only for options, and a trace to the request or an assumption.

#### Scenario: Rendered specs rules
- **WHEN** `openspec instructions specs --json` runs after setup
- **THEN** its `rules` contain the EARS, one-outcome, WHERE and trace rules

### Requirement: Option ladder in the design

The warrant design rules SHALL require recording the first option that fully
works, in the order existing code or tool, standard library, installed
dependency, new code, with the reason each earlier option failed.

#### Scenario: Rendered design rule
- **WHEN** `openspec instructions design --json` runs after setup
- **THEN** its `rules` contain the option-ladder rule

### Requirement: Review and verification tasks

The warrant tasks rules SHALL require a review group followed by a verification
group with one task per contract verification command, and a checks-not-run
record.

#### Scenario: Rendered tasks rules
- **WHEN** `openspec instructions tasks --json` runs after setup
- **THEN** its `rules` contain the review, verification and not-run rules

### Requirement: Glossary terms

The warrant proposal and specs rules SHALL require using the terms of the
glossary named in the contract and adding a new term to it once the requester
confirms its meaning.

#### Scenario: Rendered glossary rule
- **WHEN** `openspec instructions specs --json` runs after setup
- **THEN** its `rules` contain the glossary rule

### Requirement: Apply guidance

The warrant apply guidance SHALL direct the agent to follow `warrant-tdd`,
`warrant-minimal-change` and `warrant-verify`.

#### Scenario: Rendered apply guidance
- **WHEN** `openspec instructions apply --json` runs for a change after setup
- **THEN** its `operationGuidance` names the three skills
