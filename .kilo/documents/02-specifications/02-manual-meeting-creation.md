# Specification: Manual Meeting Creation API (LLM-free)

## Functional Requirements

### FR-1: Create meeting from text (cheap insert, no LLM)
- `POST /api/v1/meetings/manual` creates a `Meeting` record directly from the request payload.
- No LLM call is performed during creation; structured understanding is deferred to the existing `POST /api/v1/meetings/{id}/analyze` endpoint.
- Mirrors the existing `POST /meetings/sync` pattern: creation and analysis are separate steps.

### FR-2: Request shape
- `text` (required, non-empty string): stored verbatim as the meeting `transcript`.
- `title` (optional string): if provided, used as the meeting title.
- `date` (optional ISO 8601 datetime): if provided, used as the meeting date.
- `duration_minutes` (optional int): if provided, stored.
- `participants` (optional object): if provided, stored as-is.

### FR-3: Field defaults & fallbacks
- `title` omitted → derived from the first non-empty line of `text` (capped at 200 chars); if `text` is blank → `"Untitled Meeting"`.
- `date` omitted → current UTC time (stored naive, normalized to UTC).
- `participants` omitted → empty object `{}`.
- `transcript` → always the raw `text`.

### FR-4: Synthetic identifier
- `fireflies_id = "manual-<uuid4>"` (satisfies non-null unique constraint, no migration).

### FR-5: Response & errors
- Success → `200 OK` with `MeetingResponse`.
- `text` missing/empty → `422 Unprocessable Entity`.

## Non-Functional Requirements
- **Cost**: creation must not depend on an external LLM/API key; it is a fast, free DB insert.
- **Architecture**: reuse `MeetingRepository`, existing schemas, and the `Meeting` model; no new external dependencies.
- **Consistency**: separate create vs. analyze, matching `sync`/`analyze` endpoints.

## API Contract
### Request
```json
{
  "text": "Kickoff with Alice and Bob",
  "title": "Project Kickoff",
  "duration_minutes": 45,
  "participants": { "Alice": true, "Bob": true }
}
```
### Response `200 OK`
```json
{
  "id": "uuid",
  "fireflies_id": "manual-<uuid>",
  "title": "Project Kickoff",
  "date": "2026-08-27T...",
  "duration_minutes": 45,
  "participants": { "Alice": true, "Bob": true },
  "transcript": "Kickoff with Alice and Bob",
  "transcript_url": null,
  "created_at": "...",
  "updated_at": "..."
}
```
