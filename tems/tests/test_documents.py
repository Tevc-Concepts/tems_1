def test_documents_smoke():
    import tems.tems_documents.doctype.document_checklist.document_checklist as dc
    assert hasattr(dc, 'DocumentChecklist')
    import tems.tems_documents.report.checklist_count_by_context.checklist_count_by_context as rpt
    assert callable(getattr(rpt, 'execute', None))
