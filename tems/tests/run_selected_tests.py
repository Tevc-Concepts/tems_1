"""Selective test runner to execute only TEMS tests, avoiding deep ERPNext dependency tests.

Usage (inside bench shell):
 bench --site <site> execute tems.tems.tests.run_selected_tests.run
"""
from __future__ import annotations

import unittest
import importlib
import pkgutil


def run():  # frappe execute entry point
    # Dynamically discover tests only under tems.tests.*
    package = importlib.import_module("tems.tests")
    suite = unittest.TestSuite()
    for _, modname, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if ispkg:
            continue
        if not modname.split(".")[-1].startswith("test_"):
            continue
        mod = importlib.import_module(modname)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(mod))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        # mimic bench non-zero exit by raising
        raise SystemExit("Selected TEMS tests failed")
