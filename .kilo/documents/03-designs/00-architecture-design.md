# Architecture Design

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        n8n (Orchestration)                   │
│  Triggers: Cron (daily summary), Webhooks (future)          │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │   API       │  │  Business    │  │   AI / LLM        │  │
│  │   Routes    │→ │   Logic      │→ │   Abstraction     │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
│                            │                    │            │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │   API       │  │  Data        │  │   External        │  │
│  │   Schemas   │  │   Access     │  │   Integrations    │  │
│  │  (Pydantic) │  │  (SQLAlchemy)│  │  (Fireflies, etc) │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    └─────────────────┘
```

## Project Structure

```
pm-workflow/
├── .ai-instructions/           # AI execution instructions
├── .vscode/                    # Editor config
├── docs/                       # Project documentation
│   └── requirements.md
├── src/                        # Source code
│   └── pm_workflow/
│       ├── __init__.py
│       ├── main.py             # FastAPI app entry
│       ├── config.py           # Settings (Pydantic Settings)
│       ├── database.py         # SQLAlchemy engine, session
│       │
│       ├── api/                # API layer
│       │   ├── __init__.py
│       │   ├── deps.py         # Dependency injection
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── router.py
│       │   │   ├── meetings.py
│       │   │   ├── search.py
│       │   │   └── summaries.py
│       │   └── schemas/        # Pydantic request/response models
│       │       ├── __init__.py
│       │       ├── meeting.py
│       │       ├── analysis.py
│       │       └── summary.py
│       │
│       ├── core/               # Core abstractions
│       │   ├── __init__.py
│       │   ├── entity.py       # Base ORM model
│       │   └── exceptions.py   # Custom exceptions
│       │
│       ├── models/             # SQLAlchemy ORM models
│       │   ├── __init__.py
│       │   ├── meeting.py
│       │   ├── analysis.py
│       │   └── summary.py
│       │
│       ├── repositories/       # Data access layer
│       │   ├── __init__.py
│       │   ├── base.py         # BaseRepository
│       │   ├── meeting.py
│       │   ├── analysis.py
│       │   └── summary.py
│       │
│       ├── services/           # Business logic
│       │   ├── __init__.py
│       │   ├── meeting.py      # MeetingService
│       │   ├── analysis.py     # AnalysisService
│       │   ├── summary.py      # SummaryService
│       │   └── sync.py         # SyncService (Fireflies)
│       │
│       ├── integrations/       # External integrations
│       │   ├── __init__.py
│       │   ├── fireflies.py    # Fireflies API client
│       │   └── llm/            # LLM abstraction
│       │       ├── __init__.py
│       │       ├── base.py     # BaseLLMProvider
│       │       ├── gemini.py   # Gemini provider
│       │       └── prompt_manager.py
│       │
│       └── prompts/            # Prompt templates
│           ├── __init__.py
│           ├── analysis.txt    # Meeting analysis prompt
│           └── summary.txt     # Daily summary prompt
│
├── tests/                      # pytest tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_repositories.py
│   │   ├── test_services.py
│   │   └── test_llm.py
│   ├── integration/
│   │   ├── test_api.py
│   │   └── test_sync.py
│   └── fixtures/
│       └── sample_transcript.txt
│
├── alembic/                    # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
└── README.md
```

## Architecture Decisions

### 1. Monorepo, Single Service
**Tradeoff**: Simplicity over microservices. A single FastAPI service is easier to develop, test, and deploy for MVP. Can split later if needed.

### 2. Layered Architecture (API → Service → Repository → Model)
**Tradeoff**: More files, but clear separation of concerns. Enables testing each layer independently.

### 3. LLM Abstraction Layer
**Tradeoff**: Extra interface file, but enables swapping providers without touching business logic. Critical for future flexibility.

### 4. Prompt Templates as Files
**Tradeoff**: Slightly harder to edit than inline strings, but prompts are first-class citizens and can be version-controlled, reviewed, and A/B tested.

### 5. Pydantic for API Schemas, SQLAlchemy for ORM
**Tradeoff**: Dual model definitions (Pydantic + SQLAlchemy). Avoids leakage of ORM models to API layer and keeps API contracts stable.

### 6. Repository Pattern
**Tradeoff**: Extra abstraction over raw SQLAlchemy session. Enables mocking for tests and centralizes query logic.

### 7. Dependency Injection via FastAPI Depends
**Tradeoff**: Tightly coupled to FastAPI. Acceptable for MVP; can extract to external DI container later if needed.

### 8. Docker Compose for Local Dev
**Tradeoff**: Requires Docker. Acceptable given team familiarity and production parity.

## Database Design

### ER Diagram

```
┌──────────────┐       ┌─────────────────┐
│   meetings   │───┐   │ meeting_analyses│
│              │   └──▶│                 │
│ id PK        │       │ id PK           │
│ fireflies_id │       │ meeting_id FK   │
│ title        │       │ decisions       │
│ date         │       │ action_items    │
│ ...          │       │ risks           │
└──────────────┘       │ ...             │
                       └─────────────────┘
                       ┌─────────────────┐
                       │  daily_summaries│
                       │                 │
                       │ id PK           │
                       │ date (unique)   │
                       │ summary_json    │
                       │ ...             │
                       └─────────────────┘
```

### Indexing Strategy
- `meetings.date` (B-tree)
- `meetings.fireflies_id` (unique, B-tree)
- `daily_summaries.date` (unique, B-tree)
- Full-text search on `meetings.transcript` using `tsvector` (PostgreSQL)
- GIN index on `meeting_analyses` JSONB fields for entity search

## Error Handling Strategy

- External API failures (Fireflies, LLM): Logged, retried with exponential backoff, stored with status in DB
- Invalid LLM responses: Stored as raw_response, parsed fields set to null, alert via logging
- Database errors: Standard SQLAlchemy exceptions, wrapped in service layer
- API errors: Consistent JSON error format with request ID for tracing

## Security Considerations (MVP)

- API keys via environment variables (.env, never committed)
- No secrets in code or logs
- Input validation via Pydantic
- Future: OAuth2, rate limiting, RBAC
