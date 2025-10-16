# TEMS AI Module - API Reference

## Table of Contents
1. [Prediction API](#prediction-api)
2. [Analysis API](#analysis-api)
3. [Training API](#training-api)
4. [Domain Handlers](#domain-handlers)

---

## Prediction API

Base path: `/api/method/tems_ai.api.predict`

### 1. Generic Prediction

**Endpoint:** `/api/method/tems_ai.api.predict.run`

**Method:** POST

**Parameters:**
- `domain` (string, required): Domain name (fleet, operations, safety, finance)
- `dataset` (object, optional): Input dataset for prediction
- `model` (string, optional): Specific model name to use

**Example Request:**
```json
{
  "domain": "fleet",
  "dataset": {
    "odometer": 50000,
    "days_since_maintenance": 180
  },
  "model": "Fleet Maintenance Predictor"
}
```

**Example Response:**
```json
{
  "success": true,
  "domain": "fleet",
  "result": {
    "prediction": "maintenance_needed",
    "confidence": 0.85,
    "details": {
      "recommended_date": "2025-11-15",
      "components": ["brake_pads", "oil_filter"]
    }
  }
}
```

---

### 2. Predict Maintenance

**Endpoint:** `/api/method/tems_ai.api.predict.predict_maintenance`

**Method:** POST

**Parameters:**
- `vehicle` (string, required): Vehicle ID

**Example Request:**
```json
{
  "vehicle": "VEH-001"
}
```

**Example Response:**
```json
{
  "success": true,
  "vehicle": "VEH-001",
  "prediction": {
    "maintenance_needed": true,
    "confidence": 0.87,
    "recommended_date": "2025-11-20",
    "priority": "medium"
  }
}
```

---

### 3. Predict ETA

**Endpoint:** `/api/method/tems_ai.api.predict.predict_eta`

**Method:** POST

**Parameters:**
- `trip` (string, required): Trip Allocation ID

**Example Request:**
```json
{
  "trip": "TRIP-2025-001"
}
```

**Example Response:**
```json
{
  "success": true,
  "trip": "TRIP-2025-001",
  "prediction": {
    "predicted_duration_minutes": 245,
    "estimated_arrival": "2025-10-16T18:30:00",
    "confidence": 0.82,
    "factors": {
      "historical_avg": 230,
      "time_of_day_factor": 1.2,
      "weather_factor": 1.0
    }
  }
}
```

---

### 4. Predict Risk

**Endpoint:** `/api/method/tems_ai.api.predict.predict_risk`

**Method:** POST

**Parameters:**
- `driver` (string, required): Driver/Employee ID
- `route` (string, required): Route name

**Example Request:**
```json
{
  "driver": "EMP-001",
  "route": "Lagos-Abuja"
}
```

**Example Response:**
```json
{
  "success": true,
  "driver": "EMP-001",
  "route": "Lagos-Abuja",
  "prediction": {
    "risk_score": 35.5,
    "risk_level": "medium",
    "confidence": 0.78,
    "recommendation": "Approve with caution"
  }
}
```

---

### 5. Batch Predict

**Endpoint:** `/api/method/tems_ai.api.predict.batch_predict`

**Method:** POST

**Parameters:**
- `domain` (string, required): Domain name
- `records` (array, required): List of record IDs

**Example Request:**
```json
{
  "domain": "fleet",
  "records": ["VEH-001", "VEH-002", "VEH-003"]
}
```

**Example Response:**
```json
{
  "success": true,
  "domain": "fleet",
  "total": 3,
  "results": [
    {
      "record": "VEH-001",
      "prediction": {"health_score": 85}
    },
    {
      "record": "VEH-002",
      "prediction": {"health_score": 72}
    },
    {
      "record": "VEH-003",
      "prediction": {"health_score": 91}
    }
  ]
}
```

---

## Analysis API

Base path: `/api/method/tems_ai.api.analyze`

### 1. Generic Analysis

**Endpoint:** `/api/method/tems_ai.api.analyze.run`

**Method:** POST

**Parameters:**
- `domain` (string, required): Domain name
- `analysis_type` (string, optional): Type of analysis (summary, trends, alerts). Default: "summary"
- `days` (int, optional): Analysis period in days. Default: 7

**Example Request:**
```json
{
  "domain": "fleet",
  "analysis_type": "summary",
  "days": 30
}
```

**Example Response:**
```json
{
  "success": true,
  "domain": "fleet",
  "analysis_type": "summary",
  "result": {
    "period_days": 30,
    "total_insights": 245,
    "avg_confidence": 0.81,
    "insights_by_type": [
      {"type": "forecast", "count": 180},
      {"type": "anomaly", "count": 65}
    ]
  }
}
```

---

### 2. Get Insights

**Endpoint:** `/api/method/tems_ai.api.analyze.get_insights`

**Method:** GET/POST

**Parameters:**
- `domain` (string, optional): Domain filter
- `limit` (int, optional): Number of insights. Default: 20

**Example Response:**
```json
{
  "success": true,
  "domain": "fleet",
  "total": 20,
  "insights": [
    {
      "name": "AI-INSIGHT-00001",
      "domain": "fleet",
      "insight_type": "forecast",
      "prediction_value": "maintenance_needed",
      "confidence_score": 0.85,
      "timestamp": "2025-10-16 10:30:00"
    }
  ]
}
```

---

### 3. Get Alerts

**Endpoint:** `/api/method/tems_ai.api.analyze.get_alerts`

**Method:** GET/POST

**Parameters:**
- `domain` (string, optional): Domain filter
- `limit` (int, optional): Number of alerts. Default: 20

**Example Response:**
```json
{
  "success": true,
  "domain": "safety",
  "total": 5,
  "alerts": [
    {
      "name": "AI-INSIGHT-00050",
      "domain": "safety",
      "insight_type": "risk",
      "prediction_value": "high",
      "alert_message": "High risk driver detected: EMP-001",
      "status": "Alert"
    }
  ]
}
```

---

### 4. Model Performance

**Endpoint:** `/api/method/tems_ai.api.analyze.model_performance`

**Method:** POST

**Parameters:**
- `model_name` (string, required): Model name
- `limit` (int, optional): Number of predictions to analyze. Default: 100

**Example Request:**
```json
{
  "model_name": "Fleet Maintenance Predictor",
  "limit": 100
}
```

**Example Response:**
```json
{
  "success": true,
  "metrics": {
    "model_name": "Fleet Maintenance Predictor",
    "total_predictions": 100,
    "avg_confidence": 0.83,
    "high_confidence_count": 72,
    "medium_confidence_count": 25,
    "low_confidence_count": 3,
    "confidence_distribution": {
      "high": 72.0,
      "medium": 25.0,
      "low": 3.0
    }
  }
}
```

---

### 5. Model Drift Analysis

**Endpoint:** `/api/method/tems_ai.api.analyze.model_drift`

**Method:** POST

**Parameters:**
- `model_name` (string, required): Model name
- `window_days` (int, optional): Analysis window. Default: 30

**Example Response:**
```json
{
  "success": true,
  "analysis": {
    "model_name": "Fleet Maintenance Predictor",
    "window_days": 30,
    "data_points": 28,
    "confidence_trend": "stable",
    "latest_confidence": 0.84,
    "earliest_confidence": 0.82
  }
}
```

---

### 6. Domain Dashboard

**Endpoint:** `/api/method/tems_ai.api.analyze.domain_dashboard`

**Method:** POST

**Parameters:**
- `domain` (string, required): Domain name

**Example Response:**
```json
{
  "success": true,
  "domain": "fleet",
  "dashboard": {
    "recent_insights": [...],
    "active_alerts": [...],
    "summary": {...},
    "configurations": [...],
    "stats": {
      "total_insights": 245,
      "total_alerts": 12,
      "enabled_models": 2
    }
  }
}
```

---

## Training API

Base path: `/api/method/tems_ai.api.train`

### 1. Trigger Training

**Endpoint:** `/api/method/tems_ai.api.train.run`

**Method:** POST

**Parameters:**
- `model_name` (string, required): Model name
- `training_data` (object, optional): Training dataset

**Example Request:**
```json
{
  "model_name": "Fleet Maintenance Predictor",
  "training_data": {}
}
```

**Example Response:**
```json
{
  "success": true,
  "model": "Fleet Maintenance Predictor",
  "status": "training_queued",
  "message": "Training job has been queued"
}
```

---

### 2. Schedule Training

**Endpoint:** `/api/method/tems_ai.api.train.schedule_training`

**Method:** POST

**Parameters:**
- `model_name` (string, required): Model name
- `frequency` (string, optional): Frequency (daily, weekly, monthly). Default: "weekly"

**Example Response:**
```json
{
  "success": true,
  "model": "Fleet Maintenance Predictor",
  "frequency": "weekly",
  "message": "Model will be retrained weekly"
}
```

---

### 3. Training Status

**Endpoint:** `/api/method/tems_ai.api.train.get_training_status`

**Method:** GET/POST

**Parameters:**
- `model_name` (string, required): Model name

**Example Response:**
```json
{
  "success": true,
  "model": "Fleet Maintenance Predictor",
  "status": {
    "auto_retrain": 1,
    "retrain_frequency": "weekly",
    "last_trained": "2025-10-10 01:00:00",
    "training_status": "idle"
  }
}
```

---

### 4. Validate Training Data

**Endpoint:** `/api/method/tems_ai.api.train.validate_training_data`

**Method:** POST

**Parameters:**
- `domain` (string, required): Domain name
- `record_count` (int, optional): Expected record count

**Example Response:**
```json
{
  "success": true,
  "domain": "fleet",
  "validation": {
    "vehicles": 50,
    "maintenance_records": 250,
    "sufficient": true
  }
}
```

---

## Domain Handlers

Internal functions that can be imported and used in server-side code.

### Fleet AI Handler

**Module:** `tems.tems_ai.handlers.fleet_ai`

```python
from tems.tems_ai.handlers.fleet_ai import (
    predict_maintenance_schedule,
    detect_fuel_anomaly,
    calculate_vehicle_health_score,
    optimize_maintenance_budget
)

# Predict maintenance
result = predict_maintenance_schedule("VEH-001")

# Detect fuel anomaly
anomaly = detect_fuel_anomaly("VEH-001", fuel_consumption=12.5)

# Calculate health score
health = calculate_vehicle_health_score("VEH-001")

# Optimize budget
allocation = optimize_maintenance_budget(fleet_size=50, budget=500000)
```

---

### Operations AI Handler

**Module:** `tems.tems_ai.handlers.operations_ai`

```python
from tems.tems_ai.handlers.operations_ai import (
    predict_trip_eta,
    optimize_route,
    detect_route_deviation,
    predict_vehicle_demand,
    calculate_operational_efficiency
)

# Predict ETA
eta = predict_trip_eta("TRIP-001")

# Optimize route
route = optimize_route("Lagos", "Abuja", waypoints=["Ibadan"])

# Predict demand
demand = predict_vehicle_demand("Lagos", forecast_days=7)

# Calculate efficiency
efficiency = calculate_operational_efficiency("2025-10-01", "2025-10-15")
```

---

### Safety AI Handler

**Module:** `tems.tems_ai.handlers.safety_ai`

```python
from tems.tems_ai.handlers.safety_ai import (
    predict_driver_risk_score,
    predict_journey_risk,
    detect_fatigue_patterns,
    predict_incident_hotspots,
    calculate_safety_compliance_score
)

# Driver risk score
risk = predict_driver_risk_score("EMP-001")

# Journey risk
journey_risk = predict_journey_risk("JOURNEY-001")

# Fatigue detection
fatigue = detect_fatigue_patterns("EMP-001", period_days=30)

# Incident hotspots
hotspots = predict_incident_hotspots(region="Lagos")

# Compliance score
compliance = calculate_safety_compliance_score("EMP-001", entity_type="driver")
```

---

### Finance AI Handler

**Module:** `tems.tems_ai.handlers.finance_ai`

```python
from tems.tems_ai.handlers.finance_ai import (
    predict_vehicle_profitability,
    detect_cost_anomaly,
    optimize_pricing,
    forecast_cash_flow,
    calculate_roi_score,
    identify_cost_savings_opportunities
)

# Profitability forecast
profitability = predict_vehicle_profitability("VEH-001", forecast_days=30)

# Cost anomaly
anomaly = detect_cost_anomaly("VEH-001", cost_amount=5000, cost_type="maintenance")

# Pricing optimization
pricing = optimize_pricing("Lagos-Abuja", season="peak")

# Cash flow forecast
cash_flow = forecast_cash_flow(days=30)

# ROI calculation
roi = calculate_roi_score("new_vehicle", amount=5000000, vehicle="VEH-001")

# Cost savings
savings = identify_cost_savings_opportunities(vehicle="VEH-001")
```

---

## Error Handling

All API endpoints return standardized error responses:

```json
{
  "success": false,
  "error": "Error message description"
}
```

Common error codes:
- Invalid domain
- Model not found
- Insufficient data
- Configuration not enabled
- Authentication required

---

## Authentication

All API endpoints require authentication:

**Token-based:**
```bash
curl -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  http://site.com/api/method/tems_ai.api.predict.run
```

**Session-based:**
Use Frappe's built-in session authentication when calling from client-side code.

---

## Rate Limiting

API endpoints may be rate-limited based on your Frappe configuration.

---

## Webhooks (Future Feature)

Subscribe to AI events:
- `ai_insight_generated`
- `ai_alert_triggered`
- `ai_model_retrained`

---

## Support

For API issues or questions:
- Check Error Log in Frappe Desk
- Review `/workspace/development/frappe-bench/logs/`
- Contact: code@tevcng.com
