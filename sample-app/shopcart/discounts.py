from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable

# Business rule: combined coupons can never take more than half off an order.
MAX_DISCOUNT_PERCENT = Decimal("50")


@dataclass(frozen=True)
class Coupon:
    code: str
    percent: Decimal
    expires: date  # last day the coupon can be used


def is_valid(coupon: Coupon, today: date) -> bool:
    return today < coupon.expires


def total_discount(
    subtotal: Decimal, coupons: Iterable[Coupon], today: date | None = None
) -> Decimal:
    today = today or date.today()
    total = Decimal("0")
    for coupon in coupons:
        if not is_valid(coupon, today):
            continue
        percent = min(coupon.percent, MAX_DISCOUNT_PERCENT)
        total += subtotal * percent / 100
    return total
