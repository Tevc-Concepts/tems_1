import frappe
from frappe import _

no_cache = 1

def get_context(context):
    """Context for driver portal page"""
    context.no_cache = 1
    context.no_breadcrumbs = True
    context.skip_frappe_bundle = True  # Don't load Frappe's JS/CSS
    
    # Critical: Tell Frappe to render raw HTML without base template
    frappe.response['type'] = 'page'
    frappe.local.response.http_status_code = 200
    
    # Allow guest access for now - authentication will be handled by the PWA
    # Uncomment below to enforce login
    # if frappe.session.user == "Guest":
    #     frappe.local.flags.redirect_location = "/login?redirect-to=/driver"
    #     raise frappe.Redirect
    
    return context
