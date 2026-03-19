#!/bin/bash
set -e

echo "=============================================="
echo "Building: Why Rotating Fluids Make Polygons"
echo "Paper Series (5 PDFs)"
echo "=============================================="
echo ""

echo "[1/5] Paper 1: Mathematical Foundations..."
cd paper-1-mathematics && pdflatex -interaction=nonstopmode main > /dev/null && bibtex main > /dev/null 2>&1 && pdflatex -interaction=nonstopmode main > /dev/null && pdflatex -interaction=nonstopmode main > /dev/null && cd ..
echo "  Done ($(grep -c 'Output written' paper-1-mathematics/main.log) passes)"

echo "[2/5] Paper 2: Classical and Quantum Physics..."
cd paper-2-physics && pdflatex -interaction=nonstopmode main > /dev/null && bibtex main > /dev/null 2>&1 && pdflatex -interaction=nonstopmode main > /dev/null && pdflatex -interaction=nonstopmode main > /dev/null && cd ..
echo "  Done"

echo "[3/5] Paper 3: Planetary Applications..."
cd paper-3-planets && pdflatex -interaction=nonstopmode main > /dev/null && bibtex main > /dev/null 2>&1 && pdflatex -interaction=nonstopmode main > /dev/null && pdflatex -interaction=nonstopmode main > /dev/null && cd ..
echo "  Done"

echo "[4/5] Paper A: Appendices..."
cd paper-A-appendices && pdflatex -interaction=nonstopmode main > /dev/null && bibtex main > /dev/null 2>&1 && pdflatex -interaction=nonstopmode main > /dev/null && pdflatex -interaction=nonstopmode main > /dev/null && cd ..
echo "  Done"

echo "[5/5] Paper 0: Overview..."
cd paper-0-overview && pdflatex -interaction=nonstopmode main > /dev/null && pdflatex -interaction=nonstopmode main > /dev/null && cd ..
echo "  Done"

echo ""
echo "=============================================="
echo "All papers built successfully."
echo "=============================================="
echo ""
echo "PDFs:"
for d in paper-0-overview paper-1-mathematics paper-2-physics paper-3-planets paper-A-appendices; do
    pages=$(pdfinfo $d/main.pdf 2>/dev/null | grep Pages | awk '{print $2}' || echo "?")
    echo "  $d/main.pdf ($pages pages)"
done
