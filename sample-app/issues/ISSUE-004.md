# ISSUE-004: We sold more units than we had in the warehouse

**Reporter:** warehouse · **Severity:** critical · **Labels:** bug, inventory

We had 5 monitors (C100) in stock. Two customers ordered 3 each within a few minutes.
Both orders were accepted. Now we owe one customer a monitor we don't have.

Expected: the second order fails with "not enough stock" because only 2 units were still
available after the first order reserved 3.
