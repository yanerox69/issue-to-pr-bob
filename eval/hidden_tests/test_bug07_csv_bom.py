from decimal import Decimal

from shopcart.csv_import import load_products


def test_excel_utf8_bom(tmp_path):
    f = tmp_path / "excel.csv"
    f.write_bytes("﻿sku,name,price,category\nA100,Wireless Mouse,24.99,peripherals\n".encode("utf-8"))
    [p] = load_products(f)
    assert p.sku == "A100"
    assert p.price == Decimal("24.99")


def test_plain_utf8_still_works(tmp_path):
    f = tmp_path / "plain.csv"
    f.write_text("sku,name,price,category\nA100,Ratón inalámbrico,24.99,peripherals\n", encoding="utf-8")
    assert load_products(f)[0].name == "Ratón inalámbrico"
