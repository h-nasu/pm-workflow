# Task Breakdown: Rename `text` → `transcript`

| # | Task | Files | Verification |
|---|------|-------|--------------|
| 1 | Rename schema field `text` → `transcript` | `api/schemas/meeting.py` | import + tests |
| 2 | Update service to read `payload.transcript` (`_derive_title` param + call site) | `services/meeting.py` | unit tests |
| 3 | Update endpoint summary wording | `api/v1/meetings.py` | n/a |
| 4 | Update unit tests to use `transcript=` | `tests/unit/test_meeting_service.py` | `pytest tests/unit` |
| 5 | Update integration tests to send `"transcript":` | `tests/integration/test_api.py` | `pytest tests/integration` |
| 6 | Update docs examples/notes | `docs/api-endpoints.md` | docs render |
| 7 | Run full suite + lint + typecheck | repo root | `pytest`, `ruff`, `mypy` |
