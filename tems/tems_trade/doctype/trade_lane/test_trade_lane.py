import frappe


def test_trade_lane_smoke():
    # Smoke: can create a new doc in memory
    doc = frappe.new_doc("Trade Lane")
    assert doc.doctype == "Trade Lane"
