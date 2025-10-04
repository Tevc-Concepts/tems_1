import frappe

def execute():
    """Seed minimal finance data for Allocation Rule and sample Lease Loan if absent."""
    # Allocation Rule sample
    if not frappe.db.exists("Allocation Rule", {"title": "Vehicle Overhead Allocation"}):
        doc = frappe.get_doc({
            "doctype": "Allocation Rule",
            "title": "Vehicle Overhead Allocation",
            "allocation_basis": "Vehicle",
            "percentage": 5.0,
            "notes": "Seed rule: apply 5% overhead to vehicle direct costs"
        })
        doc.insert(ignore_permissions=True)

    # Sample Lease Loan (if Lease Loan DocType exists)
    if frappe.db.table_exists("Lease Loan") and not frappe.db.exists("Lease Loan", {"loan_name": "Seed Test Loan"}):
        try:
            vehicle = frappe.get_all("Vehicle", limit=1, pluck="name")
            vehicle_name = vehicle[0] if vehicle else None
            loan = frappe.get_doc({
                "doctype": "Lease Loan",
                "loan_name": "Seed Test Loan",
                "principal": 100000,
                "rate": 12.0,
                "status": "Active",
                "vehicle": vehicle_name
            })
            loan.insert(ignore_permissions=True)
        except Exception:
            pass
