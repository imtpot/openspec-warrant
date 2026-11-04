# Spec Delta

## ADDED Requirements

### Requirement: Page content

WHEN a page is exported, the export SHALL contain the customer's orders at
positions `(number - 1) * size` to `number * size - 1` of the sorted list.

#### Scenario: Second page of two
- **WHEN** a customer has 4 orders and page 2 of size 2 is exported
- **THEN** the file holds the third and fourth orders

### Requirement: Order

The export SHALL sort orders by date with the newest first, and orders with the
same date by id ascending.

#### Scenario: Same date
- **WHEN** orders 7 and 3 have the same date
- **THEN** order 3 comes before order 7

### Requirement: Page past the end

IF the page starts after the last order, THEN the export SHALL write a file
with only the header row.

#### Scenario: Page 5 of 2 orders
- **WHEN** a customer has 2 orders and page 5 of size 2 is exported
- **THEN** the file holds only the header row
