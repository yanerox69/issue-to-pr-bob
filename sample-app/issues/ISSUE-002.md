# ISSUE-002: Coupon rejected on its last valid day

**Reporter:** customer support · **Severity:** high · **Labels:** bug, discounts

We ran the `FALL20` campaign with the email copy "valid until September 30". Customers
who tried to use it **on September 30** got no discount. On September 29 it worked fine.

Support handled 40+ complaints and had to issue manual refunds. The `expires` field on a
coupon is documented as the last day the coupon can be used.
