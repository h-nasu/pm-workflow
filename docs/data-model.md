# Data Model Changes

## MeetingSummary Model

The `DailySummary` model has been replaced with `MeetingSummary`, changing the summary system from date-based aggregation to a one-to-one per-meeting model.

### Previous Model: DailySummary

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `date` | Date | The date the summary covers (unique) |
| `summary_text` | Text | Generated summary text |
| `summary_json` | JSON | Structured summary data |
| `meeting_count` | Integer | Number of meetings summarized |
| `created_at` | DateTime | Record creation timestamp |
| `updated_at` | DateTime | Record update timestamp |

### New Model: MeetingSummary

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `meeting_id` | UUID | Foreign key to `meetings.id` (unique) |
| `summary_text` | Text | Generated summary text |
| `summary_json` | JSON | Structured summary data |
| `created_at` | DateTime | Record creation timestamp |
| `updated_at` | DateTime | Record update timestamp |

### Key Changes

- **Removed**: `date` column and `meeting_count` column
- **Added**: `meeting_id` foreign key with unique constraint
- **Relationship**: `MeetingSummary` has a one-to-one relationship with `Meeting`

## Summary Generation Logic

The summary generation service now builds context from multiple sources:

1. **Transcript + Analysis (preferred)**: Uses both the meeting transcript and the structured analysis data
2. **Transcript only**: Falls back to transcript when analysis is not available
3. **Analysis only**: Falls back to analysis when transcript is not available
4. **Error**: Raises an exception when neither transcript nor analysis is available

The LLM prompt has been updated to expect per-meeting context instead of a date-based meeting list.
