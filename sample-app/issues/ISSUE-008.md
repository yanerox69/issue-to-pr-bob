# ISSUE-008: Delivery estimates are too early for orders near the weekend

**Reporter:** logistics · **Severity:** medium · **Labels:** bug, shipping

Our carrier does not deliver or move parcels on Saturdays or Sundays.

An express order (2 business days) placed on **Friday 2026-09-25** is shown with an
estimated delivery of **Monday 2026-09-28**. It should be **Tuesday 2026-09-29**
(Monday = day 1, Tuesday = day 2). Customers are complaining about "late" deliveries
that are actually on time.
