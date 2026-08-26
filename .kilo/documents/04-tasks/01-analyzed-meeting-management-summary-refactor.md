# Task Breakdown: Analyzed Meeting Management & Summary Generation Refactor

## Execution Order Overview

| Phase | Focus | Parallelizable |
|-------|-------|----------------|
| **Phase 1** | Database schema & model changes | No — must precede services |
| **Phase 2** | Repository & service layer refactor | Partially — analysis and summary repos are independent |
| **Phase 3** | API layer changes | Partially — analysis and summary endpoints are independent |
| **Phase 4** | Tests, migration, and verification | No — depends on all prior phases |

---

## Phase 1: Database Schema & Model Changes

### Task 1.1: Create `MeetingSummary` ORM Model

- **Owner Agent**: `backend`
- **Objective**: Define the new `MeetingSummary` model to replace the date-based `DailySummary` with a meeting-based 1:1 model.
- **Inputs / Prerequisites**: Existing `TimestampedModel` base, existing `Meeting` model
- **Files or Modules Likely Affected**:
  - `src/pm_workflow/models/summary.py`
  - `src/pm_workflow/models/meeting.py`
- **Acceptance Criteria**:
  1. `MeetingSummary` class is defined with `meeting_id` (FK to `meetings.id`, unique, indexed), `summary_text`, `summary_json`, plus inherited `id`, `created_at`, `updated_at`.
  2. `MeetingSummary.__tablename__` is `"meeting_summaries"`.
  3. `Meeting` model has a `summary: Mapped["MeetingSummary"]` relationship with `back_populates="meeting"`.
  4. `MeetingSummary` has a `meeting: Mapped["Meeting"]` relationship with `back_populates="summary"`.
  5. `DailySummary` class is removed from `summary.py` (or marked deprecated if migration requires keeping it temporarily).
- **Dependencies**: None
- **Test / Verification Notes**:
  - Run `pytest tests/unit/test_models.py -k summary` and confirm no import errors.
  - Verify SQLAlchemy can reflect the new schema in an in-memory SQLite database.

---

### Task 1.2: Create Alembic Migration

- **Owner Agent**: `backend`
- **Objective**: Create an Alembic migration that drops the `daily_summaries` table and creates `meeting_summaries`.
- **Inputs / Prerequisites**: Task 1.1 complete; Alembic configured and functional
- **Files or Modules Likely Affected**:
  - `alembic/versions/*_refactor_summary_to_meeting_based.py`
- **Acceptance Criteria**:
  1. Migration `upgrade()` creates `meeting_summaries` table with columns: `id`, `meeting_id`, `summary_text`, `summary_json`, `created_at`, `updated_at`.
  2. Migration `downgrade()` drops `meeting_summaries` and recreates `daily_summaries` (for reversibility).
  3. `meeting_id` column has `ForeignKey("meetings.id", ondelete="CASCADE")`, `unique=True`, and an index.
  4. Migration runs successfully against a test database: `alembic upgrade head`.
  5. Migration is reversible: `alembic downgrade -1` works without error.
- **Dependencies**: Task 1.1
- **Test / Verification Notes**:
  - Run `alembic upgrade head` and `alembic downgrade -1` in a temporary environment.
  - Verify no data loss concerns (document assumption that `daily_summaries` has no production data).

---

## Phase 2: Repository & Service Layer Refactor

### Task 2.1: Update `AnalysisRepository` with Date-Range Query

- **Owner Agent**: `backend`
- **Objective**: Add a method to list `MeetingAnalysis` records filtered by the parent meeting's date range.
- **Inputs / Prerequisites**: Task 1.1 complete (model relationships available)
- **Files or Modules Likely Affected**:
  - `src/pm_workflow/repositories/analysis.py`
- **Acceptance Criteria**:
  1. New method `list_by_date_range(db, start_date: datetime, end_date: datetime) -> list[MeetingAnalysis]` is added.
  2. The method joins `MeetingAnalysis` with `Meeting` and filters on `Meeting.date`.
  3. Existing `get_by_meeting_id` method remains unchanged and functional.
- **Dependencies**: Task 1.1
- **Test / Verification Notes**:
  - Add unit test in `tests/unit/test_repositories.py` that creates a meeting and analysis, then verifies `list_by_date_range` returns the correct record.

---

### Task 2.2: Refactor `SummaryRepository`

- **Owner Agent**: `backend`
- **Objective**: Replace date-based lookup with meeting-based lookup in the summary repository.
- **Inputs / Prerequisites**: Task 1.1 complete
- **Files or Modules Likely Affected**:
  - `src/pm_workflow/repositories/summary.py`
- **Acceptance Criteria**:
  1. `SummaryRepository` now operates on `MeetingSummary` instead of `DailySummary`.
  2. `get_by_date` is removed.
  3. New method `get_by_meeting_id(db, meeting_id: UUID) -> MeetingSummary | None` is added.
  4. Generic CRUD methods (`get_all`, `create`, `update`, `delete`) inherited from `BaseRepository` continue to work with `MeetingSummary`.
- **Dependencies**: Task 1.1
- **Test / Verification Notes**:
  - Add unit tests for `get_by_meeting_id` (create, query, verify None for missing meeting_id).
  - Update existing tests in `test_repositories.py` to use `MeetingSummary` instead of `DailySummary`.

---

### Task 2.3: Refactor `SummaryService` — Multi-Source Context & Fallback

- **Owner Agent**: `backend`
- **Objective**: Rewrite summary generation to use meeting_id, build context from transcript + analysis, and implement fallback logic.
- **Inputs / Prerequisites**: Task 2.2 complete
- **Files or Modules Likely Affected**:
  - `src/pm_workflow/services/summary.py`
- **Acceptance Criteria**:
  1. New method `generate_meeting_summary(db, meeting_id: UUID) -> MeetingSummary` is implemented.
  2. Method loads the `Meeting` by `meeting_id`. If missing, raises `ValueError` (or appropriate exception).
  3. Method loads existing `MeetingSummary` for idempotent updates.
  4. **Context building logic**:
     - If `MeetingAnalysis` exists: builds context from `meeting.transcript` + structured analysis fields (decisions, action_items, risks, dependencies, missing_information, client_requests, requirements, open_questions, project_status, suggested_next_actions).
     - If `MeetingAnalysis` does NOT exist: builds context from `meeting.transcript` only.
     - If `meeting.transcript` is `None` and `MeetingAnalysis` exists: builds context from analysis only.
     - If both are missing: raises `ValueError("Cannot generate summary: meeting has no transcript and no analysis")`.
  5. LLM prompt is loaded via `PromptManager` and formatted with the built context.
  6. LLM response is parsed into `summary_text` and `summary_json`.
  7. Existing `MeetingSummary` is updated if found; otherwise a new record is created.
  8. Old `generate_daily_summary` method is removed (or kept as deprecated if needed for backward compat — recommended to remove).
- **Dependencies**: Task 2.2
- **Test / Verification Notes**:
  - Mock `Meeting`, `MeetingAnalysis`, `LLMProvider`, and `PromptManager`.
  - Test case 1: meeting has transcript + analysis → summary generated with both sources.
  - Test case 2: meeting has transcript only → summary generated with transcript only.
  - Test case 3: meeting has analysis only (transcript is None) → summary generated with analysis only.
  - Test case 4: meeting has neither → exception raised.
  - Test case 5: existing `MeetingSummary` is updated, not duplicated.

---

### Task 2.4: Update Summary Prompt Template

- **Owner Agent**: `backend`
- **Objective**: Update the LLM prompt to expect per-meeting context instead of a date-based meeting list.
- **Inputs / Prerequisites**: Task 2.3 complete (knows what context is passed)
- **Files or Modules Likely Affected**:
  - `src/pm_workflow/prompts/summary.txt`
- **Acceptance Criteria**:
  1. Prompt no longer references `{date}` or `{meetings_context}` (date + list of meetings).
  2. Prompt accepts placeholders for a single meeting's transcript and analysis content.
  3. Prompt instructs the LLM to produce a concise, structured summary for one meeting.
  4. Prompt remains a plain-text file loadable by `PromptManager`.
- **Dependencies**: Task 2.3
- **Test / Verification Notes**:
  - Load the prompt in a test and verify `format()` works with the new placeholders.
  - Verify the rendered prompt is under the LLM token limit for typical meeting sizes.

---

## Phase 3: API Layer Changes

### Task 3.1: Add Analyzed Meeting API Endpoints

- **Owner Agent**: `backend`
- **Objective**: Expose endpoints to list and retrieve analyzed meeting records.
- **Inputs / Prerequisites**: Task 2.1 complete
- **Files or Modules Likely Affected**:
  - `src/pm_workflow/api/v1/analysis.py` (new file)
  - `src/pm_workflow/api/v1/__init__.py`
- **Acceptance Criteria**:
  1. New file `analysis.py` is created with an `APIRouter`.
  2. `GET /api/v1/analysis/` returns a paginated list of `AnalysisResponse` schemas.
     - Accepts optional `start_date` and `end_date` query parameters.
     - Defaults to `limit=100`, `offset=0`.
  3. `GET /api/v1/analysis/{meeting_id}` returns a single `AnalysisResponse`.
     - Returns `404` if the meeting or analysis does not exist.
  4. Router is included in `api_router` with prefix `/analysis` and tag `["analysis"]`.
  5. Error handling follows existing patterns (`HTTPException` with appropriate status codes).
- **Dependencies**: Task 2.1
- **Test / Verification Notes**:
  - Test list endpoint with no filters, with date filters, with pagination.
  - Test get by ID for existing and non-existing meeting IDs.
  - Use FastAPI `TestClient` with mocked DB session.

---

### Task 3.2: Refactor Summary API Endpoints

- **Owner Agent**: `backend`
- **Objective**: Replace date-based summary endpoints with meeting-based endpoints.
- **Inputs / Prerequisites**: Task 2.3 complete
- **Files or Modules Likely Affected**:
  - `src/pm_workflow/api/v1/summaries.py`
  - `src/pm_workflow/api/schemas/summary.py`
- **Acceptance Criteria**:
  1. `DailySummaryResponse` is removed or marked deprecated.
  2. `MeetingSummaryResponse` schema is added to `summary.py`.
  3. `GET /api/v1/summaries/meeting/{meeting_id}` returns a `MeetingSummaryResponse` or `404`.
  4. `POST /api/v1/summaries/meeting/{meeting_id}/generate` calls `SummaryService.generate_meeting_summary` and returns the generated summary.
  5. Old `/summaries/daily` and `/summaries/daily/generate` routes are removed.
  6. Error handling wraps service exceptions in `HTTPException(500)`.
- **Dependencies**: Task 2.3
- **Test / Verification Notes**:
  - Test get endpoint for existing and non-existing summaries.
  - Test generate endpoint: verifies LLM is called, summary is created, and response matches schema.
  - Test that old daily endpoints return `404`.

---

### Task 3.3: Update API Router & Documentation

- **Owner Agent**: `backend`
- **Objective**: Ensure all new routes are registered and FastAPI auto-docs reflect the changes.
- **Inputs / Prerequisites**: Tasks 3.1 and 3.2 complete
- **Files or Modules Likely Affected**:
  - `src/pm_workflow/api/v1/__init__.py`
- **Acceptance Criteria**:
  1. `analysis_router` is included in `api_router` with prefix `/analysis` and tags `["analysis"]`.
  2. `summaries_router` continues to work with updated routes.
  3. Running `uvicorn pm_workflow.main:app --reload` and visiting `/docs` shows the new endpoints with correct request/response schemas.
- **Dependencies**: Task 3.1, Task 3.2
- **Test / Verification Notes**:
  - Start the app locally and verify `/docs` renders the new endpoints.
  - Run `pytest` to confirm no import or routing errors.

---

## Phase 4: Tests & Verification

### Task 4.1: Update Unit Tests for Repositories

- **Owner Agent**: `qa`
- **Objective**: Update existing repository tests and add new tests for the refactored data access layer.
- **Inputs / Prerequisites**: Tasks 2.1, 2.2 complete
- **Files or Modules Likely Affected**:
  - `tests/unit/test_repositories.py`
- **Acceptance Criteria**:
  1. All existing `DailySummary` references are replaced with `MeetingSummary`.
  2. New tests for `AnalysisRepository.list_by_date_range` are added.
  3. New tests for `SummaryRepository.get_by_meeting_id` are added.
  4. All tests pass: `pytest tests/unit/test_repositories.py`.
- **Dependencies**: Task 2.1, Task 2.2
- **Test / Verification Notes**:
  - Use in-memory SQLite fixture from `conftest.py`.
  - Verify 100% coverage of changed repository methods.

---

### Task 4.2: Update Unit Tests for SummaryService

- **Owner Agent**: `qa`
- **Objective**: Add comprehensive unit tests for the refactored `SummaryService`.
- **Inputs / Prerequisites**: Task 2.3 complete
- **Files or Modules Likely Affected**:
  - `tests/unit/test_services.py` (or create if missing)
- **Acceptance Criteria**:
  1. Tests cover all four context-building scenarios: transcript+analysis, transcript-only, analysis-only, neither (error).
  2. Tests verify LLM prompt is formatted correctly with the built context.
  3. Tests verify idempotent behavior (existing summary is updated, not duplicated).
  4. Tests verify `HTTPException` propagation from API layer.
  5. All tests pass: `pytest tests/unit/ -k summary`.
- **Dependencies**: Task 2.3
- **Test / Verification Notes**:
  - Use `unittest.mock.AsyncMock` for the LLM provider.
  - Use `MagicMock` for `PromptManager`.
  - Assert `summary_repo.create` or `summary_repo.update` is called with expected arguments.

---

### Task 4.3: Update Integration Tests for API Endpoints

- **Owner Agent**: `qa`
- **Objective**: Update API integration tests to cover the new analyzed meeting and meeting summary endpoints.
- **Inputs / Prerequisites**: Tasks 3.1, 3.2 complete
- **Files or Modules Likely Affected**:
  - `tests/integration/test_api.py`
  - `tests/unit/test_summaries_api.py`
- **Acceptance Criteria**:
  1. Integration tests for `GET /api/v1/analysis/` and `GET /api/v1/analysis/{meeting_id}` are added.
  2. Integration tests for `GET /api/v1/summaries/meeting/{meeting_id}` and `POST /api/v1/summaries/meeting/{meeting_id}/generate` are added.
  3. Old daily summary integration tests are removed or updated.
  4. All tests pass: `pytest tests/`.
- **Dependencies**: Task 3.1, Task 3.2
- **Test / Verification Notes**:
  - Use FastAPI `TestClient` with a test database fixture.
  - Seed test data (meetings, analyses) before running endpoint tests.

---

### Task 4.4: Run Alembic Migration & Full Test Suite

- **Owner Agent**: `backend`
- **Objective**: Apply the migration and verify the entire test suite passes against the new schema.
- **Inputs / Prerequisites**: Tasks 1.2, 4.1, 4.2, 4.3 complete
- **Files or Modules Likely Affected**:
  - `alembic/versions/*_refactor_summary_to_meeting_based.py`
- **Acceptance Criteria**:
  1. `alembic upgrade head` succeeds without errors.
  2. `alembic downgrade -1` succeeds without errors.
  3. Full test suite passes: `pytest tests/`.
  4. No linting errors: `ruff check src/ tests/`.
  5. No type errors: `mypy src/`.
- **Dependencies**: All prior tasks
- **Test / Verification Notes**:
  - Run tests in a clean virtual environment to catch missing imports or dependency issues.
  - Verify `pm_workflow.db` (SQLite) can be created and migrated if used locally.

---

## Dependency Graph

```
Task 1.1 ─────────────────┐
                          ├──► Task 2.1 ──► Task 3.1 ──► Task 4.3 ──┐
Task 1.1 ─────────────────┘                                         │
                          ├──► Task 2.2 ──► Task 2.3 ──► Task 3.2 ──┤
Task 1.2 ─────────────────┘                      │                 │
                                                  ├──► Task 4.2 ──┤
Task 2.3 ────────────────────────────────────────┤                 │
                                                  ├──► Task 4.1 ──┤
Task 3.1 ────────────────────────────────────────┤                 │
                                                  ├──► Task 4.3 ──┘
Task 3.2 ────────────────────────────────────────┘
                          │
Task 2.3 ─────────────────┘
                          │
Task 2.4 ─────────────────┘
                          │
All above ─────────────────┴──► Task 4.4
```

---

## Parallelization Opportunities

- **Phase 2**: Task 2.1 (AnalysisRepository) and Task 2.2 (SummaryRepository) can be worked on in parallel after Task 1.1.
- **Phase 3**: Task 3.1 (Analysis endpoints) and Task 3.2 (Summary endpoints) can be worked on in parallel after their respective service tasks complete.
- **Phase 4**: Task 4.1, 4.2, and 4.3 can be started as soon as their respective implementation tasks finish, in parallel.

---

## Estimated Effort

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1 | 1.1, 1.2 | 2–3 hours |
| Phase 2 | 2.1, 2.2, 2.3, 2.4 | 4–6 hours |
| Phase 3 | 3.1, 3.2, 3.3 | 3–4 hours |
| Phase 4 | 4.1, 4.2, 4.3, 4.4 | 3–4 hours |
| **Total** | | **12–17 hours** |

---

## Suggested Agent Assignments

| Task ID | Title | Owner Agent |
|---------|-------|-------------|
| 1.1 | Create `MeetingSummary` ORM Model | `backend` |
| 1.2 | Create Alembic Migration | `backend` |
| 2.1 | Update `AnalysisRepository` | `backend` |
| 2.2 | Refactor `SummaryRepository` | `backend` |
| 2.3 | Refactor `SummaryService` | `backend` |
| 2.4 | Update Summary Prompt Template | `backend` |
| 3.1 | Add Analyzed Meeting API Endpoints | `backend` |
| 3.2 | Refactor Summary API Endpoints | `backend` |
| 3.3 | Update API Router & Documentation | `backend` |
| 4.1 | Update Unit Tests for Repositories | `qa` |
| 4.2 | Update Unit Tests for SummaryService | `qa` |
| 4.3 | Update Integration Tests for API Endpoints | `qa` |
| 4.4 | Run Migration & Full Test Suite | `backend` + `qa` |
