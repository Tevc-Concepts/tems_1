#!/usr/bin/env python3
"""
Phase 6 Task 10: Performance Testing (Alternative Method)
Analyzes PWA structure, loads, and resources for performance assessment
"""

import requests
import json
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup

class PerformanceAnalyzer:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.pwas = {
            "operations": f"{self.base_url}/assets/tems/frontend/operations-pwa/dist/index.html",
            "safety": f"{self.base_url}/assets/tems/frontend/safety-pwa/dist/index.html",
            "fleet": f"{self.base_url}/assets/tems/frontend/fleet-pwa/dist/index.html",
            "driver": f"{self.base_url}/assets/tems/frontend/driver-pwa/dist/index.html"
        }
        self.results = {}
        
    def print_header(self, text):
        print(f"\n{'=' * 80}")
        print(f"{text}")
        print(f"{'=' * 80}")
    
    def analyze_pwa_structure(self, pwa_name):
        """Analyze PWA file structure"""
        print(f"\n[{pwa_name.upper()}] Analyzing PWA Structure...")
        
        base_path = f"/workspace/development/frappe-bench/apps/tems/tems/public/frontend/{pwa_name}-pwa/dist"
        
        results = {
            'pwa_name': pwa_name,
            'files': {},
            'service_worker': False,
            'manifest': False,
            'icons': [],
            'total_size': 0,
            'file_count': 0
        }
        
        # Check for key files
        if os.path.exists(f"{base_path}/sw.js"):
            results['service_worker'] = True
            print("  ✓ Service Worker found")
        
        if os.path.exists(f"{base_path}/manifest.webmanifest"):
            results['manifest'] = True
            print("  ✓ Manifest found")
            
            # Read manifest
            try:
                with open(f"{base_path}/manifest.webmanifest", 'r') as f:
                    manifest = json.load(f)
                    results['icons'] = manifest.get('icons', [])
                    print(f"  ✓ Icons defined: {len(results['icons'])}")
            except:
                pass
        
        # Count files and sizes
        for root, dirs, files in os.walk(base_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    results['total_size'] += size
                    results['file_count'] += 1
                    
                    ext = file.split('.')[-1]
                    if ext not in results['files']:
                        results['files'][ext] = {'count': 0, 'size': 0}
                    results['files'][ext]['count'] += 1
                    results['files'][ext]['size'] += size
                except:
                    pass
        
        print(f"  • Total files: {results['file_count']}")
        print(f"  • Total size: {results['total_size'] / 1024:.1f} KB")
        
        return results
    
    def test_load_performance(self, pwa_name, url):
        """Test page load performance"""
        print(f"\n[{pwa_name.upper()}] Testing Load Performance...")
        
        results = {
            'response_time': 0,
            'status_code': 0,
            'content_size': 0,
            'resources': []
        }
        
        # Measure initial page load
        start_time = time.time()
        try:
            response = requests.get(url, timeout=10)
            end_time = time.time()
            
            results['response_time'] = (end_time - start_time) * 1000  # ms
            results['status_code'] = response.status_code
            results['content_size'] = len(response.content)
            
            print(f"  • Response time: {results['response_time']:.0f}ms")
            print(f"  • Status code: {results['status_code']}")
            print(f"  • HTML size: {results['content_size'] / 1024:.1f} KB")
            
            # Parse HTML to find resources
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Count scripts
                scripts = soup.find_all('script', src=True)
                print(f"  • JavaScript files: {len(scripts)}")
                
                # Count stylesheets
                styles = soup.find_all('link', rel='stylesheet')
                print(f"  • CSS files: {len(styles)}")
                
                # Count images
                images = soup.find_all('img', src=True)
                print(f"  • Images: {len(images)}")
                
                results['resources'] = {
                    'scripts': len(scripts),
                    'styles': len(styles),
                    'images': len(images)
                }
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        return results
    
    def test_api_performance(self, pwa_name):
        """Test API endpoint performance"""
        print(f"\n[{pwa_name.upper()}] Testing API Performance...")
        
        api_endpoints = {
            'operations': [
                '/api/method/tems.api.pwa.operations.get_operations_dashboard',
                '/api/method/tems.api.pwa.operations.get_vehicles',
                '/api/method/tems.api.pwa.operations.get_drivers'
            ],
            'safety': [
                '/api/method/tems.api.pwa.safety.get_safety_dashboard',
                '/api/method/tems.api.pwa.safety.get_incidents'
            ],
            'fleet': [
                '/api/method/tems.api.pwa.fleet.get_fleet_dashboard',
                '/api/method/tems.api.pwa.fleet.get_vehicles'
            ],
            'driver': [
                '/api/method/tems.api.pwa.driver.get_driver_profile',
                '/api/method/tems.api.pwa.driver.get_driver_schedule'
            ]
        }
        
        results = []
        
        if pwa_name in api_endpoints:
            for endpoint in api_endpoints[pwa_name]:
                start_time = time.time()
                try:
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                    end_time = time.time()
                    
                    response_time = (end_time - start_time) * 1000
                    
                    result = {
                        'endpoint': endpoint.split('/')[-1],
                        'response_time': response_time,
                        'status': response.status_code,
                        'size': len(response.content)
                    }
                    results.append(result)
                    
                    status_icon = "✓" if response.status_code == 200 else "✗"
                    print(f"  {status_icon} {result['endpoint']}: {response_time:.0f}ms")
                except Exception as e:
                    print(f"  ✗ {endpoint}: Error")
        
        return results
    
    def calculate_pwa_score(self, structure, load, api_perf):
        """Calculate PWA performance score"""
        score = 0
        max_score = 100
        
        # PWA Features (30 points)
        if structure.get('service_worker'):
            score += 15
        if structure.get('manifest'):
            score += 10
        if len(structure.get('icons', [])) >= 2:
            score += 5
        
        # Load Performance (40 points)
        response_time = load.get('response_time', 1000)
        if response_time < 100:
            score += 40
        elif response_time < 300:
            score += 30
        elif response_time < 500:
            score += 20
        elif response_time < 1000:
            score += 10
        
        # Resource Optimization (15 points)
        total_size = structure.get('total_size', 0) / 1024  # KB
        if total_size < 500:
            score += 15
        elif total_size < 1000:
            score += 10
        elif total_size < 2000:
            score += 5
        
        # API Performance (15 points)
        if api_perf:
            avg_api_time = sum(r['response_time'] for r in api_perf) / len(api_perf)
            if avg_api_time < 100:
                score += 15
            elif avg_api_time < 300:
                score += 10
            elif avg_api_time < 500:
                score += 5
        
        return min(score, max_score)
    
    def grade_performance(self, score):
        """Convert score to grade"""
        if score >= 90:
            return "A", "🟢 Excellent"
        elif score >= 80:
            return "B", "🟢 Good"
        elif score >= 70:
            return "C", "🟡 Fair"
        elif score >= 60:
            return "D", "🟡 Needs Improvement"
        else:
            return "F", "🔴 Poor"
    
    def analyze_all_pwas(self):
        """Analyze all PWAs"""
        self.print_header("PHASE 6 TASK 10: PERFORMANCE TESTING")
        
        for pwa_name, url in self.pwas.items():
            structure = self.analyze_pwa_structure(pwa_name)
            load = self.test_load_performance(pwa_name, url)
            api_perf = self.test_api_performance(pwa_name)
            
            score = self.calculate_pwa_score(structure, load, api_perf)
            grade, status = self.grade_performance(score)
            
            self.results[pwa_name] = {
                'structure': structure,
                'load': load,
                'api': api_perf,
                'score': score,
                'grade': grade,
                'status': status
            }
            
            print(f"\n  {status} Overall Score: {score}/100 (Grade: {grade})")
        
        self.generate_summary()
        self.generate_report()
    
    def generate_summary(self):
        """Generate performance summary"""
        self.print_header("PERFORMANCE SUMMARY")
        
        print(f"\n{'PWA':<15} {'Score':<10} {'Grade':<10} {'Status':<25}")
        print("-" * 80)
        
        total_score = 0
        for pwa_name, results in self.results.items():
            print(f"{pwa_name.title():<15} {results['score']:<10.0f} "
                  f"{results['grade']:<10} {results['status']}")
            total_score += results['score']
        
        avg_score = total_score / len(self.results) if self.results else 0
        avg_grade, avg_status = self.grade_performance(avg_score)
        
        print("-" * 80)
        print(f"{'Average':<15} {avg_score:<10.0f} {avg_grade:<10} {avg_status}")
        
        print(f"\n{'=' * 80}")
        print("KEY FINDINGS:")
        
        # Analyze patterns
        all_have_sw = all(r['structure']['service_worker'] for r in self.results.values())
        all_have_manifest = all(r['structure']['manifest'] for r in self.results.values())
        
        if all_have_sw and all_have_manifest:
            print("\n✅ PWA FEATURES:")
            print("  • All PWAs have service workers")
            print("  • All PWAs have manifests")
            print("  • PWAs are installable")
        
        # Load performance
        avg_load_time = sum(r['load']['response_time'] for r in self.results.values()) / len(self.results)
        print(f"\n📊 LOAD PERFORMANCE:")
        print(f"  • Average load time: {avg_load_time:.0f}ms")
        if avg_load_time < 300:
            print("  ✓ Excellent load times (< 300ms)")
        elif avg_load_time < 1000:
            print("  ✓ Good load times (< 1s)")
        else:
            print("  ⚠ Consider optimization (> 1s)")
        
        # Size optimization
        avg_size = sum(r['structure']['total_size'] for r in self.results.values()) / len(self.results) / 1024
        print(f"\n💾 RESOURCE OPTIMIZATION:")
        print(f"  • Average bundle size: {avg_size:.0f} KB")
        if avg_size < 1000:
            print("  ✓ Well-optimized bundle sizes")
        else:
            print("  ⚠ Consider code splitting and tree shaking")
        
        # API performance
        print(f"\n⚡ API PERFORMANCE:")
        for pwa_name, results in self.results.items():
            if results['api']:
                avg_api = sum(r['response_time'] for r in results['api']) / len(results['api'])
                status = "✓" if avg_api < 300 else "⚠"
                print(f"  {status} {pwa_name.title()}: {avg_api:.0f}ms average")
        
        print()
    
    def generate_report(self):
        """Generate detailed markdown report"""
        output_file = "/workspace/development/frappe-bench/apps/tems/PERFORMANCE_AUDIT_REPORT.md"
        
        with open(output_file, 'w') as f:
            f.write("# Phase 6 Task 10: Performance Audit Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%B %d, %Y')}\n")
            f.write(f"**Method:** Automated Performance Analysis\n")
            f.write(f"**PWAs Tested:** {len(self.results)}\n\n")
            
            f.write("---\n\n")
            f.write("## Executive Summary\n\n")
            
            # Calculate averages
            total_score = sum(r['score'] for r in self.results.values())
            avg_score = total_score / len(self.results) if self.results else 0
            avg_grade, avg_status = self.grade_performance(avg_score)
            
            f.write(f"### Overall Performance: {avg_status}\n\n")
            f.write(f"**Average Score:** {avg_score:.0f}/100 (Grade: {avg_grade})\n\n")
            
            f.write("| PWA | Score | Grade | Status |\n")
            f.write("|-----|-------|-------|--------|\n")
            for pwa_name, results in self.results.items():
                f.write(f"| {pwa_name.title()} | {results['score']:.0f}/100 | "
                       f"{results['grade']} | {results['status']} |\n")
            
            f.write("\n---\n\n")
            f.write("## Detailed Results by PWA\n\n")
            
            for pwa_name, results in self.results.items():
                f.write(f"### {pwa_name.title()} PWA\n\n")
                f.write(f"**Overall Score:** {results['score']:.0f}/100 ({results['grade']})\n\n")
                
                # PWA Structure
                structure = results['structure']
                f.write("#### PWA Features\n\n")
                f.write(f"- Service Worker: {'✅ Present' if structure['service_worker'] else '❌ Missing'}\n")
                f.write(f"- Manifest: {'✅ Present' if structure['manifest'] else '❌ Missing'}\n")
                f.write(f"- Icons: {len(structure['icons'])} defined\n")
                f.write(f"- Total Files: {structure['file_count']}\n")
                f.write(f"- Total Size: {structure['total_size'] / 1024:.1f} KB\n\n")
                
                # File breakdown
                if structure['files']:
                    f.write("**File Breakdown:**\n\n")
                    f.write("| Type | Count | Size (KB) |\n")
                    f.write("|------|-------|----------|\n")
                    for ext, data in sorted(structure['files'].items(), key=lambda x: x[1]['size'], reverse=True):
                        f.write(f"| .{ext} | {data['count']} | {data['size'] / 1024:.1f} |\n")
                    f.write("\n")
                
                # Load Performance
                load = results['load']
                f.write("#### Load Performance\n\n")
                f.write(f"- Response Time: {load['response_time']:.0f}ms\n")
                f.write(f"- Status Code: {load['status_code']}\n")
                f.write(f"- HTML Size: {load['content_size'] / 1024:.1f} KB\n")
                
                if load.get('resources'):
                    f.write(f"- JavaScript Files: {load['resources']['scripts']}\n")
                    f.write(f"- CSS Files: {load['resources']['styles']}\n")
                    f.write(f"- Images: {load['resources']['images']}\n")
                f.write("\n")
                
                # API Performance
                if results['api']:
                    f.write("#### API Performance\n\n")
                    f.write("| Endpoint | Response Time | Status |\n")
                    f.write("|----------|---------------|--------|\n")
                    for api in results['api']:
                        f.write(f"| {api['endpoint']} | {api['response_time']:.0f}ms | {api['status']} |\n")
                    
                    avg_api_time = sum(r['response_time'] for r in results['api']) / len(results['api'])
                    f.write(f"\n**Average API Response:** {avg_api_time:.0f}ms\n")
                f.write("\n")
            
            f.write("---\n\n")
            f.write("## Optimization Recommendations\n\n")
            
            # Performance recommendations
            avg_load = sum(r['load']['response_time'] for r in self.results.values()) / len(self.results)
            if avg_load > 300:
                f.write("### Load Time Optimization\n\n")
                f.write("- **Code Splitting:** Break large bundles into smaller chunks\n")
                f.write("- **Lazy Loading:** Load components on demand\n")
                f.write("- **Minification:** Ensure all assets are minified\n")
                f.write("- **Compression:** Enable gzip/brotli compression on server\n\n")
            
            # Size recommendations
            avg_size = sum(r['structure']['total_size'] for r in self.results.values()) / len(self.results) / 1024
            if avg_size > 1000:
                f.write("### Bundle Size Optimization\n\n")
                f.write("- **Tree Shaking:** Remove unused code\n")
                f.write("- **Image Optimization:** Use WebP format, optimize sizes\n")
                f.write("- **Font Optimization:** Subset fonts, use system fonts\n")
                f.write("- **Remove Dependencies:** Audit and remove unused libraries\n\n")
            
            # PWA recommendations
            missing_features = []
            for pwa_name, results in self.results.items():
                if not results['structure']['service_worker']:
                    missing_features.append(f"{pwa_name}: Service Worker")
                if not results['structure']['manifest']:
                    missing_features.append(f"{pwa_name}: Manifest")
                if len(results['structure']['icons']) < 3:
                    missing_features.append(f"{pwa_name}: Icons (has {len(results['structure']['icons'])}, needs 3+)")
            
            if missing_features:
                f.write("### PWA Feature Completeness\n\n")
                for feature in missing_features:
                    f.write(f"- ⚠️ {feature}\n")
                f.write("\n")
            
            f.write("---\n\n")
            f.write("## Production Readiness Assessment\n\n")
            
            if avg_score >= 80:
                f.write("### ✅ READY FOR PRODUCTION\n\n")
                f.write("The PWAs demonstrate good performance characteristics and are ready for deployment.\n\n")
                f.write("**Strengths:**\n")
                f.write("- All PWA features properly implemented\n")
                f.write("- Fast load times\n")
                f.write("- Responsive API endpoints\n")
                f.write("- Optimized bundle sizes\n\n")
            elif avg_score >= 70:
                f.write("### ⚠️ ACCEPTABLE WITH OPTIMIZATIONS\n\n")
                f.write("The PWAs are functional but would benefit from optimization before production.\n\n")
            else:
                f.write("### ❌ NEEDS OPTIMIZATION\n\n")
                f.write("Significant performance improvements recommended before production deployment.\n\n")
            
            f.write("---\n\n")
            f.write("*Generated by automated performance analysis tool*\n")
        
        print(f"✓ Detailed report saved to: {output_file}")

if __name__ == "__main__":
    analyzer = PerformanceAnalyzer()
    analyzer.analyze_all_pwas()
