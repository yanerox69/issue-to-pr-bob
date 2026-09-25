from datetime import date

import pytest

from shopcart.dates import add_business_days, estimated_delivery


def test_business_days_within_week():
    assert add_business_days(date(2026, 9, 21), 3) == date(2026, 9, 24)


def test_express_delivery():
    assert estimated_delivery(date(2026, 9, 21), "express") == date(2026, 9, 23)


def test_unknown_shipping():
    with pytest.raises(ValueError):
        estimated_delivery(date(2026, 9, 21), "teleport")
