frappe.ui.form.on('Incident Report', {
    validate(frm) {
        // Basic placeholder for future severity-based checks
        if (!frm.doc.incident_date) {
            frappe.msgprint(__('Incident Date required'));
            frappe.validated = false;
        }
    }
});
