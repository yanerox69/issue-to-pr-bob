import pytest

from shopcart.inventory import OutOfStock


def test_reserve_reduces_available(inventory):
    inventory.reserve("A100", 3)
    assert inventory.available("A100") == 7


def test_reserve_more_than_stock_fails(inventory):
    with pytest.raises(OutOfStock):
        inventory.reserve("A100", 11)


def test_commit_and_release(inventory):
    inventory.reserve("A100", 4)
    inventory.commit("A100", 3)
    inventory.release("A100", 1)
    assert inventory.available("A100") == 7
