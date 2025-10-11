// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cargo Delivery Log", {
    refresh(frm) {
        frm.set_query("consignment", () => ({ filters: {} }));
        if (!frm.doc.timestamp) {
            frm.set_value("timestamp", frappe.datetime.now_datetime());
        }
    },
});
