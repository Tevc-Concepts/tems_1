frappe.ui.form.on('Governance Policy', {
    validate(frm) {
        if (frm.doc.acknowledgement_required && (!frm.doc.attached_files || frm.doc.attached_files.length === 0)) {
            frappe.msgprint(__('Acknowledgement required — attach at least one file.'));
            frappe.validated = false;
        }
    },
});
