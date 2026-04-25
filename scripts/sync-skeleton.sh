#!/usr/bin/env bash
# Fast-forward .skeleton submodule, remove deprecated paths at consumer root,
# overwrite manifest-listed files from .skeleton/.
set -euo pipefail

die() { echo "sync-skeleton: $*" >&2; exit 1; }

repo_root() {
  git rev-parse --show-toplevel 2>/dev/null || die "not inside a git repository"
}

list_manifest_pairs() {
  local mf="$1"
  [[ -f "$mf" ]] || die "missing manifest: $mf"
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    [[ "$line" == *"|"* ]] || die "manifest line missing | : $line"
    echo "$line"
  done <"$mf"
}

validate_dep_path() {
  local p="$1"
  [[ -n "$p" ]] || return 1
  [[ "$p" != /* ]] || return 1
  [[ "$p" != *..* ]] || return 1
  [[ "$p" != .skeleton/* ]] || return 1
  return 0
}

main() {
  local root mf dep
  root="$(repo_root)"
  cd "$root"

  [[ -f .gitmodules ]] && grep -qF '[submodule ".skeleton"]' .gitmodules 2>/dev/null \
    || die "no .skeleton submodule (.gitmodules missing or submodule not registered)"

  [[ -d .skeleton/.git ]] || die ".skeleton is not a git checkout (run: git submodule update --init .skeleton)"

  echo "sync-skeleton: updating submodule .skeleton ..."
  git submodule update --init .skeleton
  if ! git -C .skeleton pull --ff-only 2>/dev/null; then
    echo "sync-skeleton: pull in .skeleton failed (often detached HEAD); trying git submodule update --remote .skeleton ..." >&2
    git submodule update --remote .skeleton || die "could not fast-forward .skeleton submodule"
  fi

  mf="$root/.skeleton/skeleton.manifest"
  [[ -f "$mf" ]] || die "missing .skeleton/skeleton.manifest"

  local depfile="$root/.skeleton/DEPRECATED_PATHS"
  if [[ -f "$depfile" ]]; then
    echo "sync-skeleton: applying deprecations from .skeleton/DEPRECATED_PATHS ..."
    while IFS= read -r line || [[ -n "$line" ]]; do
      dep="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
      [[ -z "$dep" || "$dep" == \#* ]] && continue
      validate_dep_path "$dep" || die "unsafe deprecation path: $dep"
      if [[ -e "$root/$dep" ]]; then
        if git ls-files --error-unmatch "$dep" >/dev/null 2>&1; then
          if [[ -d "$root/$dep" ]]; then
            git rm -r -f "$dep" >/dev/null
          else
            git rm -f "$dep" >/dev/null
          fi
        else
          rm -rf "${root:?}/$dep"
        fi
        echo "sync-skeleton: removed $dep"
      fi
    done <"$depfile"
  fi

  echo "sync-skeleton: copying manifest paths from .skeleton/ to repo root ..."
  local line src dst
  while IFS= read -r line; do
    src="${line%%|*}"
    dst="${line#*|}"
    src="$(echo "$src" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    dst="$(echo "$dst" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [[ "$src" == "SKELETON_REPO" || "$dst" == "SKELETON_REPO" ]] && continue
    [[ -f "$root/.skeleton/$dst" ]] || die "missing .skeleton/$dst"
    mkdir -p "$(dirname "$root/$src")"
    cp -f "$root/.skeleton/$dst" "$root/$src"
  done < <(list_manifest_pairs "$mf")

  for f in init-skeleton sync-skeleton scripts/init-skeleton.sh scripts/sync-skeleton.sh; do
    if [[ -f "$root/.skeleton/$f" ]]; then
      mkdir -p "$(dirname "$root/$f")"
      cp -f "$root/.skeleton/$f" "$root/$f"
    fi
  done

  chmod +x "$root/push-skeleton" "$root/init-skeleton" "$root/sync-skeleton" \
    "$root/develop" \
    "$root/scripts/init-skeleton.sh" "$root/scripts/sync-skeleton.sh" \
    "$root/scripts/serve-docs.sh" 2>/dev/null || true

  rm -f "$root/SKELETON_REPO"

  git add .skeleton
  while IFS= read -r line; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    [[ "$line" == *"|"* ]] || continue
    src="${line%%|*}"
    src="$(echo "$src" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [[ "$src" == "SKELETON_REPO" ]] && continue
    [[ -f "$root/$src" ]] && git add -f "$root/$src"
  done < <(list_manifest_pairs "$mf")

  for f in init-skeleton sync-skeleton scripts/init-skeleton.sh scripts/sync-skeleton.sh; do
    [[ -f "$root/$f" ]] && git add -f "$root/$f"
  done

  echo "sync-skeleton: done. Submodule pointer and template files are staged; review 'git status' and commit."
}

main "$@"
