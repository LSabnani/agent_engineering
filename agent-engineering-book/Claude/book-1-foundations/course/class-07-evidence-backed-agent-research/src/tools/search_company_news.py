"""search_company_news — a narrow tool that looks for recent news about a
named company.

Permission level: READ_ONLY, network. Per the book's own requirements
(§2, "we should not require paid sales databases for the first version"),
no search API is wired up yet — Tavily/Exa/Serper/etc. are explicitly
optional-later integrations. Without a `fixture_dir`, this tool returns a
clear, honest "not configured" error rather than silently returning
nothing or fabricating results — an unconfigured dependency is a different
failure mode from "searched and found nothing," and callers need to be
able to tell them apart.
"""

import json
import re
from pathlib import Path

from tool_result import ok, empty, error

PERMISSION = "read_only_network"


def _slug(company_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", company_name.lower()).strip("_")


def search_company_news(company_name: str, max_results: int = 5, fixture_dir: Path | None = None) -> dict:
    if not company_name or not isinstance(company_name, str):
        return error(
            stage="search_company_news",
            error_type="invalid_input",
            attempted_action="search for company news",
            recoverable=False,
            message="company_name must be a non-empty string",
        )

    if not isinstance(max_results, int) or max_results < 1:
        return error(
            stage="search_company_news",
            error_type="invalid_input",
            attempted_action=f"search news for {company_name!r}",
            recoverable=False,
            message="max_results must be a positive integer",
        )

    if fixture_dir is None:
        return error(
            stage="search_company_news",
            error_type="not_configured",
            attempted_action=f"search news for {company_name!r}",
            recoverable=False,
            message=(
                "no search provider is configured for this class — search "
                "APIs are an optional-later integration, not part of the MVP"
            ),
        )

    fixture_path = Path(fixture_dir) / f"{_slug(company_name)}.json"
    if not fixture_path.exists():
        return empty(metadata={"company_name": company_name, "source": "fixture"})

    results = json.loads(fixture_path.read_text())
    if not results:
        return empty(metadata={"company_name": company_name, "source": "fixture"})

    return ok(results[:max_results], metadata={"company_name": company_name, "source": "fixture"})
