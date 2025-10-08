from __future__ import annotations
import frappe
from typing import Callable, Iterable
import traceback


def ensure_min_records(
    *,
    doctype: str,
    target: int,
    make_doc: Callable[[int], dict],
    context: dict,
    context_key: str,
    ignore_mandatory: bool = True,
    allow_existing: bool = True,
) -> list[str]:
    """Generic utility to guarantee at least `target` records for a DocType.

    - Skips gracefully if DocType not installed.
    - Collects existing records (up to target) if allow_existing=True.
    - Uses `make_doc(i)` to produce each new document dict.
    - Adds name list to context[context_key].
    - Returns list of record names.
    """
    if not frappe.db.exists("DocType", doctype):
        missing = context.setdefault("_missing_doctypes", set())
        missing.add(doctype)
        return []
    bucket = context.setdefault(context_key, [])
    # Add existing
    if allow_existing and not bucket:
        existing = frappe.get_all(doctype, pluck="name", limit=target)
        bucket.extend(existing)
    idx = 0
    while len(bucket) < target and idx < target * 2:  # safety cap
        idx += 1
        data = make_doc(idx)
        try:
            doc = frappe.get_doc(data)
            doc.insert(ignore_permissions=True, ignore_mandatory=ignore_mandatory)
            bucket.append(doc.name)
        except Exception:  # pragma: no cover - logging centralized elsewhere
            frappe.db.rollback()
            continue
    return bucket


def summarize_missing(context: dict) -> list[str]:
    missing = context.get("_missing_doctypes") or []
    return sorted(missing)


def log_error(context: dict, category: str, exc: Exception, *, capture_tb: bool = False):
    errs = context.setdefault("_errors", [])
    if capture_tb:
        tb = traceback.format_exc(limit=6)
        errs.append(f"{category}: {exc} | TB: {tb.splitlines()[-1]}")
    else:
        errs.append(f"{category}: {exc}")


def log(context: dict, message: str):
    msgs = context.setdefault("_log", [])
    msgs.append(message)

def write_error_file(context: dict):
    if not context.get("_errors"):
        return
    import frappe
    from frappe.utils import now_datetime
    path = frappe.get_site_path("demo_data_errors.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Demo Data Errors\n\n")
        f.write(f"Generated: {now_datetime()}\n\n")
        for line in context["_errors"][-200:]:
            f.write(f"- {line}\n")


def write_debug_json(filename: str, payload: dict):
    """Write a JSON debug artifact into the site path."""
    import json
    path = frappe.get_site_path(filename)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, default=str)
    except Exception:
        pass


def dump_recent_errors(limit: int = 50):  # bench execute entrypoint if needed
    ctx = frappe._dict()
    path = frappe.get_site_path("demo_data_errors.md")
    out = []
    if frappe.utils.file_manager.os.path.exists(path):  # type: ignore[attr-defined]
        with open(path, "r", encoding="utf-8") as fh:
            lines = [l.strip() for l in fh.readlines() if l.startswith('- ')]
            out = lines[-limit:]
    return {"recent": out}
