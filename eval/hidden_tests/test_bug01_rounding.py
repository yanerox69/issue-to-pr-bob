from decimal import Decimal

from shopcart.pricing import round_money


def test_half_up():
    assert round_money(Decimal("2.665")) == Decimal("2.67")
    assert round_money(Decimal("0.125")) == Decimal("0.13")


def test_other_values_unchanged():
    assert round_money(Decimal("2.664")) == Decimal("2.66")
    assert round_money(Decimal("2.675")) == Decimal("2.68")
