// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Operation Plan", {
    vehicle: async function (frm) {
        if (!frm.doc.vehicle) return;
        try {
            const v = await frappe.db.get_value("Vehicle", frm.doc.vehicle, ["vehicle_type", "custom_vehicle_type"]);
            const vt = (v?.message?.vehicle_type || v?.message?.custom_vehicle_type || "").trim();
            if (vt) {
                const title = vt.charAt(0).toUpperCase() + vt.slice(1).toLowerCase();
                if (["Cargo", "Passenger"].includes(title)) {
                    frm.set_value("operation_mode", title);
                }
            }
        } catch (e) {
            // no-op
        }
    }
});
