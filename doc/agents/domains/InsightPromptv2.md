CONTEXT:
TEMS is an enterprise transport OS with many modules. We need a complete Insights Guide for the platform that enumerates all dashboards, KPI number-cards, charts, reports, and drill-down behaviors. Outputs must be consumable by Frappe Insights and PWA dashboards (Operations PWA, Driver PWA, Safety PWA). The guide must include data sources (DocTypes/fields), frequency of update, sample query or report SQL/Frappe Query Report definition, recommended widgets, and sample templates for interactivity (filters, drill-down targets, and action buttons).

TASK:
Produce a full "TEMS Insights & Dashboard Guide" that includes:

1. Executive summary (purpose of insights and who uses them).
2. Global insights architecture:
   - Data ingestion cadence (real-time via Movement Log, near-real-time via sensor ingestion, and nightly batch jobs).
   - Data mart design (pre-aggregated KPIs per vehicle/day and per asset/day).
   - Storage suggestions for heavy telemetry (time-series DB or efficient Frappe table schema).

3. List of Dashboards (for each user role) — for each dashboard provide:
   - Dashboard ID / Title
   - Target role(s)
   - Purpose (1–2 lines)
   - Widgets list (Number cards, Tables, Charts, Maps)
   - Data sources (DocType names and exact fields used)
   - Update frequency (real-time/5m/1h/daily)
   - Filters (date range, vehicle_type, vehicle_id, route, driver)
   - Drill-down behavior (what clicking a widget opens; exact DocType/form or drill report)
   - Alerts/thresholds (when to trigger notifications)
   - Example Frappe Insight config (JSON snippet) or Query Report SQL/Script

Suggested dashboards include (but are not limited to):
- Executive Overview Dashboard (system-wide KPIs)
- Operations Live Map & Control Dashboard
- Fleet Utilization & Availability Dashboard
- Vehicle Profitability Dashboard (vehicle-level, tyre cost drilldown)
- Tyre Intelligence Dashboard (per tyre health, cost/km)
- Predictive Maintenance Dashboard (predicted failures)
- Safety & Incidents Dashboard (incidents trend, top-risk vehicles/drivers)
- Cargo Operations Dashboard (consignments, manifests, LTL vs FTL metrics)
- Passenger Operations Dashboard (occupancy, fare revenue, cancellations)
- Finance Ledger Dashboard (revenue, cost breakdown, FX impact)
- Compliance & Documents Dashboard (expiring licenses, insurance)
- AI Center Dashboard (model health, predictions produced, accuracy metrics)

4. Detailed KPI Catalog — for each KPI include:
   - KPI name
   - Definition (formula)
   - DocTypes/fields used
   - Aggregation window (hour/day/week/month)
   - Acceptable thresholds and colors (green/yellow/red)
   - Drill-down target(s)
   - Sample query or calculation pseudo-code

Examples to include:
- Vehicle Utilization % = (Time in Transit) / (Available Time)
  - Data sources: Movement Log (status timestamps) + Vehicle availability calendar
- Tyre Cost per Km = (Tyre purchase + maintenance + disposal share) / Km driven
  - Data sources: Tyre logs + Movement Log + Cost & Revenue Ledger
- On-Time Delivery % = (Deliveries On Time) / (Total Deliveries)
  - Data sources: Movement Log (delivered timestamp) + Order expected delivery time

5. Charts & Visual Patterns:
   - Time-series charts (vehicle uptime, incidents per day)
   - Heatmaps/Geo maps for route congestion
   - Sankey for flow of consignments across hubs
   - Waterfall chart for cost composition per vehicle
   - Gauge for Tyre Health Index
   - Example chart config (library agnostic) and example Frappe Insight mapping

6. Drill-down UX patterns:
   - Number card → opens a List view filtered → click a row opens the DocType form
   - Chart segment → opens a filtered report or small modal with top N records
   - Map pin → open quick-action panel: call driver, reassign vehicle, view history
   - Alerts panel → action buttons (Acknowledge, Send Message, Reassign)

7. Alerts & Notification Rules:
   - Provide sample rules (thresholds, frequency, escalation path)
   - For each alert include: trigger condition, primary recipients, severity, auto-actions (reassign, pause trip)

8. AI-Driven Insights:
   - Which dashboards show AI outputs and how to surface explainability (confidence, top features)
   - Sample insight card template: "Predicted Failure: Vehicle XYZ — 72% chance within 7 days. Top factors: tyre wear, oil temp, mileage."
   - Recommend refresh cadence and retrain schedule for these models.

9. Implementation checklist:
   - Which Query Reports to create vs. which to model in Insights
   - Required fixtures to deploy (dashboard JSON exports)
   - Data retention & archiving policy
   - Performance tuning tips (pre-aggregate nightly, cache cards, use pagination)

10. Delivery artifacts:
   - `docs/INSIGHTS_GUIDE.md` (complete guide)
   - Example `insights/` folder containing sample KPI card JSONs, chart configs, and 5 Query Report definitions (SQL/Script).
   - A `CHECKLIST.md` for product managers to validate dashboards after deployment.

CONSTRAINTS:
- Use TEMS doctypes by name (Operation Plan, Movement Log, Vehicle, Tyre, Cost & Revenue Ledger, Cargo Consignment, Passenger Trip, Employee, Asset).
- Provide at least 20 KPI definitions spanning Operations, Fleet, Tyre, Safety, Finance, Cargo, Passenger, and AI.
- Include sample queries or pseudo code for the top 10 most important KPIs.
- All diagrams and examples must be reproducible in Frappe Insights or JavaScript-based dashboards (mapbox, chart.js, recharts).

EXPECTED OUTPUT:
- `docs/INSIGHTS_GUIDE.md`: full actionable guide.
- `insights/kpis.json`: array of KPI definitions (name, formula, doctypes, fields, aggregation window).
- `insights/sample_dashboards/` with 3 dashboard JSON examples (Executive Overview, Vehicle Profitability, Tyre Intelligence).
- `insights/query_reports/` directory with 5 example Query Report definitions.

INSTRUCTIONS FOR AI:
- Produce clear, numbered sections and a contents table in the guide.
- For each KPI provide the exact DocType and field names (or a best-guess mapping if field names differ, note that they may need mapping to actual field names).
- Include drill-down targets with the exact DocType name to open.
- Keep code snippets short, precise, and ready to paste into Frappe Query Report or Insight JSON.
