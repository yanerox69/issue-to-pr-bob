# ISSUE-003: Stacked coupons give more than 50% off

**Reporter:** revenue ops · **Severity:** high · **Labels:** bug, discounts, money-loss

Business rule: no matter how many coupons a customer combines, the total discount on an
order must never exceed 50%.

A customer combined `STUDENT40` (40%) and `BLACKFRIDAY40` (40%) on a $100 order and paid
$20 — an 80% discount. Expected: $50 off, they pay $50.

A single 70% coupon correctly gets capped at 50%, so the cap exists; it just doesn't work
when coupons are combined.
