import frappe
from frappe import _

def get_context(context):
    """Context for driver portal page"""
    context.no_cache = 1
    context.no_breadcrumbs = True
    
    # Allow guest access for now - authentication will be handled by the PWA
    # Uncomment below to enforce login
    # if frappe.session.user == "Guest":
    #     frappe.local.flags.redirect_location = "/login?redirect-to=/driver"
    #     raise frappe.Redirect
    
    return context
