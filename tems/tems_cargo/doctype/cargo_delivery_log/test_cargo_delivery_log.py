def test_import_cargo_delivery_log_doctype_module():
    mod = __import__("tems.tems.tems_cargo.doctype.cargo_delivery_log.cargo_delivery_log", fromlist=["*"])
    assert mod is not None
