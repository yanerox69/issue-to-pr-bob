# shopcart

Small order-management library: carts, pricing (discounts + sales tax), inventory
reservations, orders and delivery estimates.

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m shopcart quote --catalog data/products.csv --item A100:2 --item B200:1 --region CA
```

Open bug reports live in [`issues/`](issues/).

## Layout

| Module | Responsibility |
|---|---|
| `models.py` | `Product`, `LineItem`, `Cart` |
| `pricing.py` | subtotal, rounding, order totals |
| `discounts.py` | coupons and the combined-discount cap |
| `tax.py` | sales-tax rates by region |
| `inventory.py` | stock and reservations |
| `orders.py` | placing, cancelling and reordering orders |
| `dates.py` | business days and delivery estimates |
| `csv_import.py` | product catalog import |
