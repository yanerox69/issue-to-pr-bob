from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price: Decimal
    category: str = "general"


@dataclass
class LineItem:
    product: Product
    quantity: int

    @property
    def total(self) -> Decimal:
        return self.product.price * self.quantity


@dataclass
class Cart:
    customer_id: str
    items: list[LineItem] = field(default_factory=list)

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        for item in self.items:
            if item.product.sku == product.sku:
                item.quantity += quantity
                return
        self.items.append(LineItem(product, quantity))

    def remove(self, sku: str) -> None:
        self.items = [i for i in self.items if i.product.sku != sku]

    def is_empty(self) -> bool:
        return not self.items
