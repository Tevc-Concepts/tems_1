---
applyTo: '**'
---
# PROJECT_CONTEXT:
- Frappe/ERPNext v15+ site.
- Main custom app: TEMS (already in codebase). All code, assets, overrides MUST live under apps/tems.
- Integrations: ERPNext modules (HRMS, Drive), and Frappe Insights. Keep custom doctypes, pages, workspaces inside TEMS.
- Target: modular features (Leadership, People, Fleet, Safety, Trade, Informal Economy, Climate + Finance/CRM/SCM).
- UI: Use Frappe UI components and Desk customization (Workspaces, Dashboards, Pages). Use TEMS theme CSS (no direct edits to frappe/erpnext core files).
- Deploy/testing: ensure bench migrate, bench build, bench clear-cache after changes. Verify cron/jobs on v15 (test scheduled jobs).

2 — App scaffolding & key files (what Copilot should create/edit)
Paths relative to your bench:
apps/tems/tems/hooks.py — register css/js, fixtures, scheduled jobs, doc events, whitelisted methods. See below sample snippet.
apps/tems/tems/doctype/* — all custom DocTypes (e.g., Journey Plan, Spot Check, Driver Qualification, Asset, Inspection).

apps/tems/tems/public/css/tems_theme.css — theme/overrides for Desk & Website.
apps/tems/tems/www/* — optional Jinja pages / public pages (driver portal micro-pages).
apps/tems/tems/templates/pages/* & apps/tems/tems/templates/includes/* — desk pages and partials.
apps/tems/tems/fixtures/*.json — role, workspace, custom field fixtures to auto-install.
apps/tems/tems/patches/v15/*.py — DB migrations and seed data.
apps/tems/tems/config/desk_workspace/*.json — workspace json exported as fixtures.
Add build.json / package.json as needed to compile CSS assets.

3 — hooks.py snippet (copy into TEMS/hooks.py)

This tells Frappe to include CSS, JS and fixtures from TEMS app:
app_name = "tems"
app_title = "TEMS"
app_publisher = "Tevc Concepts Limited"
app_description = "Transport Excellence Management System customizations"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_version = "0.1.0"
### include in desk (backend)
app_include_css = "/assets/tems/css/tems_theme.css"
app_include_js = "/assets/tems/js/tems_desk.js"
### include in web (website)
web_include_css = "/assets/tems/css/tems_theme.css"
web_include_js = "/assets/tems/js/tems_web.js"
### fixtures to install roles, workspaces, custom fields, workspace pages
fixtures = [
    {"dt": "Role", "filters": [["name", "in", ["TEMS Executive","Fleet Manager","Safety Officer","Driver","Informal Operator","Border Agent","Community Leader","Maintenance Tech"]]]},
    "Workspace",
    "Custom Field",
    "Print Format",
    "Report"
]
### doc events (server-side hooks)
doc_events = {
    "Journey Plan": {
        "on_submit": "tems.api.journey.on_submit",
        "validate": "tems.api.journey.validate_journey"
    },
    "Asset": {
        "after_insert": "tems.api.assets.after_insert"
    }
}
scheduler_events = {
    "daily": [
        "tems.tasks.daily_sync_checkpoint",
        "tems.tasks.daily_interest_compute"
    ],
    "cron": {
        "0 1 * * *": ["tems.tasks.compute_nightly_jobs"]
    }
}

Use fixtures so Copilot can generate roles, workspace and workspace pages automatically on bench --site <site> migrate. See Frappe hooks docs for hook names. 
Frappe Docs

# 4 — DocType + Data Model guidance (Copilot tasks)

For each module, create a custom DocType inside tems app. Provide Copilot these rules:

Always extend ERPNext master records by linking to core doctypes where appropriate (e.g., Link to Employee, Vehicle or Item).

Keep new fields in TEMS Custom DocTypes; do not alter core doctypes unless absolutely necessary — prefer Custom Field fixtures.

Add permissions in doctype JSON: roles and permission levels (read, write, create, submit, cancel).

Example essential DocTypes to create:

Journey Plan (fields: route, driver (Link Employee), vehicle (Link Asset), start_time, end_time, risk_score, weather_snapshot, sos_contact)
Spot Check (fields: inspector, photos, gps, notes, findings)
Driver Qualification (link Employee → license, medical_clearance, expiry_date)
Asset (if you must extend beyond ERPNext Vehicle)
Maintenance Work Order (link Asset, vendor, status, parts used)
Informal Operator Profile (KYC minimal via phone, USSD id)
Ask Copilot to autogenerate standard DB indices on frequently queried fields (gps coordinates, geohash, route_id, status).

# 5 — Workspace / Desk Customization & Role Workspaces
Workspaces are the user entry point. Create role-based workspaces (JSON fixtures) under config/desk_workspace/<role>_workspace.json. Each workspace should contain:
Dashboard widgets (KPI cards) — create KPI Cards via Frappe/Insight and link widgets.
Shortcuts: quick links to core masters, create forms, frequent reports.
Masters: grouped DocTypes (e.g., Fleet: Vehicles, Assets, Work Orders; People: Employees, Training).
Reports: Query reports, Script reports.
Page links: Insights dashboards and Drive folders.
Example Fleet Manager workspace skeleton (workspace JSON):
{
 "title": "Fleet Manager",
 "name": "Fleet Manager",
 "shortcuts": [
   {"type":"doctype","name":"Asset"},
   {"type":"doctype","name":"Maintenance Work Order"},
   {"type":"page","name":"fleet-dashboard"}
 ],
 "cards": [
   {"type":"card","doctype":"Asset","metric":"availability_percent"},
   {"type":"card","doctype":"Maintenance Work Order","metric":"open_wo_count"}
 ]
}

You can export workspace JSON from UI and include as fixtures. Workspace customization docs: the Desk page and Workspace docs explain edit flows. 
Frappe Docs
+1
#  6 — Role & Permission design (practical rules)
Suggested roles:
- TEMS Administrator (full)
- TEMS Executive (dashboards, strategy)
- Operations Manager
- Operations Officer
- Fleet Officer
- Fleet Manager
- Safety Officer
- Safety Manager
- Business Transformation Officer
- Driver
- Maintenance Technician
- Informal Operator
- Border Agent
- Community Leader
- Read-Only Auditor

### Permission rules:
Least privilege: give create/submit only where necessary (Driver can create Inspections but cannot change Asset master).
Use permission levels for field-level control.
Use role-based Client Scripts for UI behaviors (see next section).
Provide Copilot with a roles.json fixture so roles are created during install.

# 7 — Client Scripts, Server Methods, & Page Customizations
- Use Client Scripts for small UI behaviors (validate fields, hide/show). Store these as DocType Client Script fixtures in TEMS.
- Use Server-side Python for heavy logic and scheduled tasks (in tems/api/*.py and tems/tasks/*.py).
- Use Page and Page Script to build custom Desk pages (frappe.ui.make_app_page) for interactive dashboards and route maps.
- For complex front ends (maps, heavy visualisation), either:
- Build a Frappe Page (Jinja + frappe.call) and use Frappe UI components; OR
- Build a small React/Vite app and serve it via TEMS as a separate web app and call Frappe REST APIs. (Both are valid — - - Frappe docs mention both patterns). 
Medium
Example small Client Script (validate license expiry on save):
```
frappe.ui.form.on('Driver Qualification', {
  validate(frm) {
    if (frm.doc.expiry_date && frappe.datetime.get_diff(frm.doc.expiry_date, frappe.datetime.nowdate()) < 0) {
      frappe.msgprint(__('License expired — update before assigning journeys'));
      frappe.validated = false;
    }
  }
})
```
# 8 — Theme & Styling (Frappe UI) — safe override pattern

Do not edit core CSS. Instead:
Add a theme/stylesheet inside TEMS:
apps/tems/tems/public/css/tems_theme.css
- Register in hooks.py with app_include_css and web_include_css (shown above).
- Use specific selectors or scoped classes (e.g., .tems-branding .page-head) to avoid breaking future updates.
- Include build.json to compile and assets path so bench build picks it up.

Examples:
- Override size and brand colors using variables or specific classes (avoid global element selectors).
- Provide accessible font-size scale and high-contrast mode toggles.
- Guides and community examples show using a custom app to host theme assets and registering them in hooks for safe overrides. 
Auriga IT
+1

# 9 — Frappe Insights & Dashboards integration
- Install frappe_insights / insights on the site and use its dashboards/charts for KPI visualizations.
- Export insights dashboards (JSON) and include them as fixtures or link them from TEMS workspace pages. Users can add Insights dashboards as page links in their workspace. Community posts explain exporting/importing Insights dashboard configs. 
GitHub
+1
For real-time charts: create Script Reports or Query Reports that Insights can consume.

# 10 — Drive (file & doc mgmt), HRMS & cross-app links

- For Drive, link folders to DocTypes (e.g., Spot Check → photos folder). Use file and File DocType references.
- For HRMS, connect Driver/Employee to Employee (ERPNext HR) to reuse payroll/training features.
- Use attachments and file_url for photos; implement thumbnail generation in TEMS tasks.

# 11 — Dev/Deploy checklist for Copilot to run tasks

- When Copilot generates code, ensure it outputs and then you run:
bench --site <site> install-app tems (if not already installed)
bench --site <site> migrate
bench build
bench clear-cache
bench restart

- Verify scheduled jobs and cron: run a small scheduled task to confirm scheduler is active — there are v15 reports of cron issues when new apps are installed; test scheduled jobs after install. (Important: v15 had a community thread reporting cron issues after custom app install — test your scheduling). 

# Frappe Forum
# 12 — Example Copilot/GPT-5 prompt for implementing one feature
- Use this template when asking Copilot to create a feature:
- TASK: Create TEMS Journey Plan DocType + Desk Page + Workspace card for Fleet Manager.

### CONSTRAINTS:
- Use Frappe v15 patterns.
- All files must go inside apps/tems.
- Add fixtures: Workspace 'Fleet Manager', Client Script for Journey Plan validation, Role 'Fleet Manager'.
- hooks.py entries must register assets and doc_events.
- Include tests: unit test for server method tems.api.journey.validate_journey that rejects journeys assigned to expired driver qualification.
- Provide minimal UI: Desk page 'fleet-dashboard' with 2 KPI cards (Asset availability, Open Work Orders).
- Create migration patch if DocType fields required.
- Use Frappe UI components (frappe.ui.form, frappe.render_template) for page.
- Include installation notes and bench commands.

This single prompt gives Copilot everything needed to output code, fixtures, and install steps.

# 13 — Acceptance tests & verification

Ask Copilot to generate:
Automated unit tests for key server functions (pytest style with Frappe test utilities).
A smoke-test script that:
Creates roles and users, Assigns workspace,
- Creates a Journey Plan with expired driver qualification and expects validation failure,

- Creates inspection and uploads a file to Drive, checks file exists.

# 14 — Operational tips & gotchas (from v15 community notes)

- Use fixtures for Roles/Workspaces so installation is repeatable.
- When overriding styles, prefer a TEMS theme app approach — register CSS in hooks.
- Frappe Insights dashboards can be exported/imported or linked from workspace pages — include dashboards as fixtures or add links to insights dashboards in workspace config. 
- Test scheduled jobs immediately after installing a new custom app (v15 users have reported cron/scheduler issues in some cases).
