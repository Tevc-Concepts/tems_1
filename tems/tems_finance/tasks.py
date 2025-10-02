"""Scheduled task stubs for TEMS Finance (no-op)."""
from __future__ import annotations

import frappe


def _log(msg: str) -> None:
    try:
        frappe.logger("tems").info(msg)
    except Exception:
        print(f"[TEMS][Finance] {msg}")


def update_vehicle_profitability() -> None:
    _log("finance.update_vehicle_profitability noop")


def daily_interest_compute() -> None:
    _log("finance.daily_interest_compute noop")


def update_fx_rates() -> None:
    _log("finance.update_fx_rates noop")
