# fix: coupon rejected on expiry date (ISSUE-002)

Fixes ISSUE-002

## Root cause

[`is_valid()`](shopcart/discounts.py:18) compared today against the expiry date with strict
less-than (`today < coupon.expires`). The `expires` field is documented as the **last day**
the coupon can be used, so a coupon presented on its expiry date was incorrectly rejected.

## Fix

Changed the comparison from `<` to `<=` in [`shopcart/discounts.py`](shopcart/discounts.py:18):

```python
# before
return today < coupon.expires

# after
return today <= coupon.expires
```

One character, no behavioural change for any other date — coupons still expire the day after
`expires`.

## Verification

- Added `test_issue_002_coupon_valid_on_expiry_date` in [`tests/test_discounts.py`](tests/test_discounts.py)
  which asserts `is_valid()` returns `True` when `today == coupon.expires`.
- All **21 tests pass**.

## Risk

Minimal. The only changed line is the boundary condition in a pure function with no side
effects. Any caller that relied on the off-by-one (incorrectly) would have been wrong by
design.
