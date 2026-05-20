"""@HRT-OPS-002 Local CA export for iPhone / LAN clients (FR-0002)."""

from __future__ import annotations

import socket
from typing import TextIO

from hearth_cli.install_context import ResolvedInstall


def _guess_lan_ip() -> str | None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("192.0.2.1", 80))
            return sock.getsockname()[0]
    except OSError:
        return None


def print_ca_export_instructions(stdout: TextIO, *, lan_ip: str | None) -> None:
    host_hint = lan_ip or "<HOST-LAN-IP>"
    print(
        "\n".join(
            [
                "Local CA export is running (up to 10 minutes).",
                "",
                "On each iPhone (same Wi-Fi as this host):",
                f"  1. Safari → http://{host_hint}:8080/ca.crt",
                "  2. Install the downloaded configuration profile.",
                "  3. Settings → General → VPN & Device Management → install profile.",
                "  4. Settings → General → About → Certificate Trust Settings",
                "     → enable full trust for the Caddy local root CA.",
                "  5. Force-quit Safari, then open https://hearth.home.arpa/",
                "",
                "DNS: hearth.home.arpa must resolve to this host on the phone.",
            ],
        ),
        file=stdout,
    )


def cmd_ca_export(
    resolved: ResolvedInstall,
    stdout: TextIO,
    stderr: TextIO,
    *,
    run_compose,
) -> int:
    """Run the ``ca-export`` compose profile (blocks until timeout or Ctrl+C)."""
    if not resolved.compose_file.is_file():
        print(f"hearth ca-export: missing compose file: {resolved.compose_file}", file=stderr)
        return 1

    print_ca_export_instructions(stdout, lan_ip=_guess_lan_ip())
    return run_compose(
        resolved,
        [
            "--profile",
            "ca-export",
            "up",
            "--abort-on-container-exit",
            "--exit-code-from",
            "ca-export",
            "ca-export",
        ],
        stderr,
    )
