# Copyright (c) 2025, Tevc Concepts Limited and contributors
# For license information, please see license.txt

import frappe
from pydoc import doc
from frappe.model.document import Document


class RiskRegister(Document):


	
	# Server Script: Risk Register - before_save
	# Calculate inherent and residual risk scores and rating
	def before_save(self):
		self.inherent_risk_score = (self.likelihood or 0) * (self.impact or 0)

		# Controls effectiveness can dampen residual by a factor
		effect_map = {
			"Ineffective": 1.0,
			"Partial": 0.85,
			"Adequate": 0.7,
			"Strong": 0.5
		}
		factor = effect_map.get(self.controls_effectiveness, 1.0)
		base_residual = (self.residual_likelihood or self.likelihood or 0) * (self.residual_impact or self.impact or 0)
		self.residual_risk_score = round(base_residual * factor, 2)

		self.risk_rating = calc_rating(self.residual_risk_score)


	def calc_rating(score):
		if score <= 5:
			return "Low"
		if score <= 10:
			return "Moderate"
		if score <= 15:
			return "High"
		return "Critical"