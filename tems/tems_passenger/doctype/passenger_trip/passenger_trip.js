// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Passenger Trip", {
    refresh(frm) {
        // filter Vehicle to Passenger
        frm.set_query("vehicle", () => ({ filters: { vehicle_type: ["in", ["Passenger"]] } }));
        // if linked operation plan present, ensure mode is Passenger
        if (frm.doc.operation_plan) {
            frappe.db.get_value("Operation Plan", frm.doc.operation_plan, ["operation_mode"]).then(r => {
                const mode = r?.message?.operation_mode;
                if (mode && mode !== "Passenger") {
                    frappe.msgprint({
                        message: __("Selected Operation Plan is not Passenger mode."),
                        indicator: "red"
                    });
                }
            });
        }
    },
});
