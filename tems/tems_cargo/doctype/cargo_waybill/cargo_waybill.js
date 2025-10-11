// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cargo Waybill", {
    refresh(frm) {
        frm.set_query("consignment", () => ({ filters: {} }));
        frm.set_query("manifest", () => ({ filters: {} }));
    },
    consignment: async function (frm) {
        if (frm.doc.consignment) {
            // pre-filter manifest to same operation plan as consignment
            const c = await frappe.db.get_value("Cargo Consignment", frm.doc.consignment, ["operation_plan"]);
            const op = c?.message?.operation_plan;
            if (op) {
                frm.set_query("manifest", () => ({ filters: { operation_plan: op } }));
            }
        }
    }
});
