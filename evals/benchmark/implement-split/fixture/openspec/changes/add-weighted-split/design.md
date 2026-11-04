# Design

## Decisions

### 1. Interface

`split(total: int, weights: list[int]) -> list[int]` in `app/split.py`, one
share per weight, in the order of the weights.

### 2. Integer arithmetic

Each base share is `total * weight // sum(weights)`; the remainder
`total * weight % sum(weights)` orders the extra units. Integer arithmetic
avoids floating point errors. Option ladder: no existing code or standard
library function does this; this is the minimum that works.
