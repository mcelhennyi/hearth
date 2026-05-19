"""T-FR-0003-08: plugin enter session env + ``plugin --exit`` restoration."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from hearth_install.plugin_session import (
    FROM_ENV,
    STACK_ENV,
    PluginEnterSessionError,
    exit_plugin_enter_session,
    pop_enter_target,
    prepare_enter_environment,
    session_stack_from,
)


def test_prepare_and_pop_single_frame(tmp_path: Path) -> None:
    outer = tmp_path / "outer"
    outer.mkdir()
    env: dict[str, str] = {}
    prepare_enter_environment(env, from_dir=outer)
    assert session_stack_from(env) == [str(outer.resolve())]
    assert env[FROM_ENV] == str(outer.resolve())

    target = pop_enter_target(env)
    assert target.resolve() == outer.resolve()
    assert STACK_ENV not in env
    assert FROM_ENV not in env


def test_nested_enter_stack_pop_order(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    env: dict[str, str] = {}
    prepare_enter_environment(env, from_dir=a)
    prepare_enter_environment(env, from_dir=b)
    assert session_stack_from(env) == [str(a.resolve()), str(b.resolve())]

    first = pop_enter_target(env)
    assert first.resolve() == b.resolve()
    assert env[FROM_ENV] == str(a.resolve())

    second = pop_enter_target(env)
    assert second.resolve() == a.resolve()
    assert FROM_ENV not in env


def test_pop_empty_stack_raises() -> None:
    env: dict[str, str] = {}
    with pytest.raises(PluginEnterSessionError, match="HEARTH_PLUGIN_ENTER_STACK is empty"):
        pop_enter_target(env)


def test_exit_restores_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = tmp_path / "home"
    plugin = tmp_path / "plugin"
    home.mkdir()
    plugin.mkdir()
    monkeypatch.chdir(plugin)

    pocket: dict[str, str] = {}
    prepare_enter_environment(pocket, from_dir=home)
    exit_plugin_enter_session(env=pocket)
    assert Path.cwd().resolve() == home.resolve()


def test_malformed_stack_raises() -> None:
    env = {STACK_ENV: "not-json"}
    with pytest.raises(PluginEnterSessionError, match="invalid"):
        pop_enter_target(env)


def test_non_array_stack_raises() -> None:
    env = {STACK_ENV: json.dumps({"oops": True})}
    with pytest.raises(PluginEnterSessionError, match="invalid"):
        pop_enter_target(env)
