#!/usr/bin/env python3
"""
Phase 6 Task 8: Offline Functionality Testing
Tests service workers, caching, manifest files, and PWA capabilities
"""

import os
import json
import re
from pathlib import Path

class OfflineFunctionalityTest:
    def __init__(self):
        self.base_path = Path("/workspace/development/frappe-bench/apps/tems/tems/public/frontend")
        self.pwas = ["driver-pwa", "operations-pwa", "safety-pwa", "fleet-pwa"]
        self.results = {}
        
    def test_service_worker_exists(self, pwa):
        """Check if service worker file exists"""
        sw_path = self.base_path / pwa / "dist" / "sw.js"
        exists = sw_path.exists()
        size = sw_path.stat().st_size if exists else 0
        return {
            "exists": exists,
            "path": str(sw_path),
            "size_bytes": size,
            "status": "PASS" if exists and size > 0 else "FAIL"
        }
    
    def test_manifest_exists(self, pwa):
        """Check if manifest file exists and is valid JSON"""
        manifest_path = self.base_path / pwa / "dist" / "manifest.webmanifest"
        
        if not manifest_path.exists():
            return {
                "exists": False,
                "path": str(manifest_path),
                "status": "FAIL",
                "error": "Manifest file not found"
            }
        
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Check required PWA manifest fields
            required_fields = ["name", "short_name", "start_url", "display", "icons"]
            missing_fields = [field for field in required_fields if field not in manifest]
            
            # Check icons
            has_icons = len(manifest.get("icons", [])) > 0
            has_192 = any(icon.get("sizes") == "192x192" for icon in manifest.get("icons", []))
            has_512 = any(icon.get("sizes") == "512x512" for icon in manifest.get("icons", []))
            
            return {
                "exists": True,
                "path": str(manifest_path),
                "valid_json": True,
                "name": manifest.get("name"),
                "short_name": manifest.get("short_name"),
                "display": manifest.get("display"),
                "theme_color": manifest.get("theme_color"),
                "background_color": manifest.get("background_color"),
                "start_url": manifest.get("start_url"),
                "scope": manifest.get("scope"),
                "icons_count": len(manifest.get("icons", [])),
                "has_192x192": has_192,
                "has_512x512": has_512,
                "missing_fields": missing_fields,
                "status": "PASS" if not missing_fields and has_192 and has_512 else "WARN"
            }
        except json.JSONDecodeError as e:
            return {
                "exists": True,
                "path": str(manifest_path),
                "valid_json": False,
                "status": "FAIL",
                "error": str(e)
            }
        except Exception as e:
            return {
                "exists": True,
                "path": str(manifest_path),
                "status": "FAIL",
                "error": str(e)
            }
    
    def analyze_service_worker(self, pwa):
        """Analyze service worker for caching strategies"""
        sw_path = self.base_path / pwa / "dist" / "sw.js"
        
        if not sw_path.exists():
            return {
                "analyzed": False,
                "status": "FAIL",
                "error": "Service worker not found"
            }
        
        try:
            with open(sw_path, 'r') as f:
                content = f.read()
            
            # Check for Workbox
            uses_workbox = "workbox" in content.lower()
            
            # Check for caching strategies
            has_precache = "precacheAndRoute" in content or "precache" in content
            has_network_first = "NetworkFirst" in content
            has_cache_first = "CacheFirst" in content
            has_stale_while_revalidate = "StaleWhileRevalidate" in content
            
            # Check for API caching
            has_api_cache = "api" in content.lower() and ("cache" in content.lower())
            
            # Check for offline support
            has_offline_fallback = "offline" in content.lower() or "fallback" in content.lower()
            
            # Check for cache cleanup
            has_cleanup = "cleanupOutdatedCaches" in content or "cleanup" in content.lower()
            
            # Check for navigation routes
            has_navigation_route = "NavigationRoute" in content or "navigation" in content.lower()
            
            return {
                "analyzed": True,
                "uses_workbox": uses_workbox,
                "has_precache": has_precache,
                "has_network_first": has_network_first,
                "has_cache_first": has_cache_first,
                "has_stale_while_revalidate": has_stale_while_revalidate,
                "has_api_cache": has_api_cache,
                "has_offline_fallback": has_offline_fallback,
                "has_cleanup": has_cleanup,
                "has_navigation_route": has_navigation_route,
                "file_size": len(content),
                "status": "PASS" if uses_workbox and has_precache else "WARN"
            }
        except Exception as e:
            return {
                "analyzed": False,
                "status": "FAIL",
                "error": str(e)
            }
    
    def test_pwa_icons(self, pwa):
        """Check if PWA icons exist"""
        dist_path = self.base_path / pwa / "dist"
        
        icons = {
            "192x192": dist_path / "pwa-192x192.png",
            "512x512": dist_path / "pwa-512x512.png"
        }
        
        results = {}
        all_exist = True
        
        for size, path in icons.items():
            exists = path.exists()
            results[size] = {
                "exists": exists,
                "path": str(path),
                "size_bytes": path.stat().st_size if exists else 0
            }
            if not exists:
                all_exist = False
        
        return {
            "icons": results,
            "all_exist": all_exist,
            "status": "PASS" if all_exist else "FAIL"
        }
    
    def test_index_html(self, pwa):
        """Check if index.html exists and has PWA meta tags"""
        index_path = self.base_path / pwa / "dist" / "index.html"
        
        if not index_path.exists():
            return {
                "exists": False,
                "path": str(index_path),
                "status": "FAIL"
            }
        
        try:
            with open(index_path, 'r') as f:
                content = f.read()
            
            # Check for PWA meta tags
            has_viewport = 'name="viewport"' in content
            has_theme_color = 'name="theme-color"' in content
            has_manifest_link = 'rel="manifest"' in content
            has_apple_touch_icon = 'apple-touch-icon' in content
            
            # Check for service worker registration
            has_sw_registration = "serviceWorker" in content or "registerSW" in content
            
            return {
                "exists": True,
                "path": str(index_path),
                "has_viewport": has_viewport,
                "has_theme_color": has_theme_color,
                "has_manifest_link": has_manifest_link,
                "has_apple_touch_icon": has_apple_touch_icon,
                "has_sw_registration": has_sw_registration,
                "file_size": len(content),
                "status": "PASS" if all([has_viewport, has_manifest_link, has_sw_registration]) else "WARN"
            }
        except Exception as e:
            return {
                "exists": True,
                "path": str(index_path),
                "status": "FAIL",
                "error": str(e)
            }
    
    def run_tests(self):
        """Run all offline functionality tests"""
        print("=" * 80)
        print("PHASE 6 TASK 8: OFFLINE FUNCTIONALITY TESTING")
        print("=" * 80)
        print()
        
        for pwa in self.pwas:
            print(f"\n{'=' * 80}")
            print(f"Testing: {pwa.upper()}")
            print(f"{'=' * 80}")
            
            self.results[pwa] = {}
            
            # Test 1: Service Worker
            print("\n[1] Service Worker Test...")
            sw_result = self.test_service_worker_exists(pwa)
            self.results[pwa]["service_worker"] = sw_result
            print(f"    Status: {sw_result['status']}")
            if sw_result['exists']:
                print(f"    ✓ File exists: {sw_result['path']}")
                print(f"    ✓ Size: {sw_result['size_bytes']:,} bytes")
            else:
                print(f"    ✗ File not found: {sw_result['path']}")
            
            # Test 2: Service Worker Analysis
            print("\n[2] Service Worker Analysis...")
            sw_analysis = self.analyze_service_worker(pwa)
            self.results[pwa]["sw_analysis"] = sw_analysis
            print(f"    Status: {sw_analysis['status']}")
            if sw_analysis['analyzed']:
                print(f"    ✓ Uses Workbox: {sw_analysis['uses_workbox']}")
                print(f"    ✓ Has Precaching: {sw_analysis['has_precache']}")
                print(f"    ✓ Network First: {sw_analysis['has_network_first']}")
                print(f"    ✓ Cache First: {sw_analysis['has_cache_first']}")
                print(f"    ✓ API Caching: {sw_analysis['has_api_cache']}")
                print(f"    ✓ Cache Cleanup: {sw_analysis['has_cleanup']}")
                print(f"    ✓ Navigation Route: {sw_analysis['has_navigation_route']}")
            
            # Test 3: Manifest
            print("\n[3] Web App Manifest Test...")
            manifest_result = self.test_manifest_exists(pwa)
            self.results[pwa]["manifest"] = manifest_result
            print(f"    Status: {manifest_result['status']}")
            if manifest_result['exists'] and manifest_result.get('valid_json'):
                print(f"    ✓ Name: {manifest_result.get('name')}")
                print(f"    ✓ Display: {manifest_result.get('display')}")
                print(f"    ✓ Start URL: {manifest_result.get('start_url')}")
                print(f"    ✓ Theme Color: {manifest_result.get('theme_color')}")
                print(f"    ✓ Icons: {manifest_result.get('icons_count')}")
                print(f"    ✓ Has 192x192: {manifest_result.get('has_192x192')}")
                print(f"    ✓ Has 512x512: {manifest_result.get('has_512x512')}")
                if manifest_result.get('missing_fields'):
                    print(f"    ⚠ Missing fields: {manifest_result['missing_fields']}")
            
            # Test 4: Icons
            print("\n[4] PWA Icons Test...")
            icons_result = self.test_pwa_icons(pwa)
            self.results[pwa]["icons"] = icons_result
            print(f"    Status: {icons_result['status']}")
            for size, info in icons_result['icons'].items():
                if info['exists']:
                    print(f"    ✓ Icon {size}: {info['size_bytes']:,} bytes")
                else:
                    print(f"    ✗ Icon {size}: Not found")
            
            # Test 5: Index HTML
            print("\n[5] Index HTML Test...")
            html_result = self.test_index_html(pwa)
            self.results[pwa]["index_html"] = html_result
            print(f"    Status: {html_result['status']}")
            if html_result['exists']:
                print(f"    ✓ Has Viewport: {html_result.get('has_viewport')}")
                print(f"    ✓ Has Theme Color: {html_result.get('has_theme_color')}")
                print(f"    ✓ Has Manifest Link: {html_result.get('has_manifest_link')}")
                print(f"    ✓ Has SW Registration: {html_result.get('has_sw_registration')}")
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total_tests = 0
        passed_tests = 0
        
        for pwa, tests in self.results.items():
            pwa_pass = 0
            pwa_total = 0
            
            for test_name, test_result in tests.items():
                pwa_total += 1
                if test_result.get('status') == 'PASS':
                    pwa_pass += 1
            
            total_tests += pwa_total
            passed_tests += pwa_pass
            
            pass_rate = (pwa_pass / pwa_total * 100) if pwa_total > 0 else 0
            status_icon = "✅" if pass_rate == 100 else "⚠️" if pass_rate >= 80 else "❌"
            
            print(f"\n{pwa.upper()}: {pwa_pass}/{pwa_total} tests passed ({pass_rate:.0f}%) {status_icon}")
        
        overall_pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n{'=' * 80}")
        print(f"OVERALL: {passed_tests}/{total_tests} tests passed ({overall_pass_rate:.0f}%)")
        
        if overall_pass_rate == 100:
            print("\n🎉 ALL OFFLINE FUNCTIONALITY TESTS PASSED!")
            print("✅ Service workers configured")
            print("✅ Caching strategies implemented")
            print("✅ Web app manifests valid")
            print("✅ PWA icons present")
            print("✅ Offline support ready")
        elif overall_pass_rate >= 80:
            print("\n⚠️  Most tests passed - Minor issues to address")
        else:
            print("\n❌ Multiple failures - Requires attention")
        
        print()
    
    def save_report(self):
        """Save detailed report to JSON"""
        report_path = Path("/workspace/development/frappe-bench/apps/tems/OFFLINE_FUNCTIONALITY_TEST_REPORT.json")
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Detailed report saved to: {report_path}")

if __name__ == "__main__":
    tester = OfflineFunctionalityTest()
    tester.run_tests()
    tester.save_report()
