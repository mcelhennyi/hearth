"""CLI: ``python -m hearth_install``."""

from __future__ import annotations

import argparse
from pathlib import Path

from hearth_install.layout import ensure_heart_layout


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create or refresh the Hearth Docker profile layout under <install-dir>/heart.",
    )
    parser.add_argument(
        "install_dir",
        type=Path,
        help="Install root (parent of heart/), e.g. /opt/hearth or ~/hearth-deploy",
    )
    parser.add_argument(
        "--hearth-ref",
        default="unknown",
        help='Git ref or label stored in VERSION.json when created (default: "%(default)s").',
    )
    args = parser.parse_args()
    heart = ensure_heart_layout(args.install_dir, hearth_ref=args.hearth_ref)
    print(f"OK: {heart}")


if __name__ == "__main__":
    main()
