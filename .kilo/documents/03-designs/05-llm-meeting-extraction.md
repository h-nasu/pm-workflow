# Design: LLM-based Meeting Extraction Endpoint

## Technology Stack
- FastAPI, SQLAlchemy 2.0, Pydantic v2.
- `BaseLLMProvider` / `GeminiProvider`, `PromptManager`, `MeetingRepository`.
- `pytest` + mocks + in-memory SQLite.

## API Contract
- **Path:** `POST /api/v1/meetings/extract`
- **Request:** `MeetingExtractRequest { text: str }`
- **Response:** `MeetingResponse`

## Data Flow
```
Client → POST /meetings/extract {text}
  → meetings.py:extract_meeting (async)
    → GeminiProvider + PromptManager
    → LLMMeetingService.create_from_text(db, text)
       1. prompt = prompt_manager.load("manual_meeting").format(text=text)
       2. raw = await llm.generate(prompt, schema=ManualMeetingExtraction.model_json_schema())
       3. extracted = ManualMeetingExtraction.model_validate(raw)
       4. build Meeting(fireflies_id="manual-<uuid4>", ...)
    → meeting_repo.create(db, meeting)
  → MeetingResponse (200)
```

## Component Design
### `api/schemas/meeting.py`
- `MeetingExtractRequest(BaseModel)`: `text: str = Field(..., min_length=1)`.

### `services/meeting.py`
- `ManualMeetingExtraction(BaseModel)`: `title?`, `date?` (str), `duration_minutes?`, `participants: list[str]`, `transcript?`.
- `_parse_date(raw: str | None) -> datetime`: ISO parse (handle `Z`), tz→naive UTC; fallback now.
- `LLMMeetingService`:
  - `__init__(self, llm, prompt_manager)`
  - `async create_from_text(self, db, text) -> Meeting`

### `prompts/manual_meeting.txt`
- `{text}` placeholder; instructs JSON extraction.

### `api/v1/meetings.py`
- `POST /extract` (before `/{meeting_id}`), returns `MeetingResponse`; maps `LLMError`/`ValidationError` → 422, others → 500.

## Key Decisions
1. Separate endpoint from `manual` — both options coexist (LLM vs no-LLM).
2. Synthetic `manual-<uuid4>` id (no schema migration).
3. Reuse `MeetingResponse`.
4. Provider built in endpoint (consistent with `sync`/`analyze`).
