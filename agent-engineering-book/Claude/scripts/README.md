# scripts/

Repository tooling for Book 1. Run from `agent-engineering-book/` with the
root `pyproject.toml` dev dependencies installed (`pip install -e ".[dev]"`).

## `check_manifest.py`

Validates `book-1-foundations/manifest.yaml`: every listed class has every
required artifact (`README.md`, `BUILD.md`, `GRADING.md`,
`requirements-dev.txt`, and the standard directories), and no class-*
folder that looks implemented (has its own `tests/chNN/`) is missing from
the manifest.

```
python3 scripts/check_manifest.py
```

## `sync_shared_tests.py`

Propagates `book-1-foundations/tests_shared/` (canonical foundational
tests) into every class that should carry them, per the manifest's
`depends_on` chain. Edit a foundational test in `tests_shared/`, then run
this to reach every class — don't edit a class's copy directly.

```
python3 scripts/sync_shared_tests.py           # write: propagate canonical -> all classes
python3 scripts/sync_shared_tests.py --check   # read-only: fail if anything has drifted
```

## `create_class.py`

Scaffolds the next class from a copy of a previous one — copies approved
project artifacts (not caches, venvs, or OS files), writes placeholder
`README.md`/`BUILD.md`/`GRADING.md`, and refuses to overwrite an existing
class directory.

```
python3 scripts/create_class.py --from class-03-instruction-architecture-and-claude-md \
    --number 4 --slug skills-and-reusable-capabilities
```

Does **not** register the new class in `manifest.yaml` and does **not**
create its `tests/chNN/` — that's the actual work of building the class.
Once `tests/ch04/` genuinely exists and passes, register it:

```
python3 scripts/create_class.py --from class-03-instruction-architecture-and-claude-md \
    --number 4 --slug skills-and-reusable-capabilities --register
```

`--register` refuses if `tests/chNN/` doesn't exist yet, and appends to
`manifest.yaml` as text rather than reserializing it, so the file's
explanatory header comments survive.
