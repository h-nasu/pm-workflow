# MVP Specification

## Functional Requirements

### FR-1: Fireflies Integration
- Poll Fireflies API for new transcripts
- Download transcript text and metadata
- Store raw transcript for audit

### FR-2: AI Analysis
- Send transcript to LLM (Gemini default)
- Extract structured data:
  - Decisions
  - Action Items
  - Risks
  - Dependencies
  - Missing Information
  - Client Requests
  - Requirements
  - Open Questions
  - Project Status
  - Suggested Next Actions
- Validate JSON response against schema

### FR-3: Storage
- Store meetings, transcripts, and analysis results in PostgreSQL
- Support search across meetings and extracted entities

### FR-4: Search
- Full-text search on meeting titles, transcripts, and extracted entities
- Filter by date, project, participant

### FR-5: Daily Summary
- Generate morning summary from previous day's meetings
- Include key decisions, action items, and risks
- Output as structured JSON and human-readable text

## API Contracts

### POST /api/v1/meetings/sync
Trigger Fireflies sync for a date range.

### GET /api/v1/meetings
List meetings with pagination and filters.

### GET /api/v1/meetings/{meeting_id}
Get meeting detail with analysis.

### POST /api/v1/meetings/{meeting_id}/analyze
Re-analyze a meeting.

### GET /api/v1/search
Search meetings and entities.

### GET /api/v1/summaries/daily
Get daily morning summary.

### POST /api/v1/summaries/daily/generate
Generate daily summary for a specific date.

## Data Model

### meetings
- id (UUID)
- fireflies_id (string, unique)
- title (string)
- date (datetime)
- duration_minutes (int)
- participants (jsonb)
- transcript (text)
- transcript_url (string)
- created_at, updated_at

### meeting_analyses
- id (UUID)
- meeting_id (UUID, FK)
- decisions (jsonb)
- action_items (jsonb)
- risks (jsonb)
- dependencies (jsonb)
- missing_information (jsonb)
- client_requests (jsonb)
- requirements (jsonb)
- open_questions (jsonb)
- project_status (jsonb)
- suggested_next_actions (jsonb)
- raw_response (jsonb)
- model_used (string)
- created_at

### daily_summaries
- id (UUID)
- date (date, unique)
- summary_text (text)
- summary_json (jsonb)
- meeting_count (int)
- created_at, updated_at

## Validation Rules

- All LLM responses must be validated against Pydantic schemas before storage
- Invalid responses are logged and stored as raw_response with null parsed fields
- Fireflies API errors must not crash the sync process
