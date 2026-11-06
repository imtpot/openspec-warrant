## MODIFIED Requirements

### Requirement: Fail for the expected reason

IF a new test fails for a reason other than the missing behavior (which
includes a function, module or attribute under test that does not exist yet),
such as an import or syntax error in the test, THEN the TDD skill SHALL fix the
test until it fails for the missing behavior.

#### Scenario: Import error
- **WHEN** the new test fails because of a misspelled import
- **THEN** the skill fixes the import and runs the test again before writing code

#### Scenario: Function not written yet
- **WHEN** the new test fails because the function it calls does not exist yet
- **THEN** the skill treats the failure as red and writes the function in Green

### Requirement: Mutation check

WHEN the TDD skill has finished every scenario and boundary case, the TDD
skill SHALL apply each realistic mutation of the changed code temporarily, run
the tests against it, revert it, and add a test that fails on the mutation and
passes after the revert for each mutation that no test fails on.

#### Scenario: Rounding mutation not caught
- **WHEN** replacing round-half-up with round-half-even fails no test
- **THEN** the skill adds a test that fails on that mutation and passes on the code

#### Scenario: Mutation reverted
- **WHEN** the mutation check ends
- **THEN** the production code has none of the applied mutations
