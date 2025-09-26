def test_finance_smoke():
    import tems.tems_finance.doctype.fleet_cost.fleet_cost as fc
    assert hasattr(fc, 'FleetCost')
    # report smoke
    import tems.tems_finance.report.total_cost_by_type.total_cost_by_type as rpt
    assert callable(getattr(rpt, 'execute', None))
