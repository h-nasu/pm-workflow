# Development Record: LLM-based Meeting Extraction Endpoint

## Summary
Added `POST /api/v1/meetings/extract` — an LLM-assisted alternative to the LLM-free `POST /api/v1/meetings/manual`. The new endpoint accepts raw `text`, uses the LLM to extract structured meeting fields, and persists a `Meeting` record. Both creation paths now coexist.

## Changes Made

| File | Change |
|------|--------|
| `src/pm_workflow/api/schemas/meeting.py` | `MeetingExtractRequest { text }` |
| `src/pm_workflow/prompts/manual_meeting.txt` | Re-added LLM extraction prompt |
| `src/pm_workflow/services/meeting.py` | `LLMMeetingService` + `ManualMeetingExtraction` + `_parse_date` |
| `src/pm_workflow/api/v1/meetings.py` | `POST /extract` endpoint (before `/{meeting_id}`) |
| `tests/unit/test_llm_meeting_service.py` | Unit tests for LLM service |
| `tests/integration/test_api.py` | Integration tests for `/extract` |
| `README.md`, `docs/api-endpoints.md` | Documented the new endpoint |

## Key Decisions
- Separate endpoint from `manual` so callers choose LLM vs no-LLM.
- Synthetic `fireflies_id = "manual-<uuid4>"` (no schema migration).
- Reuses `MeetingResponse`; error mapping (`LLMError`/`ValidationError` → 422, others → 500) mirrors `AnalysisService`.
- Provider/prompt manager built in the endpoint, consistent with `sync`/`analyze`.

## Verification
- `pytest tests/` → 41 passed (8 new: 5 unit + 2 integration + reuse of the manual suite).
- `ruff` clean on new/changed files (pre-existing repo-wide B008/BLE001 patterns in `meetings.py` unchanged).
- `mypy` clean on `services/meeting.py` and `schemas/meeting.py`; `meetings.py` retains pre-existing un-typed route-handler patterns.
