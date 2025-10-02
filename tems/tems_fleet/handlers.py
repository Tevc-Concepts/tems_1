from __future__ import annotations

import frappe


def update_vehicle_profitability(doc, method=None):
    frappe.logger("tems").info("Vehicle updated: %s", getattr(doc, "name", None))


def validate_vehicle_assets(doc, method=None):
    # Ensure vehicle has attached assets if required; placeholder
    return


def rollup_asset_cost_to_vehicle(doc, method=None):
    # Placeholder for rolling up Asset costs to Vehicle-level metrics
    return


def prevent_asset_without_vehicle(doc, method=None):
    # Ensure assets remain linked properly; placeholder
    return
