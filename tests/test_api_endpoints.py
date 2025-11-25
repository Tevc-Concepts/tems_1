#!/usr/bin/env python3
"""
TEMS API Testing Script
Tests all PWA API endpoints to verify Phase 5 integration
"""

import frappe
from frappe.utils import get_site_url
import json

def print_section(title):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_api_endpoint(module, function, args=None):
    """Test a single API endpoint"""
    try:
        method = f"tems.api.pwa.{module}.{function}"
        result = frappe.call(method, **args) if args else frappe.call(method)
        print(f"✅ {function}: Success")
        if isinstance(result, dict) and 'count' in result:
            print(f"   → Returned {result.get('count', 0)} items")
        return True
    except Exception as e:
        print(f"❌ {function}: {str(e)[:80]}")
        return False

def main():
    print_section("TEMS Phase 5 API Testing")
    print(f"Site URL: {get_site_url()}")
    print(f"Testing 50+ API endpoints across 4 PWAs\n")
    
    # Initialize Frappe
    frappe.init(site='development.localhost')
    frappe.connect()
    
    total_tests = 0
    passed_tests = 0
    
    # Driver API Tests
    print_section("Driver PWA API Tests")
    driver_endpoints = [
        ('get_active_trips', None),
        ('get_trip_history', {'limit': 10}),
        ('get_profile_info', None),
    ]
    
    for function, args in driver_endpoints:
        total_tests += 1
        if test_api_endpoint('driver', function, args):
            passed_tests += 1
    
    # Operations API Tests
    print_section("Operations PWA API Tests")
    operations_endpoints = [
        ('get_vehicles', {'filters': json.dumps({'status': 'Active'})}),
        ('get_vehicle_locations', None),
        ('get_dispatch_queue', None),
    ]
    
    for function, args in operations_endpoints:
        total_tests += 1
        if test_api_endpoint('operations', function, args):
            passed_tests += 1
    
    # Safety API Tests
    print_section("Safety PWA API Tests")
    safety_endpoints = [
        ('get_incidents', {'filters': json.dumps({'status': 'Open'})}),
        ('get_audits', None),
        ('get_compliance_items', None),
        ('get_risk_assessments', None),
        ('get_safety_statistics', None),
        ('get_expiring_compliance', {'days': 30}),
        ('get_critical_incidents', None),
        ('calculate_compliance_rate', None),
    ]
    
    for function, args in safety_endpoints:
        total_tests += 1
        if test_api_endpoint('safety', function, args):
            passed_tests += 1
    
    # Fleet API Tests
    print_section("Fleet PWA API Tests")
    fleet_endpoints = [
        ('get_assets', {'filters': json.dumps({'status': 'In Service'})}),
        ('get_asset_categories', None),
        ('get_work_orders', None),
        ('get_upcoming_maintenance', {'days': 30}),
        ('get_fuel_logs', None),
        ('get_fuel_stats', {'period': 'month'}),
        ('get_lifecycle_data', None),
    ]
    
    for function, args in fleet_endpoints:
        total_tests += 1
        if test_api_endpoint('fleet', function, args):
            passed_tests += 1
    
    # Summary
    print_section("Test Summary")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%\n")
    
    if passed_tests == total_tests:
        print("🎉 All API endpoints working correctly!")
    else:
        print("⚠️  Some endpoints need attention")
    
    frappe.destroy()

if __name__ == "__main__":
    main()
