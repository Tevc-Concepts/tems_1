import frappe
from typing import Iterable


def get_tems_settings():
    """Fetch cached TEMS Settings single doc (or None)."""
    try:
        return frappe.get_cached_doc("TEMS Settings")
    except Exception:
        return None


def _get_users_for_roles(roles: Iterable[str]) -> list[str]:
    users: set[str] = set()
    for r in roles:
        rows = frappe.get_all("Has Role", filters={"role": r}, fields=["parent"])
        for d in rows:
            users.add(d.get("parent"))
    return [u for u in users if u]


def apply_incident_folder_permissions(entity_name: str):
    """
    Share the Drive folder (Drive File entity) with users in configured roles.
    Uses Drive Permission doctype (row per user + flags).
    Safe no-op if settings missing or entity invalid.
    """
    settings = get_tems_settings()
    if not settings:
        return
    share_table = getattr(settings, "share_roles", None) or []
    share_roles = [getattr(row, "role", None) for row in share_table]
    share_roles = [r for r in share_roles if r]
    if not share_roles:
        return

    exists = frappe.db.exists("Drive File", {"name": entity_name, "is_group": 1, "is_active": 1})
    if not exists:
        return

    users = _get_users_for_roles(share_roles)
    if not users:
        return

    flags = {
        "read": int(bool(getattr(settings, "grant_read", 0))),
        "upload": int(bool(getattr(settings, "grant_upload", 0))),
        "write": int(bool(getattr(settings, "grant_write", 0))),
        "share": int(bool(getattr(settings, "grant_share", 0))),
        "comment": 1,
    }

    for user in users:
        try:
            # idempotent: if exists, update; else insert
            existing = frappe.db.exists("Drive Permission", {"entity": entity_name, "user": user})
            if existing:
                frappe.db.set_value("Drive Permission", existing, flags)
            else:
                doc = frappe.get_doc(
                    {
                        "doctype": "Drive Permission",
                        "entity": entity_name,
                        "user": user,
                        **flags,
                    }
                )
                doc.insert(ignore_permissions=True)
        except Exception:
            frappe.log_error(
                f"Failed to set Drive Permission for {user} on {entity_name}",
                "TEMS Drive Integration",
            )
