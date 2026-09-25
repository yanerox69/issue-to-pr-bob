# ISSUE-006: Catalog import crashes when a product name contains a comma

**Reporter:** catalog team · **Severity:** medium · **Labels:** bug, import

Our supplier's CSV export quotes names that contain commas, which is standard CSV:

```csv
sku,name,price,category
D100,"Cable, USB-C to USB-C (2m)",12.99,accessories
```

Importing it crashes with `decimal.InvalidOperation`. Files without commas in names work.
