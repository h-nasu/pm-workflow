# Implementation Plan: LLM-based Meeting Extraction Endpoint

## Executive Summary
Add a new endpoint `POST /api/v1/meetings/extract` that accepts raw meeting `text`, uses the LLM to extract structured fields (title, date, duration, participants, transcript), and persists a `Meeting` record. This complements the existing LLM-free `POST /api/v1/meetings/manual`, giving callers both options.

## Problem Understanding
The `manual` endpoint was intentionally made LLM-free (cheap insert). But there is still value in an LLM-assisted path that parses free-form notes into structured fields automatically. This restores the original LLM behavior as a *separate, opt-in* endpoint rather than forcing every manual insert through the LLM.

## Scope
### In Scope
- New `POST /api/v1/meetings/extract` endpoint (LLM extraction).
- `MeetingExtractRequest` schema (`text` only).
- `LLMMeetingService` with `ManualMeetingExtraction` model + `_parse_date` helper.
- New prompt template `prompts/manual_meeting.txt`.
- Unit + integration tests.
- Docs update (README + `docs/api-endpoints.md`).

### Out of Scope
- Modifying the existing `manual` endpoint (unchanged, LLM-free).
- Auto-analysis (separate `/analyze` endpoint remains for that).

## Assumptions
- LLM provider reachable at request time.
- `fireflies_id` stays non-null/unique → synthetic `manual-<uuid4>`.

## Constraints
- Reuse `BaseLLMProvider`, `PromptManager`, `MeetingRepository`.
- Tests use `pytest` + mocks + in-memory SQLite.
- Route declared before `/{meeting_id}` to avoid path capture.

## Proposed Approach
1. Schema `MeetingExtractRequest { text }`.
2. `LLMMeetingService.create_from_text(db, text)` → prompt → `llm.generate(schema=ManualMeetingExtraction.model_json_schema())` → validate → build `Meeting` (synthetic id) → persist.
3. Endpoint error mapping: `LLMError`/`ValidationError` → 422; other → 500.
4. Prompt `manual_meeting.txt` with `{text}` placeholder.
5. Tests + docs.

## Risks
| Risk | Mitigation |
|------|------------|
| LLM returns malformed JSON | `ValidationError` → 422 |
| LLM omits date/title | fallback to now / "Untitled Meeting" |
| Route conflict | declare `/extract` before `/{meeting_id}` |
