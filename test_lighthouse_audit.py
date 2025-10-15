#!/usr/bin/env python3
"""
Phase 6 Task 10: Performance Testing with Lighthouse
Runs Lighthouse audits on all 4 PWAs and generates comprehensive performance reports
"""

import subprocess
import json
import os
from datetime import datetime

class LighthouseAuditor:
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
    
    def check_lighthouse_installed(self):
        """Check if Lighthouse CLI is installed"""
        try:
            result = subprocess.run(
                ["lighthouse", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✓ Lighthouse CLI installed: {version}")
                return True
            else:
                print("✗ Lighthouse CLI not found")
                return False
        except FileNotFoundError:
            print("✗ Lighthouse CLI not found")
            return False
    
    def install_lighthouse(self):
        """Install Lighthouse CLI using npm"""
        self.print_header("Installing Lighthouse CLI")
        print("Running: npm install -g lighthouse")
        
        try:
            subprocess.run(
                ["npm", "install", "-g", "lighthouse"],
                check=True
            )
            print("✓ Lighthouse CLI installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install Lighthouse: {e}")
            return False
        except FileNotFoundError:
            print("✗ npm not found. Please install Node.js and npm first.")
            return False
    
    def run_lighthouse_audit(self, pwa_name, url):
        """Run Lighthouse audit for a single PWA"""
        print(f"\n[{pwa_name.upper()}] Running Lighthouse audit...")
        print(f"URL: {url}")
        
        output_dir = "/workspace/development/frappe-bench/apps/tems/lighthouse-reports"
        os.makedirs(output_dir, exist_ok=True)
        
        json_output = f"{output_dir}/{pwa_name}-lighthouse.json"
        html_output = f"{output_dir}/{pwa_name}-lighthouse.html"
        
        # Lighthouse CLI command
        cmd = [
            "lighthouse",
            url,
            "--output=json",
            "--output=html",
            "--output-path", f"{output_dir}/{pwa_name}-lighthouse",
            "--chrome-flags='--headless --no-sandbox --disable-gpu'",
            "--quiet"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print(f"  ✓ Audit completed")
                print(f"  ✓ JSON report: {json_output}")
                print(f"  ✓ HTML report: {html_output}")
                
                # Parse results
                if os.path.exists(json_output):
                    with open(json_output, 'r') as f:
                        lighthouse_data = json.load(f)
                        return self.parse_lighthouse_results(pwa_name, lighthouse_data)
                else:
                    print(f"  ⚠ JSON output not found at {json_output}")
                    return None
            else:
                print(f"  ✗ Audit failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"  ✗ Audit timed out after 120 seconds")
            return None
        except Exception as e:
            print(f"  ✗ Error running audit: {e}")
            return None
    
    def parse_lighthouse_results(self, pwa_name, data):
        """Parse Lighthouse JSON results"""
        try:
            categories = data.get('categories', {})
            
            results = {
                'pwa_name': pwa_name,
                'url': data.get('finalUrl', ''),
                'fetch_time': data.get('fetchTime', ''),
                'scores': {
                    'performance': categories.get('performance', {}).get('score', 0) * 100,
                    'accessibility': categories.get('accessibility', {}).get('score', 0) * 100,
                    'best_practices': categories.get('best-practices', {}).get('score', 0) * 100,
                    'seo': categories.get('seo', {}).get('score', 0) * 100,
                    'pwa': categories.get('pwa', {}).get('score', 0) * 100
                },
                'metrics': {}
            }
            
            # Extract key metrics
            audits = data.get('audits', {})
            
            metrics_to_extract = {
                'first-contentful-paint': 'First Contentful Paint',
                'largest-contentful-paint': 'Largest Contentful Paint',
                'total-blocking-time': 'Total Blocking Time',
                'cumulative-layout-shift': 'Cumulative Layout Shift',
                'speed-index': 'Speed Index',
                'interactive': 'Time to Interactive'
            }
            
            for audit_key, metric_name in metrics_to_extract.items():
                if audit_key in audits:
                    audit = audits[audit_key]
                    if 'displayValue' in audit:
                        results['metrics'][metric_name] = audit['displayValue']
                    elif 'numericValue' in audit:
                        results['metrics'][metric_name] = f"{audit['numericValue']:.0f}"
            
            self.results[pwa_name] = results
            return results
            
        except Exception as e:
            print(f"  ✗ Error parsing results: {e}")
            return None
    
    def print_pwa_results(self, pwa_name, results):
        """Print results for a single PWA"""
        if not results:
            print(f"\n[{pwa_name.upper()}] No results available")
            return
        
        print(f"\n[{pwa_name.upper()}] Lighthouse Audit Results")
        print(f"URL: {results['url']}")
        print(f"Audited: {results['fetch_time']}")
        
        print("\nScores:")
        scores = results['scores']
        for category, score in scores.items():
            icon = "🟢" if score >= 90 else "🟡" if score >= 50 else "🔴"
            print(f"  {icon} {category.replace('_', ' ').title()}: {score:.0f}/100")
        
        if results['metrics']:
            print("\nKey Metrics:")
            for metric, value in results['metrics'].items():
                print(f"  • {metric}: {value}")
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        self.print_header("LIGHTHOUSE AUDIT SUMMARY")
        
        if not self.results:
            print("No results to report")
            return
        
        # Calculate averages
        avg_scores = {
            'performance': 0,
            'accessibility': 0,
            'best_practices': 0,
            'seo': 0,
            'pwa': 0
        }
        
        count = len(self.results)
        
        print("\nScores by PWA:")
        print(f"{'PWA':<15} {'Performance':<12} {'PWA':<12} {'A11y':<12} {'Best Prac':<12} {'SEO':<12}")
        print("-" * 80)
        
        for pwa_name, results in self.results.items():
            scores = results['scores']
            print(f"{pwa_name.title():<15} "
                  f"{scores['performance']:<12.0f} "
                  f"{scores['pwa']:<12.0f} "
                  f"{scores['accessibility']:<12.0f} "
                  f"{scores['best_practices']:<12.0f} "
                  f"{scores['seo']:<12.0f}")
            
            for key in avg_scores:
                avg_scores[key] += scores[key]
        
        print("-" * 80)
        
        # Calculate and print averages
        for key in avg_scores:
            avg_scores[key] = avg_scores[key] / count if count > 0 else 0
        
        print(f"{'Average':<15} "
              f"{avg_scores['performance']:<12.0f} "
              f"{avg_scores['pwa']:<12.0f} "
              f"{avg_scores['accessibility']:<12.0f} "
              f"{avg_scores['best_practices']:<12.0f} "
              f"{avg_scores['seo']:<12.0f}")
        
        # Overall assessment
        print(f"\n{'=' * 80}")
        print("OVERALL ASSESSMENT:")
        
        all_good = all(score >= 90 for score in avg_scores.values())
        mostly_good = all(score >= 70 for score in avg_scores.values())
        
        if all_good:
            print("🎉 EXCELLENT! All categories score 90+")
            print("✅ PWAs are optimized for production deployment")
        elif mostly_good:
            print("✅ GOOD! All categories score 70+")
            print("⚠️  Some optimization opportunities available")
        else:
            print("⚠️  NEEDS IMPROVEMENT")
            print("❌ Some categories require optimization")
        
        # Recommendations
        print(f"\n{'=' * 80}")
        print("RECOMMENDATIONS:")
        
        if avg_scores['performance'] < 90:
            print("\n📊 Performance:")
            print("  • Optimize images (use WebP, lazy loading)")
            print("  • Minimize JavaScript bundles")
            print("  • Enable server-side caching")
            print("  • Use CDN for static assets")
        
        if avg_scores['pwa'] < 90:
            print("\n📱 PWA:")
            print("  • Ensure service workers are properly registered")
            print("  • Verify manifest.json is complete")
            print("  • Add offline fallback pages")
            print("  • Test install prompts")
        
        if avg_scores['accessibility'] < 90:
            print("\n♿ Accessibility:")
            print("  • Add ARIA labels to interactive elements")
            print("  • Ensure sufficient color contrast")
            print("  • Add alt text to all images")
            print("  • Test keyboard navigation")
        
        if avg_scores['best_practices'] < 90:
            print("\n✨ Best Practices:")
            print("  • Enable HTTPS in production")
            print("  • Add security headers (see Security Audit report)")
            print("  • Resolve console errors/warnings")
            print("  • Use modern JavaScript APIs")
        
        if avg_scores['seo'] < 90:
            print("\n🔍 SEO:")
            print("  • Add meta descriptions")
            print("  • Ensure proper heading hierarchy")
            print("  • Add structured data markup")
            print("  • Create robots.txt and sitemap.xml")
        
        print()
    
    def generate_markdown_report(self):
        """Generate detailed markdown report"""
        output_file = "/workspace/development/frappe-bench/apps/tems/PERFORMANCE_AUDIT_REPORT.md"
        
        with open(output_file, 'w') as f:
            f.write("# Phase 6 Task 10: Performance Audit Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%B %d, %Y')}\n")
            f.write(f"**Tool:** Google Lighthouse CLI\n")
            f.write(f"**PWAs Tested:** {len(self.results)}\n\n")
            
            f.write("---\n\n")
            f.write("## Executive Summary\n\n")
            
            # Calculate averages
            avg_scores = {
                'performance': 0,
                'accessibility': 0,
                'best_practices': 0,
                'seo': 0,
                'pwa': 0
            }
            
            count = len(self.results)
            for results in self.results.values():
                for key in avg_scores:
                    avg_scores[key] += results['scores'][key]
            
            for key in avg_scores:
                avg_scores[key] = avg_scores[key] / count if count > 0 else 0
            
            f.write("### Average Scores Across All PWAs\n\n")
            f.write("| Category | Score | Status |\n")
            f.write("|----------|-------|--------|\n")
            
            for category, score in avg_scores.items():
                icon = "🟢" if score >= 90 else "🟡" if score >= 50 else "🔴"
                status = "Excellent" if score >= 90 else "Good" if score >= 70 else "Needs Improvement"
                f.write(f"| {category.replace('_', ' ').title()} | {score:.0f}/100 | {icon} {status} |\n")
            
            f.write("\n---\n\n")
            f.write("## Individual PWA Results\n\n")
            
            for pwa_name, results in self.results.items():
                f.write(f"### {pwa_name.title()} PWA\n\n")
                f.write(f"**URL:** {results['url']}\n\n")
                
                f.write("#### Scores\n\n")
                f.write("| Category | Score | Grade |\n")
                f.write("|----------|-------|-------|\n")
                
                scores = results['scores']
                for category, score in scores.items():
                    grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
                    f.write(f"| {category.replace('_', ' ').title()} | {score:.0f}/100 | {grade} |\n")
                
                if results['metrics']:
                    f.write("\n#### Key Performance Metrics\n\n")
                    f.write("| Metric | Value |\n")
                    f.write("|--------|-------|\n")
                    for metric, value in results['metrics'].items():
                        f.write(f"| {metric} | {value} |\n")
                
                f.write("\n")
            
            f.write("---\n\n")
            f.write("## Optimization Recommendations\n\n")
            
            # Add recommendations based on scores
            if avg_scores['performance'] < 90:
                f.write("### Performance Optimization\n\n")
                f.write("- **Image Optimization:** Convert images to WebP format, implement lazy loading\n")
                f.write("- **JavaScript Bundling:** Use code splitting and tree shaking\n")
                f.write("- **Caching Strategy:** Implement aggressive caching for static assets\n")
                f.write("- **CDN Usage:** Serve static assets from CDN\n")
                f.write("- **Minification:** Minify CSS, JavaScript, and HTML\n\n")
            
            if avg_scores['pwa'] < 90:
                f.write("### PWA Enhancement\n\n")
                f.write("- **Service Worker:** Ensure proper registration and update strategies\n")
                f.write("- **Manifest:** Complete all required fields in manifest.json\n")
                f.write("- **Offline Support:** Implement comprehensive offline fallbacks\n")
                f.write("- **Install Prompts:** Test and optimize install experience\n")
                f.write("- **Icons:** Provide all required icon sizes\n\n")
            
            if avg_scores['accessibility'] < 90:
                f.write("### Accessibility Improvements\n\n")
                f.write("- **ARIA Labels:** Add descriptive labels to all interactive elements\n")
                f.write("- **Color Contrast:** Ensure WCAG AA compliance (4.5:1 ratio)\n")
                f.write("- **Alt Text:** Add meaningful alt text to all images\n")
                f.write("- **Keyboard Navigation:** Test and fix tab order\n")
                f.write("- **Screen Reader:** Test with NVDA/JAWS/VoiceOver\n\n")
            
            if avg_scores['best_practices'] < 90:
                f.write("### Best Practices\n\n")
                f.write("- **HTTPS:** Enable in production (see Security Audit report)\n")
                f.write("- **Security Headers:** Configure via nginx (see PRODUCTION_SECURITY_SETUP.md)\n")
                f.write("- **Console Errors:** Resolve all JavaScript errors and warnings\n")
                f.write("- **Modern APIs:** Use current JavaScript standards\n")
                f.write("- **Dependencies:** Update to latest stable versions\n\n")
            
            if avg_scores['seo'] < 90:
                f.write("### SEO Optimization\n\n")
                f.write("- **Meta Tags:** Add title, description, and Open Graph tags\n")
                f.write("- **Headings:** Use proper heading hierarchy (h1, h2, h3)\n")
                f.write("- **Structured Data:** Add JSON-LD markup for rich snippets\n")
                f.write("- **Sitemap:** Generate and submit XML sitemap\n")
                f.write("- **Robots.txt:** Configure crawling permissions\n\n")
            
            f.write("---\n\n")
            f.write("## HTML Reports\n\n")
            f.write("Detailed HTML reports with specific recommendations are available at:\n\n")
            for pwa_name in self.results.keys():
                f.write(f"- `lighthouse-reports/{pwa_name}-lighthouse.html`\n")
            
            f.write("\n---\n\n")
            f.write("*Generated by Lighthouse CLI automated testing*\n")
        
        print(f"\n✓ Detailed markdown report saved to: {output_file}")
    
    def run_all_audits(self):
        """Run Lighthouse audits for all PWAs"""
        self.print_header("PHASE 6 TASK 10: PERFORMANCE TESTING WITH LIGHTHOUSE")
        
        # Check if Lighthouse is installed
        if not self.check_lighthouse_installed():
            print("\nLighthouse CLI is required for performance testing.")
            print("Attempting to install...")
            if not self.install_lighthouse():
                print("\n❌ Unable to install Lighthouse. Please install manually:")
                print("   npm install -g lighthouse")
                return
        
        # Run audits for each PWA
        for pwa_name, url in self.pwas.items():
            results = self.run_lighthouse_audit(pwa_name, url)
            if results:
                self.print_pwa_results(pwa_name, results)
        
        # Generate summary
        self.generate_summary_report()
        
        # Generate detailed markdown report
        self.generate_markdown_report()

if __name__ == "__main__":
    auditor = LighthouseAuditor()
    auditor.run_all_audits()
