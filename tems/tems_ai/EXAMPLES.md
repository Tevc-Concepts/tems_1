# TEMS AI Module - Implementation Examples

## Quick Start Examples

### Example 1: Predictive Maintenance Alert System

**Scenario:** Automatically alert fleet managers when vehicles need maintenance.

```python
# File: tems/tems_fleet/api/vehicle.py

import frappe
from tems.tems_ai.handlers.fleet_ai import predict_maintenance_schedule
from tems.tems_ai.services.alert_engine import trigger_alert

def on_vehicle_update(doc, method):
    """
    Hook that runs when a vehicle is updated.
    Checks if maintenance is needed.
    """
    # Only check vehicles that are active and have odometer data
    if doc.status == "Active" and doc.odometer:
        # Get AI prediction
        prediction = predict_maintenance_schedule(doc.name)
        
        # Store prediction on vehicle doc
        doc.db_set("ai_maintenance_score", prediction.get("confidence", 0))
        
        # If high confidence that maintenance is needed, trigger alert
        if prediction.get("confidence", 0) > 0.85:
            trigger_alert(
                domain="fleet",
                alert_type="predictive_maintenance",
                severity="high",
                message=f"Vehicle {doc.name} requires maintenance soon",
                details=prediction,
                recipients=["fleet.manager@company.com"]
            )
```

**Register the hook in hooks.py:**
```python
doc_events = {
    "Vehicle": {
        "on_update": "tems.tems_fleet.api.vehicle.on_vehicle_update"
    }
}
```

---

### Example 2: Real-time Driver Risk Assessment

**Scenario:** Assess driver risk before approving a journey.

```python
# File: tems/tems_safety/api/journey_plan.py

import frappe
from tems.tems_ai.handlers.safety_ai import predict_journey_risk

def validate_journey_plan(doc, method):
    """
    Validate journey plan using AI risk assessment.
    """
    # Get AI risk prediction
    risk_assessment = predict_journey_risk(doc.name)
    
    # Store risk score
    doc.risk_score = risk_assessment.get("overall_risk_score", 0)
    doc.risk_level = risk_assessment.get("risk_level", "unknown")
    
    # Prevent submission if risk is too high
    if risk_assessment.get("overall_risk_score", 0) > 70:
        frappe.throw(
            f"Journey risk too high: {risk_assessment.get('recommendation')}",
            title="High Risk Journey"
        )
    
    # Require additional approval for medium risk
    if risk_assessment.get("overall_risk_score", 0) > 50:
        doc.requires_supervisor_approval = 1
        frappe.msgprint(
            "This journey has elevated risk and requires supervisor approval",
            indicator="orange"
        )
```

---

### Example 3: Dynamic Pricing Based on Demand

**Scenario:** Adjust route pricing based on AI demand forecasts.

```python
# File: tems/tems_finance/api/pricing.py

import frappe
from tems.tems_ai.handlers.finance_ai import optimize_pricing
from tems.tems_ai.handlers.operations_ai import predict_vehicle_demand

@frappe.whitelist()
def get_recommended_price(route, date):
    """
    Get AI-recommended pricing for a route.
    """
    # Determine season based on date
    month = frappe.utils.getdate(date).month
    season = "peak" if month in [12, 1, 7, 8] else "regular"
    
    # Get pricing recommendation
    pricing = optimize_pricing(route, season)
    
    # Get demand forecast to adjust further
    region = route.split("-")[0]  # Extract origin
    demand = predict_vehicle_demand(region, date_range=7)
    
    # Adjust price based on demand
    base_price = pricing.get("recommended_price", 0)
    demand_forecast = demand.get("forecast", [{}])[0]
    demand_level = demand_forecast.get("predicted_demand", 0)
    
    # Higher demand = higher price
    if demand_level > 20:
        final_price = base_price * 1.1
        demand_note = "High demand period"
    elif demand_level < 10:
        final_price = base_price * 0.9
        demand_note = "Low demand period"
    else:
        final_price = base_price
        demand_note = "Normal demand"
    
    return {
        "route": route,
        "date": date,
        "season": season,
        "base_price": base_price,
        "recommended_price": final_price,
        "demand_note": demand_note,
        "confidence": pricing.get("confidence", 0)
    }
```

---

### Example 4: Automated Cost Anomaly Detection

**Scenario:** Detect and flag unusual costs automatically.

```python
# File: tems/tems_finance/api/ledger.py

import frappe
from tems.tems_ai.handlers.finance_ai import detect_cost_anomaly
from tems.tems_ai.services.alert_engine import trigger_alert

def on_ledger_submit(doc, method):
    """
    Check for cost anomalies when cost/revenue is submitted.
    """
    if doc.cost_amount and doc.cost_amount > 0:
        # Run anomaly detection
        anomaly = detect_cost_anomaly(
            vehicle=doc.vehicle,
            cost_amount=doc.cost_amount,
            cost_type=doc.cost_type
        )
        
        # Flag if anomaly detected
        if anomaly.get("anomaly"):
            doc.db_set("anomaly_detected", 1)
            doc.db_set("anomaly_severity", anomaly.get("severity"))
            
            # Alert finance team on high severity
            if anomaly.get("severity") in ["high", "critical"]:
                trigger_alert(
                    domain="finance",
                    alert_type="cost_anomaly",
                    severity="high",
                    message=f"Unusual cost detected: {doc.cost_type} for {doc.vehicle}",
                    details=anomaly,
                    recipients=["finance.manager@company.com"]
                )
```

---

### Example 5: Driver Performance Dashboard Widget

**Scenario:** Create a dashboard card showing driver AI scores.

```python
# File: tems/tems_safety/page/safety_dashboard.py

import frappe
from tems.tems_ai.handlers.safety_ai import predict_driver_risk_score

@frappe.whitelist()
def get_driver_performance_widget():
    """
    Get driver performance data for dashboard widget.
    """
    # Get all active drivers
    drivers = frappe.get_all(
        "Employee",
        filters={
            "designation": ["like", "%Driver%"],
            "status": "Active"
        },
        fields=["name", "employee_name"],
        limit=20
    )
    
    driver_scores = []
    
    for driver in drivers:
        try:
            # Get AI risk score
            risk_data = predict_driver_risk_score(driver["name"])
            
            driver_scores.append({
                "driver_id": driver["name"],
                "driver_name": driver["employee_name"],
                "safety_score": risk_data.get("safety_score", 0),
                "risk_level": risk_data.get("risk_level", "unknown"),
                "recent_incidents": risk_data.get("breakdown", {}).get("recent_incidents", 0)
            })
        except Exception as e:
            frappe.log_error(f"Error getting score for {driver['name']}: {str(e)}")
    
    # Sort by safety score (lowest first - needs attention)
    driver_scores.sort(key=lambda x: x["safety_score"])
    
    return {
        "drivers": driver_scores[:10],  # Top 10 needing attention
        "total_drivers": len(drivers),
        "high_risk_count": sum(1 for d in driver_scores if d["risk_level"] in ["high", "critical"])
    }
```

---

### Example 6: Scheduled Report with AI Insights

**Scenario:** Daily email report with AI predictions and alerts.

```python
# File: tems/tems_ai/reports/daily_ai_summary.py

import frappe
from frappe.utils import today, add_days
from tems.tems_ai.services.insights_engine import get_recent_insights
from tems.tems_ai.services.alert_engine import get_active_alerts

def send_daily_ai_summary():
    """
    Send daily AI summary email to executives.
    Scheduled to run daily at 08:00 AM.
    """
    # Get yesterday's insights
    insights = get_recent_insights(domain=None, limit=50)
    yesterday_insights = [
        i for i in insights 
        if frappe.utils.getdate(i.get("creation")) >= frappe.utils.add_days(today(), -1)
    ]
    
    # Get active alerts
    alerts = get_active_alerts(domain=None, limit=20)
    
    # Group by domain
    insights_by_domain = {}
    for insight in yesterday_insights:
        domain = insight.get("domain")
        if domain not in insights_by_domain:
            insights_by_domain[domain] = []
        insights_by_domain[domain].append(insight)
    
    # Build email content
    html_content = f"""
    <h2>TEMS AI Daily Summary - {today()}</h2>
    
    <h3>Summary</h3>
    <ul>
        <li>Total Insights Generated: {len(yesterday_insights)}</li>
        <li>Active Alerts: {len(alerts)}</li>
    </ul>
    
    <h3>Insights by Domain</h3>
    """
    
    for domain, domain_insights in insights_by_domain.items():
        html_content += f"""
        <h4>{domain.title()}</h4>
        <ul>
        """
        for insight in domain_insights[:5]:  # Top 5 per domain
            html_content += f"""
            <li>
                {insight.get("insight_type")}: {insight.get("prediction_value")} 
                (Confidence: {insight.get("confidence_score", 0):.2f})
            </li>
            """
        html_content += "</ul>"
    
    html_content += """
    <h3>Active Alerts</h3>
    <ul>
    """
    
    for alert in alerts[:10]:  # Top 10 alerts
        html_content += f"""
        <li>
            <strong>{alert.get("domain").upper()}</strong>: {alert.get("alert_message")}
        </li>
        """
    
    html_content += """
    </ul>
    
    <p>View full details in the AI Center workspace.</p>
    """
    
    # Send email
    frappe.sendmail(
        recipients=["executive@company.com", "operations@company.com"],
        subject=f"TEMS AI Daily Summary - {today()}",
        message=html_content,
        delayed=False
    )
```

**Register in hooks.py:**
```python
scheduler_events = {
    "cron": {
        "0 8 * * *": ["tems.tems_ai.reports.daily_ai_summary.send_daily_ai_summary"]
    }
}
```

---

### Example 7: Client-Side AI Dashboard (Vue/React)

**Scenario:** Interactive AI dashboard on a custom page.

```javascript
// File: frontend/src/pages/AIDashboard.vue

<template>
  <div class="ai-dashboard">
    <h1>AI Insights Dashboard</h1>
    
    <div class="domain-selector">
      <button 
        v-for="domain in domains" 
        :key="domain"
        @click="selectedDomain = domain"
        :class="{'active': selectedDomain === domain}"
      >
        {{ domain }}
      </button>
    </div>
    
    <div class="insights-grid">
      <div class="card">
        <h3>Recent Insights</h3>
        <div v-for="insight in recentInsights" :key="insight.name">
          <div class="insight-item">
            <span class="type">{{ insight.insight_type }}</span>
            <span class="confidence">{{ (insight.confidence_score * 100).toFixed(0) }}%</span>
            <p>{{ insight.prediction_value }}</p>
          </div>
        </div>
      </div>
      
      <div class="card">
        <h3>Active Alerts</h3>
        <div v-for="alert in activeAlerts" :key="alert.name">
          <div class="alert-item" :class="alert.prediction_value">
            <strong>{{ alert.alert_message }}</strong>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { call } from 'frappe-ui'

export default {
  setup() {
    const domains = ['fleet', 'operations', 'safety', 'finance']
    const selectedDomain = ref('fleet')
    const recentInsights = ref([])
    const activeAlerts = ref([])
    
    const loadDashboard = async () => {
      try {
        const result = await call('tems_ai.api.analyze.domain_dashboard', {
          domain: selectedDomain.value
        })
        
        if (result.success) {
          recentInsights.value = result.dashboard.recent_insights
          activeAlerts.value = result.dashboard.active_alerts
        }
      } catch (error) {
        console.error('Failed to load dashboard:', error)
      }
    }
    
    onMounted(loadDashboard)
    watch(selectedDomain, loadDashboard)
    
    return {
      domains,
      selectedDomain,
      recentInsights,
      activeAlerts
    }
  }
}
</script>
```

---

### Example 8: Webhook Integration for External Systems

**Scenario:** Send AI insights to external system via webhook.

```python
# File: tems/tems_ai/integrations/webhooks.py

import frappe
import requests

def send_insight_webhook(insight_doc):
    """
    Send AI insight to external webhook.
    Called after insight is created.
    """
    # Get webhook settings
    webhook_url = frappe.db.get_single_value("TEMS Settings", "ai_webhook_url")
    webhook_secret = frappe.db.get_single_value("TEMS Settings", "ai_webhook_secret")
    
    if not webhook_url:
        return
    
    # Prepare payload
    payload = {
        "event": "ai_insight_generated",
        "timestamp": insight_doc.creation.isoformat(),
        "data": {
            "domain": insight_doc.domain,
            "insight_type": insight_doc.insight_type,
            "prediction": insight_doc.prediction_value,
            "confidence": insight_doc.confidence_score,
            "model": insight_doc.model_used
        }
    }
    
    # Send webhook
    try:
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Secret": webhook_secret
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        response.raise_for_status()
        frappe.logger().info(f"Webhook sent successfully for {insight_doc.name}")
        
    except Exception as e:
        frappe.log_error(f"Webhook failed: {str(e)}", "AI Webhook")
```

---

## Best Practices

1. **Always check confidence scores** before acting on predictions
2. **Cache results** where appropriate to avoid repeated API calls
3. **Handle errors gracefully** - AI predictions may fail
4. **Log all AI decisions** for audit trails
5. **Test with sample data** before production deployment
6. **Monitor model performance** regularly
7. **Set appropriate alert thresholds** to avoid alert fatigue
8. **Provide feedback loops** - update models with actual outcomes

## Performance Tips

- Use batch predictions for multiple records
- Schedule heavy AI tasks during off-peak hours
- Cache frequent predictions (e.g., vehicle health scores)
- Use database indexes on frequently queried fields
- Limit historical data lookback periods

## Security Considerations

- Never expose API keys in client-side code
- Use role-based permissions for AI features
- Validate all user inputs before processing
- Log sensitive AI decisions
- Encrypt model credentials
- Use HTTPS for all API calls

---

For more examples and support:
- Review TEMS AI documentation
- Check `/apps/tems/tems/tems_ai/tests/` for unit tests
- Contact: code@tevcng.com
