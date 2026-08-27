# Development Record: Manual Meeting Creation API (LLM-free)

## Summary
Implemented `POST /api/v1/meetings/manual` as a cheap, LLM-free insert. The raw `text` payload is stored as the `transcript`; optional `title`/`date`/`duration_minutes`/`participants` may be supplied. No LLM is invoked on creation; structured understanding is deferred to the existing `/analyze` endpoint (mirroring `sync` vs `analyze`).

## Changes Made

| File | Change |
|------|--------|
| `src/pm_workflow/api/schemas/meeting.py` | `ManualMeetingCreate` with `text` + optional metadata fields |
| `src/pm_workflow/services/meeting.py` | `ManualMeetingService.create_from_payload` + `_derive_title` + `_normalize_date` (no LLM) |
| `src/pm_workflow/api/v1/meetings.py` | `POST /manual` sync handler, no LLM/provider dependency |
| `src/pm_workflow/prompts/manual_meeting.txt` | Deleted (no longer used) |
| `tests/unit/test_meeting_service.py` | LLM-free unit tests |
| `tests/integration/test_api.py` | Endpoint integration tests (no LLM mock) |
| `README.md`, `docs/api-endpoints.md` | Documented the LLM-free endpoint |

## Verification
- `pytest tests/` → 33 passed.
- `ruff check` on changed files → clean (only pre-existing repo-wide B008/BLE001 patterns remain in `meetings.py`).
- `mypy` on new modules → clean.
