# Proposal

## Why

Support exports a customer's orders by copying rows from the database by hand.

## What Changes

- `export_page(orders, customer, number, size, path)` writes one page of a
  customer's orders as CSV and compresses it with gzip.

## Capabilities

### New Capabilities
- `order-export`: export a page of a customer's orders.

### Modified Capabilities
None.

## Impact

New `app/export.py` and its tests.

## Why code is needed

No existing tool in this project writes order pages.

## Out of scope

This change exports one page; it adds no command line.

Features and options deliberately left out:

- Formats other than CSV.

## Assumptions

Confirmed by the requester: pages are 1-based; the newest order comes first,
and orders with the same date are ordered by id ascending. No other decision is
open.
