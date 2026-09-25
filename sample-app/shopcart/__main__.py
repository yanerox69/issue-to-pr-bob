"""CLI: python -m shopcart quote --catalog data/products.csv --item A100:2 --region CA"""

import argparse
from datetime import date
from decimal import Decimal

from .csv_import import load_products
from .discounts import Coupon
from .models import Cart
from .pricing import compute_total


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="shopcart")
    sub = parser.add_subparsers(dest="command", required=True)
    quote = sub.add_parser("quote", help="price a cart")
    quote.add_argument("--catalog", required=True)
    quote.add_argument("--item", action="append", default=[], help="SKU:QTY")
    quote.add_argument("--region", required=True)
    quote.add_argument("--coupon", action="append", default=[], help="CODE:PERCENT:YYYY-MM-DD")
    args = parser.parse_args(argv)

    catalog = {p.sku: p for p in load_products(args.catalog)}
    cart = Cart(customer_id="cli")
    for spec in args.item:
        sku, qty = spec.split(":")
        cart.add(catalog[sku], int(qty))
    coupons = []
    for spec in args.coupon:
        code, pct, expires = spec.split(":")
        coupons.append(Coupon(code, Decimal(pct), date.fromisoformat(expires)))

    for key, value in compute_total(cart, args.region, coupons).items():
        print(f"{key:>9}: {value}")


if __name__ == "__main__":
    main()
