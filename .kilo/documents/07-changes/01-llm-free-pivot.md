# Change Log: Manual Meeting Creation API

## Change 1: LLM-free create path (pivot from initial design)

- **When**: After initial implementation (LLM-extraction based) was completed.
- **Why**: The user correctly noted that running an LLM on every manual insert is expensive and unnecessary. The system's value (meeting understanding) is already delivered by the separate `POST /meetings/{id}/analyze` endpoint, and the `sync` endpoint already separates creation from analysis. A simple text insert should be cheap and dependency-free.
- **What changed**:
  - Removed `ManualMeetingExtraction`, `_parse_date`, and the LLM/`PromptManager` dependency from `services/meeting.py`.
  - Deleted `prompts/manual_meeting.txt` (no longer referenced).
  - `ManualMeetingService.create_from_text(db, text)` → `create_from_payload(db, payload)`.
  - `ManualMeetingCreate` now carries optional `title`, `date`, `duration_minutes`, `participants` in addition to required `text`.
  - Endpoint `create_manual_meeting` is now a sync handler with no `GeminiProvider`/`PromptManager`.
  - Title derives from first non-empty line of `text` (≤200 chars) when omitted; date defaults to now (naive UTC); participants default to `{}`; transcript = raw `text`.
  - Updated unit/integration tests (removed LLM mocks) and docs (README + `docs/api-endpoints.md`).
- **Impact**: Creation no longer requires `GEMINI_API_KEY`, has no latency/cost, and cannot fail due to LLM/validation errors. Structured understanding remains available via `/analyze`.
