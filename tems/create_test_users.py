"""
TEMS Phase 6 - Test User Setup Script
Creates test users for all TEMS roles with proper permissions
"""

import frappe
from frappe.utils.password import update_password

def create_test_users():
    """Create test users for TEMS PWA testing"""
    
    frappe.init(site='tems.local')
    frappe.connect()
    frappe.set_user('Administrator')
    
    test_users = [
        {
            'email': 'driver.test@tems.local',
            'first_name': 'Test',
            'last_name': 'Driver',
            'roles': ['Driver', 'TEMS Driver'],
            'pwa': 'Driver PWA'
        },
        {
            'email': 'operations.test@tems.local',
            'first_name': 'Test',
            'last_name': 'Operations',
            'roles': ['Operations Manager', 'TEMS Operations'],
            'pwa': 'Operations PWA'
        },
        {
            'email': 'safety.test@tems.local',
            'first_name': 'Test',
            'last_name': 'Safety',
            'roles': ['Safety Officer', 'TEMS Safety'],
            'pwa': 'Safety PWA'
        },
        {
            'email': 'fleet.test@tems.local',
            'first_name': 'Test',
            'last_name': 'Fleet',
            'roles': ['Fleet Manager', 'TEMS Fleet'],
            'pwa': 'Fleet PWA'
        }
    ]
    
    print("\n" + "="*70)
    print("  TEMS Phase 6 - Creating Test Users")
    print("="*70 + "\n")
    
    created_users = []
    
    for user_data in test_users:
        try:
            # Check if user exists
            if frappe.db.exists('User', user_data['email']):
                print(f"⚠️  User {user_data['email']} already exists. Updating...")
                user = frappe.get_doc('User', user_data['email'])
            else:
                # Create new user
                user = frappe.get_doc({
                    'doctype': 'User',
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'enabled': 1,
                    'send_welcome_email': 0,
                    'user_type': 'System User'
                })
                user.insert(ignore_permissions=True)
                print(f"✅ Created user: {user_data['email']}")
            
            # Assign roles
            existing_roles = [d.role for d in user.roles]
            for role in user_data['roles']:
                if role not in existing_roles:
                    # Check if role exists, create if not
                    if not frappe.db.exists('Role', role):
                        role_doc = frappe.get_doc({
                            'doctype': 'Role',
                            'role_name': role,
                            'desk_access': 1
                        })
                        role_doc.insert(ignore_permissions=True)
                        print(f"   → Created role: {role}")
                    
                    user.append('roles', {
                        'role': role
                    })
            
            user.save(ignore_permissions=True)
            
            # Set password
            password = 'test123'  # Simple password for testing
            update_password(user.name, password)
            
            created_users.append({
                'email': user_data['email'],
                'password': password,
                'pwa': user_data['pwa'],
                'roles': user_data['roles']
            })
            
            print(f"   → Assigned roles: {', '.join(user_data['roles'])}")
            print(f"   → Password set: {password}")
            print(f"   → PWA Access: {user_data['pwa']}\n")
            
        except Exception as e:
            print(f"❌ Error creating user {user_data['email']}: {str(e)}\n")
            frappe.log_error(f"Test user creation failed: {str(e)}", "Phase 6 Setup")
    
    frappe.db.commit()
    
    # Print summary
    print("\n" + "="*70)
    print("  Test Users Summary")
    print("="*70 + "\n")
    
    print("| Email                         | Password | PWA             | Roles |")
    print("|-------------------------------|----------|-----------------|-------|")
    for user in created_users:
        roles_str = ', '.join(user['roles'][:2])  # Show first 2 roles
        print(f"| {user['email']:29} | {user['password']:8} | {user['pwa']:15} | {roles_str[:30]:30} |")
    
    print("\n" + "="*70)
    print(f"  Total Users Created: {len(created_users)}")
    print("="*70 + "\n")
    
    # Create credentials file
    with open('/workspace/development/frappe-bench/apps/tems/TEST_CREDENTIALS.txt', 'w') as f:
        f.write("TEMS Phase 6 - Test User Credentials\n")
        f.write("="*70 + "\n\n")
        f.write("IMPORTANT: These are test credentials only. Do not use in production!\n\n")
        
        for user in created_users:
            f.write(f"{user['pwa']}:\n")
            f.write(f"  Email:    {user['email']}\n")
            f.write(f"  Password: {user['password']}\n")
            f.write(f"  Roles:    {', '.join(user['roles'])}\n")
            f.write(f"  URL:      http://localhost:8000/{user['pwa'].lower().split()[0]}\n\n")
    
    print("📝 Credentials saved to: TEST_CREDENTIALS.txt\n")
    
    frappe.destroy()
    
    return created_users

if __name__ == "__main__":
    create_test_users()
