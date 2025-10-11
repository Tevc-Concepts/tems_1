import frappe


def test_import_cargo_consignment_doctype_module():
    mod = __import__("tems.tems.tems_cargo.doctype.cargo_consignment.cargo_consignment", fromlist=["CargoConsignment"])
    assert mod is not None
