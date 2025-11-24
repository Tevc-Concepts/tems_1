# Copyright (c) 2025, TEMS and contributors
# For license information, please see license.txt

# import frappe
import frappe
from datetime import datetime, date
from typing import Any
from frappe.utils import now_datetime, get_datetime
from frappe.model.document import Document
from tems.tems_main.api.drive_integration import get_tems_settings, apply_incident_folder_permissions

class SafetyIncident(Document):
    def validate(self):
        # incident_date cannot be in the future
        incident_date_val: Any = self.get("incident_date")
        if isinstance(incident_date_val, (str, datetime, date)):
            try:
                dt = get_datetime(incident_date_val)
                if dt and dt > now_datetime():
                    frappe.throw("Incident Date & Time cannot be in the future")
            except Exception:
                pass

        # major/critical must have a vehicle
        sev_val: Any = self.get("severity")
        severity = sev_val.lower() if isinstance(sev_val, str) else ""
        if severity in {"major", "critical"} and not self.get("vehicle"):
            frappe.throw("Vehicle is required for Major or Critical incidents")

        # ensure status is one of allowed values
        allowed = {"Open", "Under Investigation", "Closed"}
        status_val: Any = self.get("status")
        if isinstance(status_val, str) and status_val not in allowed:
            frappe.throw("Invalid status value")

    def before_submit(self):
        # Do not allow submitting with status Closed without description
        desc = self.get("description") or ""
        if not isinstance(desc, str):
            desc = str(desc)
        if (self.get("status") == "Closed") and not desc.strip():
            frappe.throw("Provide a description before closing the incident")

    def after_insert(self):
        # Create a Drive folder for this incident if Drive is installed and user has access
        try:
            if frappe.get_installed_apps() and "drive" in frappe.get_installed_apps():
                # Use TEMS Settings if available
                settings = get_tems_settings()
                team = None
                parent = None
                if settings:
                    team = getattr(settings, "default_drive_team", None)
                    parent = getattr(settings, "incident_parent_folder", None)
                if not team:
                    teams = frappe.get_all("Drive Team", pluck="name", limit=1)
                    team = teams[0] if teams else None
                if team:
                    folder = frappe.call(
                        "drive.api.files.create_folder",
                        team=team,
                        title=f"Incident {self.name}",
                        personal=False,
                        parent=parent,
                    )
                    if folder and folder.get("name"):
                        self.db_set("attachments_folder", folder.get("name"), update_modified=False)
                        # Apply permissions from settings
                        apply_incident_folder_permissions(folder.get("name"))
        except Exception:
            frappe.log_error("Failed to create or configure Drive folder for Safety Incident", "TEMS Safety")

        # Auto-create an Issue and notify Safety Managers for critical incidents
        sev_val: Any = self.get("severity")
        sev = sev_val.lower() if isinstance(sev_val, str) else ""
        if sev == "critical":
            try:
                issue = frappe.get_doc({
                    "doctype": "Issue",
                    "subject": f"Critical Safety Incident {self.name}",
                    "description": (self.get("description") or f"Critical incident created: {self.name}"),
                })
                issue.insert(ignore_permissions=True)
            except Exception:
                frappe.log_error("Failed to create Issue for critical Safety Incident", "TEMS Safety")

            # Notify Safety Manager role users
            try:
                users = [d.parent for d in frappe.get_all("Has Role", filters={"role": "Safety Manager"}, fields=["parent"])]
                if users:
                    frappe.sendmail(
                        recipients=users,
                        subject=f"Critical Safety Incident {self.name}",
                        message=f"A critical safety incident has been reported: <b>{self.name}</b>.",
                    )
            except Exception:
                frappe.log_error("Failed to notify Safety Managers for critical Safety Incident", "TEMS Safety")
