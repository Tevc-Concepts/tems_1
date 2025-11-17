# Copyright (c) 2025, Tevc Concepts Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ERiskAssessment(Document):
	# Server Script: Risk Assessment - before_save
	def before_save(self):
		scores = []
		for r in self.get("risks") or []:
			if r.residual_risk_score:
				scores.append(r.residual_risk_score)
		avg = sum(scores)/len(scores) if scores else 0
		self.overall_residual_rating = (
			"Low" if avg <= 5 else
			"Moderate" if avg <= 10 else
			"High" if avg <= 15 else
			"Critical"
		)

