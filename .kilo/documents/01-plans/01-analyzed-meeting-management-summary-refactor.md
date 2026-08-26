# Implementation Plan: Analyzed Meeting Management & Summary Generation Refactor

## Executive Summary

This plan covers two interconnected features for the pm-workflow project:
1. **Analyzed Meeting Management** — expose CRUD-style endpoints to retrieve and filter analyzed meeting records (`MeetingAnalysis`).
2. **Summary Generation Refactor** — transition the summary model from date-based aggregation (`DailySummary`) to a one-to-one per-meeting model (`MeetingSummary`), with multi-source data inputs (transcription + analysis) and a fallback mechanism.

Both features touch the API layer, data models, repositories, services, and database schema. An architecture review is required before implementation.

---

## Problem Understanding

### Feature 1: Analyzed Meeting Management
The `MeetingAnalysis` table already exists with a 1:1 relationship to `Meeting`, but there are **no public API endpoints** to:
- List all analyzed meetings
- Filter analyzed meetings by the date of their parent meeting
- Retrieve a single analyzed meeting record by its `meeting_id`

### Feature 2: Summary Generation Refactor
The current `DailySummary` model is date-based (`target_date` → multiple meetings aggregated into one summary). The memo indicates the desired state is:
- **One summary per meeting** (1:1 relationship with `meeting_id`)
- **Multi-source input**: summary generation should consume both the meeting transcript and the structured analysis output (`MeetingAnalysis`)
- **Fallback**: if `MeetingAnalysis` does not exist for a meeting, generate the summary using only the transcript

This requires a data model change, service logic rewrite, prompt update, and API contract changes.

---

## Scope

### In Scope
- New API endpoints for analyzed meeting retrieval
- Database schema migration from `daily_summaries` (date-based) to `meeting_summaries` (meeting_id-based)
- Updated `SummaryService` with multi-source context building and fallback logic
- Updated LLM prompt for per-meeting summary generation
- Alembic migration for schema changes
- Unit and integration tests for new endpoints and service logic

### Out of Scope (Future)
- Webhook-based summary generation (manual trigger only for MVP)
- Summary caching or invalidation strategies
- Batch summary generation for all meetings
- Historical data migration from `daily_summaries` to `meeting_summaries`
- UI layer (API-only MVP)

---

## Assumptions

1. **Data Volume**: The project is in early MVP stage; there is no significant production data in `daily_summaries` that must be preserved.
2. **Meeting Uniqueness**: Each `Meeting` row is unique by `id` and has at most one `MeetingAnalysis`. This is already enforced by the DB schema and repository logic.
3. **LLM Availability**: The LLM provider remains accessible and the prompt can be updated without changing provider APIs.
4. **API Consumers**: Since this is an internal MVP, breaking changes to summary endpoints are acceptable.
5. **Transcription Availability**: `Meeting.transcript` may be `NULL`; the fallback logic must handle this gracefully.

---

## Constraints

1. **Framework**: FastAPI + SQLAlchemy 2.0 + Alembic (must follow existing patterns)
2. **Database**: PostgreSQL (must use Alembic for migrations)
3. **LLM Abstraction**: Must use the existing `BaseLLMProvider` and `PromptManager` (no direct API calls in services)
4. **Testing**: Must use `pytest` + `unittest.mock` + in-memory SQLite (existing test pattern)
5. **Naming**: Follow existing naming conventions (`PascalCase` for models, `snake_case` for tables, `*_repo` for repositories)
6. **No Client-Facing Docs**: This is backend-only; no `docs/` updates needed unless explicitly requested.

---

## Proposed Approach

### Feature 1: Analyzed Meeting Management
1. Add repository methods to `AnalysisRepository` for listing and date-filtering analyzed meetings by joining with `Meeting.date`.
2. Add new API routes under `/api/v1/analysis/`:
   - `GET /api/v1/analysis/` — list analyzed meetings (optional `start_date` / `end_date` filters)
   - `GET /api/v1/analysis/{meeting_id}` — get a single analyzed meeting by meeting UUID
3. Add Pydantic schemas if needed (reuse `AnalysisResponse`).

### Feature 2: Summary Generation Refactor
1. **Model**: Rename `DailySummary` to `MeetingSummary` (or keep the class name but redefine its columns). Replace `date` with `meeting_id` (FK, unique). Remove `meeting_count`.
2. **Migration**: Drop the old `daily_summaries` table (or rename it) and create `meeting_summaries`.
3. **Repository**: Update `SummaryRepository` to use `meeting_id` instead of `date`.
4. **Service**: Rewrite `SummaryService.generate_meeting_summary(db, meeting_id)`:
   - Load the `Meeting`
   - Check if `MeetingAnalysis` exists
   - Build LLM context from transcript + analysis (or transcript only)
   - Call LLM with updated prompt
   - Create or update `MeetingSummary`
5. **Prompt**: Update `summary.txt` to expect per-meeting context instead of a list of meetings for a date.
6. **API**: Replace `/api/v1/summaries/daily` endpoints with:
   - `GET /api/v1/summaries/meeting/{meeting_id}` — get meeting summary
   - `POST /api/v1/summaries/meeting/{meeting_id}/generate` — generate meeting summary

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Existing `daily_summaries` data loss | Low | Medium | Project is early-stage; no production data. If data exists, add a data migration step. |
| LLM prompt behavior change | Medium | Medium | Write tests with mocked LLM responses to verify prompt structure. |
| Breaking API consumers | Low | Low | MVP is API-only and internal; no external consumers. |
| `Meeting.transcript` is NULL | Medium | Medium | Fallback logic must handle `None` transcript and produce a meaningful fallback summary. |
| `meeting_id` FK constraint violation | Low | Medium | Validate `meeting_id` exists before creating summary. |

---

## Open Questions

1. **Data Migration**: Should existing `daily_summaries` rows be migrated to `meeting_summaries`, or should the old table be dropped? Given the model change from 1:N to 1:1, migration is non-trivial. Recommendation: drop the old table for MVP.
2. **Endpoint Path**: Should analyzed meeting endpoints live under `/api/v1/analysis/` or `/api/v1/meetings/analysis/`? Recommendation: `/api/v1/analysis/` for clarity and separation of concerns.
3. **Pagination**: Should the analyzed meetings list endpoint support pagination? Recommendation: add `limit`/`offset` now (existing pattern in `list_meetings`).
4. **Summary Response Schema**: Should `MeetingSummaryResponse` include the `meeting_id` and `summary_json`? Recommendation: yes, for completeness and debugging.

---

## Decision: Architecture Work Required

**Yes.** This request involves:
- New API contracts (analyzed meeting endpoints, new summary endpoints)
- Data model changes (`DailySummary` → `MeetingSummary`)
- New database migration
- Service logic rewrite with new data flow (transcript + analysis → summary)
- Cross-cutting changes across API, service, repository, model, and prompt layers

A design document must be created before tasks are finalized.

---

## Next Steps

1. Create design document in `03-designs/`
2. Create implementation-ready tasks in `04-tasks/`
3. Assign tasks to specialist agents
4. Sequence by dependency
5. Present for review before execution
