# Spec Delta

## MODIFIED Requirements

### Requirement: Invalid agent tests

IF none of the agent's tests passes on the reference implementation, THEN the
benchmark SHALL record the fault detection share as not measured.

#### Scenario: Wrong expectation in a test
- **WHEN** an agent's only test expects a value the requirements do not give
- **THEN** the run shows fault detection as not measured

## ADDED Requirements

### Requirement: Fault caught by a reference-passing test

The benchmark SHALL count a fault as caught when at least one agent test that
passes on the reference implementation fails on the faulty implementation.

#### Scenario: Test that settles an ambiguity differently
- **WHEN** one agent test fails on the reference and another passing test fails on a fault
- **THEN** the fault counts as caught and the run's share is measured

### Requirement: Plan-implement task scores

WHEN a plan-implement run ends, the benchmark SHALL record the share of hidden
ambiguities the agent marked, the acceptance tests passed, the fault detection
share and the non-test lines added.

#### Scenario: Two of three ambiguities marked
- **WHEN** the proposal's Assumptions name the leftover cents and the report asks about percentages that do not add up to 100
- **THEN** the run records an ambiguity share of 2/3

### Requirement: Marked ambiguity

The benchmark SHALL count an ambiguity as marked only when one of its terms
appears in a proposal's Assumptions section or in a sentence that also says
assume, question, confirm, unclear, ambiguous, decided or chose.

#### Scenario: Silent decision
- **WHEN** the code handles an empty list but no text marks it as open or assumed
- **THEN** the empty-list ambiguity does not count

### Requirement: Prompts in one session

WHERE a task lists several prompts, the benchmark SHALL send each prompt after
the first as a continuation of the agent's session in the same workspace.

#### Scenario: Plan then implement
- **WHEN** the plan-implement task lists a plan prompt and an implement prompt
- **THEN** Claude gets the second prompt with `--continue` and Codex with `exec resume --last`
