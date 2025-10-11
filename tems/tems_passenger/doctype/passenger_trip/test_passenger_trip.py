def test_import_passenger_trip_doctype_module():
    mod = __import__("tems.tems.tems_passenger.doctype.passenger_trip.passenger_trip", fromlist=["*"])
    assert mod is not None
