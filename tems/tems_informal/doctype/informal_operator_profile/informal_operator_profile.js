frappe.ui.form.on('Informal Operator Profile', {
    validate(frm) {
        if (!/^\+?\d{8,15}$/.test(frm.doc.phone || '')) {
            frappe.msgprint(__('Enter a valid phone number'));
            frappe.validated = false;
        }
    }
});
