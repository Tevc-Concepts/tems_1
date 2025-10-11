// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cargo Consignment", {
    refresh(frm) {
        // filter Operation Plan to Cargo mode
        frm.set_query("operation_plan", () => ({
            filters: { operation_mode: "Cargo" },
        }));
        // filter Vehicle to Cargo
        frm.set_query("vehicle", () => ({
            filters: { vehicle_type: ["in", ["Cargo"]] },
        }));
    },
});
