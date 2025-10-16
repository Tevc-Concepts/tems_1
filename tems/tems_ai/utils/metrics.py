"""
Metrics and Evaluation Utilities
=================================
Tools for evaluating AI model performance and calculating metrics.
"""

import frappe
from typing import List, Dict, Optional
import math


def calculate_accuracy(predictions: List, actuals: List) -> float:
    """
    Calculate classification accuracy.
    
    Args:
        predictions: List of predicted values
        actuals: List of actual values
    
    Returns:
        Accuracy score (0-1)
    """
    if len(predictions) != len(actuals) or not predictions:
        return 0.0
    
    correct = sum(p == a for p, a in zip(predictions, actuals))
    return correct / len(predictions)


def calculate_mae(predictions: List[float], actuals: List[float]) -> float:
    """
    Calculate Mean Absolute Error.
    
    Args:
        predictions: List of predicted values
        actuals: List of actual values
    
    Returns:
        MAE value
    """
    if len(predictions) != len(actuals) or not predictions:
        return 0.0
    
    return sum(abs(p - a) for p, a in zip(predictions, actuals)) / len(predictions)


def calculate_rmse(predictions: List[float], actuals: List[float]) -> float:
    """
    Calculate Root Mean Squared Error.
    
    Args:
        predictions: List of predicted values
        actuals: List of actual values
    
    Returns:
        RMSE value
    """
    if len(predictions) != len(actuals) or not predictions:
        return 0.0
    
    mse = sum((p - a) ** 2 for p, a in zip(predictions, actuals)) / len(predictions)
    return math.sqrt(mse)


def calculate_mape(predictions: List[float], actuals: List[float]) -> float:
    """
    Calculate Mean Absolute Percentage Error.
    
    Args:
        predictions: List of predicted values
        actuals: List of actual values
    
    Returns:
        MAPE value (as percentage)
    """
    if len(predictions) != len(actuals) or not predictions:
        return 0.0
    
    # Filter out zero actuals to avoid division by zero
    valid_pairs = [(p, a) for p, a in zip(predictions, actuals) if a != 0]
    
    if not valid_pairs:
        return 0.0
    
    mape = sum(abs((p - a) / a) for p, a in valid_pairs) / len(valid_pairs)
    return mape * 100  # Return as percentage


def calculate_precision_recall(
    predictions: List, 
    actuals: List, 
    positive_label: str = "high"
) -> Dict[str, float]:
    """
    Calculate precision and recall for binary classification.
    
    Args:
        predictions: List of predicted labels
        actuals: List of actual labels
        positive_label: The label to consider as positive
    
    Returns:
        Dict with precision, recall, and F1 score
    """
    if len(predictions) != len(actuals) or not predictions:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    
    tp = sum(1 for p, a in zip(predictions, actuals) if p == positive_label and a == positive_label)
    fp = sum(1 for p, a in zip(predictions, actuals) if p == positive_label and a != positive_label)
    fn = sum(1 for p, a in zip(predictions, actuals) if p != positive_label and a == positive_label)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


def evaluate_model_performance(model_name: str, limit: int = 100) -> Dict:
    """
    Evaluate overall model performance based on logged predictions.
    
    Args:
        model_name: Name of the model to evaluate
        limit: Number of recent predictions to evaluate
    
    Returns:
        Performance metrics dict
    """
    # Get recent insights from this model
    insights = frappe.get_all(
        "AI Insight Log",
        filters={"model_used": model_name},
        fields=["prediction_value", "confidence_score", "actual_value"],
        order_by="creation desc",
        limit=limit
    )
    
    if not insights:
        return {"error": "No insights found for this model"}
    
    # Calculate average confidence
    avg_confidence = sum(i.get("confidence_score", 0) for i in insights) / len(insights)
    
    # Count predictions by confidence bracket
    high_confidence = sum(1 for i in insights if i.get("confidence_score", 0) > 0.8)
    medium_confidence = sum(1 for i in insights if 0.5 < i.get("confidence_score", 0) <= 0.8)
    low_confidence = sum(1 for i in insights if i.get("confidence_score", 0) <= 0.5)
    
    metrics = {
        "model_name": model_name,
        "total_predictions": len(insights),
        "avg_confidence": round(avg_confidence, 3),
        "high_confidence_count": high_confidence,
        "medium_confidence_count": medium_confidence,
        "low_confidence_count": low_confidence,
        "confidence_distribution": {
            "high": round(high_confidence / len(insights) * 100, 1),
            "medium": round(medium_confidence / len(insights) * 100, 1),
            "low": round(low_confidence / len(insights) * 100, 1)
        }
    }
    
    # If actual values are available, calculate accuracy
    insights_with_actuals = [i for i in insights if i.get("actual_value")]
    
    if insights_with_actuals:
        predictions = [i.get("prediction_value") for i in insights_with_actuals]
        actuals = [i.get("actual_value") for i in insights_with_actuals]
        
        metrics["accuracy"] = calculate_accuracy(predictions, actuals)
        metrics["validated_predictions"] = len(insights_with_actuals)
    
    return metrics


def track_model_drift(model_name: str, window_days: int = 30) -> Dict:
    """
    Track model performance drift over time.
    
    Args:
        model_name: Name of the model
        window_days: Time window to analyze
    
    Returns:
        Drift analysis dict
    """
    # Get insights from the time window
    insights = frappe.db.sql("""
        SELECT 
            DATE(creation) as prediction_date,
            AVG(confidence_score) as avg_confidence,
            COUNT(*) as prediction_count
        FROM `tabAI Insight Log`
        WHERE model_used = %s
        AND DATE(creation) >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        GROUP BY DATE(creation)
        ORDER BY prediction_date
    """, (model_name, window_days), as_dict=True)
    
    if not insights or len(insights) < 2:
        return {"error": "Insufficient data for drift analysis"}
    
    # Calculate trend
    confidences = [i["avg_confidence"] for i in insights]
    trend = "stable"
    
    if len(confidences) >= 5:
        recent_avg = sum(confidences[-5:]) / 5
        earlier_avg = sum(confidences[:-5]) / (len(confidences) - 5) if len(confidences) > 5 else confidences[0]
        
        if recent_avg < earlier_avg - 0.1:
            trend = "declining"
        elif recent_avg > earlier_avg + 0.1:
            trend = "improving"
    
    return {
        "model_name": model_name,
        "window_days": window_days,
        "data_points": len(insights),
        "confidence_trend": trend,
        "latest_confidence": confidences[-1] if confidences else 0,
        "earliest_confidence": confidences[0] if confidences else 0,
        "daily_data": insights
    }
