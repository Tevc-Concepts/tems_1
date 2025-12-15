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

# Fixtures for roles, workspaces, custom fields, etc. (already present)

"""NOTE: A unified doc_events mapping is defined later below. This early placeholder is removed during merge."""

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
home_page = "index"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Website settings
website_route_rules = [
    {"from_route": "/driver/<path:app_path>", "to_route": "driver"},
    {"from_route": "/operations/<path:app_path>", "to_route": "operations"},
    {"from_route": "/safety/<path:app_path>", "to_route": "safety"},
    {"from_route": "/fleet/<path:app_path>", "to_route": "fleet"},
]

# Pages that don't require login
has_web_view = True

# Whitelist methods for guest access
override_whitelisted_methods = {
    "tems.tems.www.index.get_live_metrics": "tems.tems.www.index.get_live_metrics"
}

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
    # Temporarily trimming fixture list to isolate migration failure (will restore after cleanup)
    # {"dt": "Number Card", "filters": ...},
    # {"dt": "Client Script", "filters": ...},
    # {"dt": "Workflow", "filters": ...},
    # "Custom Field",
    # "Print Format",
    # "Dashboard",
    # "Dashboard Chart",
    # "Email Template",
    # "Notification",
    # "Scheduled Job Type",
    # "Tag",
]

doc_events = {
    # Core Fleet assets
    "Vehicle": {
        "on_update": ["tems.tems_fleet.handlers.update_vehicle_profitability",
                      "tems.tems_fleet.api.vehicle.on_vehicle_update"],
        "on_submit": "tems.tems_fleet.handlers.validate_vehicle_assets"
    },
    "Asset": {
        "after_insert": "tems.tems_fleet.api.asset.after_insert",
        "on_update": "tems.tems_fleet.handlers.rollup_asset_cost_to_vehicle",
        "on_trash": "tems.tems_fleet.handlers.prevent_asset_without_vehicle"
    },
    "Maintenance Work Order": {
        "after_insert": "tems.tems_fleet.api.maintenance_work_order.after_insert",
        "on_update": "tems.tems_fleet.api.maintenance_work_order.on_update"
    },
    # Operations
    "Operation Plan": {
        "validate": "tems.tems_operations.handlers.validate_operation_plan",
        "before_submit": "tems.tems_operations.handlers.ensure_vehicle_available",
        "on_submit": "tems.tems_operations.handlers.log_movement_start"
    },
    "Movement Log": {"on_update": "tems.tems_operations.handlers.update_vehicle_status"},
    "Trip Allocation": {"before_insert": "tems.tems_operations.handlers.ensure_driver_vehicle_valid"},
    "Operations Event": {
        "after_insert": "tems.tems_operations.handlers.publish_operations_event",
        "on_update": "tems.tems_operations.handlers.publish_operations_event"
    },
    "SOS Event": {
        "after_insert": "tems.tems_operations.handlers.publish_sos_event",
        "on_update": "tems.tems_operations.handlers.publish_sos_event"
    },
    # Finance
    "Cost And Revenue Ledger": {"on_update": "tems.tems_finance.handlers.recalculate_vehicle_profitability"},
    # Safety
    "Journey Plan": {
        "validate": "tems.tems_safety.api.journey_plan.validate_driver_competence",
        "after_insert": "tems.tems_safety.api.journey_plan.after_insert"
    },
    "Incident Report": {
        "after_insert": "tems.tems_safety.api.incident_report.after_insert",
        "on_submit": "tems.tems_safety.handlers.log_incident_against_vehicle"
    },
    "Risk Assessment": {"before_submit": "tems.tems_safety.handlers.validate_vehicle_risk"},
    # People
    "Employee": {"on_update": "tems.tems_people.handlers.check_driver_vehicle_assignment"},
    # Supply Chain
    "Procurement Order": {"on_submit": "tems.tems_supply_chain.handlers.link_spare_parts_to_asset"},
    # Trade
    "Border Crossing": {"on_submit": "tems.tems_trade.handlers.log_vehicle_crossing"},
    # CRM
    "Order": {"on_submit": "tems.tems_crm.handlers.link_order_to_vehicle"},
    # Climate
    "Climate Alert": {"on_update": "tems.tems_climate.handlers.apply_weather_to_vehicle"},
    "Emission Log": {"on_update": "tems.tems_climate.handlers.rollup_emission_to_vehicle"},
    # Governance
    "Policy": {"on_update": "tems.tems_governance.handlers.apply_policy_to_vehicle"},
    "Spot Check": {
        "on_update": "tems.tems_governance.handlers.on_spot_check",
        "on_submit": "tems.tems_governance.handlers.on_spot_check"
    },
    "Compliance Audit": {
        "on_update": "tems.tems_governance.handlers.on_compliance_audit",
        "on_submit": "tems.tems_governance.handlers.on_compliance_audit"
    },
    # Documents
    "Compliance Document": {"on_update": "tems.tems_documents.handlers.validate_vehicle_document"},
    # Cargo & Passenger
    "Cargo Consignment": {
        "validate": "tems.tems_cargo.handlers.consignment.validate_vehicle_type"
    },
    "Passenger Trip": {
        "validate": "tems.tems_passenger.handlers.trip.validate_vehicle_type"
    },
    # Tyre Management
    "Tyre Installation Log": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_install",
        "on_update": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_removal"
    },
    "Tyre Inspection Log": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_inspection"
    },
    "Tyre Disposal Log": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_disposal"
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
        "tems.tems_fleet.tasks.compute_predictive_maintenance",  # new stub daily predictive maintenance rollup
        "tems.tems_operations.tasks.generate_daily_operations_report",
        "tems.tems_operations.tasks.validate_driver_vehicle_assignments",
        "tems.tems_finance.tasks.update_fx_rates",
        "tems.tems_people.tasks.remind_expiring_driver_docs",
        "tems.tems_people.tasks.remind_expiring_medical_clearances",
        "tems.tems_people.tasks.auto_deactivate_drivers",
        "tems.tems_supply_chain.tasks.low_stock_alert",
        # TEMS AI Module scheduled tasks
        "tems.tems_ai.tasks.update_model_performance_metrics",
        # TEMS Tyre Module scheduled tasks
        "tems.tems_tyre.tasks.update_tyre_health_scores",
        "tems.tems_tyre.tasks.predict_replacement_schedule",
        "tems.tems_tyre.tasks.sync_tyre_costs_to_finance"
	],
	"cron": {
		"0 1 * * *": ["tems.tasks.compute_nightly_jobs"],
		"0 1 * * 1": ["tems.tems_ai.tasks.retrain_models_weekly"],  # AI: Monday 01:00 AM
		"0 2 * * *": ["tems.tasks.update_tariffs", "tems.tems_ai.tasks.generate_daily_insights"],  # AI: 02:00 AM
		"0 3 * * 1": ["tems.tasks.rotate_rosca"],
		"0 3 * * 0": ["tems.tems_ai.tasks.cleanup_old_insights"],  # AI: Sunday 03:00 AM
		"0 5 * * *": ["tems.tems_ai.tasks.calculate_driver_risk_scores"],  # AI: 05:00 AM
		"0 6 * * *": ["tems.tems_ai.tasks.generate_fleet_maintenance_predictions"],  # AI: 06:00 AM
		"0 7 * * *": ["tems.tems_ai.tasks.forecast_financial_metrics"],  # AI: 07:00 AM
        "0 8 * * *": ["tems.tems_ai.tasks.send_daily_ai_summary"], # AI: 08:00 AM
	},
	"hourly": [
		"tems.tems_operations.tasks.hourly_sync_checkpoint",
        "tems.tems_operations.tasks.check_vehicle_availability",
        "tems.tems_tyre.tasks.monitor_tyre_sensors",
        "tems.tems_ai.tasks.evaluate_alerts_hourly"  # AI: Hourly alert evaluation
	],
	"weekly": [
		"tems.tems_operations.tasks.weekly_sync_checkpoint",
                "tems.tems_tyre.tasks.analyze_fleet_tyre_performance" # Tyre: Weekly performance analysis
	],
	"monthly": [
		"tems.tems_operations.tasks.monthly_sync_checkpoint",
		"tems.tems_safety.tasks.aggregate_emissions_monthly",
        "tems.tems_tyre.tasks.cleanup_old_sensor_data" # Tyre: Monthly sensor data cleanup
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

