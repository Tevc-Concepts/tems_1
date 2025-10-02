"""Scheduled task stubs for TEMS Governance (no-op)."""
from __future__ import annotations

import frappe


def _log(msg: str) -> None:
    try:
        frappe.logger("tems").info(msg)
    except Exception:
        print(f"[TEMS][Governance] {msg}")


def notify_overdue_investigations() -> None:
    _log("governance.notify_overdue_investigations noop")
