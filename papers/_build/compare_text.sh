#!/usr/bin/env bash
# Word-level comparison of a paper's old Markdown (from git) with its new LaTeX, for checking
# that conversion changed formatting and citation style only.
# Usage: papers/_build/compare_text.sh papers/03-from-rsp-to-sms [git-rev, default dfd94b7 = v0.3 Markdown]
set -euo pipefail
d="$(cd "$1" && pwd)"; rev="${2:-dfd94b7}"   # last commit with every paper as paper.md (v0.3)
rel="$(git -C "$d" rev-parse --show-prefix)"
out="$(mktemp -d)"
git -C "$d" show "$rev:${rel}paper.md" > "$out/old.md"
pandoc "$out/old.md" -t plain --wrap=none -o "$out/old.txt"
pandoc "$d/paper.tex" -f latex -t plain --wrap=none -o "$out/new.txt" 2>/dev/null || true
# One sentence per line to keep the diff readable.
for f in old new; do sed -E 's/([.!?]) +/\1\n/g' "$out/$f.txt" > "$out/$f.s.txt"; done
git diff --no-index --word-diff=plain --word-diff-regex='[^[:space:]]+' "$out/old.s.txt" "$out/new.s.txt" > "$out/diff.txt" || true
echo "Word diff written to $out/diff.txt ($(grep -c '\[-\|{+' "$out/diff.txt" || true) changed lines)"
