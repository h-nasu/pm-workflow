# PM Workflow

AI-first Project Management System that automates PM work through meeting understanding, project reasoning, and workflow automation.

## Features

- Fireflies API integration for transcript ingestion
- LLM-based meeting analysis (Gemini, with abstraction for other providers)
- Structured extraction: decisions, action items, risks, dependencies, etc.
- PostgreSQL storage with SQLAlchemy + Alembic
- Meeting search
- Daily morning summary generation
- Modular architecture ready for future integrations (Backlog, GitHub, Slack, etc.)

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16 (via Docker)
- Fireflies API key
- Gemini API key

## Setup

```bash
cp .env.example .env
# Edit .env with your API keys

docker-compose up -d postgres
pip install -e ".[dev]"
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://pm_user:pm_pass@localhost:5432/pm_workflow` | PostgreSQL connection string |
| `FIREFLIES_API_KEY` | _(empty)_ | Fireflies API key for transcript ingestion |
| `GEMINI_API_KEY` | _(empty)_ | Gemini API key for LLM analysis |
| `APP_ENV` | `development` | Application environment (`development`, `production`, etc.) |
| `LOG_LEVEL` | `INFO` | Logging verbosity level. Accepted values follow Python's standard `logging` module levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. See the [`logging` documentation](https://docs.python.org/3/library/logging.html#logging-levels) for details. |

## Run API

```bash
uvicorn pm_workflow.main:app --reload
```

API available at http://localhost:8000
Interactive docs at http://localhost:8000/docs

## Run Tests

```bash
pytest
```

## Run Linter

```bash
ruff check src/ tests/
```

## Architecture

```
src/pm_workflow/
├── api/                # FastAPI routes and schemas
├── core/               # Base models and exceptions
├── models/             # SQLAlchemy ORM models
├── repositories/       # Data access layer
├── services/           # Business logic
├── integrations/       # External API clients (Fireflies, LLM)
├── prompts/            # LLM prompt templates
└── main.py             # FastAPI app entry
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/v1/meetings/` - List meetings (supports `limit` and `offset` query parameters)
- `GET /api/v1/meetings/{id}` - Get meeting detail
- `POST /api/v1/meetings/sync` - Sync from Fireflies
- `POST /api/v1/meetings/{id}/analyze` - Analyze meeting
- `GET /api/v1/search/?q={query}` - Search meetings by title or transcript (requires `q`)
- `GET /api/v1/summaries/daily` - Get daily summary
- `POST /api/v1/summaries/daily/generate` - Generate daily summary

## License

MIT
