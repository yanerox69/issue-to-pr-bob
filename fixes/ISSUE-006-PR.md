# fix: catalog import crashes when product name contains a comma (ISSUE-006)

Fixes ISSUE-006

## Summary

`load_products` crashed with `decimal.InvalidOperation` whenever a CSV catalog
file contained a product whose name was a quoted field with an embedded comma
(e.g. `"Cable, USB-C to USB-C (2m)"`). The fix replaces the naïve string split
with Python's standard `csv.reader`, which handles RFC 4180 quoting correctly.

## Root cause

`shopcart/csv_import.py` parsed every row with `line.strip().split(",")`. A
comma inside a quoted field was treated as a field delimiter, shifting all
subsequent columns by one. `row["price"]` received the remainder of the name
string instead of the numeric price value, and `Decimal(...)` raised
`InvalidOperation`.

## Fix

- Added `import csv` to [`shopcart/csv_import.py`](../shopcart/csv_import.py).
- Changed `open(path, ...)` to pass `newline=""` as required by `csv.reader`.
- Replaced `f.readline().strip().split(",")` (header) and
  `line.strip().split(",")` (data rows) with a single `csv.reader` that yields
  pre-split, unquoted field lists. No other logic changed.

## Testing

New test: `tests/test_csv_import.py::test_issue_006_quoted_name_with_comma`

Writes a one-row CSV whose name field is `"Cable, USB-C to USB-C (2m)"`, loads
it, and asserts that `sku`, `price`, and `name` are all parsed correctly.

Full suite result: **21/21 tests pass.**

## Risk / what to review

- Low risk — the change is a drop-in replacement of the split calls; all
  existing field semantics are preserved.
- Confirm the `newline=""` argument does not conflict with any callers that pass
  an already-open file handle (none exist today, but worth noting for future
  API changes).
