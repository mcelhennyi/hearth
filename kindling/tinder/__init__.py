"""Kindling Tinder — Pydantic schema for tinder.toml (published as part of Kindling).

This is the authoritative copy. apps/hub/api/tinder/schema.py imports from
here once the Kindling submodule/local directory is wired as a source.

REWORK-REQUIRED (deferred per T-FR-0001-07 scope-right): apps/hub/api/tinder/schema.py
currently duplicates this file. Once kindling/ is promoted to a proper submodule, the
hub loader should import from kindling.tinder.schema directly.
"""
