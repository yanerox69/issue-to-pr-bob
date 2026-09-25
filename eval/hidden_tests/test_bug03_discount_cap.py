from datetime import date
from decimal import Decimal

from shopcart.discounts import Coupon, total_discount

TODAY = date(2026, 9, 21)
LATER = date(2026, 12, 31)


def test_combined_coupons_capped_at_50_percent():
    coupons = [Coupon("STUDENT40", Decimal("40"), LATER), Coupon("BLACKFRIDAY40", Decimal("40"), LATER)]
    assert total_discount(Decimal("100"), coupons, TODAY) == Decimal("50")


def test_combined_under_cap_still_adds_up():
    coupons = [Coupon("A", Decimal("10"), LATER), Coupon("B", Decimal("15"), LATER)]
    assert total_discount(Decimal("100"), coupons, TODAY) == Decimal("25")


def test_single_coupon_capped():
    assert total_discount(Decimal("100"), [Coupon("BIG", Decimal("70"), LATER)], TODAY) == Decimal("50")
