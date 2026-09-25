## fix: cap combined coupon discount at 50% aggregate

Fixes ISSUE-003

### Problem
Stacking coupons bypassed the 50 % business rule. Each coupon's individual
percent was capped at `MAX_DISCOUNT_PERCENT`, but the accumulated total was
returned raw. Two 40 % coupons on a $100 order produced an $80 discount
instead of the allowed maximum of $50.

### Root cause
[`total_discount()`](shopcart/discounts.py:21) in [`shopcart/discounts.py`](shopcart/discounts.py)
accumulated `subtotal * percent / 100` for every valid coupon and returned
`total` directly — no aggregate guard.

### Fix
One-line change at the return statement:

```python
# before
return total
# after
return min(total, subtotal * MAX_DISCOUNT_PERCENT / 100)
```

The guard uses the same `MAX_DISCOUNT_PERCENT` constant (`50`) already
defined in the module, so no magic numbers are introduced.

### Verification
- New test: `test_issue_003_stacked_coupons_capped_at_50_percent`
  in [`tests/test_discounts.py`](tests/test_discounts.py) — asserts two 40 %
  coupons on a $100 order yield exactly $50 off.
- Full suite: **21 / 21 tests pass**.

### Risk
Low. The change only tightens the return value; it cannot increase the
discount beyond what the loop already accumulated. Single-coupon paths
are unaffected when the lone coupon is ≤ 50 %. The only observable
behavioural change is for stacked combinations whose sum exceeded 50 %,
which was already the broken case.
