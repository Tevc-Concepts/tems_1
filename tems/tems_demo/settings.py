"""Configuration for TEMS demo data generation.

Adjust targets and caps without touching core seeding logic.
"""

TARGETS = {
    "Item": 25,
    "Purchase Order": 25,
    "Stock Entry": 20,
    "Asset": 20,
    "Employee": 30,
    "Vehicle": 20,
    "Operation Plan": 25,
    "Journey Plan": 20,
    "Incident Report": 20,
    "Risk Assessment": 20,
    "Governance Policy": 20,
    "Compliance Obligation": 20,
    "Strategic Goal": 10,
    "Leadership Meeting": 10,
    "Governance Meeting": 10,
    "Compliance Audit": 20,
    "Informal Operator Profile": 20,
    "KPI Config": 20,
    "Report Subscription": 20,
    "Spot Check": 15,
}

CEILINGS = {
    "Movement Log": 120,
    "Purchase Order": 80,
}

PRUNING = {
    "enable_movement_log_prune": True,
    "enable_purchase_order_prune": True,
    # Allow pruning (cancel+delete) of submitted Purchase Orders when True
    "purchase_order_prune_cancel_submitted": True,
}

# Strict mode: if True, any doctype whose count exceeds its TARGET will be
# automatically rebalanced down to TARGET (draft docs only unless a specific
# allow_cancel flag is provided in REBALANCE_BEHAVIOR)
STRICT_MODE = True

REBALANCE_BEHAVIOR = {
    # Allow cancel of submitted Purchase Orders during strict rebalance
    "Purchase Order": {"cancel_submitted": True},
    # Other doctypes can be added here with per-doctype rules
}

BACKUP_DIR = "demo_backups"  # folder under site for JSON backups before destructive actions

DASHBOARD_MD = "demo_dashboard.md"
DASHBOARD_HTML = "demo_dashboard.html"

def get_target(doctype: str, default: int = 0) -> int:
    return TARGETS.get(doctype, default)

def get_ceiling(doctype: str, default: int | None = None):
    return CEILINGS.get(doctype, default)
