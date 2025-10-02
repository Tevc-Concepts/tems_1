app_name = "tems"
app_title = "TEMS"
app_publisher = "Tevc Concepts Limited"
app_description = "Transport Excellence Management System customizations"
app_email = "code@tevcng.com"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_version = "0.1.0"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "tems",
# 		"logo": "/assets/tems/logo.png",
# 		"title": "Transport Enterprise Management System",
# 		"route": "/tems",
# 		"has_permission": "tems.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/tems/css/tems_theme.css"
app_include_js = "/assets/tems/js/tems_desk.js"

# include js, css files in header of web template
web_include_css = "/assets/tems/css/tems_theme.css"
web_include_js = "/assets/tems/js/tems_web.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tems/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "tems/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "tems.utils.jinja_methods",
# 	"filters": "tems.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "tems.install.before_install"
# after_install = "tems.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "tems.uninstall.before_uninstall"
# after_uninstall = "tems.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "tems.utils.before_app_install"
# after_app_install = "tems.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "tems.utils.before_app_uninstall"
# after_app_uninstall = "tems.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tems.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Fixtures

# Fixtures ensure roles/workspaces/number cards ship with the app (export-fixtures)
fixtures = [
	{"dt": "Role", "filters": [["name", "in", [
		"TEMS Executive",
		"Operations Manager",
		"Operations Officer",
		"Fleet Manager",
		"Fleet Officer",
		"Safety Officer",
		"Safety Manager",
		"Driver",
		"Informal Operator",
		"Border Agent",
		"Community Leader",
		"Maintenance Tech",
		"Finance Manager",
		"Finance Officer",
		"Analyst",
		"HR"
	]]]},
	{"dt": "Number Card", "filters": [["module", "in", ["TEMS Governance", "TEMS Operations", "TEMS People", "TEMS Fleet", "TEMS Safety", "TEMS Trade", "TEMS Informal", "TEMS Climate", "TEMS Finance", "TEMS CRM", "TEMS Supply Chain", "TEMS Documents"]]]},
    {"dt": "Client Script", "filters": [["module", "in", ["TEMS Governance", "TEMS Operations", "TEMS People", "TEMS Fleet", "TEMS Safety", "TEMS Trade", "TEMS Informal", "TEMS Climate", "TEMS Finance", "TEMS CRM", "TEMS Supply Chain", "TEMS Documents"]]]},
	{"dt": "Workflow", "filters": [["document_type", "in", ["Safety Incident"]]]},
	"Custom Field",
	"Print Format",
	"Report",
	"Dashboard",
    "Dashboard Chart",
    "Email Template",
    "Notification",
    "Scheduled Job Type",
    "Tag",
    # Intentionally exclude "Workspace" fixtures; use module-based JSON in tems_*/workspace/* instead
    ]


# Document Events
# ---------------
# Hook on document methods and events


# -------------------------------
# Document Events
# -------------------------------
doc_events = {
    # Vehicle Updates (ERPNext core doctype, extended in TEMS)
    "Vehicle": {
        "on_update": "tems.tems_fleet.handlers.update_vehicle_profitability",
        "on_submit": "tems.tems_fleet.handlers.validate_vehicle_assets"
    },

    # Asset Updates (ERPNext core doctype, extended in TEMS)
    "Asset": {
        "on_update": "tems.tems_fleet.handlers.rollup_asset_cost_to_vehicle",
        "on_trash": "tems.tems_fleet.handlers.prevent_asset_without_vehicle"
    },

    # Operations Module
    "Operation Plan": {
        "before_submit": "tems.tems_operations.handlers.ensure_vehicle_available",
        "on_submit": "tems.tems_operations.handlers.log_movement_start"
    },
    "Movement Log": {
        "on_update": "tems.tems_operations.handlers.update_vehicle_status"
    },
    "Trip Allocation": {
        "before_insert": "tems.tems_operations.handlers.ensure_driver_vehicle_valid"
    },
    "Operations Event": {
        "after_insert": "tems.tems_operations.handlers.publish_operations_event",
        "on_update": "tems.tems_operations.handlers.publish_operations_event"
    },
    "SOS Event": {
        "after_insert": "tems.tems_operations.handlers.publish_sos_event",
        "on_update": "tems.tems_operations.handlers.publish_sos_event"
    },

    # Finance Module
    "Cost And Revenue Ledger": {
        "on_update": "tems.tems_finance.handlers.recalculate_vehicle_profitability"
    },

    # Safety Module
    "Incident Report": {
        "on_submit": "tems.tems_safety.handlers.log_incident_against_vehicle"
    },
    "Risk Assessment": {
        "before_submit": "tems.tems_safety.handlers.validate_vehicle_risk"
    },

    # People (HRMS Extension)
    "Employee": {
        "on_update": "tems.tems_people.handlers.check_driver_vehicle_assignment"
    },

    # Supply Chain
    "Procurement Order": {
        "on_submit": "tems.tems_supply_chain.handlers.link_spare_parts_to_asset"
    },

    # Trade
    "Border Crossing": {
        "on_submit": "tems.tems_trade.handlers.log_vehicle_crossing"
    },

    # CRM
    "Order": {
        "on_submit": "tems.tems_crm.handlers.link_order_to_vehicle"
    },

    # Climate / ESG
    "Climate Alert": {
        "on_update": "tems.tems_climate.handlers.apply_weather_to_vehicle"
    },
    "Emission Log": {
        "on_update": "tems.tems_climate.handlers.rollup_emission_to_vehicle"
    },

    # Governance
    "Policy": {
        "on_update": "tems.tems_governance.handlers.apply_policy_to_vehicle"
    },

    # Governance domain logs (per GovernanceAgent)
    "Spot Check": {
        "on_update": "tems.tems_governance.handlers.on_spot_check",
        "on_submit": "tems.tems_governance.handlers.on_spot_check"
    },
    "Compliance Audit": {
        "on_update": "tems.tems_governance.handlers.on_compliance_audit",
        "on_submit": "tems.tems_governance.handlers.on_compliance_audit"
    },

    # Documents
    "Compliance Document": {
        "on_update": "tems.tems_documents.handlers.validate_vehicle_document"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "all": [
        "tems.tems_operations.tasks.sync_vehicle_status",
        "tems.tems_fleet.tasks.sync_asset_costs",
        "tems.tems_finance.tasks.update_vehicle_profitability"
    ],
	"daily": [
		"tems.tems_operations.tasks.daily_sync_checkpoint",
    	"tems.tems_finance.tasks.daily_interest_compute",
    	"tems.tems_governance.api.notify_upcoming_reviews_and_obligations",
		"tems.tems_governance.tasks.notify_overdue_investigations",
		"tems.tems_safety.tasks.aggregate_emissions_daily",
        "tems.tems_operations.tasks.generate_daily_operations_report",
        "tems.tems_operations.tasks.validate_driver_vehicle_assignments",
        "tems.tems_finance.tasks.update_fx_rates"
	],
	"cron": {
		"0 1 * * *": ["tems.tasks.compute_nightly_jobs"],
		"0 2 * * *": ["tems.tasks.update_tariffs"],
		"0 3 * * 1": ["tems.tasks.rotate_rosca"],
	},
	"hourly": [
		"tems.tems_operations.tasks.hourly_sync_checkpoint",
        "tems.tems_operations.tasks.check_vehicle_availability"
	],
	"weekly": [
		"tems.tems_operations.tasks.weekly_sync_checkpoint"
	],
	"monthly": [
		"tems.tems_operations.tasks.monthly_sync_checkpoint",
		"tems.tems_safety.tasks.aggregate_emissions_monthly"
	],
}

# Testing
# -------

# before_tests = "tems.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tems.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tems.task.get_dashboard_data"
# }
# -------------------------------
# Override ERPNext Doctypes (Optional, to extend Vehicle/Asset behavior)
# -------------------------------
# No overrides registered currently. Keep disabled to avoid import errors until implemented.
# override_doctype_class = {
#     "Asset": "tems.tems_fleet.overrides.CustomAsset",
#     "Vehicle": "tems.tems_fleet.overrides.CustomVehicle"
# }



# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["tems.utils.before_request"]
# after_request = ["tems.utils.after_request"]

# Job Events
# ----------
# before_job = ["tems.utils.before_job"]
# after_job = ["tems.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"tems.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

