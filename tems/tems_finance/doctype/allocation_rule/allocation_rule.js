frappe.ui.form.on('Allocation Rule', {
    validate(frm) {
        if ((frm.doc.percentage || 0) > 100) {
            frappe.msgprint(__('Percentage should not exceed 100%'));
            frappe.validated = false;
        }
    }
});
