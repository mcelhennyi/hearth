"""@HRT-OPS-002 Plugin enter/exit session environment (T-FR-0003-08)."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping, MutableMapping
from pathlib import Path

STACK_ENV = "HEARTH_PLUGIN_ENTER_STACK"
FROM_ENV = "HEARTH_PLUGIN_ENTER_FROM"


class PluginEnterSessionError(RuntimeError):
    """User-facing plugin enter/exit failure."""


def _decode_stack(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PluginEnterSessionError(
            f"invalid {STACK_ENV} (expected a JSON array of path strings)",
        ) from exc
    if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
        raise PluginEnterSessionError(f"invalid {STACK_ENV} (expected a JSON array of strings)")
    return list(data)


def _encode_stack(stack: list[str]) -> str:
    return json.dumps(stack, separators=(",", ":"))


def session_stack_from(mapping: Mapping[str, str]) -> list[str]:
    """Return a copy of the enter stack from ``mapping`` (for tests)."""

    return list(_decode_stack(mapping.get(STACK_ENV)))


def clear_enter_session(env: MutableMapping[str, str]) -> None:
    env.pop(STACK_ENV, None)
    env.pop(FROM_ENV, None)


def prepare_enter_environment(env: MutableMapping[str, str], *, from_dir: Path) -> None:
    """Record ``from_dir`` as the return target and append it to the enter stack."""

    resolved = str(from_dir.resolve())
    stack = _decode_stack(env.get(STACK_ENV))
    stack.append(resolved)
    env[STACK_ENV] = _encode_stack(stack)
    env[FROM_ENV] = resolved


def pop_enter_target(env: MutableMapping[str, str]) -> Path:
    """Pop the newest enter frame and return the directory the caller should ``chdir`` into."""

    stack = _decode_stack(env.get(STACK_ENV))
    if not stack:
        raise PluginEnterSessionError(
            "not inside a hearth plugin enter session (HEARTH_PLUGIN_ENTER_STACK is empty)",
        )
    target = Path(stack.pop())
    if stack:
        env[STACK_ENV] = _encode_stack(stack)
        env[FROM_ENV] = stack[-1]
    else:
        clear_enter_session(env)
    return target


def exit_plugin_enter_session(env: MutableMapping[str, str] | None = None) -> Path:
    """``plugin --exit``: restore working directory and trim the enter stack."""

    mapping = os.environ if env is None else env
    target = pop_enter_target(mapping)
    os.chdir(target)
    return target.resolve()
