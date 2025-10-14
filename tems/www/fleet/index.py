import frappe
from frappe import _

def get_context(context):
    """Context for fleet portal page"""
    context.no_cache = 1
    context.no_breadcrumbs = True
    
    # Allow guest access for now - authentication will be handled by the PWA
    # Uncomment below to enforce login
    # if frappe.session.user == "Guest":
    #     frappe.local.flags.redirect_location = "/login?redirect-to=/fleet"
    #     raise frappe.Redirect
    
    return context
