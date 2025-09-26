frappe.ui.form.on('Customs Clearance', {
    validate(frm) {
        if (frm.doc.status === 'Released' && !frm.doc.documents?.length) {
            frappe.msgprint(__('Attach at least one document for Released status'));
            frappe.validated = false;
        }
    }
});
