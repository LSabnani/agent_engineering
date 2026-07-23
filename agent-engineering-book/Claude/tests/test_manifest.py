"""Repo-level test (not per-class): manifest.yaml is internally consistent
and every class it lists has every required artifact. Run from the book
root with the root pyproject's dev dependencies installed.
"""

import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BOOK_ROOT / "scripts"))

from check_manifest import check_manifest  # noqa: E402


def test_manifest_has_no_errors():
    errors = check_manifest(BOOK_ROOT / "book-1-foundations")
    assert not errors, "manifest check failed:\n" + "\n".join(errors)
