// Client-side form logic for Asset Utilization Log
frappe.ui.form.on('Asset Utilization Log', {
    validate(frm) {
        if (frm.doc.utilization_hours != null && frm.doc.utilization_hours < 0) {
            frappe.msgprint(__('Utilization hours must be zero or positive'));
            frappe.validated = false;
        }
        if (!frm.doc.asset && !frm.doc.vehicle) {
            frappe.msgprint(__('Provide at least Asset or Vehicle'));
            frappe.validated = false;
        }
    }
});
