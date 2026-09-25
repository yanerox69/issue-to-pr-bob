import pytest

from shopcart.inventory import Inventory, OutOfStock


def test_cannot_reserve_already_reserved_units():
    inv = Inventory()
    inv.restock("C100", 5)
    inv.reserve("C100", 3)
    with pytest.raises(OutOfStock):
        inv.reserve("C100", 3)
    assert inv.available("C100") == 2


def test_can_reserve_exactly_what_is_left():
    inv = Inventory()
    inv.restock("C100", 5)
    inv.reserve("C100", 3)
    inv.reserve("C100", 2)
    assert inv.available("C100") == 0
