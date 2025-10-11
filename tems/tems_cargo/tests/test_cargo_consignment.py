import frappe
from types import SimpleNamespace


def test_vehicle_type_guard_for_cargo(monkeypatch):
    # Create a fake consignment doc dict and simulate validation
    d = SimpleNamespace(vehicle="V1", operation_plan=None)
    calls = {"get_value": []}

    def fake_get_value(doctype, name, fieldname=None):
        calls["get_value"].append((doctype, name, fieldname))
        if doctype == "Vehicle" and fieldname in ("vehicle_type", "custom_vehicle_type"):
            return "Cargo"
        return None

    monkeypatch.setattr(frappe.db, "get_value", fake_get_value)
    from tems.tems_cargo.handlers.consignment import validate_vehicle_type
    validate_vehicle_type(d)
    assert len(calls["get_value"]) > 0
