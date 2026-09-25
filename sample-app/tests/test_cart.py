import pytest

from shopcart.models import Cart


def test_add_merges_same_sku(mouse):
    cart = Cart("c1")
    cart.add(mouse, 1)
    cart.add(mouse, 2)
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 3


def test_add_rejects_non_positive_quantity(mouse):
    with pytest.raises(ValueError):
        Cart("c1").add(mouse, 0)


def test_remove(mouse, keyboard):
    cart = Cart("c1")
    cart.add(mouse)
    cart.add(keyboard)
    cart.remove(mouse.sku)
    assert [i.product.sku for i in cart.items] == [keyboard.sku]
