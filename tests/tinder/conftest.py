"""Ensure apps/hub/api is on sys.path so tinder.* modules resolve.

The pyproject.toml pythonpath config handles this for most test directories,
but sub-package discovery needs the explicit addition at conftest level too.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Repo root is three levels up from tests/tinder/
_API_PATH = str(Path(__file__).parent.parent.parent / "apps" / "hub" / "api")
if _API_PATH not in sys.path:
    sys.path.insert(0, _API_PATH)
