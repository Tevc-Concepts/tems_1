"""Scheduled task stubs for TEMS Safety (no-op)."""
from __future__ import annotations

import frappe


def _log(msg: str) -> None:
    try:
        frappe.logger("tems").info(msg)
    except Exception:
        print(f"[TEMS][Safety] {msg}")


def aggregate_emissions_daily() -> None:
    _log("safety.aggregate_emissions_daily noop")


def aggregate_emissions_monthly() -> None:
    _log("safety.aggregate_emissions_monthly noop")
