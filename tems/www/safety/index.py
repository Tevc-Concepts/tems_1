import frappe
from frappe import _
import os
import re

no_cache = 1

def get_context(context):
    """Context for safety portal page"""
    context.no_cache = 1
    context.no_breadcrumbs = True
    context.skip_frappe_bundle = True
    
    # Allow guest access - authentication will be handled by the PWA Vue Router
    
    # Get the built index.html and extract asset references
    dist_path = frappe.get_app_path("tems", "public", "frontend", "safety-pwa", "dist")
    index_html_path = os.path.join(dist_path, "index.html")
    
    if os.path.exists(index_html_path):
        with open(index_html_path, 'r') as f:
            html_content = f.read()
            
        # Extract JS and CSS references
        js_files = re.findall(r'<script[^>]+src="([^"]+)"', html_content)
        css_files = re.findall(r'<link[^>]+href="([^"]+\.css)"', html_content)
        preload_files = re.findall(r'<link rel="modulepreload"[^>]+href="([^"]+)"', html_content)
        manifest = re.search(r'<link rel="manifest" href="([^"]+)"', html_content)
        sw_script = re.search(r'<script[^>]+src="([^"]+registerSW\.js)"', html_content)
        
        context.js_files = js_files
        context.css_files = css_files
        context.preload_files = preload_files
        context.manifest_url = manifest.group(1) if manifest else None
        context.sw_script = sw_script.group(1) if sw_script else None
    else:
        frappe.throw(_("Safety PWA build not found. Please run 'bench build --app tems'"))
    
    return context
