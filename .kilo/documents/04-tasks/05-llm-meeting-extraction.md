# Task Breakdown: LLM-based Meeting Extraction Endpoint

| # | Task | Files | Verification |
|---|------|-------|--------------|
| 1 | Add `MeetingExtractRequest` schema | `api/schemas/meeting.py` | import + tests |
| 2 | Re-add `prompts/manual_meeting.txt` | `prompts/manual_meeting.txt` | loaded in test |
| 3 | Implement `LLMMeetingService` + `ManualMeetingExtraction` + `_parse_date` | `services/meeting.py` | unit tests |
| 4 | Add `POST /extract` endpoint | `api/v1/meetings.py` | integration test |
| 5 | Unit tests (extraction, defaults, validation error, date parse) | `tests/unit/test_llm_meeting_service.py` | `pytest tests/unit` |
| 6 | Integration tests (200 shape, 422 on empty text) | `tests/integration/test_api.py` | `pytest tests/integration` |
| 7 | Update docs (README + `docs/api-endpoints.md`) | `README.md`, `docs/api-endpoints.md` | docs render |
| 8 | Lint + typecheck + full test run | repo root | `ruff`, `mypy`, `pytest` |

## Detailed
- **Task 3**: `LLMMeetingService.create_from_text` builds `Meeting` with synthetic id; maps extracted fields; stores raw `text` as transcript fallback; persists via `meeting_repo.create`. Raises `LLMError`/`ValidationError` on failures (mirrors `AnalysisService`).
- **Task 4**: Declared before `/{meeting_id}`; builds `GeminiProvider` + `PromptManager`; error mapping as in spec.
- **Task 7**: New "Create Meeting from Text (LLM)" section in `docs/api-endpoints.md`; README endpoint table row.
