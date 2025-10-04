import frappe


def after_insert(doc, method=None):
    # Stub: enqueue predictive maintenance recalculation
    pass


def on_update(doc, method=None):
    # Stub: update uptime/downtime rollups
    pass
