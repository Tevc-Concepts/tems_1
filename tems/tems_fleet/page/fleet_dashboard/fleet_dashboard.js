frappe.pages['fleet_dashboard'].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({ parent: wrapper, title: __('Fleet Dashboard'), single_column: true });
    const $main = $(page.main);
    $main.addClass('tems-branding tems-dashboard');
    const grid = $('<div class="kpi-grid"></div>').appendTo($main);
    const card = $('<div class="kpi-card" tabindex="0"><div class="title">Open Work Orders</div><div class="value">—</div></div>').appendTo(grid);
    frappe.call('frappe.desk.doctype.number_card.number_card.get_result', {
        doc: { name: 'Open Work Orders', function: 'Count', type: 'Document Type', document_type: 'Maintenance Work Order' },
        filters: [["Maintenance Work Order", "status", "=", "Open"]]
    }).then(r => card.find('.value').text(r.message ?? 0));
};
