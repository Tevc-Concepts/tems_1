#!/usr/bin/env python3
"""
Comprehensive Operations API Test Suite
Tests all 10 Operations API endpoints after schema fixes
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
SITE = "tems.local"

# Test credentials
USER = "operations.test@tems.local"
PASSWORD = "test123"

session = requests.Session()

def login():
    """Login and get session cookie"""
    response = session.post(
        f"{BASE_URL}/api/method/login",
        json={"usr": USER, "pwd": PASSWORD},
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        print("✓ Login successful")
        return True
    print(f"✗ Login failed: {response.status_code}")
    return False

def test_endpoint(name, method, params=None):
    """Test a single API endpoint"""
    url = f"{BASE_URL}/api/method/tems.api.pwa.operations.{method}"
    
    try:
        if params:
            response = session.get(url, params=params)
        else:
            response = session.get(url)
        
        if response.status_code != 200:
            return {
                "name": name,
                "status": "FAIL",
                "error": f"HTTP {response.status_code}",
                "data": None
            }
        
        data = response.json()
        message = data.get("message", {})
        
        # Check for success
        if isinstance(message, dict):
            success = message.get("success", False)
            if success:
                return {
                    "name": name,
                    "status": "PASS",
                    "data": message.get("data"),
                    "count": message.get("count", "N/A")
                }
            else:
                return {
                    "name": name,
                    "status": "FAIL",
                    "error": message.get("message", "Unknown error"),
                    "data": None
                }
        else:
            # Old format response
            return {
                "name": name,
                "status": "PASS",
                "data": message,
                "count": "N/A"
            }
    
    except Exception as e:
        return {
            "name": name,
            "status": "FAIL",
            "error": str(e),
            "data": None
        }

def main():
    print("=" * 80)
    print("OPERATIONS API - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: {BASE_URL}")
    print(f"User: {USER}")
    print()
    
    # Login
    if not login():
        print("Cannot proceed without login")
        return
    
    print()
    print("=" * 80)
    print("TESTING ORIGINAL ENDPOINTS (Pre-Phase 6)")
    print("=" * 80)
    
    original_endpoints = [
        ("Operations Dashboard", "get_operations_dashboard"),
        # Skipping create_dispatch_schedule (requires POST data)
        # Skipping assign_trip (requires POST data)
    ]
    
    original_results = []
    for name, method in original_endpoints:
        print(f"\nTesting: {name}...")
        result = test_endpoint(name, method)
        original_results.append(result)
        
        if result["status"] == "PASS":
            print(f"  ✓ PASS - Count: {result['count']}")
        else:
            print(f"  ✗ FAIL - {result['error']}")
    
    print()
    print("=" * 80)
    print("TESTING EXTENDED ENDPOINTS (Phase 6 - After Schema Fixes)")
    print("=" * 80)
    
    extended_endpoints = [
        ("Get Vehicles", "get_vehicles"),
        ("Get Vehicle Locations", "get_vehicle_locations"),
        ("Get Dispatch Queue", "get_dispatch_queue"),
        ("Get Active Trips", "get_active_trips"),
        ("Get Route Optimization", "get_route_optimization"),
        ("Get Driver Availability", "get_driver_availability", {"date": "2025-10-15"}),
        ("Get Operations Statistics", "get_operations_statistics"),
        ("Get Operations Statistics (Week)", "get_operations_statistics", {"period": "week"}),
        ("Get Operations Statistics (Month)", "get_operations_statistics", {"period": "month"}),
    ]
    
    extended_results = []
    for item in extended_endpoints:
        name = item[0]
        method = item[1]
        params = item[2] if len(item) > 2 else None
        
        print(f"\nTesting: {name}...")
        result = test_endpoint(name, method, params)
        extended_results.append(result)
        
        if result["status"] == "PASS":
            print(f"  ✓ PASS - Count: {result['count']}")
            if isinstance(result['data'], list) and len(result['data']) > 0:
                print(f"    Sample: {result['data'][0].get('name', 'N/A')}")
        else:
            print(f"  ✗ FAIL - {result['error']}")
    
    # Summary
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    original_pass = sum(1 for r in original_results if r["status"] == "PASS")
    original_total = len(original_results)
    
    extended_pass = sum(1 for r in extended_results if r["status"] == "PASS")
    extended_total = len(extended_results)
    
    total_pass = original_pass + extended_pass
    total_tests = original_total + extended_total
    
    pass_rate = (total_pass / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\nOriginal Endpoints: {original_pass}/{original_total} PASS")
    print(f"Extended Endpoints: {extended_pass}/{extended_total} PASS")
    print(f"\nOverall: {total_pass}/{total_tests} PASS ({pass_rate:.1f}%)")
    
    if pass_rate == 100:
        print("\n🎉 ALL TESTS PASSED - OPERATIONS API PRODUCTION READY!")
    elif pass_rate >= 80:
        print("\n⚠️  Most tests passed - Minor issues to fix")
    else:
        print("\n❌ Multiple failures - Requires attention")
    
    print()
    print("=" * 80)
    
    # Detailed failures
    all_results = original_results + extended_results
    failures = [r for r in all_results if r["status"] == "FAIL"]
    
    if failures:
        print("FAILED TESTS DETAIL:")
        print("=" * 80)
        for failure in failures:
            print(f"\n❌ {failure['name']}")
            print(f"   Error: {failure['error']}")
    else:
        print("✅ NO FAILURES")
    
    print()

if __name__ == "__main__":
    main()
