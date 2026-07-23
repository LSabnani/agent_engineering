#!/usr/bin/env python3
"""One command, checking everything: `make verify` / `python3
scripts/verify_repository.py`.

Runs the same checks locally and in CI — this script *is* what CI runs, not
a separate approximation of it. Composes the existing focused tools
(check_manifest, sync_shared_tests --check, the pytest suite) rather than
reimplementing what they already check, and adds the checks that don't
belong in pytest: stray files that shouldn't be committed, broken relative
links across the book's own markdown, and class metadata matching its own
folder name.
"""

import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_manifest import check_manifest  # noqa: E402
from sync_shared_tests import sync as sync_shared_tests  # noqa: E402

BOOK_ROOT = Path(__file__).resolve().parent.parent
BOOK1_ROOT = BOOK_ROOT / "book-1-foundations"

STRAY_FILE_NAMES = {".DS_Store", "Thumbs.db"}
STRAY_SUFFIXES = {".pyc", ".sqlite", ".sqlite3"}
SECRET_FILE_NAMES = {".env"}
SECRET_SUFFIXES = {".pem", ".key"}

# Directories excluded from the broken-link scan: archive/ is a frozen
# historical record we don't police, my-work/ is gitignored personal space.
SCAN_EXCLUDE_DIR_NAMES = {"archive", "my-work", ".git"}

MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _matches_stray_pattern(relpath: str) -> str | None:
    name = Path(relpath).name
    suffix = Path(relpath).suffix
    if name in STRAY_FILE_NAMES or suffix in STRAY_SUFFIXES:
        return "stray file"
    if name in SECRET_FILE_NAMES or suffix in SECRET_SUFFIXES:
        return "possible secret"
    return None


def check_no_stray_files() -> list[str]:
    """Checks what git actually tracks or would track — not the raw
    filesystem. A raw filesystem walk would flag __pycache__ this very
    script's own imports just created, which is noise, not a real problem:
    .gitignore already keeps it out of the repository. What matters is
    whether a stray file has slipped past .gitignore and is tracked or
    about to be committed."""
    problems = []

    tracked = subprocess.run(
        ["git", "ls-files"], cwd=BOOK_ROOT, capture_output=True, text=True
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "status", "--porcelain"], cwd=BOOK_ROOT, capture_output=True, text=True
    ).stdout.splitlines()
    untracked_paths = [line[3:] for line in untracked if line]

    for relpath in tracked + untracked_paths:
        kind = _matches_stray_pattern(relpath)
        if kind:
            problems.append(f"{kind}: {relpath}")

    return problems


def check_no_broken_relative_links() -> list[str]:
    problems = []
    for md_file in BOOK_ROOT.rglob("*.md"):
        if any(part in SCAN_EXCLUDE_DIR_NAMES for part in md_file.parts):
            continue
        text = md_file.read_text(errors="ignore")
        for match in MARKDOWN_LINK_PATTERN.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (md_file.parent / target_path).resolve()
            if not resolved.exists():
                problems.append(
                    f"{md_file.relative_to(BOOK_ROOT)}: broken link to {target!r}"
                )
    return problems


def check_class_metadata_matches_folder_name() -> list[str]:
    problems = []
    manifest = yaml.safe_load((BOOK1_ROOT / "manifest.yaml").read_text())
    for entry in manifest.get("implemented_classes") or []:
        class_id = entry.get("id", "")
        match = re.match(r"^class-(\d+)-", class_id)
        if not match:
            problems.append(f"manifest entry id {class_id!r} doesn't match class-NN-slug pattern")
            continue
        folder_number = int(match.group(1))
        declared_number = entry.get("chapter")
        if folder_number != declared_number:
            problems.append(
                f"{class_id}: folder name implies chapter {folder_number}, "
                f"manifest says chapter={declared_number!r}"
            )
    return problems


def run_pytest() -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=BOOK_ROOT,
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    return result.returncode == 0, output


def main() -> int:
    all_problems: dict[str, list[str]] = {}

    all_problems["manifest"] = check_manifest(BOOK1_ROOT)
    all_problems["shared-test sync"] = sync_shared_tests(check_only=True)
    all_problems["stray files"] = check_no_stray_files()
    all_problems["relative links"] = check_no_broken_relative_links()
    all_problems["class metadata"] = check_class_metadata_matches_folder_name()

    print("Running pytest (this covers YAML/JSON parsing, schema validation, "
          "cross-file integrity, permission-deny rules, duplicate accounts, "
          "and proof-point expiry — all as gate tests)...")
    pytest_ok, pytest_output = run_pytest()
    if not pytest_ok:
        print(pytest_output)

    ok = pytest_ok
    print("\n=== make verify summary ===")
    for label, problems in all_problems.items():
        if problems:
            ok = False
            print(f"[FAIL] {label}:")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"[ OK ] {label}")
    print(f"[{'OK' if pytest_ok else 'FAIL'}] pytest suite")

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
