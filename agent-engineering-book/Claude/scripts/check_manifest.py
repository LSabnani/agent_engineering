#!/usr/bin/env python3
"""Validate book-1-foundations/manifest.yaml.

This is the single source of truth for "which classes are implemented" —
CI and `make verify` read this, not directory discovery. Every class listed
here must have every required artifact; every class-* directory that looks
implemented (has a tests/ dir) but isn't listed is itself a failure, so a
class can't quietly exist without being registered, and a class can't
quietly lose its tests without CI noticing.
"""

import re
import sys
from pathlib import Path

import yaml

REQUIRED_FILES = ["README.md", "BUILD.md", "GRADING.md", "requirements-dev.txt"]
REQUIRED_DIRS = [".claude", "config", "data", "src", "outputs", "evals", "tests"]

CLASS_NUMBER_PATTERN = re.compile(r"^class-(\d+)-")


def check_manifest(book1_root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = book1_root / "manifest.yaml"
    if not manifest_path.exists():
        return [f"manifest.yaml not found at {manifest_path}"]

    manifest = yaml.safe_load(manifest_path.read_text())
    classes = manifest.get("implemented_classes") or []
    if not classes:
        errors.append("manifest.yaml lists zero implemented classes")

    seen_ids: set[str] = set()
    all_ids = {entry.get("id") for entry in classes if entry.get("id")}

    for entry in classes:
        class_id = entry.get("id")
        if not class_id:
            errors.append(f"manifest entry missing 'id': {entry}")
            continue
        if class_id in seen_ids:
            errors.append(f"duplicate manifest entry: {class_id}")
        seen_ids.add(class_id)

        class_dir = book1_root / class_id
        if not class_dir.is_dir():
            errors.append(f"{class_id}: directory does not exist")
            continue

        for f in REQUIRED_FILES:
            if not (class_dir / f).is_file():
                errors.append(f"{class_id}: missing required file {f}")

        for d in REQUIRED_DIRS:
            if not (class_dir / d).is_dir():
                errors.append(f"{class_id}: missing required directory {d}")

        tests_subdir = entry.get("tests_subdir")
        if tests_subdir:
            if not (class_dir / "tests" / tests_subdir).is_dir():
                errors.append(
                    f"{class_id}: tests_subdir '{tests_subdir}' not found under tests/ "
                    "(a test directory was deleted or renamed without updating the manifest)"
                )
        else:
            errors.append(f"{class_id}: manifest entry missing 'tests_subdir'")

        depends_on = entry.get("depends_on")
        if depends_on and depends_on not in all_ids:
            errors.append(
                f"{class_id}: depends_on '{depends_on}' is not itself in the manifest"
            )

    # A class-* folder with its OWN chapter's tests/chNN/ subdirectory is
    # what "looks implemented" actually means — not merely having a tests/
    # directory at all. scripts/create_class.py deliberately copies forward
    # the previous class's inherited tests/ (e.g. tests/ch03/) into a new,
    # not-yet-built class-04/ scaffold, so a bare "tests/ exists" check
    # would misfire on every freshly scaffolded class. Only the class's own
    # chapter subdirectory existing means the class itself was built.
    for candidate in sorted(book1_root.glob("class-*")):
        if not candidate.is_dir() or candidate.name in seen_ids:
            continue
        match = CLASS_NUMBER_PATTERN.match(candidate.name)
        if not match:
            continue
        own_tests_subdir = f"ch{int(match.group(1)):02d}"
        if (candidate / "tests" / own_tests_subdir).is_dir():
            errors.append(
                f"{candidate.name}: has its own tests/{own_tests_subdir}/ but is not "
                "registered in manifest.yaml — implemented classes must be listed explicitly"
            )

    return errors


def main() -> int:
    book1_root = Path(__file__).resolve().parent.parent / "book-1-foundations"
    errors = check_manifest(book1_root)
    if errors:
        print("Manifest check FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"Manifest check passed ({book1_root / 'manifest.yaml'}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
