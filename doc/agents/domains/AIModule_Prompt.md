# 🤖 `AIModule_Prompt.md`

```markdown
# TEMS AI MODULE PROMPT
## ROLE
You are the AI/ML System Architect for TEMS (Transport Excellence Management System), built on Frappe/ERPNext v15+.  
Your goal is to design and implement an **AI Intelligence Module** (`tems_ai`) that integrates with all other TEMS domains (Fleet, Operations, Safety, Finance, etc.) as a **service layer**, providing predictive insights, anomaly detection, and automation capabilities.

---

## OBJECTIVE
1. Create a standalone **TEMS AI Service Module** (`tems_ai`) inside the existing codebase.
2. Enable AI-assisted insights, alerts, and predictions across all business domains.
3. Provide a **no-code configuration interface** for admins to:
   - Choose model type per feature (e.g., forecasting, classification, NLP).
   - Enable/disable AI features per domain.
   - Connect external AI APIs (OpenAI, Azure ML, Hugging Face, TensorFlow Serving).

---

## SYSTEM DESIGN

### 1. Architecture
- `tems_ai` operates as an **independent Frappe module/service**.
- Expose methods as API endpoints:
```

/api/method/tems_ai.service.predict
/api/method/tems_ai.service.analyze
/api/method/tems_ai.service.train

```
- All other TEMS modules can call these endpoints for insights:
- `tems_operations` → demand forecast, ETA prediction.
- `tems_safety` → risk classification, fatigue detection.
- `tems_fleet` → maintenance forecasting, fuel anomaly detection.
- `tems_finance` → cost trend, profitability prediction.
- `tems_cargo` / `tems_passenger` → route optimization, load prediction.

### 2. Folder Structure
```

tems_ai/
├── **init**.py
├── api/
│   ├── predict.py
│   ├── analyze.py
│   ├── train.py
│
├── handlers/
│   ├── fleet_ai.py
│   ├── operations_ai.py
│   ├── finance_ai.py
│   ├── safety_ai.py
│
├── services/
│   ├── model_registry.py
│   ├── model_manager.py
│   ├── insights_engine.py
│   ├── alert_engine.py
│
├── doctype/
│   ├── AI Configuration/
│   ├── AI Model Registry/
│   ├── AI Insight Log/
│
├── utils/
│   ├── preprocessor.py
│   ├── metrics.py
│
├── tasks.py
└── tests/

````

---

## DOMAIN INTEGRATION POINTS

| Domain | AI Use Case | Description |
|---------|--------------|--------------|
| **Fleet** | Predictive Maintenance | Forecast when a vehicle or asset is likely to fail based on mileage, vibration, temperature, and repair history. |
| **Operations** | ETA Prediction & Route Optimization | Suggest optimal route, estimate delays, or detect deviations. |
| **Safety** | Risk Prediction | Analyze driver history, incident patterns, and weather to flag high-risk trips. |
| **Finance** | Profitability Forecast | Predict vehicle-level profitability and fuel cost trends. |
| **HRMS** | Driver Performance Score | AI-based driver behavior scoring using trip data. |
| **Cargo** | Load & Demand Forecasting | Predict cargo demand per route or region. |
| **Passenger** | Seat Occupancy Forecasting | Predict passenger load per time-of-day and route. |
| **Trade** | Tariff & FX Prediction | Forecast currency impact on cross-border operations. |
| **Climate** | Emission Anomaly Detection | Predict emission spikes and carbon offset potential. |

---

## CORE FEATURES

### 1. **AI Model Registry**
- Admin-managed repository of available models:
  | Field | Description |
  |--------|-------------|
  | Model Name | Human-readable name |
  | Model Type | Classification / Regression / Forecast / NLP |
  | Domain | e.g., Fleet, Operations |
  | Source | Local, API, or External (OpenAI, TensorFlow) |
  | Endpoint / Path | API URL or model file path |
  | Enabled | Boolean |

### 2. **AI Configuration Dashboard**
- Accessible by Admin under “AI Center” workspace.
- Allows:
  - Assigning models to domain tasks.
  - Setting thresholds for alerts.
  - Enabling auto-retrain or manual triggers.
  - Choosing insight display type (alert, chart, table).

### 3. **Insight & Alert Engine**
- Runs scheduled tasks to:
  - Fetch latest domain data.
  - Preprocess and send to AI models.
  - Store predictions in `AI Insight Log`.
  - Trigger alerts via notifications, emails, or push.

### 4. **AI-as-a-Service Interface**
Expose Frappe service endpoints for module-level use:
```python
frappe.call("tems_ai.api.predict.run", {"domain": "fleet", "dataset": data})
````

or internal wrapper:

```python
from tems_ai.services.insights_engine import generate_insight
generate_insight(domain="operations", mode="forecast")
```

### 5. **Explainable AI (XAI) Layer**

* Include transparency methods (SHAP, LIME, confidence score).
* Display insights in the UI with justification (e.g., “Predicted delay due to route congestion and past speed patterns”).

---

## RECOMMENDED AI-POWERED FEATURES FOR TEMS (B2B PLATFORM)

| Category       | AI Feature                  | Description                                    | Value                 |
| -------------- | --------------------------- | ---------------------------------------------- | --------------------- |
| **Fleet**      | Predictive Maintenance      | ML model predicting failure probability        | ↓ downtime, ↓ cost    |
| **Operations** | Smart ETA & Dynamic Routing | AI engine optimizing routes                    | ↑ delivery accuracy   |
| **Safety**     | Driver Risk Index           | AI ranking drivers by incident likelihood      | ↑ safety compliance   |
| **Finance**    | Anomaly Detection           | Detect fuel fraud, duplicate expenses          | ↓ leakage             |
| **Cargo**      | Load Optimization           | AI recommends how to distribute weight         | ↑ efficiency          |
| **Passenger**  | Occupancy Prediction        | Predict demand per route/time                  | ↑ revenue utilization |
| **Climate**    | Carbon Intelligence         | Forecast emissions and recommend eco-routes    | ↑ sustainability      |
| **CRM**        | Sentiment Analysis          | Analyze feedback or complaints automatically   | ↑ service quality     |
| **Trade**      | FX & Tariff Forecast        | Predict foreign exchange and duty rate changes | ↑ margin control      |

---

## TECHNICAL CONSTRAINTS

* AI logic must be **decoupled** from business logic (call through API or service layer).
* Models can run:

  * Locally (Python/TensorFlow, Scikit-learn)
  * Remotely (via external AI APIs)
* All outputs logged in `AI Insight Log`.
* Scheduler jobs for daily/weekly predictions.
* All code ≤300 lines per `.py` file.
* Configurable via Frappe desk UI (no hard-coded models).

---

## OUTPUTS

* `tems_ai` module folder scaffold.
* Doctypes:

  * `AI Configuration`
  * `AI Model Registry`
  * `AI Insight Log`
* API Endpoints:

  * `/api/method/tems_ai.api.predict.run`
  * `/api/method/tems_ai.api.analyze.run`
* Dashboard workspace: **AI Center**
* 3 sample AI routines (Fleet Maintenance, ETA Prediction, Profitability Forecast)
* 1 unified Insight UI (chart + recommendation card)

---

## EXTENSION

* Integrate OpenAI GPT for natural language queries:
  * Example: “Show me vehicles likely to require maintenance next week.”
  * Build simple `/ai/chat` endpoint to parse query → map to domain → return insight.
* Allow external B2B clients to subscribe to predictive API:
  * `/api/tems_ai/predict_maintenance`
  * `/api/tems_ai/predict_route_eta`

---
