frappe.pages['executive_dashboard'].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({ parent: wrapper, title: __('Executive Dashboard'), single_column: true });
    const $main = $(page.main);
    $main.addClass('tems-branding tems-dashboard');
    const grid = $('<div class="kpi-grid"></div>').appendTo($main);

    const cards = [
        { title: 'Open Work Orders', doc: { name: 'Open Work Orders', function: 'Count', type: 'Document Type', document_type: 'Maintenance Work Order' }, filters: [["Maintenance Work Order", "status", "=", "Open"]] },
        { title: 'Open Safety Incidents', doc: { name: 'Open Safety Incidents', function: 'Count', type: 'Document Type', document_type: 'Safety Incident' }, filters: [["Safety Incident", "status", "!=", "Closed"]] },
        { title: "Today's Duty Assignments", doc: { name: "Today's Duty Assignments", function: 'Count', type: 'Document Type', document_type: 'Duty Assignment' }, filters: [["Duty Assignment", "schedule_slot", "Today", ""]] },
    ];

    cards.forEach(cfg => {
        const $card = $(`<div class="kpi-card" tabindex="0"><div class="title">${cfg.title}</div><div class="value">—</div></div>`).appendTo(grid);
        frappe.call('frappe.desk.doctype.number_card.number_card.get_result', {
            doc: cfg.doc,
            filters: cfg.filters
        }).then(r => $card.find('.value').text(r.message ?? 0));
    });
};
