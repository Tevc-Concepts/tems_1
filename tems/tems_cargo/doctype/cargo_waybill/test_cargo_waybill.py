def test_import_waybill_doctype_module():
    mod = __import__("tems.tems.tems_cargo.doctype.cargo_waybill.cargo_waybill", fromlist=["*"])
    assert mod is not None
