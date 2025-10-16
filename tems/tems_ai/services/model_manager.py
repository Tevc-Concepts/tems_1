"""
Model Manager Service
====================
Handles loading, execution, and management of AI/ML models.
"""

import frappe
import json
import requests
from typing import Dict, Any, Optional, List
import numpy as np
from datetime import datetime


class ModelManager:
    """
    Manages AI model lifecycle: loading, prediction, and result handling.
    """
    
    def __init__(self, model_name: str):
        """
        Initialize model manager with a specific model.
        
        Args:
            model_name: Name of the model in AI Model Registry
        """
        self.model_name = model_name
        self.model_config = self._load_model_config()
        self.model = None
    
    def _load_model_config(self) -> Dict:
        """Load model configuration from registry."""
        model_doc = frappe.get_doc("AI Model Registry", self.model_name)
        return model_doc.as_dict()
    
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run prediction using the configured model.
        
        Args:
            input_data: Input features for prediction
        
        Returns:
            Prediction results with confidence scores
        """
        source = self.model_config.get("source")
        
        if source == "API":
            return self._predict_via_api(input_data)
        elif source == "Local":
            return self._predict_local(input_data)
        elif source == "External":
            return self._predict_external(input_data)
        else:
            frappe.throw(f"Unknown model source: {source}")
    
    def _predict_via_api(self, input_data: Dict) -> Dict:
        """Call external AI API for prediction."""
        endpoint = self.model_config.get("endpoint_url")
        api_key = self.model_config.get("api_key")
        
        headers = {
            "Content-Type": "application/json"
        }
        
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        try:
            response = requests.post(
                endpoint,
                json=input_data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "prediction": result.get("prediction"),
                "confidence": result.get("confidence", 0.0),
                "details": result.get("details", {}),
                "timestamp": datetime.now(),
                "model": self.model_name
            }
        
        except requests.RequestException as e:
            frappe.log_error(f"API prediction error: {str(e)}", "AI Model Manager")
            return {
                "error": str(e),
                "prediction": None,
                "confidence": 0.0
            }
    
    def _predict_local(self, input_data: Dict) -> Dict:
        """
        Run prediction using locally stored model.
        For now, returns a stub - implement model loading logic based on framework.
        """
        # Placeholder for local model prediction
        # In production, load model using joblib, pickle, or TensorFlow
        
        model_type = self.model_config.get("model_type")
        
        # Simple rule-based fallback for demonstration
        if model_type == "Regression":
            # Example: simple regression stub
            prediction = self._simple_regression(input_data)
        elif model_type == "Classification":
            prediction = self._simple_classification(input_data)
        elif model_type == "Forecast":
            prediction = self._simple_forecast(input_data)
        else:
            prediction = 0.5
        
        return {
            "prediction": prediction,
            "confidence": 0.75,  # Placeholder confidence
            "details": {"method": "local_stub"},
            "timestamp": datetime.now(),
            "model": self.model_name
        }
    
    def _predict_external(self, input_data: Dict) -> Dict:
        """Predict using external service (OpenAI, Azure ML, etc.)."""
        api_provider = self.model_config.get("api_provider", "openai")
        
        if api_provider == "openai":
            return self._predict_openai(input_data)
        else:
            return {
                "error": f"Provider {api_provider} not yet implemented",
                "prediction": None,
                "confidence": 0.0
            }
    
    def _predict_openai(self, input_data: Dict) -> Dict:
        """Use OpenAI API for prediction (GPT models)."""
        # Placeholder - implement OpenAI integration
        return {
            "prediction": "pending_openai_implementation",
            "confidence": 0.0,
            "details": {"provider": "openai"}
        }
    
    def _simple_regression(self, input_data: Dict) -> float:
        """Simple regression stub."""
        # Extract numeric features and compute weighted average
        numeric_values = [v for v in input_data.values() if isinstance(v, (int, float))]
        return np.mean(numeric_values) if numeric_values else 0.5
    
    def _simple_classification(self, input_data: Dict) -> str:
        """Simple classification stub."""
        score = self._simple_regression(input_data)
        if score > 0.7:
            return "high"
        elif score > 0.4:
            return "medium"
        else:
            return "low"
    
    def _simple_forecast(self, input_data: Dict) -> List[float]:
        """Simple forecast stub."""
        base_value = self._simple_regression(input_data)
        # Generate simple trend
        return [base_value * (1 + i * 0.1) for i in range(7)]


def get_prediction(model_name: str, input_data: Dict) -> Dict:
    """
    Convenience function to get prediction from a model.
    
    Args:
        model_name: Name of the model
        input_data: Input features
    
    Returns:
        Prediction results
    """
    manager = ModelManager(model_name)
    return manager.predict(input_data)
