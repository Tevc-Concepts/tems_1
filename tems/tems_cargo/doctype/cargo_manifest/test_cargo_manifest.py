def test_import_manifest_doctype_module():
    mod = __import__("tems.tems.tems_cargo.doctype.cargo_manifest.cargo_manifest", fromlist=["*"])
    assert mod is not None
