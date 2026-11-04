#!/bin/sh
# Build paper.pdf for the AAAI 2027 workshop submission.
# pdflatex + bibtex in a temporary copy (no build files left in this folder), then clear the PDF
# metadata (AAAI anonymous-submission rule) and copy paper.pdf back.
# Needs TeX Live with newtx, tex-gyre and kastrup (Debian: texlive-latex-extra, texlive-fonts-extra,
# texlive-plain-generic, tex-gyre) and Python 3 with pypdf.
set -e
HERE=$(cd "$(dirname "$0")/.." && pwd)
B=$(mktemp -d)
cp "$HERE/paper.tex" "$HERE/references.bib" "$HERE/aaai2027.sty" "$HERE/aaai2027.bst" "$B/"
cp -r "$HERE/figures" "$B/"
cd "$B"
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > /dev/null
bibtex paper > /dev/null
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > /dev/null
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > /dev/null
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > /dev/null
echo "Warnings (overfull boxes, undefined references or citations, BibTeX):"
grep -E "Overfull|undefined|Rerun" paper.log || echo "  none"
grep -i warning paper.blg || true
python3 -I "$HERE/check/clean_pdf.py" paper.pdf "$HERE/paper.pdf"
pdfinfo "$HERE/paper.pdf" | grep -E "^(Pages|Page size|PDF version|Author|Creator|Producer|Title)"
rm -rf "$B"
