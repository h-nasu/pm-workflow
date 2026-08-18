# Development Roadmap

## Milestone 1: Project Foundation (Est: 4-6h)
**Goal**: Working project with database, models, and basic tests.

### Tasks
1. Initialize Python project structure (src/, tests/, pyproject.toml)
2. Configure development dependencies (FastAPI, SQLAlchemy, Alembic, Pydantic, pytest, etc.)
3. Create Docker Compose (PostgreSQL + app)
4. Implement database connection and session management
5. Define SQLAlchemy models (Meeting, MeetingAnalysis, DailySummary)
6. Create Alembic migration for initial schema
7. Create Pydantic schemas (request/response)
8. Create base repository class
9. Write unit tests for models and repositories
10. Verify DB connectivity and migration

**Acceptance**: `docker-compose up` starts PostgreSQL. `alembic upgrade head` creates tables. Tests pass.

---

## Milestone 2: AI Analysis Layer (Est: 6-8h)
**Goal**: LLM abstraction, prompt management, and transcript analysis.

### Tasks
1. Create LLM provider abstraction (BaseLLMProvider)
2. Implement Gemini provider
3. Create PromptManager (load templates from files)
4. Define Pydantic schemas for analysis output validation
5. Implement AnalysisService (orchestrates LLM calls, validates responses)
6. Create analysis prompt template
7. Create Fireflies API client (basic polling)
8. Implement SyncService (orchestrates Fireflies → Analysis → Storage)
9. Write unit tests for LLM abstraction, prompt manager, analysis service
10. Write integration tests with mocked Fireflies and LLM

**Acceptance**: Can mock LLM and Fireflies, run analysis pipeline end-to-end in tests.

---

## Milestone 3: API Layer & Daily Summary (Est: 6-8h)
**Goal**: FastAPI endpoints, search, and daily summary generation.

### Tasks
1. Create FastAPI app and routers
2. Implement meeting endpoints (list, get, sync, analyze)
3. Implement search endpoint (full-text + filters)
4. Implement daily summary endpoints
5. Create summary prompt template
6. Implement SummaryService
7. Add API error handling middleware
8. Write integration tests for API endpoints
9. Update README with setup and usage instructions

**Acceptance**: All endpoints functional. Daily summary generates from mocked data.

---

## Milestone 4: Polish & Documentation (Est: 4-6h)
**Goal**: Production readiness.

### Tasks
1. Add logging configuration
2. Add request ID tracing
3. Add retry logic for external APIs
4. Create .env.example
5. Write comprehensive README
6. Write architecture documentation in docs/
7. Run linting and type checking
8. End-to-end manual test with real Fireflies and Gemini (if keys available)

**Acceptance**: Clean lint, passing tests, documented, runnable with `docker-compose up`.

---

## Future Milestones (Not MVP)
- Milestone 5: n8n orchestration workflows
- Milestone 6: Backlog/GitHub/Slack integrations
- Milestone 7: pgvector + RAG for historical context
- Milestone 8: Multi-project and multi-organization support
- Milestone 9: Risk prediction and timeline prediction
- Milestone 10: Webhook support and real-time updates
