frappe.ui.form.on('Compliance Obligation', {
    validate(frm) {
        if (frm.doc.status === 'Compliant' && frm.doc.evidence_required && (!frm.doc.evidence_files || frm.doc.evidence_files.length === 0)) {
            frappe.msgprint(__('Evidence required — attach at least one file before marking as Compliant.'));
            frappe.validated = false;
        }
    },
});
