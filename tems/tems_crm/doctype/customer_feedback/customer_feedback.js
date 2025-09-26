frappe.ui.form.on('Customer Feedback', {
    validate(frm) {
        const rating = frm.doc.rating || 0;
        if (rating < 1 || rating > 5) {
            frappe.msgprint(__('Rating must be between 1 and 5'));
            frappe.validated = false;
        }
    }
});
