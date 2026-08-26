# Design Document: Analyzed Meeting Management & Summary Generation Refactor

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend                              │
│                                                                     │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐   │
│  │   API Layer     │    │           Service Layer              │   │
│  │                 │    │                                       │   │
│  │  GET /analysis/ │    │  AnalysisService (existing)           │   │
│  │  GET /analysis/ │    │  SummaryService (refactored)          │   │
│  │  /{id}          │    │    - generate_meeting_summary()      │   │
│  │                 │    │    - _build_summary_context()        │   │
│  │  GET /summaries │    │    - _call_llm_for_summary()         │   │
│  │  /meeting/{id}  │    │                                       │   │
│  │  POST /summaries│    └─────────────────────────────────────┘   │
│  │  /meeting/{id}/ │                      │                         │
│  │  generate       │                      ▼                         │
│  │                 │    ┌─────────────────────────────────────┐   │
│  │                 │    │        Repository Layer              │   │
│  │                 │    │                                       │   │
│  │                 │    │  AnalysisRepository                   │   │
│  │                 │    │    - list_by_date_range()            │   │
│  │                 │    │    - get_by_meeting_id()             │   │
│  │                 │    │                                       │   │
│  │                 │    │  SummaryRepository                    │   │
│  │                 │    │    - get_by_meeting_id()             │   │
│  │                 │    │    - create() / update()             │   │
│  │                 │    │                                       │   │
│  │                 │    │  MeetingRepository                    │   │
│  │                 │    │    - get()                            │   │
│  │                 │    │                                       │   │
│  │                 │    └─────────────────────────────────────┘   │
│  └─────────────────┘                      │                         │
│                                            ▼                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    SQLAlchemy ORM Models                     │   │
│  │                                                              │   │
│  │   Meeting ◄────┐  MeetingAnalysis ─┐  MeetingSummary         │   │
│  │                │                  │                         │   │
│  └────────────────┴──────────────────┴─────────────────────────┘   │
│                                            │                         │
└────────────────────────────────────────────┼─────────────────────────┘
                                             │
                                             ▼
                                     ┌─────────────┐
                                     │  PostgreSQL  │
                                     └─────────────┘
```

---

## Component Design

### 1. API Layer Changes

#### New Analyzed Meeting Endpoints
| Method | Path | Handler | Description |
|--------|------|---------|-------------|
| `GET` | `/api/v1/analysis/` | `list_analyzed_meetings()` | List analyzed meetings with optional date filter |
| `GET` | `/api/v1/analysis/{meeting_id}` | `get_analyzed_meeting()` | Get a single analyzed meeting by meeting UUID |

**Request Parameters for `GET /api/v1/analysis/`**:
- `start_date: date | None` — filter meetings analyzed on or after this date
- `end_date: date | None` — filter meetings analyzed on or before this date
- `limit: int = 100` — pagination limit
- `offset: int = 0` — pagination offset

**Response Schema**: `AnalysisResponse` (reused from existing schemas)

#### Refactored Summary Endpoints
| Method | Path | Handler | Description |
|--------|------|---------|-------------|
| `GET` | `/api/v1/summaries/meeting/{meeting_id}` | `get_meeting_summary()` | Get meeting summary by meeting UUID |
| `POST` | `/api/v1/summaries/meeting/{meeting_id}/generate` | `generate_meeting_summary()` | Generate meeting summary by meeting UUID |

**Deprecated Endpoints** (to be removed):
- `GET /api/v1/summaries/daily`
- `POST /api/v1/summaries/daily/generate`

**Response Schema**: `MeetingSummaryResponse` (new)

```python
class MeetingSummaryResponse(BaseModel):
    id: UUID
    meeting_id: UUID
    summary_text: str
    summary_json: dict
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

---

### 2. Data Model Changes

#### `MeetingSummary` Model (replaces `DailySummary`)

```python
class MeetingSummary(TimestampedModel):
    __tablename__ = "meeting_summaries"

    meeting_id: Mapped[UUID] = mapped_column(
        ForeignKey("meetings.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    summary_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    # Relationship back to Meeting
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="summary")
```

**Key differences from `DailySummary`**:
- `meeting_id` replaces `date` (FK, unique — enforces 1:1)
- Removed `meeting_count` (no longer needed; 1 summary = 1 meeting)
- Added SQLAlchemy `relationship` to `Meeting`
- Table name changes from `daily_summaries` to `meeting_summaries`

#### `Meeting` Model Update
Add a back-reference relationship:

```python
class Meeting(TimestampedModel):
    # ... existing fields ...
    summary: Mapped["MeetingSummary"] = relationship(back_populates="meeting")
```

---

### 3. Repository Layer Changes

#### `AnalysisRepository` Additions
```python
class AnalysisRepository(BaseRepository[MeetingAnalysis]):
    # ... existing methods ...

    def list_by_date_range(self, db: Session, start_date: datetime, end_date: datetime) -> list[MeetingAnalysis]:
        return (
            db.query(MeetingAnalysis)
            .join(Meeting, MeetingAnalysis.meeting_id == Meeting.id)
            .filter(Meeting.date >= start_date, Meeting.date <= end_date)
            .all()
        )
```

#### `SummaryRepository` Refactor
```python
class SummaryRepository(BaseRepository[MeetingSummary]):
    def __init__(self):
        super().__init__(MeetingSummary)

    def get_by_meeting_id(self, db: Session, meeting_id: UUID) -> MeetingSummary | None:
        return db.query(MeetingSummary).filter(SummaryRepository.model.meeting_id == meeting_id).first()
```

Remove `get_by_date()` method.

---

### 4. Service Layer Changes

#### `SummaryService` Refactor

**New method signature**:
```python
async def generate_meeting_summary(self, db: Session, meeting_id: UUID) -> MeetingSummary:
```

**Logic Flow**:
1. Load `Meeting` by `meeting_id`. If not found, raise `HTTPException(404)`.
2. Load existing `MeetingSummary` (if any) for idempotent updates.
3. Build LLM context:
   - If `MeetingAnalysis` exists for this meeting:
     - Extract structured fields (decisions, action_items, risks, etc.)
     - Combine with `meeting.transcript` into a rich context string
   - If `MeetingAnalysis` does NOT exist:
     - Use only `meeting.transcript` as context
   - If `meeting.transcript` is `None`:
     - Use only `MeetingAnalysis` content as context
     - If both are missing, raise `HTTPException(400)` with a descriptive error
4. Load the updated `summary.txt` prompt template.
5. Call `self.llm.generate(prompt)`.
6. Parse response into `summary_text` and `summary_json`.
7. If `MeetingSummary` exists: update fields.
8. If not: create new `MeetingSummary` record.
9. Return the `MeetingSummary`.

**Context Building Example**:
```
Transcript:
{meeting.transcript}

Analysis:
- Decisions: {decisions}
- Action Items: {action_items}
- Risks: {risks}
...
```

---

### 5. Prompt Update

**File**: `src/pm_workflow/prompts/summary.txt`

**Old behavior**: Receives `{date}` and `{meetings_context}` (list of meeting titles/dates for a day).

**New behavior**: Receives a single meeting's transcript and/or analysis content.

Example new prompt structure:
```
Generate a concise summary for the following meeting.

Transcript:
{transcript}

Analysis Results:
{analysis_content}

Summary:
```

---

## Data Flow

### Analyzed Meeting Retrieval
```
Client → GET /api/v1/analysis/?start_date=X&end_date=Y
       → FastAPI router
       → AnalysisRepository.list_by_date_range(db, start_date, end_date)
         └─ JOIN Meeting ON meeting_analyses.meeting_id = meetings.id
         └─ WHERE meetings.date BETWEEN start_date AND end_date
       → List[AnalysisResponse]
       → Client
```

### Single Analyzed Meeting Retrieval
```
Client → GET /api/v1/analysis/{meeting_id}
       → FastAPI router
       → AnalysisRepository.get_by_meeting_id(db, meeting_id)
       → AnalysisResponse | 404
       → Client
```

### Meeting Summary Generation (New Flow)
```
Client → POST /api/v1/summaries/meeting/{meeting_id}/generate
       → FastAPI router
       → SummaryService.generate_meeting_summary(db, meeting_id)
          1. Load Meeting
          2. Load MeetingAnalysis (optional)
          3. Build context (transcript + analysis OR transcript only)
          4. Load prompt template
          5. Call LLM
          6. Create/Update MeetingSummary
       → MeetingSummaryResponse
       → Client
```

---

## Technology Stack Decisions

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Web Framework** | FastAPI | Already in use; async support, auto-docs, type hints |
| **ORM** | SQLAlchemy 2.0 | Already in use; migrations via Alembic |
| **Database** | PostgreSQL 16 | Already in use; JSONB for structured analysis data |
| **LLM** | Google Gemini (via `BaseLLMProvider`) | Already abstracted; no changes needed |
| **Prompt Management** | `PromptManager` (file-based) | Already in use; easy to update templates |
| **Validation** | Pydantic v2 | Already in use for API schemas |
| **Testing** | pytest + unittest.mock | Already in use; in-memory SQLite for isolation |
| **Migrations** | Alembic | Already in use; required for schema changes |

No new external dependencies are required.

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Data loss from dropping `daily_summaries`** | Low | Medium | Project is early-stage; add a data migration step if production data exists |
| **LLM prompt regression** | Medium | Medium | Add tests with mocked LLM responses to verify prompt structure and parsing |
| **Missing transcript or analysis** | Medium | Medium | Service layer validates inputs and raises clear 400 errors when both sources are missing |
| **FK constraint violation on `meeting_id`** | Low | Low | Validate meeting exists before creating summary |
| **Breaking existing tests** | High | Medium | Update all tests that reference `DailySummary` or `/summaries/daily` endpoints |
| **Migration ordering** | Low | High | Ensure Alembic migration drops `daily_summaries` and creates `meeting_summaries` in a single version |

---

## File Impact Summary

| File | Action | Description |
|------|--------|-------------|
| `src/pm_workflow/models/summary.py` | **Modify** | Rename `DailySummary` to `MeetingSummary`, change columns |
| `src/pm_workflow/models/meeting.py` | **Modify** | Add back-reference relationship to `MeetingSummary` |
| `src/pm_workflow/repositories/summary.py` | **Modify** | Replace `get_by_date` with `get_by_meeting_id` |
| `src/pm_workflow/repositories/analysis.py` | **Modify** | Add `list_by_date_range` |
| `src/pm_workflow/services/summary.py` | **Refactor** | Rewrite `generate_meeting_summary` with new logic |
| `src/pm_workflow/api/schemas/summary.py` | **Modify** | Add `MeetingSummaryResponse`, remove `DailySummaryResponse` (or deprecate) |
| `src/pm_workflow/api/v1/summaries.py` | **Refactor** | Replace daily endpoints with meeting endpoints |
| `src/pm_workflow/api/v1/__init__.py` | **Modify** | Add new analysis router |
| `src/pm_workflow/prompts/summary.txt` | **Modify** | Update prompt for per-meeting context |
| `alembic/versions/*` | **Create** | Migration to drop `daily_summaries` and create `meeting_summaries` |
| `tests/unit/test_summaries_api.py` | **Modify** | Update to test new endpoints |
| `tests/unit/test_repositories.py` | **Modify** | Update summary repository tests |

---

## Non-Functional Considerations

- **Performance**: Summary generation remains bounded by LLM latency. No batch operations in MVP.
- **Reliability**: Service validates inputs before calling LLM. Fallback logic ensures summary can be generated even without analysis.
- **Maintainability**: Clear separation between context building, LLM calling, and persistence.
- **Extensibility**: New summary sources (e.g., video, audio) can be added to the context builder without changing the API contract.
