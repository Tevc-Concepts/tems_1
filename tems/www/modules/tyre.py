"""Tyre module page"""
from tems.www.modules.index import get_context as base_get_context

def get_context(context):
    context["module"] = "tyre"
    return base_get_context(context)
