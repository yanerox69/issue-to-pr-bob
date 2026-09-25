# ISSUE-005: Editing a "reorder" cart changes my past order

**Reporter:** customer (via support) · **Severity:** high · **Labels:** bug, orders, data-integrity

Steps:
1. Place an order with 2 × Wireless Mouse.
2. Go to order history → "Buy again". A new cart opens with 2 × Wireless Mouse.
3. Add one more mouse to that new cart (now 3).
4. Go back to order history: **the original order now also says 3 mice.**

Past orders must be immutable — they're used for invoices and returns.
