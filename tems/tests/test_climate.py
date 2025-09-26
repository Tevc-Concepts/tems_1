def test_emissions_report_smoke():
    import tems.tems_climate.report.emissions_by_asset_month.emissions_by_asset_month as rpt
    assert hasattr(rpt, 'execute')
