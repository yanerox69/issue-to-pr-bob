from decimal import Decimal

import pytest

from shopcart.inventory import Inventory
from shopcart.models import Product


@pytest.fixture
def mouse():
    return Product("A100", "Wireless Mouse", Decimal("24.99"), "peripherals")


@pytest.fixture
def keyboard():
    return Product("A200", "Mechanical Keyboard", Decimal("89.00"), "peripherals")


@pytest.fixture
def inventory(mouse, keyboard):
    inv = Inventory()
    inv.restock(mouse.sku, 10)
    inv.restock(keyboard.sku, 5)
    return inv
