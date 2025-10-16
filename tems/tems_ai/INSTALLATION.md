# TEMS AI Module - Installation & Setup Guide

## Prerequisites

1. **TEMS Platform** running on Frappe/ERPNext v15+
2. **Python 3.10+** (managed by bench)
3. The following packages are **automatically bundled** with TEMS app:
   - `numpy>=1.24.0` (for numerical computations and metrics)
   - `scikit-learn>=1.3.0` (for ML preprocessing and model evaluation)
   - `requests` (already included in Frappe)

## Installation Steps

### 1. Install/Update TEMS App

The `tems_ai` module is part of the TEMS app. When installing or updating TEMS, all dependencies are automatically installed:

```bash
# For new installations
cd /workspace/development/frappe-bench
bench get-app tems
bench --site <your-site> install-app tems

# For existing installations (update)
cd /workspace/development/frappe-bench
bench update --app tems
```

The required Python packages (`numpy`, `scikit-learn`) will be installed automatically as they're declared in `tems/pyproject.toml`.

### 2. Install Optional Packages (Advanced AI Features)

For deep learning capabilities (optional):

```bash
cd /workspace/development/frappe-bench
./env/bin/pip install tensorflow  # or pytorch
```

These are NOT bundled by default as they're large packages only needed for advanced use cases.

### 3. Create the DocTypes

You need to create three DocTypes through Frappe Desk:

#### A. AI Configuration DocType

1. Navigate to **Doctype List** → **New**
2. Set **Name**: `AI Configuration`
3. Add the following fields:

| Label | Fieldname | Type | Options | Mandatory |
|-------|-----------|------|---------|-----------|
| Domain | domain | Select | fleet\noperations\nsafety\nfinance\ncargo\npassenger | Yes |
| Insight Mode | insight_mode | Select | forecast\nrisk\nanomaly\nrecommendation | Yes |
| Model | model | Link | AI Model Registry | Yes |
| Enabled | enabled | Check | - | No |
| Confidence Threshold | confidence_threshold | Float | - | No |
| Alert Threshold | alert_threshold | Float | - | No |
| Alert on High Confidence | alert_on_high_confidence | Check | - | No |

3. Set **Is Submittable**: No
4. Add permissions for roles: TEMS Executive, Operations Manager, Fleet Manager
5. Save and create the DocType

#### B. AI Model Registry DocType

1. Create new DocType: `AI Model Registry`
2. Add fields:

| Label | Fieldname | Type | Options | Mandatory |
|-------|-----------|------|---------|-----------|
| Model Name | model_name | Data | - | Yes |
| Model Type | model_type | Select | Regression\nClassification\nForecast\nNLP | Yes |
| Domain | domain | Select | fleet\noperations\nsafety\nfinance | Yes |
| Source | source | Select | Local\nAPI\nExternal | Yes |
| Endpoint URL | endpoint_url | Data | - | No |
| Model Path | model_path | Data | - | No |
| API Key | api_key | Password | - | No |
| API Provider | api_provider | Select | openai\nazure_ml\nhuggingface\ntensorflow_serving | No |
| Enabled | enabled | Check | - | No |
| Confidence Threshold | confidence_threshold | Float | - | No |
| Auto Retrain | auto_retrain | Check | - | No |
| Retrain Frequency | retrain_frequency | Select | daily\nweekly\nmonthly | No |
| Last Trained Date | last_trained_date | Datetime | - | No |
| Last Performance Check | last_performance_check | Datetime | - | No |
| Avg Confidence | avg_confidence | Float | - | No |
| Total Predictions | total_predictions | Int | - | No |

3. Save and create the DocType

#### C. AI Insight Log DocType

1. Create new DocType: `AI Insight Log`
2. Add fields:

| Label | Fieldname | Type | Options | Mandatory |
|-------|-----------|------|---------|-----------|
| Domain | domain | Select | fleet\noperations\nsafety\nfinance\ncargo\npassenger | Yes |
| Insight Type | insight_type | Data | - | Yes |
| Model Used | model_used | Link | AI Model Registry | No |
| Prediction Value | prediction_value | Long Text | - | No |
| Confidence Score | confidence_score | Float | - | No |
| Details | details | JSON | - | No |
| Context Data | context_data | JSON | - | No |
| Timestamp | timestamp | Datetime | - | Yes |
| Status | status | Select | Generated\nAlert\nAlert Sent\nArchived | Yes |
| Alert Message | alert_message | Text | - | No |
| Actual Value | actual_value | Data | - | No |

3. Set **Autoname**: `AI-INSIGHT-.#####`
4. Save and create the DocType

### 4. Run Migration

After creating the DocTypes, run:

```bash
cd /workspace/development/frappe-bench
bench --site development.localhost migrate
bench build
bench clear-cache
bench restart
```

### 5. Create Sample AI Models

Navigate to **AI Model Registry** and create these sample models:

**Fleet Maintenance Predictor:**
- Model Name: `Fleet Maintenance Predictor`
- Model Type: `Forecast`
- Domain: `fleet`
- Source: `Local`
- Enabled: ✓

**ETA Prediction Model:**
- Model Name: `ETA Prediction Model`
- Model Type: `Regression`
- Domain: `operations`
- Source: `Local`
- Enabled: ✓

**Driver Risk Classifier:**
- Model Name: `Driver Risk Classifier`
- Model Type: `Classification`
- Domain: `safety`
- Source: `Local`
- Enabled: ✓

**Profitability Forecaster:**
- Model Name: `Profitability Forecaster`
- Model Type: `Forecast`
- Domain: `finance`
- Source: `Local`
- Enabled: ✓

### 6. Configure AI for Each Domain

Create AI Configurations for each domain:

**Fleet Configuration:**
- Domain: `fleet`
- Insight Mode: `forecast`
- Model: `Fleet Maintenance Predictor`
- Confidence Threshold: `0.75`
- Alert Threshold: `0.80`
- Enabled: ✓

**Operations Configuration:**
- Domain: `operations`
- Insight Mode: `forecast`
- Model: `ETA Prediction Model`
- Confidence Threshold: `0.70`
- Enabled: ✓

**Safety Configuration:**
- Domain: `safety`
- Insight Mode: `risk`
- Model: `Driver Risk Classifier`
- Confidence Threshold: `0.80`
- Alert on High Confidence: ✓
- Enabled: ✓

**Finance Configuration:**
- Domain: `finance`
- Insight Mode: `forecast`
- Model: `Profitability Forecaster`
- Confidence Threshold: `0.75`
- Enabled: ✓

### 7. Verify Scheduled Tasks

Check that AI scheduled tasks are registered:

```bash
bench --site development.localhost scheduler status
bench --site development.localhost enable-scheduler
```

### 8. Test the API Endpoints

Test the prediction API:

```bash
# Using curl
curl -X POST http://development.localhost:8000/api/method/tems_ai.api.predict.run \
  -H "Content-Type: application/json" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -d '{"domain": "fleet", "dataset": {"odometer": 50000}}'
```

Or through Python:

```python
import frappe

# Connect to site
frappe.init(site='tems.local')
frappe.connect()

# Test prediction
result = frappe.call(
    "tems.tems_ai.api.predict.run",
    domain="fleet",
    dataset={"odometer": 50000}
)

print(result)
```

### 9. Create AI Center Workspace (Optional)

1. Navigate to **Workspace List** → **New**
2. Name: `AI Center`
3. Module: `TEMS`
4. Add shortcuts:
   - AI Configuration (DocType)
   - AI Model Registry (DocType)
   - AI Insight Log (DocType)
5. Add cards/charts as needed
6. Assign to roles: TEMS Executive, Operations Manager
7. Save

## Verification Checklist

- [ ] All three DocTypes created successfully
- [ ] Sample AI models registered
- [ ] AI configurations created for each domain
- [ ] Scheduled tasks are enabled
- [ ] API endpoints respond successfully
- [ ] Insights are being generated (check AI Insight Log)
- [ ] Alerts are being triggered (check Notification Log)

## Troubleshooting

### Scheduled Tasks Not Running

```bash
# Check scheduler status
bench --site development.localhost scheduler status

# Enable if disabled
bench --site development.localhost enable-scheduler

# Check logs
tail -f /workspace/development/frappe-bench/logs/scheduler.log.1
```

### API Endpoints Returning Errors

1. Check error logs:
```bash
tail -f /workspace/development/frappe-bench/logs/database.log.1
```

2. Verify DocTypes exist:
```python
frappe.get_all("AI Configuration")
frappe.get_all("AI Model Registry")
frappe.get_all("AI Insight Log")
```

3. Check if models are enabled:
```python
frappe.get_all("AI Model Registry", filters={"enabled": 1})
```

### No Insights Being Generated

1. Check AI Configuration is enabled
2. Verify model is enabled in AI Model Registry
3. Check scheduled task logs
4. Manually trigger insight generation:

```python
from tems.tems_ai.services.insights_engine import generate_insight

result = generate_insight(domain="fleet", mode="forecast")
print(result)
```

## Advanced Configuration

### Integrating External AI APIs

To use OpenAI GPT or Azure ML:

1. Create AI Model Registry entry
2. Set Source: `External`
3. Set API Provider: `openai` or `azure_ml`
4. Add API Key (will be encrypted)
5. Add Endpoint URL
6. Update `services/model_manager.py` with provider-specific logic (if needed)

### Custom Model Training

To add your own trained models:

1. Train model using your preferred framework
2. Save model file to `apps/tems/tems/tems_ai/models/`
3. Create AI Model Registry entry
4. Set Source: `Local`
5. Set Model Path: Path to your model file
6. Update `model_manager.py` to load your model format

## Next Steps

1. Monitor AI Insight Log for predictions
2. Review alerts in Notification Log
3. Adjust confidence thresholds based on results
4. Add more domain-specific configurations
5. Integrate AI calls into your custom business logic

## Support

For issues:
- Check `/workspace/development/frappe-bench/logs/`
- Review Error Log in Frappe Desk
- Contact: code@tevcng.com
