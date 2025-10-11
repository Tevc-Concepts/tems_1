from frappe.model.document import Document
import frappe


class CargoWaybill(Document):
    def validate(self):
        manifest = getattr(self, "manifest", None)
        if manifest:
            op = frappe.db.get_value("Cargo Manifest", manifest, "operation_plan")
            if op:
                mode = frappe.db.get_value("Operation Plan", op, "operation_mode")
                if str(mode or "").strip().lower() != "cargo":
                    frappe.throw("Waybill must reference a Cargo operation.")
