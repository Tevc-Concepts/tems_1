# test_tyre_calculator.py
import frappe
import unittest
from tems.tems_tyre.utils.tyre_calculator import calculate_cost_per_km

class TestTyreCalculator(unittest.TestCase):
    def test_cost_per_km(self):
        # Create test tyre
        tyre = frappe.get_doc({
            "doctype": "Tyre",
            "brand": "Test Brand",
            "model": "Test Model",
            "size": "315/80R22.5",
            "tyre_type": "Drive",
            "cost": 50000,
            "status": "In Stock",
            "current_mileage": 10000
        }).insert()
        
        cost = calculate_cost_per_km(tyre.name)
        self.assertEqual(cost, 5.0)  # 50000 / 10000
        
        tyre.delete()