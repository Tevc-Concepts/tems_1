"""Supply Chain module page"""
import frappe
from tems.www.modules.index import get_context as base_get_context

def get_context(context):
    """Get context for supply_chain module page"""
    context["module"] = "supply_chain"
    return base_get_context(context)
