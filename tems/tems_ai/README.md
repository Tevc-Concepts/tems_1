# TEMS AI Module

## Overview
The TEMS AI Module (`tems_ai`) is a comprehensive artificial intelligence and machine learning layer that provides predictive insights, anomaly detection, and automation capabilities across all TEMS business domains.

## Quick Start

### Installation
```bash
# TEMS AI is bundled with the TEMS app
bench --site <your-site> install-app tems

# All dependencies (numpy, scikit-learn) are automatically installed
```

### Dependencies (Auto-Installed)
- ✅ `numpy>=1.24.0` - Numerical computations
- ✅ `scikit-learn>=1.3.0` - ML preprocessing and evaluation
- ✅ `requests` (via Frappe) - External API calls

**No manual setup required!** See `DEPENDENCIES.md` for details.

## Architecture

### Service Layer
The AI module operates as a **standalone service layer** that other TEMS modules can call through API endpoints or internal functions.

```
tems_ai/
├── api/               # Whitelisted API endpoints
│   ├── predict.py     # Prediction endpoints
│   ├── analyze.py     # Analysis endpoints
│   └── train.py       # Training endpoints
├── handlers/          # Domain-specific AI logic
│   ├── fleet_ai.py
│   ├── operations_ai.py
│   ├── safety_ai.py
│   └── finance_ai.py
├── services/          # Core AI services
│   ├── model_registry.py
│   ├── model_manager.py
│   ├── insights_engine.py
│   └── alert_engine.py
├── utils/             # Utilities
│   ├── preprocessor.py
│   └── metrics.py
├── doctype/           # DocTypes (AI Configuration, AI Model Registry, AI Insight Log)
└── tasks.py           # Scheduled tasks
```

## Key Features

### 1. Multi-Domain AI Support
- **Fleet**: Predictive maintenance, fuel anomaly detection, health scoring
- **Operations**: ETA prediction, route optimization, demand forecasting
- **Safety**: Driver risk scoring, journey risk assessment, fatigue detection
- **Finance**: Profitability forecasting, cost anomaly detection, ROI analysis

### 2. Model Management
- Centralized model registry
- Support for local and external models (OpenAI, Azure ML, etc.)
- Model performance tracking and drift detection
- Automatic retraining capabilities

### 3. Insights & Alerts
- Automated insight generation
- Confidence-based alerting
- Role-based notifications
- Historical insight tracking

### 4. API Endpoints

#### Prediction API
```bash
POST /api/method/tems_ai.api.predict.run
{
    "domain": "fleet",
    "dataset": {"odometer": 50000},
    "model": "Fleet Maintenance Predictor"
}
```

#### Analysis API
```bash
POST /api/method/tems_ai.api.analyze.run
{
    "domain": "fleet",
    "analysis_type": "summary",
    "days": 30
}
```

## DocTypes

### AI Configuration
Manages AI feature configuration per domain:
- Domain selection
- Insight mode
- Model assignment
- Alert thresholds
- Enable/disable toggles

### AI Model Registry
Central repository of AI models:
- Model name and type
- Source (Local, API, External)
- Endpoint/path configuration
- Performance metrics
- Auto-retrain settings

### AI Insight Log
Stores all AI-generated insights:
- Domain and insight type
- Prediction values
- Confidence scores
- Alert status
- Timestamps

## Domain-Specific Features

### Fleet AI (`handlers/fleet_ai.py`)
- `predict_maintenance_schedule()` - Predict when vehicles need maintenance
- `detect_fuel_anomaly()` - Identify unusual fuel consumption
- `calculate_vehicle_health_score()` - Overall vehicle health (0-100)
- `optimize_maintenance_budget()` - Budget allocation recommendations

### Operations AI (`handlers/operations_ai.py`)
- `predict_trip_eta()` - AI-powered ETA prediction
- `optimize_route()` - Route optimization recommendations
- `detect_route_deviation()` - Deviation detection
- `predict_vehicle_demand()` - Demand forecasting by region

### Safety AI (`handlers/safety_ai.py`)
- `predict_driver_risk_score()` - Driver risk assessment (0-100)
- `predict_journey_risk()` - Journey-specific risk scoring
- `detect_fatigue_patterns()` - Driver fatigue analysis
- `predict_incident_hotspots()` - Identify high-risk routes

### Finance AI (`handlers/finance_ai.py`)
- `predict_vehicle_profitability()` - Profitability forecasting
- `detect_cost_anomaly()` - Cost anomaly detection
- `optimize_pricing()` - AI-powered pricing recommendations
- `forecast_cash_flow()` - Cash flow projections
- `calculate_roi_score()` - Investment ROI analysis

## Scheduled Tasks

Daily tasks (configured in `hooks.py`):
- `generate_daily_insights()` - Generate insights for all domains
- `generate_fleet_maintenance_predictions()` - Fleet predictions (06:00 AM)
- `calculate_driver_risk_scores()` - Safety scoring (05:00 AM)
- `forecast_financial_metrics()` - Financial forecasting (07:00 AM)
- `update_model_performance_metrics()` - Model metrics (04:00 AM)
- `cleanup_old_insights()` - Weekly cleanup (Sunday 03:00 AM)

Hourly tasks:
- `evaluate_alerts_hourly()` - Evaluate insights and trigger alerts

Weekly tasks:
- `retrain_models_weekly()` - Automatic model retraining (Monday 01:00 AM)

## Usage Examples

### Using API Endpoints

**Predict Maintenance for a Vehicle:**
```python
import frappe

result = frappe.call(
    "tems_ai.api.predict.predict_maintenance",
    vehicle="VEH-001"
)
```

**Get AI Dashboard for Domain:**
```python
dashboard = frappe.call(
    "tems_ai.api.analyze.domain_dashboard",
    domain="fleet"
)
```

### Using Internal Functions

**Generate Insight:**
```python
from tems.tems_ai.services.insights_engine import generate_insight

insight = generate_insight(
    domain="operations",
    mode="forecast",
    context={"route": "Lagos-Abuja"}
)
```

**Trigger Alert:**
```python
from tems.tems_ai.services.alert_engine import trigger_alert

trigger_alert(
    domain="safety",
    alert_type="high_risk",
    severity="high",
    message="Critical safety issue detected",
    recipients=["safety.manager@example.com"]
)
```

## Integration with Other Modules

Other TEMS modules can leverage AI capabilities:

```python
# In tems_fleet module
from tems.tems_ai.handlers.fleet_ai import calculate_vehicle_health_score

def on_vehicle_update(doc, method):
    health = calculate_vehicle_health_score(doc.name)
    doc.health_score = health.get("health_score")
    doc.health_grade = health.get("grade")
```

## Configuration

### Enable AI for a Domain

1. Navigate to **AI Center** workspace
2. Create new **AI Configuration** record
3. Select domain and insight mode
4. Assign model
5. Set confidence thresholds
6. Enable the configuration

### Register a New Model

1. Navigate to **AI Model Registry**
2. Create new model record
3. Specify model type (Regression, Classification, Forecast, NLP)
4. Configure source (Local, API, External)
5. Add endpoint URL or model path
6. Enable the model

## Extending the Module

### Adding a New Domain Handler

1. Create `handlers/new_domain_ai.py`
2. Implement domain-specific functions
3. Update `services/insights_engine.py` to fetch data for the new domain
4. Register scheduled tasks in `hooks.py`

### Adding External AI Provider

1. Update `services/model_manager.py`
2. Add provider-specific prediction method
3. Update `AI Model Registry` to support the new provider

## Testing

```bash
# Run AI module tests
cd /workspace/development/frappe-bench
bench --site development.localhost run-tests --app tems --module tems_ai
```

## Performance Considerations

- Predictions are cached where appropriate
- Batch processing for large datasets
- Scheduled tasks run during off-peak hours
- Old insights are automatically cleaned up (90-day retention)

## Security

- All API endpoints are whitelisted and require authentication
- Role-based access control for AI configurations
- Sensitive model credentials stored securely
- Audit trail for all AI decisions

## Roadmap

- [ ] OpenAI GPT integration for natural language queries
- [ ] TensorFlow/PyTorch model loading for local predictions
- [ ] Real-time streaming predictions
- [ ] A/B testing framework for models
- [ ] Explainable AI (XAI) visualizations
- [ ] Automated model hyperparameter tuning

## Support

For issues or questions:
- Check TEMS documentation
- Review AI Insight Logs for errors
- Contact: code@tevcng.com
