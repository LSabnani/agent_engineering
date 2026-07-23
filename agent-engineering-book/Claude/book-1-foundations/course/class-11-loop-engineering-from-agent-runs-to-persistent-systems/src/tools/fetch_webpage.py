"""fetch_webpage — a narrow tool that retrieves one URL's text content.

Permission level: READ_ONLY, network. Never writes anything, never follows
a redirect to an unapproved scheme, never executes anything found on the
page — the page is data to extract facts from, per CLAUDE.md's instruction
precedence rule (Ch. 3.3), not instructions to follow.

Deterministic testing without a live network call: pass `fixture_dir` (a
directory of `<url-slug>.txt` files) and the tool reads from there instead
of the network. Gate tests always do this — hitting a real network from a
test suite would make the suite flaky and non-reproducible, exactly what
Ch. 6.6's test suite is supposed to avoid. Without `fixture_dir`, this
performs a real HTTP GET with a timeout.
"""

import re
import urllib.error
import urllib.request
from pathlib import Path

from tool_result import ok, error

PERMISSION = "read_only_network"
TIMEOUT_SECONDS = 10


def _slug(url: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", url).strip("_")


def fetch_webpage(url: str, fixture_dir: Path | None = None) -> dict:
    if not url or not isinstance(url, str):
        return error(
            stage="fetch_webpage",
            error_type="invalid_input",
            attempted_action="fetch a webpage",
            recoverable=False,
            message="url must be a non-empty string",
        )

    if not url.startswith(("http://", "https://")):
        return error(
            stage="fetch_webpage",
            error_type="invalid_input",
            attempted_action=f"fetch {url!r}",
            recoverable=False,
            message="url must start with http:// or https://",
        )

    if fixture_dir is not None:
        fixture_path = Path(fixture_dir) / f"{_slug(url)}.txt"
        if not fixture_path.exists():
            return error(
                stage="fetch_webpage",
                error_type="unavailable",
                attempted_action=f"fetch {url}",
                recoverable=True,
                message=f"no fixture found for this URL at {fixture_path}",
            )
        text = fixture_path.read_text()
        if not text.strip():
            return error(
                stage="fetch_webpage",
                error_type="empty_response",
                attempted_action=f"fetch {url}",
                recoverable=True,
                message="fixture exists but is empty",
            )
        return ok(text, metadata={"url": url, "source": "fixture"})

    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            text = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return error(
            stage="fetch_webpage",
            error_type="http_error",
            attempted_action=f"fetch {url}",
            recoverable=exc.code >= 500,
            message=f"HTTP {exc.code}: {exc.reason}",
        )
    except urllib.error.URLError as exc:
        return error(
            stage="fetch_webpage",
            error_type="unavailable",
            attempted_action=f"fetch {url}",
            recoverable=True,
            message=str(exc.reason),
        )
    except TimeoutError:
        return error(
            stage="fetch_webpage",
            error_type="timeout",
            attempted_action=f"fetch {url}",
            recoverable=True,
            message=f"no response within {TIMEOUT_SECONDS}s",
        )

    if not text.strip():
        return error(
            stage="fetch_webpage",
            error_type="empty_response",
            attempted_action=f"fetch {url}",
            recoverable=True,
            message="page returned no content",
        )
    return ok(text, metadata={"url": url, "source": "network"})
