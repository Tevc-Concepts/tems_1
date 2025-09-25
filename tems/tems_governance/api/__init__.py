from __future__ import annotations

import frappe
from frappe.utils import nowdate, add_days, getdate, formatdate


@frappe.whitelist()
def next_reviews(within_days: int = 30):
	days = int(within_days)
	today = getdate(nowdate())
	cutoff = add_days(today, days)
	return frappe.get_all(
		"Governance Policy",
		filters={"next_review_date": ["between", [formatdate(today), formatdate(cutoff)]]},
		fields=["name", "title", "owner_employee", "next_review_date", "status"],
		order_by="next_review_date asc",
	)


def notify_upcoming_reviews_and_obligations():
	policies = next_reviews(30)
	for p in policies:
		if p.get("owner_employee"):
			_notify_employee(p["owner_employee"], f"Policy '{p['title']}' review due on {p['next_review_date']}")

	today = getdate(nowdate())
	cutoff = add_days(today, 14)
	obligations = frappe.get_all(
		"Compliance Obligation",
		filters={"next_due_date": ["between", [formatdate(today), formatdate(cutoff)]], "status": ["in", ["Open", "Submitted"]]},
		fields=["name", "title", "next_due_date", "status"],
		order_by="next_due_date asc",
	)
	for o in obligations:
		for user in _system_manager_users():
			frappe.publish_realtime(
				event="governance_notice",
				message={"type": "obligation_due", "title": o["title"], "due": o["next_due_date"]},
				user=user,
			)


def _notify_employee(employee: str, message: str):
	user = frappe.db.get_value("Employee", employee, "user_id")
	if user:
		frappe.publish_realtime(event="governance_notice", message={"type": "policy_review", "message": message}, user=user)


def _system_manager_users():
	return [x[0] for x in frappe.db.sql("""
		select distinct tabUser.name
		from `tabHas Role` hr
		join `tabUser` on hr.parent = tabUser.name
		where hr.role = 'System Manager' and tabUser.enabled = 1
	""")]
