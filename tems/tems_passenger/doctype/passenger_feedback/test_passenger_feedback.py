def test_import_passenger_feedback_doctype_module():
    mod = __import__("tems.tems.tems_passenger.doctype.passenger_feedback.passenger_feedback", fromlist=["*"])
    assert mod is not None
