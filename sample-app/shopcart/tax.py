from decimal import Decimal

TAX_RATES = {
    "CA": Decimal("0.0725"),
    "NY": Decimal("0.04"),
    "TX": Decimal("0.0625"),
    "WA": Decimal("0.065"),
    "OR": Decimal("0"),
}


def rate_for(region: str) -> Decimal:
    return TAX_RATES.get(region, Decimal("0"))


def tax_for(amount: Decimal, region: str) -> Decimal:
    return amount * rate_for(region)
