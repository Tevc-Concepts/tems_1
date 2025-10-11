def test_import_passenger_manifest_doctype_module():
    mod = __import__("tems.tems.tems_passenger.doctype.passenger_manifest.passenger_manifest", fromlist=["*"])
    assert mod is not None
