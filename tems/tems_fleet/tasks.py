"""Scheduled task stubs for TEMS Fleet (no-op)."""
from __future__ import annotations

import frappe


def _log(msg: str) -> None:
    try:
        frappe.logger("tems").info(msg)
    except Exception:
        print(f"[TEMS][Fleet] {msg}")


def sync_asset_costs() -> None:
    _log("fleet.sync_asset_costs noop")
