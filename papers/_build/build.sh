#!/usr/bin/env bash
# Build paper.html and paper.pdf for every paper folder (or the folders given as arguments).
# Usage: papers/_build/build.sh [papers/01-...]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
dirs=("$@")
if [ ${#dirs[@]} -eq 0 ]; then dirs=("$ROOT"/0*/); fi
for d in "${dirs[@]}"; do
  d="$(cd "$d" && pwd)"
  [ -f "$d/paper.md" ] || { echo "skip $d (no paper.md)"; continue; }
  title="$(grep -m1 '^title:' "$d/paper.md" | sed -E 's/^title:[[:space:]]*"?([^"]*)"?/\1/')"
  ( cd "$d" && pandoc paper.md --from markdown+smart --to html5 --standalone \
      --template "$HERE/template.html" --css "$HERE/paper.css" --embed-resources \
      --resource-path "$d" --mathml -o paper.html )
  node "$HERE/pdf.js" "$d/paper.html" "$d/paper.pdf" "James Le Cuirot · $title"
  echo "built $d/paper.pdf"
done
