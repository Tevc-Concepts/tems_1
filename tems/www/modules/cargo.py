"""Cargo module page"""
from tems.www.modules.index import get_context as base_get_context

def get_context(context):
    context["module"] = "cargo"
    return base_get_context(context)
