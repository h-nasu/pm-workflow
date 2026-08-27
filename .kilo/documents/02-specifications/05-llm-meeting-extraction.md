# Specification: LLM-based Meeting Extraction Endpoint

## Functional Requirements
### FR-1: Extract and create
- `POST /api/v1/meetings/extract` accepts `{ "text": "..." }`.
- LLM extracts `title`, `date` (ISO), `duration_minutes`, `participants` (list), `transcript`.
- A `Meeting` is created and returned.

### FR-2: Field defaults
- `title` missing → `"Untitled Meeting"`.
- `date` missing/invalid → current UTC time (naive).
- `transcript` missing → original `text`.
- `participants` → `{name: True}` dict.

### FR-3: Synthetic id
- `fireflies_id = "manual-<uuid4>"`.

### FR-4: Response & errors
- `200 OK` with `MeetingResponse`.
- `422` on LLM/validation failure.
- `500` on unexpected failure.
- `422` if `text` empty.

## Non-Functional
- Reuse existing LLM abstraction; no direct API calls in service.
- Testable with mocked LLM.

## API Contract
### Request
```json
{ "text": "Sprint planning on 2024-03-10 at 14:30 with Alice and Bob for 60 minutes." }
```
### Response `200 OK`
```json
{
  "id": "uuid",
  "fireflies_id": "manual-<uuid>",
  "title": "Sprint planning",
  "date": "2024-03-10T14:30:00",
  "duration_minutes": 60,
  "participants": { "Alice": true, "Bob": true },
  "transcript": "Sprint planning on 2024-03-10 ...",
  "transcript_url": null,
  "created_at": "...",
  "updated_at": "..."
}
```
