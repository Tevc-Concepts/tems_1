def test_crm_smoke():
    import tems.tems_crm.doctype.field_service_request.field_service_request as fsr
    assert hasattr(fsr, 'FieldServiceRequest')
    import tems.tems_crm.report.fsr_open_by_priority.fsr_open_by_priority as rpt
    assert callable(getattr(rpt, 'execute', None))
