from datetime import date

from shopcart.dates import add_business_days, estimated_delivery

FRIDAY = date(2026, 9, 25)


def test_friday_express_lands_on_tuesday():
    assert estimated_delivery(FRIDAY, "express") == date(2026, 9, 29)


def test_friday_plus_one_is_monday():
    assert add_business_days(FRIDAY, 1) == date(2026, 9, 28)


def test_standard_from_friday():
    assert estimated_delivery(FRIDAY, "standard") == date(2026, 10, 2)
