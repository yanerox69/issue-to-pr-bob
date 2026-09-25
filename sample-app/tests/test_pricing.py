from datetime import date
from decimal import Decimal

from shopcart.discounts import Coupon
from shopcart.models import Cart
from shopcart.pricing import compute_total, round_money
from shopcart.tax import rate_for

TODAY = date(2026, 9, 21)


def test_round_money():
    assert round_money(Decimal("1.234")) == Decimal("1.23")


def test_total_with_tax(keyboard):
    cart = Cart("c1")
    cart.add(keyboard, 1)
    totals = compute_total(cart, "CA", today=TODAY)
    assert totals["subtotal"] == Decimal("89.00")
    assert totals["tax"] == Decimal("6.45")
    assert totals["total"] == Decimal("95.45")


def test_single_coupon(keyboard):
    cart = Cart("c1")
    cart.add(keyboard, 1)
    coupon = Coupon("WELCOME10", Decimal("10"), date(2026, 12, 31))
    totals = compute_total(cart, "OR", [coupon], today=TODAY)
    assert totals["discount"] == Decimal("8.90")
    assert totals["total"] == Decimal("80.10")


def test_expired_coupon_ignored(keyboard):
    cart = Cart("c1")
    cart.add(keyboard, 1)
    coupon = Coupon("OLD", Decimal("10"), date(2026, 1, 1))
    assert compute_total(cart, "OR", [coupon], today=TODAY)["discount"] == Decimal("0")


def test_tax_rates():
    assert rate_for("NY") == Decimal("0.04")
    assert rate_for("OR") == Decimal("0")
