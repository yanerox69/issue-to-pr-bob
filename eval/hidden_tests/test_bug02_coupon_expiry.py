from datetime import date
from decimal import Decimal

from shopcart.discounts import Coupon, is_valid

FALL20 = Coupon("FALL20", Decimal("20"), date(2026, 9, 30))


def test_valid_on_last_day():
    assert is_valid(FALL20, date(2026, 9, 30))


def test_still_valid_before_and_invalid_after():
    assert is_valid(FALL20, date(2026, 9, 29))
    assert not is_valid(FALL20, date(2026, 10, 1))
