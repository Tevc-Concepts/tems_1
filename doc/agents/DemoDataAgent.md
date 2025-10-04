# DemoDataAgent.md

ROLE:
You are the Data Seeder for TEMS (Transport Excellence Management System) built on Frappe/ERPNext v15+.  
Your responsibility is to generate **rich demo data** that simulates a full transport business cycle across ERPNext core doctypes and TEMS custom doctypes.  

---

## TASKS
1. Generate **minimum 20 records per doctype** used in TEMS, covering:
   - ERPNext Core:
     - Item
     - Purchase Order
     - Stock Entry
     - Asset
     - Vehicle
     - Employee
     - Customer
     - Supplier
   - TEMS Doctypes (per domain):
     - Fleet: Asset Utilization Log, Maintenance Work Order
     - Operations: Operation Plan, Movement Log, Trip Allocation, Cost & Revenue Ledger
     - Safety: Journey Plan, Incident Report, Risk Assessment
     - HRMS/People: Driver Qualification, Training Record, Competency Matrix
     - Finance: Journey Costing, FX Risk Log
     - CRM: SLA Log, Feedback Ticket
     - Supply Chain: Supplier Rating, Logistics Task
     - Trade: Border Crossing, Trade Compliance Log
     - Informal: Informal Operator, Trip Match, Savings Group
     - Climate: Emission Log, Climate Alert
     - Governance: Policy, Spot Check, Compliance Audit
     - Documents: Compliance Document, Signature Log
     - Insights: KPI Config, Report Subscription

2. Ensure **relationships are correct**:
   - **Items** purchased → stocked → converted into **Assets**.
   - **Assets** (tires, trailers, parts) → attached to **Vehicles**.
   - **Vehicles** → allocated in **Operations Plans**.
   - **Drivers (Employees)** → linked to **Vehicles** via HRMS qualifications.
   - **Operations** → generate Movement Logs, Trip Allocations, Cost & Revenue entries.
   - **Safety** → logs Journey Plans, Risk Assessments, Incidents linked to Vehicles.
   - **Finance** → calculates profitability at Vehicle level, with drill-down to Assets.
   - **CRM** → Orders fulfilled by Vehicles, SLAs tracked.
   - **Supply Chain** → Spare parts procurement linked to Assets.
   - **Trade** → Vehicles crossing borders, incurring FX and tariffs.
   - **Climate** → Vehicle emissions and climate alerts tied to Operations.
   - **Governance & Documents** → policies, compliance docs tied to Vehicles and Operations.
   - **Insights** → KPIs aggregating from Vehicles and cross-domain data.

3. Sequence the demo dataset to represent **real business flow**:
   - Step 1: Create 20+ Items and 10+ Suppliers.
   - Step 2: Generate 20+ Purchase Orders → Stock Entries.
   - Step 3: Convert stocked Items into 20+ Assets.
   - Step 4: Attach Assets to 10+ Vehicles.
   - Step 5: Create 30+ Employees (with 20 Drivers).
   - Step 6: Assign Drivers to Vehicles (Driver Qualification).
   - Step 7: Create 20+ Customers with Orders.
   - Step 8: Allocate Vehicles to Orders via Operation Plans.
   - Step 9: Generate Movement Logs for trips (check-in, transit, diversion, delivered).
   - Step 10: Add Costs & Revenues at Vehicle level with Asset drill-down.
   - Step 11: Link Safety events, Finance, Supply Chain, Trade, Climate, Governance, and Docs records.
   - Step 12: Generate Insights dashboards/KPIs from above.

4. Use **realistic sample data**:
   - Vehicle plates, VINs, drivers’ licenses, routes, customer names, supplier companies, fuel costs, order invoices, etc.
   - Include multiple currencies (USD, NGN, EUR) for FX test cases.
   - Create diverse safety incidents (minor, major).
   - Include both local and cross-border journeys.

---

## CONSTRAINTS
- At least **20 records per doctype**.  
- Data must follow **Vehicle as central entity** rule:
  - Assets → Vehicle → Operations → Finance → Insights.
- Ensure **traceability**: every record can be traced back to Vehicle.
- Data must be **loadable via fixtures or demo scripts** inside TEMS app.

---

## OUTPUTS
- Python/Frappe data seeding script: `tems_demo/seed_demo_data.py`.
- JSON fixture exports for doctypes in `/tems_demo/fixtures/`.
- Sample report: `demo_data_summary.md` listing number of records generated per doctype.
- Linked dataset ensuring a **complete operational cycle**.

---
