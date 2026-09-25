# ISSUE-001: Invoice totals are sometimes one cent lower than finance's numbers

**Reporter:** finance team · **Severity:** medium · **Labels:** bug, pricing

Our reconciliation job flagged ~3% of invoices where shopcart is one cent **below**
what our accounting system computes. Company policy (and the accounting system) rounds
money half-up: an amount of exactly x.xx5 always rounds up.

Example we traced by hand: an intermediate amount of `2.665` shows up on the invoice as
`2.66`, accounting says `2.67`. Same thing with `0.125` → we print `0.12`, expected `0.13`.

It doesn't happen on every order, which is what makes it hard to catch.
