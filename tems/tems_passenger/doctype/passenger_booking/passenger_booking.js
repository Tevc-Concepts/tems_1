// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Passenger Booking", {
    refresh(frm) {
        frm.set_query("trip", () => ({ filters: {} }));
    },
    seat_no: async function (frm) {
        if (!frm.doc.trip || !frm.doc.seat_no) return;
        try {
            const r = await frappe.db.get_value("Passenger Trip", frm.doc.trip, ["seat_capacity"]);
            const cap = parseInt(r?.message?.seat_capacity || 0, 10);
            const seat = parseInt(frm.doc.seat_no, 10);
            if (cap > 0 && seat > cap) {
                frappe.msgprint({
                    message: __("Seat no exceeds trip capacity (" + cap + ")"),
                    indicator: "red"
                });
                frm.set_value("seat_no", "");
            }
        } catch (e) {
            // no-op
        }
    }
});
