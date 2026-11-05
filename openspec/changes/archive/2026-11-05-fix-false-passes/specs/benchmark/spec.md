## MODIFIED Requirements

### Requirement: Marked ambiguity

The benchmark SHALL count an ambiguity as marked only when one of its terms
appears in a proposal's Assumptions section or in a sentence that also says
assume, question, confirm, unclear or ambiguous.

#### Scenario: Silent decision
- **WHEN** the code handles an empty list but no text marks it as open or assumed
- **THEN** the empty-list ambiguity does not count

#### Scenario: Decision reported as made
- **WHEN** the report says "I decided that an empty list returns an empty list" and no other text marks the empty list
- **THEN** the empty-list ambiguity does not count
