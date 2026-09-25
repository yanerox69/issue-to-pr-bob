from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN
from typing import Iterable

from . import discounts, tax
from .models import Cart

CENT = Decimal("0.01")


def round_money(amount: Decimal) -> Decimal:
    return amount.quantize(CENT, rounding=ROUND_HALF_EVEN)


def subtotal(cart: Cart) -> Decimal:
    return sum((item.total for item in cart.items), Decimal("0"))


def compute_total(
    cart: Cart,
    region: str,
    coupons: Iterable[discounts.Coupon] = (),
    today: date | None = None,
) -> dict[str, Decimal]:
    sub = subtotal(cart)
    discount = discounts.total_discount(sub, coupons, today)
    taxable = sub - discount
    tax_amount = tax.tax_for(taxable, region)
    return {
        "subtotal": round_money(sub),
        "discount": round_money(discount),
        "tax": round_money(tax_amount),
        "total": round_money(taxable + tax_amount),
    }
