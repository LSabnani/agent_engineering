"""Chapter 6 gate test: each tool has a successful case, an invalid-input
case, and a failure-mode case (Ch. 6.6's explicit requirement) — and every
result, success or failure, comes back in the one ToolResult shape
(Ch. 6.4), never a bare value or a raised exception a caller has to guess
about.
"""

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(REPO_ROOT / "src"))

# Every class folder ships its own src/, and the full cumulative suite runs
# every class in one pytest process — without purging, Python's sys.modules
# cache would silently hand a later class's test an earlier class's copy of
# these modules regardless of sys.path.insert order (and, since
# tools/save_account_brief.py itself imports validate_account_brief, that
# staleness can smuggle in a mismatched schema from a different chapter).
for _mod in list(sys.modules):
    if _mod == "tools" or _mod.startswith("tools.") or _mod in (
        "tool_result", "validate_account_brief",
    ):
        del sys.modules[_mod]

from tools.fetch_webpage import fetch_webpage  # noqa: E402
from tools.search_company_news import search_company_news  # noqa: E402
from tools.file_tools import read_local_file, write_output_file  # noqa: E402
from tools.validate_json_tool import validate_json  # noqa: E402
from tools.save_account_brief import save_account_brief  # noqa: E402


# ---------------------------------------------------------------- fetch_webpage

def test_fetch_webpage_success():
    result = fetch_webpage("https://rockwellautomation.com", fixture_dir=FIXTURES / "webpages")
    assert result["status"] == "ok"
    assert "industrial automation" in result["data"]


def test_fetch_webpage_invalid_input_bad_scheme():
    result = fetch_webpage("not-a-url", fixture_dir=FIXTURES / "webpages")
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "invalid_input"
    assert result["error"]["recoverable"] is False


def test_fetch_webpage_invalid_input_empty_string():
    result = fetch_webpage("", fixture_dir=FIXTURES / "webpages")
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "invalid_input"


def test_fetch_webpage_failure_no_fixture():
    result = fetch_webpage("https://not-a-real-fixture.example", fixture_dir=FIXTURES / "webpages")
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "unavailable"
    assert result["error"]["recoverable"] is True


# ---------------------------------------------------------- search_company_news

def test_search_company_news_success():
    result = search_company_news("Rockwell Automation", fixture_dir=FIXTURES / "search")
    assert result["status"] == "ok"
    assert len(result["data"]) == 2


def test_search_company_news_invalid_input():
    result = search_company_news("", fixture_dir=FIXTURES / "search")
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "invalid_input"


def test_search_company_news_failure_not_configured():
    """No fixture_dir at all — the honest 'not configured' failure mode,
    not a silent empty result."""
    result = search_company_news("Rockwell Automation")
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "not_configured"
    assert result["error"]["recoverable"] is False


def test_search_company_news_empty_is_not_an_error():
    result = search_company_news("A Company With No Fixture", fixture_dir=FIXTURES / "search")
    assert result["status"] == "empty"
    assert result["error"] is None


# -------------------------------------------------------------------- file_tools

def test_read_local_file_success(tmp_path):
    (tmp_path / "note.txt").write_text("hello")
    result = read_local_file("note.txt", base_dir=tmp_path)
    assert result["status"] == "ok"
    assert result["data"] == "hello"


def test_read_local_file_invalid_input_directory_not_file(tmp_path):
    (tmp_path / "subdir").mkdir()
    result = read_local_file("subdir", base_dir=tmp_path)
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "invalid_input"


def test_read_local_file_failure_not_found(tmp_path):
    result = read_local_file("nope.txt", base_dir=tmp_path)
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "not_found"
    assert result["error"]["recoverable"] is True


def test_read_local_file_refuses_path_outside_sandbox(tmp_path):
    result = read_local_file("../../etc/passwd", base_dir=tmp_path)
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "permission_denied"
    assert result["error"]["recoverable"] is False


def test_write_output_file_success(tmp_path):
    result = write_output_file("brief.json", '{"a": 1}', outputs_dir=tmp_path)
    assert result["status"] == "ok"
    assert (tmp_path / "brief.json").read_text() == '{"a": 1}'


def test_write_output_file_invalid_input_non_string_content(tmp_path):
    result = write_output_file("brief.json", 12345, outputs_dir=tmp_path)
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "invalid_input"


def test_write_output_file_refuses_path_outside_sandbox(tmp_path):
    result = write_output_file("../escape.json", "{}", outputs_dir=tmp_path)
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "permission_denied"
    assert not (tmp_path.parent / "escape.json").exists()


# --------------------------------------------------------------- validate_json

def test_validate_json_success():
    schema_path = REPO_ROOT / "schemas" / "outreach_message.schema.json"
    good = {"message_type": "email", "text": "hello", "word_count": 1}
    result = validate_json(good, schema_path)
    assert result["status"] == "ok"


def test_validate_json_invalid_input_missing_schema():
    result = validate_json({}, REPO_ROOT / "schemas" / "does-not-exist.schema.json")
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "invalid_input"


def test_validate_json_failure_schema_violation():
    schema_path = REPO_ROOT / "schemas" / "outreach_message.schema.json"
    bad = {"message_type": "carrier_pigeon", "text": "hello", "word_count": 1}
    result = validate_json(bad, schema_path)
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "schema_violation"


# ----------------------------------------------------------- save_account_brief

def _load_valid_account_brief():
    return json.loads((REPO_ROOT / "schemas" / "examples" / "example-account-brief.json").read_text())


def test_save_account_brief_success(tmp_path):
    result = save_account_brief(_load_valid_account_brief(), "brief.json", outputs_dir=tmp_path)
    assert result["status"] == "ok"
    assert (tmp_path / "brief.json").exists()


def test_save_account_brief_invalid_input_wrong_type():
    result = save_account_brief("not a dict", "brief.json", outputs_dir=Path("/tmp"))
    assert result["status"] == "error"


def test_save_account_brief_refuses_to_save_invalid_brief(tmp_path):
    """The point of this tool: composing Ch. 5's validator with Ch. 6's
    write tool so an invalid brief never reaches disk, not just gets
    written and hoped to be fine."""
    broken = _load_valid_account_brief()
    del broken["schema_version"]
    result = save_account_brief(broken, "brief.json", outputs_dir=tmp_path)
    assert result["status"] == "error"
    assert result["error"]["error_type"] == "invalid_account_brief"
    assert not (tmp_path / "brief.json").exists()
