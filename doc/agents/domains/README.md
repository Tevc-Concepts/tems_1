# TEMS Domain Agents Orchestration Guide

This guide explains how to use the **13 DomainAgent files** to build the full Enterprise Transport Management System (TEMS) inside the `tems` app on Frappe v15+.

---

## 📋 Domains (Modules)
1. Governance (Leadership & Compliance)
2. HRMS (People & Competency)
3. Fleet & Asset Management
4. Safety & Risk Management
5. Cross-Border Trade Management
6. Informal Economy Integration
7. Climate Resilience & ESG
8. Finance & Accounting
9. CRM & Customer Operations
10. Supply Chain & Procurement
11. Document & Drive
12. Analytics & Insights
13. **Operations (NEW)**

---

## 🔄 Build Sequence
1. **Start with Governance** → set Vision, Policies, Compliance structure.
2. **HRMS** → build workforce competency and driver/technician records.
3. **Fleet** → build asset tracking, maintenance, availability.
4. **Safety** → layer journey planning, risk, and incident reporting.
5. **Operations** → integrate all modules into 4P logistics execution:
   - Plan trips and vehicle allocation.
   - Assign drivers and vehicles.
   - Track movement states (Check-In, Transit, Diversion, etc.).
   - Calculate cost & revenue per order.
6. **Finance** → handle costing, billing, multi-currency accounts.
7. **CRM** → manage customers, orders, SLAs.
8. **Supply Chain** → procure parts, suppliers, inventory.
9. **Trade** → enable cross-border compliance and FX.
10. **Informal** → onboard informal operators and community logistics.
11. **Climate** → add weather, emissions, renewable planning.
12. **Documents** → centralize docs and compliance evidence.
13. **Insights** → pull all data together for dashboards, KPIs, AI-driven reporting.

---

## ⚡ Usage Instructions
- Each Agent file (`<DomainName>Agent.md`) defines: ROLE, TASKS, CONSTRAINTS, INTER-RELATIONSHIPS, OUTPUTS.
- To use:
  1. Open `<DomainName>Agent.md`.
  2. Paste it into Copilot/GPT-5 as context.
  3. Ask: “Build the `<DomainName>` module according to this instruction. Output DocTypes, Workspaces, hooks, and tests.”
  4. Place generated code in `apps/tems`.
  5. Commit outputs in GitHub under correct folders (`doctype/`, `config/desk_workspace/`, `tests/`, etc.).

---

## 🔗 Data Triangulation Highlights
- **Operations** sits at the center → consumes HR, Fleet, CRM, Finance, Safety, Supply Chain, and Trade data.
- **Finance** ties all cost and revenue points.
- **Insights** consolidates everything for decision-making.

---

## ✅ Best Practices
- Keep **all code inside TEMS app** (no edits to ERPNext/HRMS core).
- Use **fixtures** for Roles, Workspaces, Reports.
- Ensure each module includes **unit tests**.
- After building each domain, run `bench migrate`, `bench build`, and `bench clear-cache`.
- Always validate cross-domain links (e.g., Operations → Fleet + CRM + Finance).

---
