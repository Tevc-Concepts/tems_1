Perfect 👌 — here’s the **`README.md` Agent Orchestration Guide** for your `/agents` folder. It explains **the roles of each Agent.md**, the **sequence of use**, and **how they interconnect** across the TEMS lifecycle.

---

# 📖 TEMS Agent Orchestration Guide

This guide explains how to use the specialized AI Agents (`*.md` files) to build, extend, and maintain the **Transport Excellence Management System (TEMS)** on **Frappe/ERPNext v15+**.

Each Agent.md defines **role, tasks, constraints, inter-relationships, and outputs**. Together, they ensure a **clean, modular, and consistent build lifecycle**.

---

## 🛠️ Agents Overview

| Agent File              | Role                                             | Primary Outputs                         |
| ----------------------- | ------------------------------------------------ | --------------------------------------- |
| **ArchitectAgent.md**   | System design, module mapping, hooks             | ERD, Module map, hooks.py skeleton      |
| **DomainAgent.md**      | Business domain module builder                   | DocTypes, Workspaces, Unit tests        |
| **UIAgent.md**          | Desk Workspaces, Pages, Styling                  | Workspaces JSON, CSS, Dashboards        |
| **IntegrationAgent.md** | External APIs (USSD, Mobile Money, GPS, Weather) | API scripts, Scheduler jobs             |
| **DataAgent.md**        | Analytics, KPIs, Reporting, AI models            | Insights dashboards, Predictive scripts |
| **TestAgent.md**        | QA, Unit tests, Smoke tests                      | Test files, Data seeds, CI test runs    |
| **DeployAgent.md**      | Deployment, CI/CD, Migration patches             | DEPLOY.md, CI config, Patch files       |

---

## 🔄 Build Lifecycle Orchestration

### **Step 1: Architecture Setup**

* Start with **ArchitectAgent.md**.
* Define system ERD, dependencies, and core hooks.
* Output: `TEMS_ERD.md`, `Module_Map.md`, initial `hooks.py`.

---

### **Step 2: Domain Module Development**

* Use **DomainAgent.md** for each business module (Governance, People, Fleet, Safety, Trade, Informal, Climate, Finance, CRM, Supply Chain, Docs, Insights).
* Each run generates DocTypes, fixtures, and tests.
* Ensure **Link fields** across modules (e.g., Journey → Driver → Vehicle → Costing).

---

### **Step 3: UI & Workspace Customization**

* Run **UIAgent.md** to build Workspaces for each role (Executive, Fleet Manager, Safety Officer, etc.).
* Style with `tems_theme.css`.
* Output: role dashboards, Insights widgets, Desk pages.

---

### **Step 4: Integrations**

* Use **IntegrationAgent.md** for APIs: Mobile Money, USSD, GPS, Weather.
* Scheduler jobs configured in `hooks.py`.
* Outputs: API modules in `tems/api/`.

---

### **Step 5: Analytics & Insights**

* Run **DataAgent.md** to build dashboards and predictive reports.
* Export Insights dashboards as fixtures.
* Outputs: KPI Config, Report Subscription, analytics scripts.

---

### **Step 6: Testing**

* Use **TestAgent.md** to generate:

  * Unit tests (`tems/tests/test_*.py`)
  * Smoke tests for new installs
  * Test fixtures (patches/test_data)
* Validate offline-first behavior, inter-module data flow, and reporting triangulation.

---

### **Step 7: Deployment**

* Finish with **DeployAgent.md**.
* Outputs: `DEPLOY.md`, patch files, CI/CD scripts.
* Automate: `bench migrate`, `bench build`, and scheduled job health checks.

---

## 📊 Data Triangulation Principle

At each stage, ensure **cross-domain linking** for proper reporting:

* **Driver Performance** → HR (training) + Fleet (uptime) + Safety (incidents) + Finance (cost).
* **Journey Risk** → Safety (incidents) + Climate (weather) + Governance (policies).
* **Asset Lifecycle Cost** → Fleet (utilization) + Finance (TCO) + Procurement (spares).
* **Compliance Report** → Trade (tariffs) + Governance (audits) + Finance (fees).
* **Carbon/ESG** → Fleet (fuel/EV) + Climate (emissions) + Finance (credits).

---

## ⚡ How to Use the Agents

1. Open the `.md` file for the agent you need.
2. Paste the **TASK/CONSTRAINTS/OUTPUTS** into VS Code Copilot or GPT-5.
3. Run the generated code inside the `tems` app.
4. Commit outputs to GitHub in structured folders:

   ```
   tems/doctype/*
   tems/config/desk_workspace/*
   tems/public/css/tems_theme.css
   tems/api/*
   tems/tests/*
   tems/patches/*
   ```

---

## ✅ Best Practices

* Keep **all customizations inside `apps/tems`**.
* Use **fixtures** for Roles, Workspaces, Custom Fields.
* Never modify ERPNext/HRMS/Drive/Insights core directly.
* Test cross-module data flow with **TestAgent** before deploy.
* Document every module in `/docs` for governance & audits.

---

## 🚀 Final Note

This Agent-based workflow ensures **focus + modularity**:

* **Architect** designs →
* **Domain** builds →
* **UI** personalizes →
* **Integration** connects →
* **Data** reports →
* **Test** validates →
* **Deploy** delivers.
