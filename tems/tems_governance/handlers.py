import frappe


def on_spot_check(doc, method=None):
    # Broadcast governance log for leadership oversight
    frappe.publish_realtime(
        event="governance_event",
        message={
            "type": "spot_check",
            "name": getattr(doc, "name", None),
            "inspector": getattr(doc, "inspector", None),
            "status": getattr(doc, "status", None),
        },
    )


def on_compliance_audit(doc, method=None):
    frappe.publish_realtime(
        event="governance_event",
        message={
            "type": "compliance_audit",
            "name": getattr(doc, "name", None),
            "severity": getattr(doc, "severity", None),
            "status": getattr(doc, "status", None),
        },
    )


def apply_policy_to_vehicle(doc, method=None):
    # Placeholder to satisfy hook; real logic can propagate policy changes
    frappe.logger().info("Governance policy updated: %s", getattr(doc, "name", None))
