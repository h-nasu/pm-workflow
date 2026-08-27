# Change Log: LLM-based Meeting Extraction Endpoint

## Change: Add `POST /api/v1/meetings/extract` (LLM-assisted creation)
- **When**: After the `manual` endpoint was made LLM-free (and the field renames / Swagger example improvements).
- **Why**: Provide both creation options — cheap LLM-free `manual` (store transcript directly) and LLM-assisted `extract` (parse free-form text into structured fields). The original LLM behavior is restored as a separate, opt-in endpoint rather than forced on every insert.
- **What changed**:
  - `MeetingExtractRequest` schema (`text`).
  - Re-added `prompts/manual_meeting.txt`.
  - `LLMMeetingService` (with `ManualMeetingExtraction`, `_parse_date`) in `services/meeting.py`.
  - `POST /extract` endpoint in `api/v1/meetings.py` (declared before `/{meeting_id}`).
  - Unit + integration tests; README + `docs/api-endpoints.md` updated.
- **Behavior**: `extract` uses the LLM to fill title/date/duration/participants/transcript (with safe fallbacks); `manual` is unchanged. Both use synthetic `manual-<uuid4>` ids. Error mapping: `LLMError`/`ValidationError` → 422, others → 500.
