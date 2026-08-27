# Task Breakdown: Manual Meeting Creation API (LLM-free)

## Execution Order

| # | Task | Files | Verification |
|---|------|-------|--------------|
| 1 | Add `ManualMeetingCreate` schema (text + optional metadata) | `api/schemas/meeting.py` | import + tests |
| 2 | Implement `ManualMeetingService` (no LLM) + `_derive_title` + `_normalize_date` | `services/meeting.py` | unit tests |
| 3 | Add `POST /manual` endpoint (sync, no LLM) | `api/v1/meetings.py` | integration test |
| 4 | Unit tests (defaults, title derivation, date normalization, persistence) | `tests/unit/test_meeting_service.py` | `pytest tests/unit` |
| 5 | Integration tests (200 shape, title derivation, 422 on empty text) | `tests/integration/test_api.py` | `pytest tests/integration` |
| 6 | Update docs (README + `docs/api-endpoints.md`) | `README.md`, `docs/api-endpoints.md` | docs rendered |
| 7 | Lint + typecheck + full test run | repo root | `ruff`, `mypy`, `pytest` |

## Detailed Tasks

### Task 1: Schema
- `ManualMeetingCreate`: `text: str = Field(..., min_length=1)`, plus optional `title`, `date`, `duration_minutes`, `participants` (dict, default `{}`).

### Task 2: Service (LLM-free)
- `_derive_title(text)`: first non-empty line ≤200 chars, else `"Untitled Meeting"`.
- `_normalize_date(value)`: `None` → naive now(UTC); tz-aware → naive UTC; naive → unchanged.
- `ManualMeetingService.create_from_payload(db, payload)`: builds `Meeting` with `fireflies_id="manual-<uuid4>"`, maps fields (transcript = text), persists via `meeting_repo.create`.
- No `BaseLLMProvider`/`PromptManager` usage.

### Task 3: Endpoint
- `POST /api/v1/meetings/manual` returning `MeetingResponse`.
- Declared before `/{meeting_id}` route.
- Sync handler; no LLM/provider construction.

### Tasks 4–5: Tests
- Unit: provided fields used; defaults (title from text, now date, empty participants); title derivation (first line, truncation, whitespace fallback); date normalization (tz-aware → naive UTC); persistence.
- Integration: `200` with correct shape; title derived when omitted; `422` on empty `text`.

### Tasks 6–7: Docs & verification
- README endpoint table + `docs/api-endpoints.md` new section (LLM-free, optional fields).
- `ruff check`, `mypy`, `pytest` all green.
