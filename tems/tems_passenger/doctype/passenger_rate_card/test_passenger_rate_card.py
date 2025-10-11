def test_import_passenger_rate_card_doctype_module():
    mod = __import__("tems.tems.tems_passenger.doctype.passenger_rate_card.passenger_rate_card", fromlist=["*"])
    assert mod is not None
