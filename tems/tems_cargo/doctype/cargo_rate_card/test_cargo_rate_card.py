def test_import_cargo_rate_card_doctype_module():
    mod = __import__("tems.tems.tems_cargo.doctype.cargo_rate_card.cargo_rate_card", fromlist=["*"])
    assert mod is not None
