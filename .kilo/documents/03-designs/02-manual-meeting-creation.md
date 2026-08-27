# Design: Manual Meeting Creation API (LLM-free)

## Technology Stack
- FastAPI, SQLAlchemy 2.0, Pydantic v2, `MeetingRepository` (existing).
- No LLM provider / PromptManager dependency in the create path.
- `pytest` + in-memory SQLite for tests (existing stack).

## API Contract
- **Path:** `POST /api/v1/meetings/manual`
- **Request schema:** `ManualMeetingCreate { text, title?, date?, duration_minutes?, participants? }`
- **Response schema:** `MeetingResponse` (existing)
- **Errors:** `200`, `422`

## Data Flow
```
Client
  │  POST /api/v1/meetings/manual  { text, optional metadata }
  ▼
meetings.py:create_manual_meeting (sync)
  │  service = ManualMeetingService()
  ▼
ManualMeetingService.create_from_payload(db, payload)
  │  1. title = payload.title or _derive_title(payload.text)
  │  2. date  = _normalize_date(payload.date)   # now() UTC if None, tz→naive UTC
  │  3. participants = payload.participants or {}
  │  4. transcript = payload.text
  │  5. Meeting(fireflies_id="manual-<uuid4>", ...)
  ▼
meeting_repo.create(db, meeting)
  ▼
MeetingResponse (200)
```

## Component Design

### `api/schemas/meeting.py`
`ManualMeetingCreate(BaseModel)`: `text: str` (min_length=1), `title: str | None`, `date: datetime | None`, `duration_minutes: int | None`, `participants: dict[str, Any]` (default `{}`).

### `services/meeting.py`
- `_derive_title(text)`: first non-empty line (≤200 chars), else `"Untitled Meeting"`.
- `_normalize_date(value)`: `None` → naive now(UTC); tz-aware → converted to naive UTC; naive → unchanged.
- `ManualMeetingService.create_from_payload(db, payload) -> Meeting`: builds and persists the `Meeting` with `fireflies_id="manual-<uuid4>"`. No LLM.

### `api/v1/meetings.py`
- `POST /manual` (declared before `/{meeting_id}`). Sync handler, no `GeminiProvider`/`PromptManager` import for this route. Returns `MeetingResponse`.

## Key Decisions
1. **No LLM on create** — cost/latency/key-dependency removed; matches `sync` (create) vs `analyze` (understand) separation.
2. **`text` is the transcript** — raw notes preserved exactly.
3. **Synthetic `fireflies_id`** — preserves non-null unique constraint without migration.
4. **Naive-UTC dates** — consistent with the `Meeting.date` column (no timezone) and the rest of the app (e.g. `sync.py`).
