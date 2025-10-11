// Copyright (c) 2025
// For license information, please see license.txt

frappe.ui.form.on('Strategic Goal', {
refresh(frm) {
        // calculate the achievement percentage based on target and actual values
        if (frm.doc.target_value && frm.doc.actual_value) {
            let achievement = (frm.doc.actual_value / frm.doc.target_value) * 100;
            frm.set_value('achievement', achievement.toFixed(2));
        } else {
            frm.set_value('achievement', 0);
        }
    },
validate(frm) {
    // Custom validation logic - target value should not be less than actual value and target value must be above zero
    if (frm.doc.target_value <= 0) {
        frappe.msgprint(__('Target value must be greater than zero'));
        frappe.validated = false;
    }
    // Ensure title is not empty
    if (!frm.doc.title) {
        frappe.msgprint(__('Title is required'));
        frappe.validated = false;
    }
}
});
