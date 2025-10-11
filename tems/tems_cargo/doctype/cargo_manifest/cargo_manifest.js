// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cargo Manifest", {
    refresh(frm) {
        frm.set_query("operation_plan", () => ({ filters: { operation_mode: "Cargo" } }));
        frm.set_query("vehicle", () => ({ filters: { vehicle_type: ["in", ["Cargo"]] } }));
    },
});
