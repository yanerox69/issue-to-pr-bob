import copy
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable

from . import dates, pricing
from .discounts import Coupon
from .inventory import Inventory
from .models import Cart, LineItem


@dataclass
class Order:
    id: str
    customer_id: str
    items: list[LineItem]
    region: str
    totals: dict[str, Decimal]
    placed_on: date
    delivery: date
    status: str = "open"


class OrderBook:
    def __init__(self, inventory: Inventory) -> None:
        self.inventory = inventory
        self._orders: dict[str, Order] = {}

    def place(
        self,
        cart: Cart,
        region: str,
        coupons: Iterable[Coupon] = (),
        today: date | None = None,
        shipping: str = "standard",
    ) -> Order:
        if cart.is_empty():
            raise ValueError("cannot place an empty order")
        today = today or date.today()
        reserved = []
        try:
            for item in cart.items:
                self.inventory.reserve(item.product.sku, item.quantity)
                reserved.append(item)
        except Exception:
            for item in reserved:
                self.inventory.release(item.product.sku, item.quantity)
            raise

        order_id = f"ORD-{len(self._orders) + 1:05d}"
        order = Order(
            id=order_id,
            customer_id=cart.customer_id,
            items=list(cart.items),
            region=region,
            totals=pricing.compute_total(cart, region, coupons, today),
            placed_on=today,
            delivery=dates.estimated_delivery(today, shipping),
        )
        self._orders[order_id] = order
        return order

    def get(self, order_id: str) -> Order:
        return self._orders[order_id]

    def all(self) -> list[Order]:
        return list(self._orders.values())

    def cancel(self, order_id: str) -> None:
        order = self._orders.pop(order_id)
        for item in order.items:
            self.inventory.release(item.product.sku, item.quantity)

    def reorder(self, order_id: str) -> Cart:
        """Start a new cart pre-filled with the items of a past order."""
        order = self.get(order_id)
        return Cart(customer_id=order.customer_id, items=copy.copy(order.items))
