frappe.ui.form.on('Journey Plan', {
    validate(frm) {
        if (frm.doc.end_time && frm.doc.start_time && frm.doc.end_time < frm.doc.start_time) {
            frappe.msgprint(__('End Time cannot be before Start Time'));
            frappe.validated = false;
        }
    }
});
