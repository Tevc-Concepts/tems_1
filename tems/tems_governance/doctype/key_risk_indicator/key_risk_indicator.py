# Copyright (c) 2025, Tevc Concepts Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class KeyRiskIndicator(Document):
	# Server Script: Key Risk Indicator - before_save
	def before_save(self):
		self.update_status()

	def update_status(self):
		val = self.current_value or 0
		if val >= (self.threshold_high or 0):
			self.status = "Alert"
		elif val >= (self.threshold_medium or 0):
			self.status = "Warning"
		else:
			self.status = "Normal"

