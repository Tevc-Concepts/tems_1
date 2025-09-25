"""
Backward-compat shim for tems.tems_governance.api

This file exists only to forward imports to the package module at
`tems.tems_governance.api.__init__`. Prefer importing from the package.
"""

from __future__ import annotations

# Forward all public names from the package module
from .__init__ import *  # type: ignore  # noqa: F401,F403
