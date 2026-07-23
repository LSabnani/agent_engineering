#!/usr/bin/env python3
"""Sync book-1-foundations/tests_shared/ (canonical) into every manifest-
listed class's tests/ directory, or --check that they're already in sync.

Why a sync step exists instead of a live import: every class folder is
designed to be self-sufficient (copy class-05/ out on its own and it still
runs). A live import from tests_shared/ would break that guarantee the
moment a class folder is copied independently. So tests_shared/ is the
single place a foundational test gets edited; this script propagates that
edit into every class's real, standalone copy. --check is what CI runs to
make sure that propagation actually happened — it fails the build if any
class's copy has drifted from canonical, rather than silently tolerating
the drift.
"""

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

import yaml

BOOK1_ROOT = Path(__file__).resolve().parent.parent / "book-1-foundations"
SHARED_ROOT = BOOK1_ROOT / "tests_shared"


def _load_classes() -> list[dict]:
    manifest = yaml.safe_load((BOOK1_ROOT / "manifest.yaml").read_text())
    return manifest["implemented_classes"]


def _applicable_subdirs(class_id: str, classes_by_id: dict) -> list[str]:
    """Walk the depends_on chain to collect every tests_subdir this class
    should carry — its own, plus every ancestor's."""
    subdirs = []
    seen = set()
    current = classes_by_id.get(class_id)
    while current and current["id"] not in seen:
        seen.add(current["id"])
        subdirs.append(current["tests_subdir"])
        dep = current.get("depends_on")
        current = classes_by_id.get(dep) if dep else None
    return subdirs


def sync(check_only: bool) -> list[str]:
    classes = _load_classes()
    classes_by_id = {c["id"]: c for c in classes}
    problems: list[str] = []

    for entry in classes:
        class_dir = BOOK1_ROOT / entry["id"]
        for subdir in _applicable_subdirs(entry["id"], classes_by_id):
            shared_dir = SHARED_ROOT / subdir
            if not shared_dir.is_dir():
                problems.append(f"tests_shared/{subdir}/ does not exist")
                continue

            target_dir = class_dir / "tests" / subdir
            # Every file, not just *.py — Ch. 6 added non-Python fixtures
            # (fixtures/*.txt, *.json) that a test file depends on just as
            # much as its own source. Missing those silently would mean
            # --check passes while a test actually can't run standalone.
            for shared_file in sorted(f for f in shared_dir.rglob("*") if f.is_file()):
                rel = shared_file.relative_to(shared_dir)
                target_file = target_dir / rel
                if check_only:
                    if not target_file.exists():
                        problems.append(f"{entry['id']}/tests/{subdir}/{rel} is missing")
                    elif not filecmp.cmp(shared_file, target_file, shallow=False):
                        problems.append(
                            f"{entry['id']}/tests/{subdir}/{rel} is out of "
                            f"sync with tests_shared/{subdir}/{rel}"
                        )
                else:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(shared_file, target_file)

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="verify sync without writing anything"
    )
    args = parser.parse_args()

    problems = sync(check_only=args.check)
    if problems:
        print("Shared-test sync check FAILED:" if args.check else "Sync encountered problems:")
        for p in problems:
            print(f"  - {p}")
        if args.check:
            print("\nRun `python3 scripts/sync_shared_tests.py` (no --check) to fix.")
        return 1

    print("Shared tests are in sync." if args.check else "Shared tests synced to all classes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
