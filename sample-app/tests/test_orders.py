from datetime import date

import pytest

from shopcart.models import Cart
from shopcart.orders import OrderBook

MONDAY = date(2026, 9, 21)


def test_place_order(inventory, mouse):
    book = OrderBook(inventory)
    cart = Cart("c1")
    cart.add(mouse, 2)
    order = book.place(cart, "CA", today=MONDAY)
    assert order.id == "ORD-00001"
    assert inventory.available("A100") == 8
    assert book.get(order.id) is order


def test_cancel_releases_stock(inventory, mouse):
    book = OrderBook(inventory)
    cart = Cart("c1")
    cart.add(mouse, 2)
    order = book.place(cart, "CA", today=MONDAY)
    book.cancel(order.id)
    assert inventory.available("A100") == 10
    assert book.all() == []


def test_empty_cart_rejected(inventory):
    with pytest.raises(ValueError):
        OrderBook(inventory).place(Cart("c1"), "CA")


def test_reorder_copies_items(inventory, mouse):
    book = OrderBook(inventory)
    cart = Cart("c1")
    cart.add(mouse, 2)
    order = book.place(cart, "CA", today=MONDAY)
    again = book.reorder(order.id)
    assert again.customer_id == "c1"
    assert [(i.product.sku, i.quantity) for i in again.items] == [("A100", 2)]
