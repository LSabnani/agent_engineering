#!/usr/bin/env python3
"""Scaffold the next Book 1 class from a copy of the previous one.

Usage:
    python scripts/create_class.py --from class-03-instruction-architecture-and-claude-md \\
        --number 4 --slug skills-and-reusable-capabilities

    # once the class is actually built and tests/ch04/ exists and passes:
    python scripts/create_class.py --from class-03-instruction-architecture-and-claude-md \\
        --number 4 --slug skills-and-reusable-capabilities --register

Copies the --from class's approved project artifacts (not caches, virtual
environments, or OS files) into a new class-NN-<slug>/ folder, refuses to
overwrite an existing class, and writes placeholder README.md / BUILD.md /
GRADING.md for the new chapter. It deliberately does NOT create the new
chapter's own tests/chNN/ directory or add it to manifest.yaml — building
that content is the actual work of the class, not something to fake with a
template. Use --register only once tests/chNN/ genuinely exists and passes;
--register checks for that and refuses otherwise.
"""

import argparse
import shutil
import sys
from pathlib import Path

import yaml

BOOK1_ROOT = Path(__file__).resolve().parent.parent / "book-1-foundations"

EXCLUDE_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    ".DS_Store",
    "Thumbs.db",
}
EXCLUDE_SUFFIXES = {".pyc", ".egg-info"}


def _ignore(directory, names):
    ignored = set()
    for name in names:
        if name in EXCLUDE_NAMES or any(name.endswith(s) for s in EXCLUDE_SUFFIXES):
            ignored.add(name)
    return ignored


def _title_from_slug(slug: str) -> str:
    return slug.replace("-", " ").title()


def _write_placeholder_docs(class_dir: Path, number: int, slug: str, title: str, from_id: str):
    chapter_ref = f"manuscript/book-1-foundations/ch{number:02d}-{slug}.md"

    (class_dir / "README.md").write_text(
        f"""# Class {number:02d} — {title}

**Not yet built.** This folder was scaffolded from `../{from_id}/` by
`scripts/create_class.py` — it currently contains that class's cumulative
implementation, unchanged, plus these placeholder docs for Chapter
{number}.

Read `../../{chapter_ref}` first, then replace this README, `BUILD.md`,
and `GRADING.md` with real content once the class is actually built, and
add `tests/ch{number:02d}/` with real gate tests.

Register this class in `../manifest.yaml` only after `tests/ch{number:02d}/`
exists and passes — run `create_class.py ... --register` to do that check
and the registration together.
"""
    )

    (class_dir / "BUILD.md").write_text(
        f"""# Building Class {number:02d} with Claude

TODO — write the practical, step-by-step, Claude-driven build guide for
this chapter, following the pattern in earlier classes' `BUILD.md` files:
goal, prerequisites, numbered steps (what to ask Claude and why), a verify
section ending in a `pytest` command, and a "grade it" pointer to
`GRADING.md`.
"""
    )

    (class_dir / "GRADING.md").write_text(
        f"""# Class {number:02d} Grading Criteria

TODO — write the class-specific qualitative criteria for
`../../GRADING-RUBRIC-TEMPLATE.md`'s LLM-as-judge step: what would make
this class's deliverable good versus merely present, and an
independent-understanding-not-a-copy criterion per
`HOW-TO-WORK-A-CLASS.md`'s anti-gaming guidance.
"""
    )


def create(from_id: str, number: int, slug: str) -> Path:
    source_dir = BOOK1_ROOT / from_id
    if not source_dir.is_dir():
        raise SystemExit(f"--from class does not exist: {source_dir}")

    new_id = f"class-{number:02d}-{slug}"
    target_dir = BOOK1_ROOT / new_id
    if target_dir.exists():
        raise SystemExit(
            f"refusing to overwrite existing class directory: {target_dir}\n"
            "Remove it first if you really mean to regenerate it."
        )

    shutil.copytree(source_dir, target_dir, ignore=_ignore)

    title = _title_from_slug(slug)
    _write_placeholder_docs(target_dir, number, slug, title, from_id)

    return target_dir


def register(number: int, slug: str, from_id: str) -> None:
    new_id = f"class-{number:02d}-{slug}"
    class_dir = BOOK1_ROOT / new_id
    tests_subdir = f"ch{number:02d}"

    if not (class_dir / "tests" / tests_subdir).is_dir():
        raise SystemExit(
            f"refusing to register {new_id}: tests/{tests_subdir}/ does not exist yet. "
            "Build and test the class for real before registering it — "
            "registering a class without its own tests is exactly the silent-skip "
            "failure mode manifest.yaml exists to prevent."
        )

    manifest_path = BOOK1_ROOT / "manifest.yaml"
    original_text = manifest_path.read_text()
    manifest = yaml.safe_load(original_text)
    classes = manifest["implemented_classes"]

    if any(c["id"] == new_id for c in classes):
        raise SystemExit(f"{new_id} is already registered in manifest.yaml")

    # Append as text rather than re-serializing the whole structure through
    # yaml.safe_dump — a full re-dump silently drops every comment in the
    # file, including the header explaining what this file is for. Appending
    # in place preserves it.
    new_entry = (
        f"\n  - id: {new_id}\n"
        f"    chapter: {number}\n"
        f"    tests_subdir: {tests_subdir}\n"
        f"    depends_on: {from_id}\n"
    )
    manifest_path.write_text(original_text.rstrip("\n") + "\n" + new_entry)
    print(f"Registered {new_id} in manifest.yaml.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from", dest="from_id", required=True, help="existing class id to copy from")
    parser.add_argument("--number", type=int, required=True, help="chapter/class number, e.g. 4")
    parser.add_argument("--slug", required=True, help="kebab-case slug matching the manuscript filename")
    parser.add_argument(
        "--register",
        action="store_true",
        help="also add to manifest.yaml — only works if tests/chNN/ already exists",
    )
    args = parser.parse_args()

    if args.register:
        register(args.number, args.slug, args.from_id)
        return 0

    target_dir = create(args.from_id, args.number, args.slug)
    print(f"Created {target_dir.relative_to(BOOK1_ROOT.parent)}")
    print(f"  - copied from: {args.from_id}")
    print("  - README.md / BUILD.md / GRADING.md written as placeholders")
    print(f"  - NOT registered in manifest.yaml — build tests/ch{args.number:02d}/ first, "
          f"then re-run with --register")
    return 0


if __name__ == "__main__":
    sys.exit(main())
