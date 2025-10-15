#!/usr/bin/env python3
"""
TEMS Phase 6 - Comprehensive API Testing
Tests all PWA API endpoints with authentication
"""

import requests
import json
from datetime import datetime

class TEMSAPITester:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = {
            'driver': [],
            'operations': [],
            'safety': [],
            'fleet': []
        }
        
    def print_header(self, title):
        """Print section header"""
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    
    def login(self, usr, pwd):
        """Login to Frappe"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/method/login",
                data={'usr': usr, 'pwd': pwd}
            )
            if response.status_code == 200:
                print(f"✅ Login successful: {usr}")
                return True
            else:
                print(f"❌ Login failed: {usr} - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    def logout(self):
        """Logout from Frappe"""
        try:
            response = self.session.post(f"{self.base_url}/api/method/logout")
            if response.status_code == 200:
                print("✅ Logout successful\n")
                return True
        except Exception as e:
            print(f"❌ Logout error: {str(e)}\n")
            return False
    
    def test_endpoint(self, module, method, params=None, pwa_name=''):
        """Test a single API endpoint"""
        endpoint = f"{self.base_url}/api/method/tems.api.pwa.{module}.{method}"
        
        try:
            if params:
                response = self.session.get(endpoint, params=params)
            else:
                response = self.session.get(endpoint)
            
            success = response.status_code == 200
            
            result = {
                'method': method,
                'status': response.status_code,
                'success': success,
                'endpoint': endpoint
            }
            
            if success:
                try:
                    data = response.json()
                    result['response'] = data
                    
                    # Check for standard response format
                    if isinstance(data, dict):
                        result['has_message'] = 'message' in data
                        if 'message' in data and isinstance(data['message'], dict):
                            result['data_success'] = data['message'].get('success', False)
                            result['count'] = data['message'].get('count', 0)
                except:
                    pass
                
                print(f"  ✅ {method}")
                if 'count' in result:
                    print(f"     → Returned {result['count']} items")
            else:
                print(f"  ❌ {method} - Status: {response.status_code}")
                result['error'] = response.text[:100]
            
            self.test_results[pwa_name].append(result)
            return success
            
        except Exception as e:
            print(f"  ❌ {method} - Error: {str(e)[:80]}")
            self.test_results[pwa_name].append({
                'method': method,
                'success': False,
                'error': str(e)
            })
            return False
    
    def test_driver_api(self):
        """Test Driver PWA APIs"""
        self.print_header("Driver PWA API Tests")
        
        if not self.login('driver.test@tems.local', 'test123'):
            return
        
        tests = [
            ('get_active_trips', None),
            ('get_trip_history', {'limit': 10}),
            ('get_upcoming_trips', None),
            ('get_profile_info', None),
            ('get_documents', None),
            ('get_notifications', None),
        ]
        
        passed = 0
        for method, params in tests:
            if self.test_endpoint('driver', method, params, 'driver'):
                passed += 1
        
        print(f"\n  Driver API: {passed}/{len(tests)} tests passed")
        self.logout()
    
    def test_operations_api(self):
        """Test Operations PWA APIs"""
        self.print_header("Operations PWA API Tests")
        
        if not self.login('operations.test@tems.local', 'test123'):
            return
        
        tests = [
            ('get_vehicles', {'filters': json.dumps({'status': 'Active'})}),
            ('get_vehicle_locations', None),
            ('get_dispatch_queue', None),
            ('get_active_trips', None),
            ('get_route_optimization', None),
            ('get_driver_availability', None),
            ('get_operations_statistics', None),
        ]
        
        passed = 0
        for method, params in tests:
            if self.test_endpoint('operations', method, params, 'operations'):
                passed += 1
        
        print(f"\n  Operations API: {passed}/{len(tests)} tests passed")
        self.logout()
    
    def test_safety_api(self):
        """Test Safety PWA APIs"""
        self.print_header("Safety PWA API Tests")
        
        if not self.login('safety.test@tems.local', 'test123'):
            return
        
        tests = [
            ('get_incidents', {'filters': json.dumps({'status': 'Open'})}),
            ('get_audits', None),
            ('get_compliance_items', None),
            ('get_risk_assessments', None),
            ('get_safety_statistics', None),
            ('get_expiring_compliance', {'days': '30'}),
            ('get_critical_incidents', None),
            ('calculate_compliance_rate', None),
        ]
        
        passed = 0
        for method, params in tests:
            if self.test_endpoint('safety', method, params, 'safety'):
                passed += 1
        
        print(f"\n  Safety API: {passed}/{len(tests)} tests passed")
        self.logout()
    
    def test_fleet_api(self):
        """Test Fleet PWA APIs"""
        self.print_header("Fleet PWA API Tests")
        
        if not self.login('fleet.test@tems.local', 'test123'):
            return
        
        tests = [
            ('get_assets', {'filters': json.dumps({'status': 'In Service'})}),
            ('get_asset_categories', None),
            ('get_work_orders', None),
            ('get_upcoming_maintenance', {'days': '30'}),
            ('get_fuel_logs', None),
            ('get_fuel_stats', {'period': 'month'}),
            ('get_lifecycle_data', None),
        ]
        
        passed = 0
        for method, params in tests:
            if self.test_endpoint('fleet', method, params, 'fleet'):
                passed += 1
        
        print(f"\n  Fleet API: {passed}/{len(tests)} tests passed")
        self.logout()
    
    def generate_report(self):
        """Generate test report"""
        self.print_header("Test Summary Report")
        
        total_tests = sum(len(results) for results in self.test_results.values())
        total_passed = sum(
            sum(1 for r in results if r.get('success'))
            for results in self.test_results.values()
        )
        
        print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for pwa, results in self.test_results.items():
            if results:
                passed = sum(1 for r in results if r.get('success'))
                print(f"{pwa.upper()} PWA: {passed}/{len(results)} passed")
        
        print(f"\n{'='*70}")
        print(f"TOTAL: {total_passed}/{total_tests} tests passed")
        print(f"Success Rate: {(total_passed/total_tests*100):.1f}%")
        print(f"{'='*70}\n")
        
        # Save detailed report
        report_file = '/workspace/development/frappe-bench/apps/tems/API_TEST_REPORT.json'
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_tests': total_tests,
                'total_passed': total_passed,
                'success_rate': (total_passed/total_tests*100),
                'results': self.test_results
            }, f, indent=2)
        
        print(f"📝 Detailed report saved to: API_TEST_REPORT.json\n")
        
        if total_passed == total_tests:
            print("🎉 All API tests passed!")
        elif total_passed / total_tests >= 0.8:
            print("✅ Most API tests passed (>80%)")
        else:
            print("⚠️  Some API endpoints need attention")

def main():
    print("\n" + "="*70)
    print("  TEMS Phase 6 - Comprehensive API Testing")
    print("="*70)
    print("\nTesting 30+ API endpoints across 4 PWAs")
    print("Base URL: http://localhost:8000\n")
    
    tester = TEMSAPITester()
    
    # Run all tests
    tester.test_driver_api()
    tester.test_operations_api()
    tester.test_safety_api()
    tester.test_fleet_api()
    
    # Generate report
    tester.generate_report()

if __name__ == "__main__":
    main()
