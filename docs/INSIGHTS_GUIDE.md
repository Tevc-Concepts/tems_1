# TEMS Insights & Dashboard Guide

_Last updated: 2025-10-20 • Owners: TEMS Insights Guild • Contact: insights@tems.app_

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Global Insights Architecture](#2-global-insights-architecture)
   1. [Data Ingestion Cadence](#21-data-ingestion-cadence)
   2. [Data Mart Design](#22-data-mart-design)
   3. [Telemetry Storage Recommendations](#23-telemetry-storage-recommendations)
3. [Dashboard Catalog](#3-dashboard-catalog)
   1. [Executive Overview Dashboard](#31-executive-overview-dashboard-ins-dash-0001)
   2. [Operations Live Map & Control](#32-operations-live-map--control-ins-dash-0002)
   3. [Fleet Utilization & Availability](#33-fleet-utilization--availability-ins-dash-0003)
   4. [Vehicle Profitability](#34-vehicle-profitability-ins-dash-0004)
   5. [Tyre Intelligence](#35-tyre-intelligence-ins-dash-0005)
   6. [Predictive Maintenance](#36-predictive-maintenance-ins-dash-0006)
   7. [Safety & Incidents](#37-safety--incidents-ins-dash-0007)
   8. [Cargo Operations](#38-cargo-operations-ins-dash-0008)
   9. [Passenger Operations](#39-passenger-operations-ins-dash-0009)
   10. [Finance Ledger](#310-finance-ledger-ins-dash-0010)
   11. [Compliance & Documents](#311-compliance--documents-ins-dash-0011)
  12. [AI Center](#312-ai-center-ins-dash-0012)
  13. [Business Review Snapshot](#313-business-review-snapshot)
4. [KPI Catalog](#4-kpi-catalog)
5. [Charts & Visual Patterns](#5-charts--visual-patterns)
6. [Drill-down UX Patterns](#6-drill-down-ux-patterns)
7. [Alerts & Notification Rules](#7-alerts--notification-rules)
8. [AI-Driven Insights](#8-ai-driven-insights)
9. [Implementation Checklist](#9-implementation-checklist)
10. [Appendix](#10-appendix)

---

## 1. Executive Summary
The TEMS Insights program delivers a unified analytics layer across Desk workspaces and the Operations, Driver, and Safety PWAs. Insights are designed for four primary audiences:
- **Strategic Leaders (Executives, Transformation Office):** monitor profitability, growth, and risk posture at a glance.
- **Operational Controllers (Operations & Fleet teams):** orchestrate daily dispatch, utilization, and maintenance decisions.
- **Risk & Compliance (Safety, Governance, Finance):** enforce regulatory readiness and triage incidents quickly.
- **Field Actors (Drivers, Maintenance Techs):** receive focused cards actionable via PWAs (next trip, tyre alert, inspection tasks).

Dashboards interoperate with Frappe Insights for desktop and are mirrored into JS-based PWA widgets by reusing the same query/report definitions. Drill-downs point back to the authoritative DocTypes (e.g., `Movement Log`, `Operation Plan`, `Tyre Inspection Log`) to ensure analysts can pivot from KPI to transaction.

---

## 2. Global Insights Architecture
Insights consume operational events emitted by the TEMS modules and roll them into consumable metrics. The architecture follows the layered pattern already defined for TEMS, with a dedicated analytics services slice.

### 2.1 Data Ingestion Cadence
- **Real-time stream (≤30 seconds latency):**
  - `Movement Log.status`, `Movement Log.gps_lat`, `Movement Log.gps_lng`
  - SocketIO channel `tems.operations.live` pushes updates to the Operations PWA map and the Live Control dashboard.
- **Near real-time (≤5 minutes):**
  - Tyre sensor packets (`Tyre Sensor Data.sensor_id`, `Tyre Sensor Data.temperature`, `Tyre Sensor Data.pressure`) arriving via ingestion API.
  - AI inference outputs (`AI Insight Log.prediction_type`, `confidence`) published by scheduled cron jobs.
- **Batch (nightly @ 01:15 server time):**
  - Profitability snapshots (`Cost & Revenue Ledger`, `Fleet Costs` aggregated per vehicle/day).
  - Compliance aging (`Document Checklist Item.valid_to`, `Driver Qualification.expiry_date`).
  - KPI caches stored in `tems_insights_kpi_cache` table for quick Desk load.

### 2.2 Data Mart Design
- **Operational Mart (`ins_ops_vehicle_daily`):**
  - Grain: `vehicle` × `operating_date`
  - Measures: `transit_minutes`, `idle_minutes`, `completed_trips`, `on_time_deliveries`, `total_distance_km`
  - Sources: `Movement Log`, `Operation Plan`, `Passenger Trip`
- **Asset Mart (`ins_asset_daily`):**
  - Grain: `asset` × `operating_date`
  - Measures: `maintenance_cost`, `tyre_health_index_avg`, `sensor_packets_received`
  - Sources: `Asset`, `Tyre Inspection Log`, `Tyre Sensor Data`, `Cost & Revenue Ledger`
- **Financial Mart (`ins_fin_vehicle_monthly`):**
  - Grain: `vehicle` × `fiscal_month`
  - Measures: `revenue`, `direct_costs`, `tyre_cost_share`, `margin_pct`, `fx_impact`
  - Sources: `Cost & Revenue Ledger`, `Fleet Costs`, `Exchange Rate Log`
- **Compliance Mart (`ins_compliance_daily`):**
  - Grain: `entity_type` × `entity_id`
  - Measures: `items_due`, `items_overdue`, `avg_age_days`
  - Sources: `Document Checklist Item`, `Driver Qualification`, `Insurance Policy`

All marts are materialized tables refreshed by `tems.tems_insights.tasks.refresh_data_marts` (nightly) and incremental updaters triggered hourly for delta loads.

### 2.3 Telemetry Storage Recommendations
- For high-volume sensor feeds (tyre, engine CAN, GPS trails beyond Movement Log granularity):
  - Option A: Deploy TimescaleDB atop MariaDB or migrate telemetry tables to an external PostgreSQL/Timescale instance while mirroring aggregates back to Frappe via scheduled jobs.
  - Option B: Use optimized Frappe tables (`Tyre Sensor Data`, `Vehicle Telemetry Log`) with composite indexes `(vehicle, reading_timestamp)` and monthly partitioning using `creation` date.
- Retain raw telemetry for 90 days in hot storage; move historical archives to S3-compatible object storage in Parquet format for BI workloads.
- Provide API endpoints for PWAs that query the analytics mart rather than raw telemetry to minimize mobile payload size.

---

## 3. Dashboard Catalog
Each dashboard definition below specifies the associated role, widget catalogue, data sources, refresh cadence, filters, drill-down behavior, alert thresholds, and an example Insights configuration snippet. IDs follow the `INS-DASH-XXXX` convention.

### 3.1 Executive Overview Dashboard (INS-DASH-0001)
- **Target roles:** TEMS Executive, Transformation Office, Finance Manager
- **Purpose:** Snapshot of profitability, service reliability, and fleet readiness across all business lines.
- **Widgets:**

| Widget ID | Type | Metric / Query | Source DocTypes & Fields | Update | Drill-down Target | Alert Threshold |
|-----------|------|----------------|---------------------------|--------|-------------------|-----------------|
| EXEC-KPI-01 | Number card | Vehicle Utilization % | `Movement Log.status`, `Movement Log.from_timestamp`, `Movement Log.to_timestamp` | Hourly | List `Movement Log` filtered by `vehicle` & date range | < 75% (yellow), < 65% (red) |
| EXEC-KPI-02 | Number card | Revenue per Vehicle-Day | `Cost & Revenue Ledger.vehicle`, `debit`, `credit`, `posting_date` | Daily | Query Report `Vehicle Profitability Detail` | < NGN 150,000 red |
| EXEC-KPI-03 | Number card | On-Time Delivery % | `Movement Log.actual_delivery_ts`, `Operation Plan.expected_arrival` | Hourly | Query Report `Operations Service Level` | < 90% yellow, < 85% red |
| EXEC-CH-01 | Combo chart | Margin % vs Cost composition | `ins_fin_vehicle_monthly` mart | Daily | `Cost & Revenue Ledger` (filtered by vehicle) | Margin < 18% alert |
| EXEC-CH-02 | Sankey | Revenue flow Cargo → Passenger → Trade lanes | `Cost & Revenue Ledger.business_unit`, `Cargo Consignment.trade_lane` | Daily | `Cargo Consignment` list view filtered by `trade_lane` | - |

- **Filters:** `posting_date` (relative ranges), `business_unit`, `vehicle_type`
- **Alerts:** Slack/Email to Executives if revenue per vehicle-day drops 15% week-over-week.
- **Example config snippet:**
```json
{
  "dashboard": "executive_overview",
  "components": [
    {
      "type": "number",
      "title": "Vehicle Utilization %",
      "query": "kpi_vehicle_utilization",
      "format": {"decimals": 1, "suffix": "%"},
      "thresholds": {"warning": 75, "danger": 65}
    },
    {
      "type": "combo",
      "title": "Margin vs Cost Mix",
      "query": "chart_margin_cost_mix",
      "options": {"series": ["margin_pct", "tyre_cost_share", "fuel_cost_share"]}
    }
  ],
  "filters": [
    {"field": "posting_date", "type": "date", "default": "last_30_days"},
    {"field": "vehicle_type", "type": "select", "options": ["Cargo", "Passenger"]}
  ]
}
```

### 3.2 Operations Live Map & Control (INS-DASH-0002)
- **Target roles:** Operations Manager, Operations Officer, Control Room Analyst
- **Purpose:** Monitor live vehicle positions, SLA exceptions, and trigger control actions.
- **Widgets:**

| Widget ID | Type | Metric / Query | Source | Update | Drill-down | Alert |
|-----------|------|----------------|--------|--------|------------|-------|
| OPS-MAP-01 | Map (Mapbox/Leaflet) | Live GPS by vehicle | `Movement Log.gps_lat`, `Movement Log.gps_lng`, `Movement Log.status` | Real-time | Map pin opens `Movement Log` quick panel + `Operation Plan` | If status `Delayed` > 15 min send Teams alert |
| OPS-TBL-01 | Table | Exception queue | `Operations Event.event_type`, `severity`, `vehicle`, `raised_at` | 1 min | List view `Operations Event` | Severity = Critical triggers SMS |
| OPS-KPI-01 | Number | In-Transit Vehicles | `Movement Log.status = "In Transit"` | Real-time | Filtered list | < 50% of planned dispatch red |
| OPS-KPI-02 | Number | Average Delay (mins) | `Movement Log.delay_minutes` | 5 min | Query Report `Operations Delay Detail` | > 25 yellow, > 40 red |

- **Filters:** `route`, `driver`, `vehicle`, `operation_mode`
- **Alerts:** Automated re-assignment suggestion when map pin clicked and `Operation Plan.has_backup = 1`.
- **Config excerpt:** streaming map uses `tems.operations.live` SocketIO channel; fallback to `ins_ops_vehicle_daily` for historical playback.

### 3.3 Fleet Utilization & Availability (INS-DASH-0003)
- **Target roles:** Fleet Manager, Fleet Officer
- **Purpose:** Understand fleet allocation, downtime reasons, and capacity gaps.
- **Widgets:**

| Widget ID | Type | Metric | Source | Update | Drill-down | Alert |
|-----------|------|--------|--------|--------|------------|-------|
| FLEET-KPI-01 | Number | Fleet Availability % | `Vehicle.status`, `Maintenance Work Order.schedule_start`, `schedule_end` | Hourly | `Vehicle` list filtered by `status` | < 80% warning |
| FLEET-CH-01 | Stacked bar | Downtime by reason | `Maintenance Work Order.downtime_reason`, `downtime_hours` | Daily | `Maintenance Work Order` list | Reason `Critical Failure` > 5 triggers email |
| FLEET-TBL-01 | Table | Vehicles idle >48h | `ins_ops_vehicle_daily.idle_minutes` | Hourly | `Operation Plan` filtered by vehicle | Idle vehicles >2 days message to Ops |
| FLEET-CH-02 | Heatmap | Utilization by weekday/hour | `Movement Log.from_timestamp` | Daily | Drill to `Movement Log` calendar | - |

- **Filters:** `depot`, `vehicle_type`, `week`
- **Config snippet:** `chart_downtime_reason` referencing SQL query `SELECT downtime_reason, SUM(downtime_hours) ... GROUP BY downtime_reason`.

### 3.4 Vehicle Profitability (INS-DASH-0004)
- **Target roles:** Finance Manager, Fleet Manager
- **Purpose:** Compare margins per vehicle with consumable cost drivers.
- **Widgets:**

| Widget ID | Type | Metric | Source | Update | Drill-down | Alert |
|-----------|------|--------|--------|--------|------------|-------|
| PROF-KPI-01 | Number | Margin % | `ins_fin_vehicle_monthly.margin_pct` | Daily | `Cost & Revenue Ledger` filtered by vehicle/month | < 15% red |
| PROF-KPI-02 | Number | Tyre Cost per Km | `ins_asset_daily.tyre_cost_per_km` | Daily | Query Report `Tyre Cost Breakdown` | > NGN 40 red |
| PROF-CH-01 | Waterfall | Revenue → Net Margin | `Cost & Revenue Ledger` aggregated by account head | Daily | `Vehicle Profitability Detail` report | - |
| PROF-TBL-01 | Table | Top 10 Profitable Vehicles | Same as above | Daily | `Vehicle` form | - |

- **Filters:** `fiscal_month`, `vehicle_type`, `currency`
- **Alert:** `Margin %` drop >5pp vs prior month triggers workflow to Finance Manager.
- **Example config:** See `insights/sample_dashboards/vehicle_profitability.json`.

### 3.5 Tyre Intelligence (INS-DASH-0005)
- **Target roles:** Tyre Manager, Maintenance Tech, Safety Officer
- **Purpose:** Track tyre health, cost efficiency, and upcoming replacements.
- **Widgets:**

| Widget ID | Type | Metric | Source | Update | Drill-down | Alert |
|-----------|------|--------|--------|--------|------------|-------|
| TYRE-KPI-01 | Gauge | Avg Tyre Health Index | `Tyre.health_index`, `ins_asset_daily.tyre_health_index_avg` | 5 min | `Tyre` list filtered by `health_index` | < 65 warning, < 50 red |
| TYRE-KPI-02 | Number | Upcoming Replacements (7d) | `Tyre Inspection Log.replacement_due_date` | Hourly | `Tyre Inspection Log` filtered by date | > 15 triggers reminder |
| TYRE-CH-01 | Line chart | Cost per Km trend | `ins_asset_daily.tyre_cost_per_km` | Daily | Query Report `Tyre Cost Trend` | > NGN 35 sustained 3 days sends email |
| TYRE-TBL-01 | Table | Sensors Offline > 10m | `Tyre Sensor Data.last_packet_ts` | 5 min | `Tyre Sensor Data` list | Device offline auto-create `Maintenance Work Order` |

- **Filters:** `tyre_brand`, `axle_position`, `vehicle`
- **JSON snippet:** Provided in `insights/sample_dashboards/tyre_intelligence.json`.

### 3.6 Predictive Maintenance (INS-DASH-0006)
- **Target roles:** Maintenance Tech Lead, Fleet Manager
- **Purpose:** Surface AI predictions for component failures and schedule interventions.
- **Widgets:**

| Widget ID | Type | Metric | Source | Update | Drill-down | Alert |
|-----------|------|--------|--------|--------|------------|-------|
| PM-KPI-01 | Number | Predicted Failures (7d) | `AI Insight Log.prediction_type = "failure"` | Hourly | `AI Insight Log` filtered by `prediction_window_days` | > 10 warning |
| PM-TBL-01 | Table | Vehicles at Risk | `AI Insight Log.vehicle`, `confidence`, `top_features` | Hourly | Vehicle form + `Maintenance Work Order` quick create | Confidence > 0.7 auto-create WO |
| PM-CH-01 | Bar | Failure probability by subsystem | `AI Insight Log.subsystem` | Hourly | `Maintenance Work Order` list filtered by `subsystem` | - |

- **Filters:** `subsystem`, `depot`, `confidence_band`
- **Alerts:** High-confidence predictions escalate to Maintenance Lead via SMS.

### 3.7 Safety & Incidents (INS-DASH-0007)
- **Target roles:** Safety Manager, Safety Officer, Compliance Lead
- **Purpose:** Monitor incident trends, driver risk, and compliance tasks.
- **Widgets:**

| Widget ID | Type | Metric | Source | Update | Drill-down | Alert |
|-----------|------|--------|--------|--------|------------|-------|
| SAFE-KPI-01 | Number | Incident Frequency Rate | `Incident Report.incident_date`, `vehicle`, `severity` | Daily | `Incident Report` list filtered by severity | Rate > 2/100 trips red |
| SAFE-KPI-02 | Number | Open Spot Checks | `Spot Check.status` | Daily | `Spot Check` list | > 20 pending red |
| SAFE-CH-01 | Area chart | Incidents per day (30d) | `Incident Report.incident_date` | Daily | `Incident Report` timeline | Spikes trigger Slack |
| SAFE-CH-02 | Bubble map | Incident density by route | `Movement Log.route_id`, `Incident Report.gps_lat/lng` | Daily | Map -> incident detail | - |

- **Filters:** `severity`, `route`, `vehicle`, `driver`

### 3.8 Cargo Operations (INS-DASH-0008)
- **Target roles:** Cargo Manager, Dispatch Coordinator
- **Purpose:** Manage consignments, manifest status, and OTIF performance.
- **Widgets:**

| Widget ID | Type | Metric | Source | Update | Drill-down | Alert |
|-----------|------|--------|--------|--------|------------|-------|
| CARGO-KPI-01 | Number | OTIF % | `Cargo Consignment.delivered_qty`, `expected_delivery_date`, `actual_delivery_date` | Hourly | `Cargo Consignment` list filtered by status | < 92% warning |
| CARGO-TBL-01 | Table | Pending Customs Clearance | `Border Crossing.status` | Hourly | `Border Crossing` doc | Items > 5 escalate |
| CARGO-CH-01 | Sankey | Flow Origin → Hub → Destination | `Cargo Manifest.origin_hub`, `destination_hub` | Daily | `Cargo Manifest` form | - |
| CARGO-KPI-02 | Number | LTL vs FTL Ratio | `Cargo Consignment.load_type` | Daily | Query Report `Cargo Load Mix` | LTL > 70% for 3 days warn |

- **Filters:** `trade_lane`, `customer`, `hub`

### 3.9 Passenger Operations (INS-DASH-0009)
- **Target roles:** Passenger Ops Manager, Station Supervisor
- **Purpose:** Track ridership, occupancy, cancellations, and revenue.
- **Widgets:**

| Widget ID | Type | Metric | Source | Update | Drill-down | Alert |
|-----------|------|--------|--------|--------|------------|-------|
| PASS-KPI-01 | Number | Occupancy Ratio | `Passenger Trip.booked_seats`, `capacity` | Hourly | `Passenger Trip` list filtered by route | < 65% warning |
| PASS-KPI-02 | Number | Cancellation Rate | `Passenger Trip.status` | Hourly | Query Report `Passenger Cancellation Detail` | > 10% red |
| PASS-CH-01 | Line | Fare Revenue trend | `Cost & Revenue Ledger.account = "Fare Revenue"` | Daily | `Cost & Revenue Ledger` list | Drop >15% day/day alert |
| PASS-TBL-01 | Table | Top routes by revenue | Same as above | Daily | `Route Schedule` form | - |

- **Filters:** `route_id`, `departure_station`, `time_window`

### 3.10 Finance Ledger (INS-DASH-0010)
- **Target roles:** Finance Manager, Finance Officer, Auditor
- **Purpose:** Provide financial rollups, cash flow visibility, and FX impacts.
- **Widgets:**

| Widget ID | Type | Metric | Source | Update | Drill-down | Alert |
|-----------|------|--------|--------|--------|------------|-------|
| FIN-KPI-01 | Number | Total Revenue (MTD) | `Cost & Revenue Ledger.account = "Revenue"` | Daily | `Cost & Revenue Ledger` ledger view | - |
| FIN-KPI-02 | Number | Total Costs (MTD) | Same | Daily | Same | - |
| FIN-CH-01 | Line | FX Impact by currency | `Exchange Rate Log`, `Cost & Revenue Ledger.fx_difference` | Daily | Query Report `FX Impact Detail` | > NGN 5M red |
| FIN-TBL-01 | Table | Outstanding Receivables >30d | `Cost & Revenue Ledger.customer`, `due_date` | Daily | Customer ledger | > NGN 10M escalate |

- **Filters:** `fiscal_month`, `currency`, `business_unit`

### 3.11 Compliance & Documents (INS-DASH-0011)
- **Target roles:** Compliance Officer, HR Manager, Safety Manager
- **Purpose:** Ensure documents, licenses, and insurance remain valid.
- **Widgets:**

| Widget ID | Type | Metric | Source | Update | Drill-down | Alert |
|-----------|------|--------|--------|--------|------------|-------|
| COMP-KPI-01 | Number | Expiring Driver Licenses (30d) | `Driver Qualification.expiry_date` | Daily | `Driver Qualification` list filtered by date | > 10 red |
| COMP-KPI-02 | Number | Vehicle Insurance Overdue | `Document Checklist Item.status` | Daily | `Document Checklist Item` list | > 0 triggers compliance ticket |
| COMP-TBL-01 | Table | Policy compliance status | `Compliance Obligation.status`, `owner` | Daily | `Compliance Obligation` form | - |
| COMP-CH-01 | Bar | Compliance aging by module | `ins_compliance_daily.items_overdue` | Daily | `Compliance Audit` list | - |

- **Filters:** `module`, `responsible_role`

### 3.12 AI Center (INS-DASH-0012)
- **Target roles:** AI Lead, Transformation Office, Maintenance Manager
- **Purpose:** Govern AI model health, adoption, and bias checks.
- **Widgets:**

| Widget ID | Type | Metric | Source | Update | Drill-down | Alert |
|-----------|------|--------|--------|--------|------------|-------|
| AI-KPI-01 | Number | Predictions Generated (24h) | `AI Insight Log` | Hourly | `AI Insight Log` list | < 50 indicates pipeline issue |
| AI-KPI-02 | Number | Actions Taken (24h) | `AI Insight Log.action_taken` | Hourly | `Maintenance Work Order` or `Operations Event` | Adoption < 60% warning |
| AI-CH-01 | Line | Model Accuracy Trend | `AI Model Registry.validation_accuracy` | Daily | `AI Model Registry` form | Accuracy drop >5% triggers retrain |
| AI-TBL-01 | Table | Insight backlog (unacknowledged) | `AI Insight Log.status = "New"` | Hourly | `AI Insight Log` detail | > 25 escalate |

- **Filters:** `model_id`, `prediction_type`, `vehicle`
- **Alerts:** Auto-create ticket if backlog > 20 for >2 hours.

---

### 3.13 Business Review Snapshot
The outline below recaps every dashboard using simple business language. Each entry calls out the widgets and why they matter so reviewers can focus on outcomes, not tooling.

- **Executive Overview**
  - *Headline cards:* Vehicle Utilization %, Revenue per Vehicle-Day, On-Time Delivery % (daily pulse on growth and reliability).
  - *Charts:* Margin vs Cost Mix (see whether profits are healthy), Revenue Flow by Business Line (understand which divisions pull weight).
  - *Table:* Top 10 Vehicles by Margin (high-performers for recognition or duplication).
- **Operations Live Map & Control**
  - *Map:* Live vehicle locations and status (spot delays instantly).
  - *Queue table:* List of emerging issues ranked by urgency.
  - *Headline cards:* Vehicles currently on the road, Average delay minutes.
- **Fleet Utilization & Availability**
  - *Headline card:* Fleet availability % (readiness to serve orders).
  - *Charts:* Downtime by reason, Utilization heatmap by day/hour (identify bottlenecks and slow periods).
  - *Table:* Vehicles idle more than 48h (reassignment or disposal candidates).
- **Vehicle Profitability**
  - *Headline cards:* Average margin %, Tyre cost per kilometer (financial efficiency lens).
  - *Charts:* Revenue-to-net margin waterfall, Margin trend (month-on-month health).
  - *Tables:* Top earners, Vehicles with high tyre spend (targeted interventions).
- **Tyre Intelligence**
  - *Gauge:* Average tyre health (safety and maintenance readiness).
  - *Headline card:* Tyres needing replacement within a week.
  - *Charts:* Tyre cost per kilometer trend, Sensor temperature heatmap (spot wear and tear).
  - *Table:* Sensors offline more than 10 minutes (keep monitoring live).
- **Predictive Maintenance**
  - *Headline card:* Predicted failures in next 7 days (forward-looking risk).
  - *Table:* Vehicles at highest risk with confidence scores and key factors.
  - *Chart:* Risk by subsystem (engine, tyres, etc.) to focus maintenance plans.
- **Safety & Incidents**
  - *Headline cards:* Incident frequency rate, Open spot checks (compliance posture).
  - *Charts:* Daily incident trend, Route-based incident hotspots.
- **Cargo Operations**
  - *Headline cards:* On-time and in-full %, LTL vs FTL ratio (service level vs profitability mix).
  - *Table:* Loads pending customs clearance (flag revenue at risk).
  - *Chart:* Flow of goods from origin to destination hubs (balance network).
- **Passenger Operations**
  - *Headline cards:* Seat occupancy ratio, Cancellation rate (demand and satisfaction signals).
  - *Chart:* Fare revenue trend (growth trajectory).
  - *Table:* Top routes by revenue (where to invest or market).
- **Finance Ledger**
  - *Headline cards:* Total revenue and costs month-to-date.
  - *Chart:* Currency impact on results (FX exposure).
  - *Table:* Customers owing more than 30 days (collections focus list).
- **Compliance & Documents**
  - *Headline cards:* Driver licences expiring soon, Overdue insurance (regulatory guardrail).
  - *Table:* Policy obligations with owners and status (action tracker).
  - *Chart:* Ageing of compliance tasks by department (see lagging areas).
- **AI Center**
  - *Headline cards:* Predictions generated vs actions taken (adoption score).
  - *Chart:* Model accuracy trend (trust level in AI outputs).
  - *Table:* Unacknowledged insights (follow-up backlog).

## 4. KPI Catalog
The 21 KPIs below are prioritized from executive visibility through operations execution. Each entry lists the exact data sources and includes pseudo SQL or calculation hints. Refer to `insights/kpis.json` for machine-readable definitions.

| # | KPI Name | Definition | Primary DocTypes & Fields | Window | Thresholds (Green / Yellow / Red) | Drill-down | Query / Formula Sketch |
|---|----------|------------|---------------------------|--------|----------------------------------|------------|------------------------|
| 1 | Vehicle Utilization % | `(Transit Minutes ÷ Available Minutes) × 100` | `Movement Log.status`, `from_timestamp`, `to_timestamp`; `Operation Plan.planned_start`, `planned_end` | Day | ≥85 / 75-84 / <75 | `Movement Log` filtered by vehicle & day | `SELECT vehicle, SUM(transit_minutes)/SUM(available_minutes)*100 ...` |
| 2 | Fleet Availability % | `Available Vehicles ÷ Total Active Vehicles × 100` | `Vehicle.status`, `Maintenance Work Order.status` | Day | ≥90 / 80-89 / <80 | `Vehicle` list `status = Available` | `WITH downtime AS (...) SELECT ...` |
| 3 | Average Turnaround Time | `Avg(delivery_ts - pickup_ts)` for completed trips | `Movement Log.pickup_ts`, `delivery_ts` | Rolling 7d | ≤6h / 6-8h / >8h | `Movement Log` query report | `SELECT AVG(TIMESTAMPDIFF(MINUTE, pickup_ts, delivery_ts)) ...` |
| 4 | On-Time Delivery % | `On-time Deliveries ÷ Total Deliveries × 100` | `Movement Log.actual_delivery_ts`, `Operation Plan.expected_arrival` | Day | ≥95 / 90-94 / <90 | `Operations Service Level` report | `SUM(CASE WHEN actual<=expected THEN 1 END)/COUNT(*)` |
| 5 | In-Transit Vehicles | `COUNT(status = "In Transit")` | `Movement Log.status` | Real-time | ≥ Planned / < Planned-10% / < Planned-20% | `Movement Log` list | `SELECT COUNT(*) ... WHERE status='In Transit'` |
| 6 | Tyre Health Index Avg | `AVG(Tyre.health_index)` | `Tyre.health_index` | 5 min | ≥80 / 65-79 / <65 | `Tyre` list sorted by health | `SELECT AVG(health_index) FROM tabTyre ...` |
| 7 | Tyre Cost per Km | `(Tyre costs ÷ KM driven)` | `Cost & Revenue Ledger.asset`, `amount`; `Movement Log.distance_km`; `Tyre Installation Log.vehicle` | Month | ≤25 / 26-35 / >35 | `Tyre Cost Breakdown` report | `SUM(costs)/SUM(distance_km)` grouped by tyre/vehicle |
| 8 | Predictive Failure Risk Score | `MAX(confidence)` of failure predictions per vehicle | `AI Insight Log.prediction_type`, `confidence`, `vehicle` | Hour | ≤0.4 / 0.41-0.7 / >0.7 | `AI Insight Log` record | `SELECT vehicle, MAX(confidence) ... WHERE prediction_type='failure'` |
| 9 | Maintenance Backlog | `COUNT(Work Orders status in {Open, Scheduled})` | `Maintenance Work Order.status` | Day | ≤15 / 16-30 / >30 | `Maintenance Work Order` list | `SELECT COUNT(*) FROM ... WHERE status IN (...)` |
| 10 | Mean Time Between Failures (MTBF) | `Avg time between `Maintenance Work Order` close events` | `Maintenance Work Order.closed_on`, `asset` | Rolling 90d | ≥45d / 30-44d / <30d | `Maintenance Work Order` timeline | `SELECT asset, AVG(DATEDIFF(next_failure, prev_failure)) ...` |
| 11 | Fuel Efficiency (km/l) | `SUM(distance_km) ÷ SUM(fuel_liters)` | `Fuel Log.liters`, `Movement Log.distance_km` | Week | ≥4.5 / 3.5-4.4 / <3.5 | `Fuel Log` report | `SELECT vehicle, SUM(distance_km)/SUM(liters) ...` |
| 12 | Revenue per Vehicle-Day | `SUM(net_revenue) ÷ active vehicle-days` | `Cost & Revenue Ledger`, `ins_ops_vehicle_daily.active_flag` | Day | ≥₦180k / 150k-179k / <150k | `Vehicle Profitability Detail` | `SELECT vehicle, SUM(revenue-cost)/COUNT(active_day)` |
| 13 | Gross Margin % | `(Revenue - Direct Cost) ÷ Revenue × 100` | `Cost & Revenue Ledger.account` | Month | ≥22 / 18-21 / <18 | `Cost & Revenue Ledger` ledger | `SELECT vehicle, ((rev-cost)/rev)*100 ...` |
| 14 | Outstanding Compliance Items | `COUNT(Document Checklist Item.status = "Open")` | `Document Checklist Item`, `Driver Qualification` | Day | ≤10 / 11-20 / >20 | `Document Checklist Item` | `SELECT entity_type, COUNT(*) ... WHERE status='Open'` |
| 15 | Incident Frequency Rate | `(Incidents ÷ Completed Trips) × 100` | `Incident Report`, `Movement Log.status` | Month | ≤1.5 / 1.5-2.0 / >2.0 | `Incident Report` list | `SELECT (COUNT(incident)/COUNT(trip))*100 ...` |
| 16 | Driver Risk Score | Weighted blend of incidents, spot checks, fatigue | `Incident Report.driver`, `Spot Check.findings`, `AI Insight Log.prediction_type='driver_risk'` | Week | ≤30 / 31-50 / >50 | `Driver` form with risk section | `score = (incidents*15)+(spot_findings*10)+(ai_score*60)` |
| 17 | Cargo OTIF Rate | `On time + full deliveries ÷ total cargo deliveries` | `Cargo Consignment.expected_delivery_date`, `actual_delivery_date`, `delivered_qty`, `ordered_qty` | Week | ≥95 / 90-94 / <90 | `Cargo Consignment` list | `SELECT SUM(CASE WHEN ... )/COUNT(*) ...` |
| 18 | Passenger Occupancy Ratio | `Seats sold ÷ capacity` | `Passenger Trip.booked_seats`, `capacity` | Day | ≥80 / 65-79 / <65 | `Passenger Trip` list | `SELECT route, SUM(booked)/SUM(capacity) ...` |
| 19 | AI Insight Adoption Rate | `Actions taken ÷ insights generated` | `AI Insight Log.action_taken`, `status` | Day | ≥75 / 60-74 / <60 | `AI Insight Log` | `SELECT SUM(action_taken)/COUNT(*) ...` |
| 20 | Carbon Emissions per Km | `Total CO₂e ÷ distance` | `Emissions Log.co2e_amount`, `Movement Log.distance_km` | Month | ≤1.2 / 1.2-1.5 / >1.5 | `Emissions Log` report | `SELECT SUM(co2e)/SUM(distance) ...` |
| 21 | Sensor Data Freshness | `Now() - last_packet_ts` minutes | `Tyre Sensor Data.last_packet_ts`, `Vehicle Telemetry Log.timestamp` | 5 min | ≤5 / 6-10 / >10 | `Tyre Sensor Data` list | `SELECT vehicle, TIMESTAMPDIFF(MINUTE, MAX(last_packet_ts), NOW()) ...` |

---

## 5. Charts & Visual Patterns
- **Time-series (Line/Area):** Vehicle uptime, incidents per day, fuel efficiency. Recommend Chart.js or Frappe Charts with `time_series: true` and rolling average overlays.
- **Heatmaps/Geo maps:** Route congestion using Mapbox GL JS. Data from `Movement Log` aggregated to road segments. Provide tile overlay for high-density points.
- **Sankey:** Cargo flow from origin → hub → destination via ECharts `sankey` option. Frappe Insights mapping uses chart type `custom` with dataset edges.
- **Waterfall:** Display cost composition (Revenue → Direct Costs → Tyre Costs → Net Margin). Use Plotly waterfall or Frappe custom chart.
- **Gauge:** Tyre Health Index gauge with color stops (0-50 red, 50-65 amber, 65-100 green). For Insights, wrap Chart.js gauge plugin; for PWA, reuse same dataset via REST endpoint `/api/method/tems.tems_insights.api.get_metric?metric=tyre_health_index`.
- **Example mapping:**
```json
{
  "chart_name": "chart_vehicle_uptime",
  "type": "line",
  "dataset": {
    "query": "chart_vehicle_uptime",
    "x_field": "operating_date",
    "y_fields": ["uptime_pct", "rolling_7d_avg"],
    "time_series": true
  },
  "options": {"fill": false, "tension": 0.3}
}
```

---

## 6. Drill-down UX Patterns
- **Number card → List → Form:** Clicking a number card opens a list view with filters (e.g., `Vehicle Profitability Detail` Query Report). Selecting a row navigates to the relevant DocType form (`Vehicle`, `Operation Plan`).
- **Chart segment → Modal:** Chart segments (bar/slice) trigger a modal displaying top N contributing records using a secondary query (e.g., top delayed routes). Provide `onSelect` callback hooking into `frappe.set_route`.
- **Map pin → Quick-action panel:** Map markers show status, ETA, driver contact. Provide buttons: `Call Driver` (tel link), `Reassign Vehicle` (opens `Operation Plan` with pre-filled substitute), `View History` (navigates to timeline view).
- **Alerts panel → Action buttons:** Alerts list shows rule name, severity, timer. Buttons: `Acknowledge` (updates `AI Insight Log.status`), `Send Message` (invokes `frappe.call` to push notification), `Reassign` (launches workflow for `Operation Plan`).

---

## 7. Alerts & Notification Rules
Sample alert catalogue (configure in `tems.tems_insights.alerts`):
- **Revenue Slump Alert**
  - Trigger: Revenue per Vehicle-Day drops >15% vs 7-day average.
  - Severity: High. Recipients: Finance Manager, TEMS Executive.
  - Channel: Email + Teams. Auto-action: Create `Operations Event` tagged `Revenue Investigation`.
- **Tyre Health Critical**
  - Trigger: Tyre Health Index < 50 for >15 minutes.
  - Severity: Critical. Recipients: Tyre Manager, Maintenance Lead.
  - Channel: SMS + In-app alert. Auto-action: Create `Maintenance Work Order` with `priority = High`.
- **Incident Spike**
  - Trigger: Incident Frequency Rate > 2 per 100 trips within 24h window.
  - Severity: High. Recipients: Safety Manager, Operations Manager.
  - Channel: Slack. Auto-action: Pause new dispatch on affected routes (set `Operation Plan.allow_dispatch = 0`).
- **Sensor Offline**
  - Trigger: Sensor Data Freshness > 10 minutes.
  - Severity: Medium. Recipients: IoT Admin, Fleet Officer.
  - Channel: Email. Auto-action: Create `Maintenance Work Order` with task `Check sensor`.
- **AI Insight Backlog**
  - Trigger: Unacknowledged AI Insights > 20 for >2 hours.
  - Severity: Medium. Recipients: AI Lead, Maintenance Manager.
  - Channel: In-app. Auto-action: Escalate to Transformation Office after 4 hours.

Alerts run via `scheduler_events.hourly` and via stream processors for real-time events.

---

## 8. AI-Driven Insights
- **Dashboards showing AI outputs:** Predictive Maintenance, AI Center, Executive Overview (predicted failure overlay), Fleet Utilization (risk badge).
- **Explainability:** Each AI card displays `confidence` and top 3 features (e.g., `tyre_wear`, `oil_temperature`, `distance_since_service`). Provide `Why?` link opening a modal with SHAP-style contributions stored in `AI Insight Log.feature_importance_json`.
- **Insight card template:**
```json
{
  "title": "Predicted Failure: {vehicle}",
  "body": "{confidence}% chance of drivetrain failure within {window_days} days.",
  "footer": "Top factors: {top_factors}",
  "actions": [
    {"label": "Create Work Order", "action": "create_maintenance_work_order", "payload": {"vehicle": "{vehicle}"}},
    {"label": "Acknowledge", "action": "update_insight_status", "payload": {"status": "Acknowledged"}}
  ]
}
```
- **Refresh cadence:**
  - Failure predictions: hourly incremental runs (`tasks.generate_fleet_maintenance_predictions`).
  - Driver risk scores: every 6 hours.
  - Financial forecasts: nightly.
- **Retraining schedule:** Weekly retrain job (`tasks.retrain_models_weekly`) with holdout evaluation; manual trigger available via `bench execute tems.tems_ai.tasks.retrain_models_weekly`.

---

## 9. Implementation Checklist
- **Query Reports:** Implement the five SQL-based reports provided under `insights/query_reports/` (Operations Live Status, Vehicle Profitability Detail, Tyre Cost Trend, Incident Root Cause, Passenger Load Factor). Use `bench --site <site> execute` to validate SQL in sandbox mode.
- **Insights Models:** Create dashboards via Frappe Insights UI, then export JSON fixtures to `insights/sample_dashboards/`. Register them in `hooks.py` fixtures list when finalized.
- **KPI Cache:** Schedule nightly `tems.tems_insights.tasks.refresh_kpi_cache` and 5-minute incremental updates for high-churn metrics (utilization, health index).
- **Deployment Fixtures:**
  1. Roles/Workspaces (existing TEMS fixtures)
  2. Query Reports (`bench --site <site> export-fixtures --records "Report"`)
  3. Dashboard JSON exports (`Insights Dashboard` DocType)
- **Data Retention & Archiving:**
  - Telemetry > 90 days: archive to object storage.
  - AI insight log > 365 days: summarize and purge detail.
  - Compliance records: retain 5 years per regulatory requirement.
- **Performance Tuning:**
  - Pre-aggregate nightly; maintain covering indices on `vehicle`, `posting_date`, `status` fields.
  - Cache number cards via Redis with TTL (5 min for ops, 60 min for financials).
  - Use pagination/infinite scroll for tables over 500 rows; default sort by severity or delta.
- **Testing:**
  - Unit tests for KPI calculations under `tems/tems_insights/tests/test_kpis.py`.
  - Visual tests by product managers using `CHECKLIST.md` steps.
  - Load test SocketIO map streaming when >500 vehicles simultaneously.

---

## 10. Appendix
- **Artifacts delivered:**
  - `docs/INSIGHTS_GUIDE.md` (this guide)
  - `insights/kpis.json` (machine-readable KPI catalog)
  - `insights/sample_dashboards/*.json` (three dashboard templates)
  - `insights/query_reports/*.json` (five query report definitions)
  - `CHECKLIST.md` (product manager validation list)
- **Supporting modules:** `tems_insights`, `tems_operations`, `tems_fleet`, `tems_tyre`, `tems_ai`, `tems_finance`, `tems_safety`.
- **Future enhancements:** integrate predictive ETA heatmaps, incorporate real-time weather overlays, automate ROI per trade lane.

> _Remember_: after importing fixtures run `bench --site <site> migrate`, `bench build`, `bench clear-cache`, and test `scheduler` health to ensure all insights stay fresh.
