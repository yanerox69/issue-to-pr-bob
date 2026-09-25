from decimal import Decimal
from pathlib import Path

from shopcart.csv_import import load_products

DATA = Path(__file__).parent.parent / "data" / "products.csv"


def test_load_sample_catalog():
    products = load_products(DATA)
    assert len(products) == 5
    assert products[0].sku == "A100"
    assert products[0].price == Decimal("24.99")


def test_missing_category_defaults(tmp_path):
    f = tmp_path / "p.csv"
    f.write_text("sku,name,price,category\nZ1,Thing,1.00,\n", encoding="utf-8")
    assert load_products(f)[0].category == "general"
