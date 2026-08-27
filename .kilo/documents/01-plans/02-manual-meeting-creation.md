# Implementation Plan: Manual Meeting Creation API

## Executive Summary

Extend the PM Workflow API so the system can create meeting records from free-form text provided by a user, rather than only ingesting from Fireflies. A new endpoint accepts a text payload (plus optional metadata) and persists a new `Meeting` record directly, with no LLM call on the create path.

> **Pivot (see `07-changes/01-llm-free-pivot.md`):** The initial design used the LLM to extract structured fields from text. This was changed to an LLM-free insert after feedback that an LLM call per create is expensive and unnecessary — structured understanding is deferred to the existing `/analyze` endpoint, mirroring the `sync` (create) vs `analyze` (understand) separation.

---

## Problem Understanding

Today the system only acquires meetings via `POST /api/v1/meetings/sync`, which pulls transcripts from Fireflies and creates `Meeting` rows. There is no way to manually register a meeting (e.g. a quick note, an offline discussion, or a non-Fireflies call) without a Fireflies `id`.

The `Meeting` model requires a unique, non-null `fireflies_id`. Manual entries have no Fireflies id, so the creation flow must assign a synthetic identifier while keeping the existing schema and constraints intact (no migration required).

---

## Scope

### In Scope
- New API endpoint `POST /api/v1/meetings/manual`
- Request schema accepting raw meeting `text`
- A `ManualMeetingService` that uses `BaseLLMProvider` + `PromptManager` to extract fields
- A new LLM prompt template `prompts/manual_meeting.txt`
- Reuse of the existing `MeetingResponse` schema for the response
- Unit and integration tests
- Documentation updates (README + `docs/api-endpoints.md`)

### Out of Scope
- Auto-analysis of manually created meetings (can be triggered later via `/analyze`)
- Webhook or batch ingestion
- Schema/migration changes to `Meeting`

---

## Assumptions
1. The LLM provider (Gemini) is reachable at request time for extraction.
2. `fireflies_id` must remain non-null and unique; manual entries use a `manual-<uuid>` synthetic id.
3. If extraction fails to produce a title, a sensible default ("Untitled Meeting") is used.
4. If a date cannot be parsed, the current UTC time is used.

---

## Constraints
- Follow existing patterns: FastAPI router, `MeetingRepository`, `BaseLLMProvider`, `PromptManager`.
- No direct external API calls inside the service layer (use the LLM abstraction).
- Tests use `pytest` + `unittest.mock` + in-memory SQLite (existing pattern).

---

## Proposed Approach
1. Add `ManualMeetingCreate` request schema (`text` only).
2. Implement `ManualMeetingService.create_from_text(db, text)` in `services/meeting.py`, using a `ManualMeetingExtraction` pydantic model for the LLM response and a `_parse_date` helper.
3. Add `prompts/manual_meeting.txt` to drive extraction.
4. Add the `POST /manual` route (declared before `/{meeting_id}` to avoid path conflicts), reusing `MeetingResponse`.
5. Write unit tests (service logic, date parsing) and an integration test (endpoint with mocked LLM/provider).
6. Update README and API docs.

---

## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| LLM returns malformed JSON | Medium | Medium | Wrap in `ValidationError` → `422` |
| LLM returns no date | Medium | Low | Fallback to `datetime.now(timezone.utc)` |
| `manual-<uuid>` collision | Very Low | Low | UUID4 guarantees uniqueness |
| Route conflict with `/{meeting_id}` | Low | Medium | Declare `/manual` before path-param routes |

---

## Next Steps
1. Create specification in `02-specifications/`
2. Create design in `03-designs/`
3. Create tasks in `04-tasks/`
4. Implement following `rules/coding.md`
5. Test, document, review
