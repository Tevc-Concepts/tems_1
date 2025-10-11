import frappe
from types import SimpleNamespace


def test_vehicle_type_guard_for_passenger(monkeypatch):
    d = SimpleNamespace(vehicle="BUS-1")
    calls = []

    def fake_get_value(doctype, name, fieldname=None):
        calls.append((doctype, name, fieldname))
        if doctype == "Vehicle" and fieldname in ("vehicle_type", "custom_vehicle_type"):
            return "Passenger"
        return None

    monkeypatch.setattr(frappe.db, "get_value", fake_get_value)
    from tems.tems_passenger.handlers.trip import validate_vehicle_type
    validate_vehicle_type(d)
    assert calls
