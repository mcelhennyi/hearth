"""Spark v1 permission model and topic-pattern matching.

Authority: docs/design/spark-api.md §Permissions enforcement
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class PluginPermissions:
    spark_call: list[str] = field(default_factory=list)
    spark_publish: list[str] = field(default_factory=list)
    spark_subscribe: list[str] = field(default_factory=list)


def _pattern_to_regex(pattern: str) -> re.Pattern[str]:
    """Convert a Spark topic pattern to a compiled regex.

    ``*`` matches exactly one dot-delimited segment (no dots).
    ``>`` at the end matches everything that follows (the rest of the topic).
    """
    parts = pattern.split(".")
    regex_parts: list[str] = []
    for i, part in enumerate(parts):
        if part == ">":
            # must be last segment; matches rest of topic
            regex_parts.append(r".*")
            break
        elif part == "*":
            regex_parts.append(r"[^.]+")
        else:
            regex_parts.append(re.escape(part))
        if i < len(parts) - 1 and parts[i + 1] != ">":
            regex_parts.append(r"\.")
    return re.compile("^" + "".join(regex_parts) + "$")


def _matches_any(patterns: list[str], value: str) -> bool:
    return any(_pattern_to_regex(p).match(value) for p in patterns)


def can_call(caller_permissions: PluginPermissions, target_slug: str, method: str) -> bool:
    """Check if *caller* is allowed to call *target_slug*.*method*."""
    call_target = f"{target_slug}.{method}"
    return _matches_any(caller_permissions.spark_call, call_target)


def can_publish(publisher_permissions: PluginPermissions, topic: str) -> bool:
    """Check if the publisher is allowed to publish *topic*."""
    return _matches_any(publisher_permissions.spark_publish, topic)


def can_subscribe(subscriber_permissions: PluginPermissions, topic_pattern: str) -> bool:
    """Check if the subscriber is allowed to subscribe to *topic_pattern*."""
    return _matches_any(subscriber_permissions.spark_subscribe, topic_pattern)


def topic_matches_pattern(topic: str, pattern: str) -> bool:
    """Return True if *topic* is matched by the subscriber *pattern*."""
    return bool(_pattern_to_regex(pattern).match(topic))
