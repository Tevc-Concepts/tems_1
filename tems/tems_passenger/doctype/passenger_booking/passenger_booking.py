from frappe.model.document import Document
import frappe


class PassengerBooking(Document):
    def validate(self):
        trip = getattr(self, "trip", None)
        seat_no = getattr(self, "seat_no", None)
        if trip:
            # Ensure trip vehicle type is Passenger
            veh = frappe.db.get_value("Passenger Trip", trip, "vehicle")
            if veh:
                vt = frappe.db.get_value("Vehicle", veh, "vehicle_type") or frappe.db.get_value("Vehicle", veh, "custom_vehicle_type")
                if str(vt or "").strip().lower() != "passenger":
                    frappe.throw("Booking must reference a Passenger vehicle.")

            # Capacity check
            capacity_raw = frappe.db.get_value("Passenger Trip", trip, "seat_capacity")
            try:
                capacity_i = int(str(capacity_raw)) if capacity_raw is not None else 0
            except Exception:
                capacity_i = 0
            try:
                seat_i = int(str(seat_no)) if seat_no is not None else None
            except Exception:
                seat_i = None

            if seat_i is None or seat_i <= 0:
                frappe.throw("Seat No must be a positive integer.")
            if seat_i is not None and capacity_i > 0 and seat_i > capacity_i:
                frappe.throw(f"Seat No {seat_i} exceeds trip capacity ({capacity_i}).")

            # Uniqueness check per trip
            exists = frappe.db.exists(
                "Passenger Booking",
                {
                    "trip": trip,
                    "seat_no": seat_i,
                    "name": ["!=", self.name or ""],
                },
            )
            if exists:
                frappe.throw(f"Seat {seat_i} is already booked for this trip.")
