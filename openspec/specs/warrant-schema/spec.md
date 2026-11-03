# warrant-schema Specification

## Purpose
Defines the `warrant` OpenSpec schema: the artifacts a change produces and the
template and instruction constraints that make requirements unambiguous,
assumptions explicit and completion verifiable.

## Requirements

### Requirement: Same artifact graph as spec-driven

The warrant schema SHALL define the artifacts proposal, specs, design and tasks
with the same dependency edges as the `spec-driven` schema of OpenSpec 1.16.

#### Scenario: Status of a new change
- **WHEN** a change is created with the warrant schema
- **THEN** `openspec status --change <name> --json` lists proposal, specs,
  design and tasks
- **AND** tasks requires specs and design, and specs and design require proposal

### Requirement: Schema validates

The warrant schema SHALL pass `openspec schema validate warrant` with OpenSpec 1.16.

#### Scenario: Validation in a target project
- **WHEN** the schema is installed in `openspec/schemas/warrant/` of a project
- **THEN** `openspec schema validate warrant` exits with code 0

### Requirement: Proposal records assumptions

The proposal template SHALL contain an Assumptions section for decisions that
the requester has not confirmed, each with an owner.

#### Scenario: Unconfirmed decision
- **WHEN** an agent writes a proposal and decides a detail the requester did not
  confirm
- **THEN** the proposal lists that decision under Assumptions with an owner

### Requirement: Proposal states why simpler options fail

The proposal instruction SHALL require a statement of why configuration, an
existing tool or a documentation change cannot meet the need.

#### Scenario: Request solvable by configuration
- **WHEN** an agent writes a proposal
- **THEN** the proposal contains a statement on configuration, existing tools
  and documentation as alternatives

### Requirement: Requirements use one EARS pattern

The specs instruction SHALL require every requirement to use exactly one EARS
pattern (ubiquitous, WHEN, WHILE, IF/THEN or WHERE), with at most two clauses
in the order WHERE, WHILE, WHEN/IF.

#### Scenario: Event requirement
- **WHEN** an agent writes a requirement for behavior caused by a trigger
- **THEN** the requirement text starts with `WHEN <trigger>,` and contains one
  `SHALL`

### Requirement: One outcome per requirement

The specs instruction SHALL require exactly one observable response per
requirement.

#### Scenario: Several exit codes
- **WHEN** a behavior has three distinct outcomes
- **THEN** the specs contain three requirements, one per outcome

### Requirement: WHERE only for options

The specs instruction SHALL restrict the WHERE pattern to optional features or
options and require WHILE for a state of the environment.

#### Scenario: Unlimited quota
- **WHEN** a requirement depends on a state of an external system
- **THEN** the requirement uses WHILE, not WHERE

### Requirement: Requirements trace to the request

The specs instruction SHALL require every requirement to trace to the request
or to a listed assumption.

#### Scenario: Unrequested output field
- **WHEN** an agent adds behavior that neither the request nor an assumption names
- **THEN** the agent removes the requirement or adds the assumption to the proposal

### Requirement: Design records the option ladder

The design instruction SHALL require recording the first option that fully
works, checked in this order: existing tool or project code, standard library,
installed dependency, new code, with the reason each earlier option failed.

#### Scenario: New dependency proposed
- **WHEN** a design adds a dependency
- **THEN** the design states why existing code, the standard library and
  installed dependencies cannot meet the need

### Requirement: Tasks end with review and verification

The tasks template SHALL end with a review group followed by a verification
group that runs the verification commands of the project contract.

#### Scenario: Generated task list
- **WHEN** an agent writes tasks for a change
- **THEN** the second-to-last group reviews the diff against the specs
- **AND** the last group runs each contract verification command

### Requirement: Checks that cannot run are reported

The tasks instruction SHALL require recording a verification that could not run
as not run, with the reason.

#### Scenario: Missing credentials
- **WHEN** a verification needs credentials that are not available
- **THEN** the task records the check as not run and names the missing credentials
