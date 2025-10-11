def test_import_passenger_booking_doctype_module():
    mod = __import__("tems.tems.tems_passenger.doctype.passenger_booking.passenger_booking", fromlist=["*"])
    assert mod is not None
