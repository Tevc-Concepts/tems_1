// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Passenger Manifest", {
    refresh(frm) {
        frm.set_query("vehicle", () => ({ filters: { vehicle_type: ["in", ["Passenger"]] } }));
        frm.set_query("trip", () => ({ filters: {} }));
    },
});
