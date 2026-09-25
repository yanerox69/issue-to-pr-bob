from datetime import date
from decimal import Decimal

from shopcart.inventory import Inventory
from shopcart.models import Cart, Product
from shopcart.orders import OrderBook

MOUSE = Product("A100", "Wireless Mouse", Decimal("24.99"))


def test_editing_reorder_cart_does_not_touch_past_order():
    inv = Inventory()
    inv.restock("A100", 10)
    book = OrderBook(inv)
    cart = Cart("c1")
    cart.add(MOUSE, 2)
    order = book.place(cart, "CA", today=date(2026, 9, 21))

    again = book.reorder(order.id)
    again.add(MOUSE, 1)

    assert again.items[0].quantity == 3
    assert book.get(order.id).items[0].quantity == 2


def test_editing_original_cart_after_placing_does_not_touch_order():
    inv = Inventory()
    inv.restock("A100", 10)
    book = OrderBook(inv)
    cart = Cart("c1")
    cart.add(MOUSE, 2)
    order = book.place(cart, "CA", today=date(2026, 9, 21))
    cart.add(MOUSE, 5)
    assert book.get(order.id).items[0].quantity == 2
