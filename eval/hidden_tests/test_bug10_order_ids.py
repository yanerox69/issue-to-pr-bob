from datetime import date
from decimal import Decimal

from shopcart.inventory import Inventory
from shopcart.models import Cart, Product
from shopcart.orders import OrderBook

MOUSE = Product("A100", "Wireless Mouse", Decimal("24.99"))


def _order(book, customer):
    cart = Cart(customer)
    cart.add(MOUSE, 1)
    return book.place(cart, "CA", today=date(2026, 9, 21))


def test_ids_unique_after_cancellation():
    inv = Inventory()
    inv.restock("A100", 10)
    book = OrderBook(inv)
    a = _order(book, "A")
    b = _order(book, "B")
    book.cancel(a.id)
    c = _order(book, "C")
    assert c.id not in (a.id, b.id)
    assert book.get(b.id).customer_id == "B"
    assert len(book.all()) == 2
