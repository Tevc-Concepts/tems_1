// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

frappe.query_reports["Fleet Tyre Metrics"] = {
	"filters": [
		{
			fieldname: "vehicle",
			label: __("Vehicle"),
			fieldtype: "Link",
			options: "Vehicle",
			default: frappe.defaults.get_user_default("Vehicle"),
		},
		{
			fieldname: "brand",
			label: __("Brand"),
			fieldtype: "Data"
		},
	]
};
