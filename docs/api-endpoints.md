# API Endpoints

## Meeting Endpoints

### Create Meeting from Transcript

```
POST /api/v1/meetings/manual
```

Creates a new meeting record from a provided transcript. The `transcript` is stored directly as the meeting `transcript`. No LLM call is performed on creation, keeping the insert fast and dependency-free; structured understanding can be generated later via `POST /api/v1/meetings/{id}/analyze`.

Optional fields let callers supply structured metadata. Any omitted field is filled with a cheap default so creation never depends on an external service.

**Request Body:**
```json
{
  "transcript": "Sprint planning on 2024-03-10 at 14:30 with Alice and Bob for 60 minutes. We discussed the roadmap.",
  "title": "Sprint Planning",
  "date": "2024-03-10T14:30:00",
  "duration_minutes": 60,
  "participants": { "Alice": true, "Bob": true }
}
```

All fields except `transcript` are optional. A minimal request only requires `transcript`.

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "fireflies_id": "manual-<uuid>",
  "title": "Sprint Planning",
  "date": "2024-03-10T14:30:00",
  "duration_minutes": 60,
  "participants": { "Alice": true, "Bob": true },
  "transcript": "Sprint planning on 2024-03-10 ...",
  "transcript_url": null,
  "created_at": "2024-03-10T...Z",
  "updated_at": "2024-03-10T...Z"
}
```

**Notes:**
- Manually created meetings use a synthetic `fireflies_id` prefixed with `manual-`.
- `transcript` is required (non-empty) and is stored as the `transcript`.
- If `title` is omitted, it is derived from the first non-empty line of `transcript` (capped at 200 characters), or `"Untitled Meeting"` if `transcript` is blank.
- If `date` is omitted, the current UTC time is used. Timezone-aware input is normalized to naive UTC.
- If `participants` is omitted, an empty object is stored.
- Returns `422 Unprocessable Entity` if `transcript` is missing or empty.

### Create Meeting from Text (LLM Extraction)

```
POST /api/v1/meetings/extract
```

Creates a new meeting record by using the configured LLM provider to extract structured meeting details (title, date, duration, participants, transcript) from the provided free-form `text`. This is the LLM-assisted alternative to `POST /api/v1/meetings/manual` (which stores the text directly without an LLM call).

**Request Body:**
```json
{
  "text": "Sprint planning on 2024-03-10 at 14:30 with Alice and Bob for 60 minutes. We discussed the roadmap."
}
```

**Response:** `200 OK`
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
  "created_at": "2024-03-10T...Z",
  "updated_at": "2024-03-10T...Z"
}
```

**Notes:**
- Manually extracted meetings use a synthetic `fireflies_id` prefixed with `manual-`.
- `text` is required (non-empty).
- If a title cannot be extracted, it defaults to `"Untitled Meeting"`.
- If a date cannot be parsed, the current UTC time is used.
- If a transcript is not extracted, the original `text` payload is stored.
- Returns `422 Unprocessable Entity` if the LLM fails or returns an invalid response; `422` if `text` is missing or empty.

## Analysis Endpoints

### List Analyses

```
GET /api/v1/analysis/
```

Returns a list of meeting analyses. Supports optional date-range filtering.

**Query Parameters:**
- `start_date` (optional): Filter analyses for meetings on or after this datetime (ISO 8601)
- `end_date` (optional): Filter analyses for meetings on or before this datetime (ISO 8601)
- `limit` (optional): Maximum number of results to return (default: 100, max: 500)
- `offset` (optional): Number of results to skip for pagination (default: 0)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "meeting_id": "uuid",
    "decisions": [],
    "action_items": [],
    "risks": [],
    "dependencies": [],
    "missing_information": [],
    "client_requests": [],
    "requirements": [],
    "open_questions": [],
    "project_status": {},
    "suggested_next_actions": [],
    "model_used": "gemini",
    "created_at": "2024-01-15T10:00:00Z"
  }
]
```

### Get Analysis by Meeting ID

```
GET /api/v1/analysis/{meeting_id}
```

Returns a single analysis for the specified meeting.

**Response:** `200 OK` or `404 Not Found`

## Summary Endpoints

### Get Meeting Summary

```
GET /api/v1/summaries/meeting/{meeting_id}
```

Returns the summary for a specific meeting.

**Response:** `200 OK` or `404 Not Found`
```json
{
  "id": "uuid",
  "meeting_id": "uuid",
  "summary_text": "Meeting summary text...",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:05:00Z"
}
```

### Generate Meeting Summary

```
POST /api/v1/summaries/meeting/{meeting_id}/generate
```

Generates a new summary for the specified meeting using the LLM provider. The summary is generated from the meeting transcript and/or analysis data.

**Response:** `200 OK` or `500 Internal Server Error`
```json
{
  "id": "uuid",
  "meeting_id": "uuid",
  "summary_text": "Generated summary text...",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:05:00Z"
}
```

**Note:** If a summary already exists for the meeting, it will be updated rather than duplicated.
