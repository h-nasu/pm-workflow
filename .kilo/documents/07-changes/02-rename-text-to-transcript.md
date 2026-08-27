# Change Log: Rename `text` → `transcript`

## Change: Request field rename for manual meeting creation
- **When**: After the LLM-free manual meeting endpoint was implemented.
- **Why**: Make the API contract self-describing. The caller submits a `transcript` (meeting notes) that is stored directly in `Meeting.transcript`; the previous `text` field with an implicit "stored as transcript" mapping was less clear.
- **What changed**:
  - `ManualMeetingCreate.text` → `transcript` (required, non-empty) in `api/schemas/meeting.py`.
  - `services/meeting.py`: `_derive_title` param renamed to `transcript`; `create_from_payload` reads `payload.transcript` for both title derivation and `Meeting.transcript`.
  - `api/v1/meetings.py`: endpoint summary wording updated to "Create a meeting from provided transcript".
  - Tests updated to the new field name (`tests/unit/test_meeting_service.py`, `tests/integration/test_api.py`).
  - Docs updated (`README.md`, `docs/api-endpoints.md`).
- **Behavior preserved**: `POST /api/v1/meetings/manual` still creates a `Meeting` from the provided notes, stored as `transcript`; title derivation, date default, participants default, and `422` on empty input are unchanged.
- **Impact**: This is an intentional request-contract change; callers must send `transcript` instead of `text`.
