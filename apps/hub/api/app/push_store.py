from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_subscriptions(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        return []
    return [item for item in raw if isinstance(item, dict)]


def save_subscriptions(path: Path, subscriptions: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(subscriptions, f, indent=2)
        f.write("\n")


def upsert_subscription(
    existing: list[dict[str, Any]], candidate: dict[str, Any]
) -> list[dict[str, Any]]:
    endpoint = candidate.get("endpoint")
    if not isinstance(endpoint, str) or not endpoint:
        raise ValueError("subscription endpoint is required")
    filtered = [item for item in existing if item.get("endpoint") != endpoint]
    filtered.append(candidate)
    return filtered
