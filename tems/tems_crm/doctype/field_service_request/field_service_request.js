frappe.ui.form.on('Field Service Request', {
    validate(frm) {
        if (frm.doc.status === 'Closed' && (frm.doc.priority || '') === 'High' && !frm.doc.correction_notes) {
            // if field not present, ignore; kept as placeholder
        }
    }
});
