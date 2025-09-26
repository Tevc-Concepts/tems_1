def test_informal_report_smoke():
    import tems.tems_informal.report.active_informal_operators.active_informal_operators as rpt
    assert hasattr(rpt, 'execute')
