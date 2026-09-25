## fix: reorder() deep-copies LineItems to prevent past-order mutation (ISSUE-005)

**Fixes ISSUE-005**

### Root cause

`OrderBook.reorder()` built the new cart with `copy.copy(order.items)` — a
shallow list copy. The list itself was new, but every `LineItem` object inside
it was the **same instance** shared with the original order.
When `Cart.add()` incremented `quantity` in-place on a `LineItem`, it silently
corrupted the historical order record.

### Fix

`shopcart/orders.py:78` — replaced `copy.copy(order.items)` with
`copy.deepcopy(order.items)`. The new cart now receives fully independent
`LineItem` instances; mutations to the new cart have no effect on the original
order.

### Verification

- Added `test_issue_005_reorder_does_not_mutate_original_order` in
  `tests/test_orders.py`: places an order for 2 units, reorders, adds 1 more
  to the new cart, and asserts the original order still shows 2 units.
- All 21 tests pass.

### Risk

Low. `deepcopy` is strictly safer than `copy` here; no callers depend on
shared identity between a new cart and a past order. The only observable
behaviour change is the fix itself.
