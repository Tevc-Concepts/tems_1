frappe.ui.form.on('Risk Assessment', {
    validate(frm) {
        if (frm.doc.risk_score != null && frm.doc.risk_score < 0) {
            frappe.msgprint(__('Risk Score cannot be negative'));
            frappe.validated = false;
        }
    }
});
