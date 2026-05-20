import sys
from pathlib import Path

_API_PATH = str(Path(__file__).parent.parent.parent / "apps" / "hub" / "api")
if _API_PATH not in sys.path:
    sys.path.insert(0, _API_PATH)
