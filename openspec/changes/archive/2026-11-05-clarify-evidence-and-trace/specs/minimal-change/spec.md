## MODIFIED Requirements

### Requirement: Every line traces to a requirement

WHILE a change belongs to an OpenSpec change, the minimal-change skill SHALL
direct the agent to remove any added line that serves none of these bases: a
requirement of that change, an item of the Protected code list, or a rule in a
file under `### Standards` of the contract.

#### Scenario: Speculative parameter
- **WHEN** the diff adds a parameter that no requirement uses
- **THEN** the agent removes the parameter before completion

#### Scenario: Input check no requirement names
- **WHEN** the diff adds validation of user input that no requirement of the change names
- **THEN** the line stays, traced as `protected: validation at trust boundaries`

#### Scenario: Line a standard requires
- **WHEN** a Standards file says "log every caught exception" and the diff adds such a log line
- **THEN** the line stays, traced as `standard: <file>`

## ADDED Requirements

### Requirement: Named trace basis

WHILE a change belongs to an OpenSpec change, the minimal-change skill SHALL
direct the agent to name each added line's basis as `requirement: <name>`,
`protected: <item>` or `standard: <file>`.

#### Scenario: Trace of a mixed diff
- **WHEN** the diff adds a verdict branch for a requirement and an input check
- **THEN** the trace names `requirement: Shortfall verdict` for the branch and `protected: validation at trust boundaries` for the check
