# fix: invoice totals off by one cent due to banker's rounding

Fixes ISSUE-001

## Root cause

[`shopcart/pricing.py`](shopcart/pricing.py) imported and applied `ROUND_HALF_EVEN`
(Python's default "banker's rounding") in `round_money()`. Banker's rounding rounds
ties toward the nearest even digit, so `2.665` became `2.66` instead of `2.67`.
Company policy mandates **half-up rounding** for all monetary values.

## Fix

Two-line change — swap `ROUND_HALF_EVEN` for `ROUND_HALF_UP` in:

1. The import on line 1 of `shopcart/pricing.py`
2. The `rounding=` argument in `round_money()` on line 12

No logic, no schema, no API surface changed.

## Verification

Added two regression tests in [`tests/test_pricing.py`](tests/test_pricing.py):

- `test_issue_001_round_half_up_2665` — asserts `2.665 → 2.67`
- `test_issue_001_round_half_up_0125` — asserts `0.125 → 0.13`

All **22 tests pass**.

## Risk

Low. `round_money()` is called only at the final aggregation step (invoice total).
The rounding mode change can shift a result by exactly `$0.01` on midpoint values;
this is the intended correction. No downstream systems consume raw `Decimal` objects
— they receive the already-rounded string/float from the serialiser.
