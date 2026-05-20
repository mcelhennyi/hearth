#!/usr/bin/env python3
from __future__ import annotations

import base64
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


def as_b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    target_dir = repo_root / "var" / "hearth" / "secrets"
    target_dir.mkdir(parents=True, exist_ok=True)

    private_path = target_dir / "vapid.priv"
    public_path = target_dir / "vapid.pub"

    private_key = ec.generate_private_key(ec.SECP256R1())
    private_value = private_key.private_numbers().private_value.to_bytes(32, "big")
    public_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )

    private_path.write_text(as_b64url(private_value), encoding="utf-8")
    public_path.write_text(as_b64url(public_bytes), encoding="utf-8")

    print(f"Wrote {private_path}")
    print(f"Wrote {public_path}")


if __name__ == "__main__":
    main()
