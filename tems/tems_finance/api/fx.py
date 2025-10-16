"""Public/whitelisted Finance API endpoints for TEMS."""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import nowdate


@frappe.whitelist()
def record_fx_rate(currency_pair: str, rate: float, exposure_amount: float = 0, exposure_currency: str | None = None):
    """Record (or update) today's FX Risk Log entry for a currency pair.

    Args:
        currency_pair: e.g. 'USD/NGN'
        rate: numeric rate used for exposure valuation
        exposure_amount: open exposure (optional)
        exposure_currency: currency of exposure (defaults to first leg of pair)
    """
    if not currency_pair or "/" not in currency_pair:
        frappe.throw(_("Invalid currency pair format. Use BASE/QUOTE e.g. USD/NGN"))
    exposure_currency = exposure_currency or currency_pair.split("/")[0]
    existing = frappe.db.get_value("FX Risk Log", {"date": nowdate(), "currency_pair": currency_pair}, "name")
    doc_fields = dict(
        doctype="FX Risk Log",
        date=nowdate(),
        currency_pair=currency_pair,
        rate_used=rate,
        exposure_amount=exposure_amount,
        exposure_currency=exposure_currency,
    )
    if existing:
        fx_doc = frappe.get_doc("FX Risk Log", str(existing))
        fx_doc.update(doc_fields)
        fx_doc.save(ignore_permissions=True)
    else:
        fx_doc = frappe.get_doc(doc_fields).insert(ignore_permissions=True)
    return fx_doc.name
