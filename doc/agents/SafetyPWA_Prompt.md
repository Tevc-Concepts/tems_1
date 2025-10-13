# TEMS PWA — SAFETY & COMPLIANCE APP PROMPT

## ROLE
You are creating the **Safety Officer’s PWA** to monitor, record, and manage safety and compliance data from the field.

---

## TASKS

1. **Authentication**
   - Login (role = Safety Officer).
   - Link to HRMS profile and assigned region.

2. **Dashboard**
   - Safety score by vehicle.
   - Active incidents, risk assessments, audit compliance.
   - Driver safety compliance rate.

3. **Incident Reporting**
   - Create new incident report (select vehicle, trip, driver).
   - Capture photos, videos, and location.
   - Categorize severity (Minor/Major/Critical).
   - Auto-notify Operations if severity ≥ Major.

4. **Audit & Checklist**
   - Perform daily pre-trip and post-trip safety inspections.
   - Validate safety equipment, tire conditions, and compliance documents.
   - Generate Safety Report PDF.

5. **Risk Assessment**
   - Record risk rating (1–10 scale).
   - Upload mitigation plan or corrective actions.
   - Flag vehicles or drivers needing retraining.

6. **Training & Alerts**
   - View assigned safety training modules.
   - Push notifications for document expiries (license, insurance, inspection).

---

## CONSTRAINTS
- Mobile-first PWA (Android/iOS + browser installable).
- Offline form submission (sync when online).
- Must use existing `tems_safety` doctypes: Incident Report, Risk Assessment, Safety Audit.
- Integrate with TEMS backend via REST API endpoints.
- Include chart widgets for trends (incident rate, compliance level).

---

## OUTPUTS
- Pages: Dashboard, Incident Form, Safety Check, Risk Log, Reports.
- Components: Camera uploader, Location picker, Severity slider, Sync status.
- Integration plan with Operations module for automatic alerts.
