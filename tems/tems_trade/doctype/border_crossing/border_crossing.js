frappe.ui.form.on('Border Crossing', {
    refresh(frm) {
        if (frm.doc.arrival_time && frm.doc.departure_time) {
            // computed server-side; keep as display only
        }
    }
});
