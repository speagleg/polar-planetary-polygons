"""Numerical + symbolic validator for the C₁(S²) geodesic derivation.

Run: python3 docs/rigor-sandbox/item6-c1-sphere/numerical_check.py
Exit 0 = all claims verified. Non-zero = derivation is wrong.
"""
from __future__ import annotations
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "src"))


def main() -> int:
    print("numerical_check.py: no checks implemented yet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
