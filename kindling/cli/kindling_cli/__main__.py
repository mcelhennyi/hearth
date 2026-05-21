"""Allow ``python -m kindling_cli`` invocation."""

from __future__ import annotations

import sys

from kindling_cli.cli import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
