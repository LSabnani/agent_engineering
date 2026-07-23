# Known Failure Cases — Class 2 Checkpoint

## Carried forward from Class 1

- Acceptance criteria are still unverified by any test — Class 2 adds a test runner, but nothing in this checkpoint's tests actually checks `docs/acceptance-criteria.md` yet. That starts piecemeal from Class 5 onward.
- The three scenario accounts are still illustrative, not a representative dataset.
- The `tests/fixtures/expected/*.yaml` files are still hand-derived predictions, not verified against any code.

## New at this checkpoint

### 1. `./scripts/check.sh` can pass locally and still fail on a clean clone

The health check and its test have no external dependency, so this is unlikely — but `WIDGETWARE_MODEL_ID` and `GOOGLE_CLOUD_PROJECT` in `.env.example` are not validated by anything yet. A participant who hardcodes a real value in application code instead of reading from the environment will not be caught by this checkpoint's tests. This becomes a real risk starting Class 4, once a model call actually depends on these values.

### 2. `config/` and `tests/contracts/` are empty except for `.gitkeep`

This is intentional — both are populated starting Class 3 and Class 5, respectively — but a participant unfamiliar with the repository structure may reasonably wonder whether this is a mistake. It is not. If `.gitkeep` is ever accidentally deleted along with the directory, `git` will not track the empty directory at all, and later `cp -r` cumulative copies in this course's checkpoints may silently produce a slightly different structure.

### 3. `ruff` is a dev dependency, not verified by this repository in isolation

This checkpoint's own test run does not confirm `ruff` is installed and correctly configured — only `pytest`'s three tests are guaranteed to run without the dev extras. Running `./scripts/check.sh` requires `pip install -e ".[dev]"` first; running `pytest` directly does not.
