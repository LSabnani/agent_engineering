# tests_shared/

Canonical source for foundational, cross-class test logic. **Do not edit
the copies inside `class-NN-.../tests/`** — edit here, then run
`python3 ../scripts/sync_shared_tests.py` to propagate the fix to every
class that carries that chapter's tests.

## Why this exists, and why classes still have real (non-symlink) copies

Every class folder is designed to be **self-sufficient** — copy
`class-05-.../` out on its own and it still runs, with no dependency on
anything outside itself. A live import from `tests_shared/` would break
that the moment a class folder is copied or extracted independently.

So instead: this directory is the single place a foundational test gets
*written or fixed*, and `scripts/sync_shared_tests.py` copies the current
canonical version into every class's `tests/chNN/` that the manifest says
should carry it (based on chapter number and the `depends_on` chain in
`../manifest.yaml`). Each class folder keeps a real, standalone copy;
`sync_shared_tests.py --check` (which CI runs) fails the build if any
class's copy has drifted from canonical — so "fix it once" is enforced by
tooling, not by hoping every copy gets updated by hand.

## Layout

- `ch02/` — foundational workspace checks, applies to every class from
  Class 02 onward.
- `ch03/` — CLAUDE.md/config structure, schema validation, candidate-account
  fit, proof-point lifecycle, cross-file integrity. Applies to every class
  from Class 03 onward.

## After editing a file here

```
cd book-1-foundations
python3 scripts/sync_shared_tests.py          # propagate to every class
python3 scripts/sync_shared_tests.py --check  # verify nothing is out of sync
```
