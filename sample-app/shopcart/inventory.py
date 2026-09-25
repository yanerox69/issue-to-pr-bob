class OutOfStock(Exception):
    pass


class Inventory:
    """Tracks physical stock and quantities reserved by open orders."""

    def __init__(self) -> None:
        self._stock: dict[str, int] = {}
        self._reserved: dict[str, int] = {}

    def restock(self, sku: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        self._stock[sku] = self._stock.get(sku, 0) + quantity

    def available(self, sku: str) -> int:
        return self._stock.get(sku, 0) - self._reserved.get(sku, 0)

    def reserve(self, sku: str, quantity: int) -> None:
        if quantity > self._stock.get(sku, 0):
            raise OutOfStock(f"not enough stock for {sku}")
        self._reserved[sku] = self._reserved.get(sku, 0) + quantity

    def release(self, sku: str, quantity: int) -> None:
        self._reserved[sku] = max(0, self._reserved.get(sku, 0) - quantity)

    def commit(self, sku: str, quantity: int) -> None:
        """Ship reserved units: they leave both stock and the reservation."""
        self._stock[sku] = self._stock.get(sku, 0) - quantity
        self.release(sku, quantity)
