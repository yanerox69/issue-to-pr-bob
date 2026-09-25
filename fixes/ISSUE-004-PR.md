# fix: reserve() oversells when reservations already exist (ISSUE-004)

Fixes ISSUE-004

## Root cause

[`Inventory.reserve()`](shopcart/inventory.py:21) guarded against overselling by
comparing the requested quantity to `self._stock.get(sku, 0)` — raw physical
stock — rather than to the units actually still available. Because it ignored
existing reservations, a second concurrent call could read the same raw stock
value and be accepted even when the available units had already been spoken for.
**Concrete failure:** stock = 5, first order reserves 3 (available drops to 2),
second order also requests 3 — guard saw 3 ≤ 5 (raw) and wrongly accepted it,
overselling by 1 unit.

## Fix

One-line change in [`shopcart/inventory.py`](shopcart/inventory.py:21):

```diff
-        if quantity > self._stock.get(sku, 0):
+        if quantity > self.available(sku):
```

`self.available(sku)` already returns `_stock − _reserved`, so the guard now
rejects any reservation that would exceed truly available units.

## Verification

Added `test_issue_004_concurrent_reservation_race` in
[`tests/test_inventory.py`](tests/test_inventory.py) — asserts that a second
reservation of 3 units against stock of 5 (with 3 already reserved) raises
`OutOfStock`. All 21 tests pass.

## Risk / what to review

- **Low risk.** Single-line change; touches only the guard condition, not the
  reservation accounting logic.
- Verify `available()` is correct under all restock / commit / release paths
  (existing tests cover this).
- No schema, API, or interface changes.
