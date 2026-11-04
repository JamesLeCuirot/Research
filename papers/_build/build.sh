#!/usr/bin/env bash
# Build paper.pdf for every paper folder (or the folders given as arguments) with latexmk.
# Usage: papers/_build/build.sh [papers/01-...]
# Installs the TeX Live packages it needs if pdflatex is missing (Debian/Ubuntu).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
if ! command -v latexmk >/dev/null || ! kpsewhich IEEEtran.bst >/dev/null 2>&1; then
  echo "Installing TeX Live packages..." >&2
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
    texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-science \
    lmodern latexmk texlive-publishers cm-super >/dev/null
fi
dirs=("$@")
if [ ${#dirs[@]} -eq 0 ]; then dirs=("$ROOT"/0*/); fi
for d in "${dirs[@]}"; do
  d="$(cd "$d" && pwd)"
  [ -f "$d/paper.tex" ] || { echo "skip $d (no paper.tex)"; continue; }
  ( cd "$d" && TEXINPUTS="$HERE//:" BSTINPUTS="$HERE//:" BIBINPUTS="$HERE//:" latexmk -pdf -interaction=nonstopmode -halt-on-error -quiet paper.tex >/dev/null \
      || { echo "LaTeX failed in $d; see $d/paper.log" >&2; exit 1; } )
  # Report undefined references/citations and overfull boxes worth a look.
  grep -E "undefined|Citation .* undefined|Reference .* undefined" "$d/paper.log" | sort -u | head -20 || true
  ( cd "$d" && latexmk -c -quiet paper.tex >/dev/null 2>&1 || true; rm -f paper.bbl.bak )
  echo "built $d/paper.pdf"
done
