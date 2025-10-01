// Copyright (c) 2025, Tevc Concepts Limited and contributors
// For license information, please see license.txt

    frappe.ui.form.on("Field Service Requests", {
    validate(frm) {
        if (frm.doc.status === 'Closed' && (frm.doc.priority || '') === 'High' && !frm.doc.correction_notes) {
            // if field not present, ignore; kept as placeholder
        }
    },
    });
