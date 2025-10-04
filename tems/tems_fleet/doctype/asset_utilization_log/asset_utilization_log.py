import frappe
from frappe.model.document import Document


class AssetUtilizationLog(Document):
    """Track point-in-time utilization of an Asset (hours, linkage to Vehicle)."""

    def validate(self):
        # Basic sanity checks
        # type: ignore[attr-defined]
        if self.utilization_hours is not None and self.utilization_hours < 0:  # noqa: E501
            frappe.throw("Utilization hours cannot be negative")

        # Optional: ensure either asset or vehicle is provided (at least one context)
        # type: ignore[attr-defined]
        if not (self.asset or self.vehicle):  # noqa: E501
            frappe.throw("Provide at least an Asset or a Vehicle reference")

    def after_insert(self):
        # Roll up utilization to Asset and Vehicle custom fields
        try:
            # type: ignore[attr-defined]
            hours = self.utilization_hours or 0
            if self.asset:  # noqa: E501
                frappe.db.sql(
                    """
                    UPDATE `tabAsset`
                    SET total_utilization_hours = COALESCE(total_utilization_hours, 0) + %(h)s
                    WHERE name = %(asset)s
                    """,
                    {"h": hours, "asset": self.asset},
                )
            if self.vehicle:  # type: ignore[attr-defined]
                # Uptime hours: simplistic assumption increment; downtime derivation left for future
                frappe.db.sql(
                    """
                    UPDATE `tabVehicle`
                    SET uptime_hours = COALESCE(uptime_hours, 0) + %(h)s
                    WHERE name = %(veh)s
                    """,
                    {"h": hours, "veh": self.vehicle},
                )
            frappe.db.commit()
        except Exception as e:  # pragma: no cover
            frappe.logger("tems").error(f"AssetUtilizationLog rollup failed: {e}")
