# ISSUE-010: An order disappeared after another customer cancelled theirs

**Reporter:** customer support · **Severity:** critical · **Labels:** bug, orders, data-loss

Sequence reconstructed from logs:
1. Customer A places an order → `ORD-00001`
2. Customer B places an order → `ORD-00002`
3. Customer A cancels `ORD-00001`
4. Customer C places an order → also gets `ORD-00002`

Customer B's order is gone from the system; C's order replaced it. Order IDs must be
unique for the lifetime of the order book, even after cancellations.
