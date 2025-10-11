frappe.ui.form.on('Incident Report', {
    validate(frm) {
        // Basic placeholder for future severity-based checks
        if (!frm.doc.incident_date) {
            frappe.msgprint(__('Incident Date required'));
            frappe.validated = false;
        }
        //update the reporter field use the user id to reporter and date to reported_date
        frm.set_value("reporter", frappe.session.user);
        frm.set_value("reported_date", frappe.utils.now_date());
    
    },
    // change in status to closed should set the closed date to today
    // also update the incident_duration field to be the difference between incident_date and closed_date
    on_submit(frm) {
        if (frm.doc.status === "Closed") {
            frm.set_value("closed_date", frappe.utils.now_date());
            if (frm.doc.incident_date) {
                // Calculate duration in days between incident_date and closed_date
                const incidentDate = frappe.datetime.str_to_obj(frm.doc.incident_date);
                const closedDate = frappe.datetime.str_to_obj(frappe.utils.now_date());
                const duration = frappe.datetime.get_day_diff(closedDate, incidentDate);
                frm.set_value("incident_duration", duration);
            }
        }
    },

});
