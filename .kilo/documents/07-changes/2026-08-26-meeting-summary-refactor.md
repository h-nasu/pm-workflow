# Change Record: Analyzed Meeting Management & Summary Generation Refactor

## Git Commit Message
Refactor summary to meeting-based and add analysis endpoints

## Change Description
Major refactoring of the summary system and addition of analyzed meeting management endpoints:

### 1. Database Schema Changes
- Replaced `DailySummary` model with `MeetingSummary` model
- Added `meeting_id` foreign key (unique, indexed) to `MeetingSummary`
- Removed `date` and `meeting_count` columns from summary table
- Added bidirectional `Meeting ↔ MeetingSummary` relationship
- Created Alembic migration `a1b2c3d4e5f6_refactor_summary_to_meeting_based.py`

### 2. Repository Layer Updates
- Added `AnalysisRepository.list_by_date_range()` with join through `Meeting.date`
- Refactored `SummaryRepository` to use `get_by_meeting_id()` on `MeetingSummary`
- Updated repository interfaces to work with meeting-based summaries

### 3. Service Layer Refactoring
- Rewrote `SummaryService.generate_meeting_summary()` with multi-source context:
  - Transcript + Analysis (preferred)
  - Transcript-only fallback
  - Analysis-only fallback
  - Raises `ValueError` when neither exists
- Updated `prompts/summary.txt` to use per-meeting placeholders instead of date-based meeting lists

### 4. API Layer Changes
- Added `GET /api/v1/analysis/` with optional date-range filtering
- Added `GET /api/v1/analysis/{meeting_id}`
- Replaced daily summary routes with:
  - `GET /api/v1/summaries/meeting/{meeting_id}`
  - `POST /api/v1/summaries/meeting/{meeting_id}/generate`
- Consolidated router registration in `src/pm_workflow/api/v1/router.py`

### 5. Testing Updates
- Added `tests/unit/test_services.py` with 6 tests covering all context-building scenarios
- Updated `tests/unit/test_repositories.py` for `MeetingSummary` and new methods
- Updated `tests/unit/test_summaries_api.py` for new endpoints
- Updated `tests/integration/test_api.py` to run against PostgreSQL
- All 25 tests pass

### 6. Documentation
- Updated `README.md` with current endpoints and setup instructions
- Consolidated API documentation into single source of truth

### 7. Router Consolidation
- Made `router.py` the single source of truth for API router configuration
- Updated `__init__.py` to simply re-export `api_router`
- Removed dual-definition pattern that caused confusion

## Reason for Change
- Original `DailySummary` model was date-based aggregation, not suitable for per-meeting summaries
- Need to generate summaries for individual meetings, not daily aggregates
- Analysis endpoints were missing from API
- Router structure had redundant definitions causing maintenance issues

## Impact Analysis
- **Breaking Change**: `DailySummary` model and related endpoints removed
- **Database**: Requires running Alembic migration to update schema
- **API**: New endpoints added; old daily summary endpoints removed
- **Tests**: All existing tests updated; 25 tests passing
- **Documentation**: README and docs/ updated to reflect changes

## Follow-up Actions
- [ ] Commit changes to git
- [ ] Run Alembic migration on production database
- [ ] Verify Swagger UI displays new endpoints after server restart
- [ ] Consider adding pagination to analysis list endpoint
- [ ] Add rate limiting to summary generation endpoint
