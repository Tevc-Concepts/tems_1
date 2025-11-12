# TEMS Insights Deployment Validation Checklist

Use this checklist after importing dashboards, KPI cards, and query reports into the target site. Sign off each section with initials and date.

## 1. Pre-requisites
- [ ] Bench updated to latest `tems` app commit (git pull + bench build)
- [ ] Site migrated (`bench --site <site> migrate`) and cache cleared
- [ ] Scheduler enabled and running (`bench --site <site> doctor` reports healthy)

## 2. Fixtures & Reports
- [ ] Uploaded query reports (`Operations Live Status`, `Vehicle Profitability Detail`, `Tyre Cost Trend`, `Incident Root Cause Breakdown`, `Passenger Load Factor`)
- [ ] Each report executes without SQL errors using the default 7-day filter window
- [ ] Insights dashboard JSON imported (`Executive Overview`, `Vehicle Profitability`, `Tyre Intelligence`)

## 3. KPI Verification
- [ ] KPI cache refresh job executed (`tems.tems_insights.tasks.refresh_kpi_cache`)
- [ ] Spot-check `Vehicle Utilization %` vs manual calculation for one vehicle
- [ ] Spot-check `Tyre Cost per Km` against finance ledger for one vehicle-month
- [ ] Spot-check `Passenger Occupancy Ratio` against passenger trip list

## 4. Dashboard Rendering
- [ ] Executive Overview loads within 3 seconds on Desk
- [ ] Operations Live Map displays active vehicles (SocketIO channel connected)
- [ ] Vehicle Profitability waterfall chart shows correct labeling
- [ ] Tyre Intelligence gauge updates when sample tyre record revised

## 5. Drill-down Paths
- [ ] KPI click navigates to expected list/report for Executive Overview
- [ ] Map pin opens quick-action modal with driver contact options
- [ ] Table rows open the matching DocType form (`Vehicle`, `Tyre`, `Passenger Trip`)

## 6. Alerts & Notifications
- [ ] Alert rules configured in `tems.tems_insights.alerts` DocType
- [ ] Trigger test alert for `Tyre Health Critical` and confirm message delivery
- [ ] AI insight backlog alert escalates after threshold breach (set via test data)

## 7. PWA Validation
- [ ] Operations PWA consumes `kpi_vehicle_utilization` endpoint successfully
- [ ] Driver PWA shows assigned insights cards for tyre replacements
- [ ] Safety PWA renders incident trend chart with new data

## 8. Sign-off
- Product Manager: ____________________ Date: __________
- Operations Lead: ____________________ Date: __________
- Finance Lead: ______________________ Date: __________
