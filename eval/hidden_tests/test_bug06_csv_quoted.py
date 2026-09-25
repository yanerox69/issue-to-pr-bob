from decimal import Decimal

from shopcart.csv_import import load_products


def test_quoted_name_with_comma(tmp_path):
    f = tmp_path / "supplier.csv"
    f.write_text(
        'sku,name,price,category\nD100,"Cable, USB-C to USB-C (2m)",12.99,accessories\n',
        encoding="utf-8",
    )
    [p] = load_products(f)
    assert p.sku == "D100"
    assert p.name == "Cable, USB-C to USB-C (2m)"
    assert p.price == Decimal("12.99")
    assert p.category == "accessories"
