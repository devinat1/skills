#!/usr/bin/env bash
# Link the tracked Jev runtime into the shared Agentic home.
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
agentic_root=${AGENTIC_HOME:-$HOME/.agentic}
target="$agentic_root/artifacts/jev"
source="$repo_root/scripts/jev"

mkdir -p "$agentic_root/artifacts"
if [[ -e "$target" && ! -L "$target" ]]; then
  printf 'Refusing to replace non-symlink %s; move it aside first.\n' "$target" >&2
  exit 1
fi
ln -sfn "$source" "$target"
printf 'Linked %s -> %s\n' "$target" "$source"
