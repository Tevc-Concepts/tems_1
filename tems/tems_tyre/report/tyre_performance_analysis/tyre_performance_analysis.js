// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

frappe.query_reports["Tyre Performance Analysis"] = {
	"filters": [
		// Filters:
		{
			fieldname: "vehicle",
			label: __("Vehicle"),
			fieldtype: "Link",
			options: "Vehicle",
			default: frappe.defaults.get_user_default("Vehicle"),
		},
		{
			fieldname: "report_date",
			label: __("Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "brand",
			label: __("Brand"),
			fieldtype: "Data"
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: [
				{ value: "In Stock", label: __("In Stock") },
				{ value: "Installed", label: __("Installed") },
				{ value: "In Repair", label: __("In Repair") },
				{ value: "Retread", label: __("Retread") },
				{ value: "Disposed", label: __("Disposed") },
			],
		},
	]
};
