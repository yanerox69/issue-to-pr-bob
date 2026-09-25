from decimal import Decimal

import pytest

from shopcart.tax import rate_for


def test_region_is_case_insensitive_and_trimmed():
    assert rate_for("ca") == Decimal("0.0725")
    assert rate_for("CA ") == Decimal("0.0725")
    assert rate_for(" ny") == Decimal("0.04")


def test_oregon_is_still_zero():
    assert rate_for("or") == Decimal("0")


def test_unknown_region_fails_loudly():
    with pytest.raises((ValueError, KeyError)):
        rate_for("ZZ")
