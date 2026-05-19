"""Admin entrypoint for the generated {{ plugin_name }} plugin."""

from __future__ import annotations

import sys

PLUGIN_SLUG = "{{ plugin_slug }}"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "install":
        print(f"{PLUGIN_SLUG} admin install hook: {' '.join(args[1:])}".rstrip())
        return 0

    print(f"{PLUGIN_SLUG} admin passthrough: {' '.join(args)}".rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
