def test_supply_chain_smoke():
    import tems.tems_supply_chain.doctype.spare_part.spare_part as sp
    assert hasattr(sp, 'SparePart')
    import tems.tems_supply_chain.report.spare_parts_min_stock_breach.spare_parts_min_stock_breach as rpt
    assert callable(getattr(rpt, 'execute', None))
