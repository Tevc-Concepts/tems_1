"""Scheduled task implementations for TEMS Finance."""
from __future__ import annotations

import frappe
from frappe.utils import nowdate
from .handlers import compute_profitability_for_all


def _log(msg: str) -> None:
    try:
        frappe.logger("tems").info(msg)
    except Exception:
        print(f"[TEMS][Finance] {msg}")


def update_vehicle_profitability() -> None:
    compute_profitability_for_all()
    _log("Vehicle profitability recomputed")


def daily_interest_compute() -> None:
    """Apply simple daily interest accrual on active Lease Loan schedules not paid.
    (Placeholder: interest_component = remaining_principal * rate/365)
    """
    loans = frappe.get_all("Lease Loan", filters={"status": "Active"}, fields=["name", "rate", "principal"])
    for loan in loans:
        loan_name = loan.name  # type: ignore[attr-defined]
        loan_rate = float(loan.rate or 0)  # type: ignore[attr-defined]
        loan_principal = float(loan.principal or 0)  # type: ignore[attr-defined]
        if not loan_rate or not loan_principal:
            continue
        interest = loan_principal * loan_rate / 100 / 365
        frappe.get_doc({  # type: ignore[call-arg]
            "doctype": "Cost And Revenue Ledger",
            "date": nowdate(),
            "vehicle": frappe.db.get_value("Lease Loan", loan_name, "vehicle"),
            "type": "Cost",
            "amount": interest,
            "notes": f"Interest accrual for loan {loan_name}",
        }).insert(ignore_permissions=True)  # type: ignore[attr-defined]
    _log(f"Accrued interest for {len(loans)} active loans")


def update_fx_rates() -> None:
    """Fetch FX rates from configured source (placeholder) and log FX Risk snapshot if exposure exists."""
    # Placeholder: just create an FX Risk Log entry for demonstration for USD/NGN
    if not frappe.db.exists("FX Risk Log", {"date": nowdate(), "currency_pair": "USD/NGN"}):
        try:
            frappe.get_doc({  # type: ignore[call-arg]
                "doctype": "FX Risk Log",
                "date": nowdate(),
                "currency_pair": "USD/NGN",
                "exposure_amount": 0,
                "exposure_currency": "USD",
                "rate_used": 0,
                "hedge_action": "None",
                "notes": "Placeholder daily FX rate capture",
            }).insert(ignore_permissions=True)  # type: ignore[attr-defined]
        except Exception:
            _log("FX rates update failed (placeholder)")
            return
    _log("FX rates update placeholder executed")
