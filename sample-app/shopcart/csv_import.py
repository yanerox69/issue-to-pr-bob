from decimal import Decimal
from pathlib import Path

from .models import Product


def load_products(path: str | Path) -> list[Product]:
    products = []
    with open(path, encoding="utf-8") as f:
        header = f.readline().strip().split(",")
        for line in f:
            if not line.strip():
                continue
            row = dict(zip(header, line.strip().split(",")))
            products.append(
                Product(
                    sku=row["sku"],
                    name=row["name"],
                    price=Decimal(row["price"]),
                    category=row.get("category") or "general",
                )
            )
    return products
