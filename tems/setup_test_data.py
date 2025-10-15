"""
TEMS Phase 6 - Create Employee Records and Sample Data
Links test users to Employee records and creates sample data for testing
"""

import frappe
from frappe.utils import nowdate, add_days, today

def create_employee_records():
    """Create Employee records for test users"""
    
    frappe.init(site='tems.local')
    frappe.connect()
    frappe.set_user('Administrator')
    
    print("\n" + "="*70)
    print("  TEMS Phase 6 - Creating Employee Records & Sample Data")
    print("="*70 + "\n")
    
    # Employee data for test users
    employees = [
        {
            'user_id': 'driver.test@tems.local',
            'first_name': 'Test',
            'last_name': 'Driver',
            'employee_name': 'Test Driver',
            'designation': 'Driver',
            'department': 'Transportation',
            'gender': 'Male',
            'date_of_birth': '1990-01-15',
            'date_of_joining': '2024-01-01',
            'status': 'Active',
            'cell_number': '+1234567890',
        },
        {
            'user_id': 'operations.test@tems.local',
            'first_name': 'Test',
            'last_name': 'Operations',
            'employee_name': 'Test Operations Manager',
            'designation': 'Operations Manager',
            'department': 'Operations',
            'gender': 'Female',
            'date_of_birth': '1988-05-20',
            'date_of_joining': '2023-06-01',
            'status': 'Active',
            'cell_number': '+1234567891',
        },
        {
            'user_id': 'safety.test@tems.local',
            'first_name': 'Test',
            'last_name': 'Safety',
            'employee_name': 'Test Safety Officer',
            'designation': 'Safety Officer',
            'department': 'Safety & Compliance',
            'gender': 'Male',
            'date_of_birth': '1985-08-12',
            'date_of_joining': '2022-03-15',
            'status': 'Active',
            'cell_number': '+1234567892',
        },
        {
            'user_id': 'fleet.test@tems.local',
            'first_name': 'Test',
            'last_name': 'Fleet',
            'employee_name': 'Test Fleet Manager',
            'designation': 'Fleet Manager',
            'department': 'Fleet Management',
            'gender': 'Female',
            'date_of_birth': '1987-11-03',
            'date_of_joining': '2023-01-10',
            'status': 'Active',
            'cell_number': '+1234567893',
        }
    ]
    
    created_employees = []
    
    for emp_data in employees:
        try:
            # Check if employee exists
            existing = frappe.db.get_value('Employee', {'user_id': emp_data['user_id']}, 'name')
            
            if existing:
                print(f"⚠️  Employee already exists for {emp_data['user_id']}")
                employee = frappe.get_doc('Employee', existing)
            else:
                # Create employee
                employee = frappe.get_doc({
                    'doctype': 'Employee',
                    'naming_series': 'HR-EMP-',
                    **emp_data
                })
                employee.insert(ignore_permissions=True)
                print(f"✅ Created Employee: {employee.employee_name} ({employee.name})")
            
            created_employees.append({
                'name': employee.name,
                'employee_name': employee.employee_name,
                'user_id': employee.user_id,
                'designation': employee.designation
            })
            
        except Exception as e:
            print(f"❌ Error creating employee for {emp_data['user_id']}: {str(e)}")
            frappe.log_error(f"Employee creation failed: {str(e)}", "Phase 6 Setup")
    
    frappe.db.commit()
    
    # Print summary
    print("\n" + "="*70)
    print("  Employee Records Created")
    print("="*70 + "\n")
    
    for emp in created_employees:
        print(f"Employee: {emp['name']}")
        print(f"  Name: {emp['employee_name']}")
        print(f"  User: {emp['user_id']}")
        print(f"  Role: {emp['designation']}\n")
    
    frappe.destroy()
    return created_employees

def create_sample_vehicles():
    """Create sample vehicles for testing"""
    
    frappe.init(site='tems.local')
    frappe.connect()
    frappe.set_user('Administrator')
    
    print("\n" + "="*70)
    print("  Creating Sample Vehicles")
    print("="*70 + "\n")
    
    vehicles = [
        {
            'make': 'Toyota',
            'model': 'HiAce',
            'license_plate': 'TEST-001',
            'year': 2023,
            'vehicle_type': 'Van',
            'capacity': 14,
            'status': 'Active'
        },
        {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'license_plate': 'TEST-002',
            'year': 2022,
            'vehicle_type': 'Bus',
            'capacity': 20,
            'status': 'Active'
        },
        {
            'make': 'Isuzu',
            'model': 'NQR',
            'license_plate': 'TEST-003',
            'year': 2023,
            'vehicle_type': 'Truck',
            'capacity': 5000,  # kg
            'status': 'Active'
        }
    ]
    
    created_vehicles = []
    
    for vehicle_data in vehicles:
        try:
            # Check if vehicle exists
            existing = frappe.db.exists('Vehicle', {'license_plate': vehicle_data['license_plate']})
            
            if existing:
                print(f"⚠️  Vehicle {vehicle_data['license_plate']} already exists")
                continue
            
            # Create vehicle
            vehicle = frappe.get_doc({
                'doctype': 'Vehicle',
                **vehicle_data
            })
            vehicle.insert(ignore_permissions=True)
            
            created_vehicles.append(vehicle.name)
            print(f"✅ Created Vehicle: {vehicle.license_plate} ({vehicle.make} {vehicle.model})")
            
        except Exception as e:
            print(f"❌ Error creating vehicle {vehicle_data['license_plate']}: {str(e)}")
            frappe.log_error(f"Vehicle creation failed: {str(e)}", "Phase 6 Setup")
    
    frappe.db.commit()
    
    print(f"\n✅ Created {len(created_vehicles)} vehicles\n")
    
    frappe.destroy()
    return created_vehicles

def create_sample_journey_plans():
    """Create sample journey plans for Driver testing"""
    
    frappe.init(site='tems.local')
    frappe.connect()
    frappe.set_user('Administrator')
    
    print("\n" + "="*70)
    print("  Creating Sample Journey Plans")
    print("="*70 + "\n")
    
    # Get driver employee
    driver_employee = frappe.db.get_value('Employee', {'user_id': 'driver.test@tems.local'}, 'name')
    
    if not driver_employee:
        print("❌ Driver employee not found. Create employees first.")
        frappe.destroy()
        return []
    
    # Get a vehicle
    vehicle = frappe.db.get_value('Vehicle', {'status': 'Active'}, 'name')
    
    if not vehicle:
        print("❌ No active vehicle found. Create vehicles first.")
        frappe.destroy()
        return []
    
    journey_plans = [
        {
            'route': 'City Center to Airport',
            'driver': driver_employee,
            'vehicle': vehicle,
            'scheduled_date': today(),
            'start_time': '08:00:00',
            'end_time': '10:00:00',
            'status': 'Scheduled',
            'distance_km': 25
        },
        {
            'route': 'Airport to Business District',
            'driver': driver_employee,
            'vehicle': vehicle,
            'scheduled_date': add_days(today(), 1),
            'start_time': '14:00:00',
            'end_time': '16:00:00',
            'status': 'Scheduled',
            'distance_km': 30
        }
    ]
    
    created_journeys = []
    
    for journey_data in journey_plans:
        try:
            journey = frappe.get_doc({
                'doctype': 'Journey Plan',
                **journey_data
            })
            journey.insert(ignore_permissions=True)
            
            created_journeys.append(journey.name)
            print(f"✅ Created Journey Plan: {journey.name} - {journey.route}")
            
        except Exception as e:
            print(f"❌ Error creating journey plan: {str(e)}")
            # Journey Plan doctype might not exist, that's okay
            print("   (Journey Plan doctype may not exist - this is optional)")
    
    frappe.db.commit()
    
    if created_journeys:
        print(f"\n✅ Created {len(created_journeys)} journey plans\n")
    else:
        print("\n⚠️  No journey plans created (doctype may not exist)\n")
    
    frappe.destroy()
    return created_journeys

def main():
    """Main execution"""
    print("\n" + "="*70)
    print("  TEMS Phase 6 - Data Setup")
    print("  Creating Employee Records and Sample Data")
    print("="*70)
    
    # Create employees
    employees = create_employee_records()
    
    # Create vehicles
    vehicles = create_sample_vehicles()
    
    # Create journey plans (optional - doctype might not exist)
    # journeys = create_sample_journey_plans()
    
    # Summary
    print("\n" + "="*70)
    print("  Setup Complete!")
    print("="*70)
    print(f"\n✅ Created {len(employees)} employees")
    print(f"✅ Created {len(vehicles)} vehicles")
    print("\n🎯 Driver and Operations APIs now have data for testing!\n")

if __name__ == "__main__":
    main()
