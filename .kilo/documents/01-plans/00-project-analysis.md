# Project Analysis

## Executive Summary

Build an AI-first Project Management System that automates PM work through meeting understanding, project reasoning, and workflow automation. The MVP focuses on Fireflies transcript ingestion, LLM analysis, structured storage, search, and daily summaries.

## Problem Statement

Traditional PM tools (Jira, Asana, Backlog) are task trackers. They do not understand meetings, extract meaning, or reason about project health. An AI Project Manager should act as an experienced PM, not a note-taker.

## MVP Scope

**In Scope:**
- Fireflies API integration (polling)
- Transcript download and parsing
- LLM-based analysis (Gemini, abstraction layer)
- Structured JSON extraction (decisions, action items, risks, etc.)
- PostgreSQL storage with SQLAlchemy + Alembic
- Meeting search
- Daily morning summary generation

**Out of Scope (Future):**
- Webhooks (use polling in MVP)
- External integrations (Backlog, GitHub, Slack, Email, Calendar)
- pgvector / RAG
- Multi-tenant / multi-project
- Web UI (MVP is API-only)

## Missing Requirements / Clarifications Needed

1. **Authentication**: No auth requirements specified. MVP will implement a simple API key for internal use. Future: OAuth2 / JWT.
2. **Fireflies API Key**: Must be provided by user. No default.
3. **Gemini API Key**: Must be provided by user.
4. **Scheduling**: Daily summary timing not specified. MVP will use a simple configurable cron or manual trigger.
5. **Project Context**: How does the AI know which project a meeting belongs to? MVP will require explicit project_id or infer from transcript metadata.
6. **User Management**: No user management specified. MVP will be single-user / single-organization.
7. **Error Handling**: Retry policies for Fireflies and LLM APIs not specified. MVP will implement basic retries with exponential backoff.

## Assumptions

- Single organization, single user for MVP
- Fireflies account exists with transcripts available
- Gemini API key available
- PostgreSQL running locally via Docker Compose
- n8n can be added later for orchestration; MVP logic lives in FastAPI

## Non-Functional Requirements

- **Performance**: Transcript analysis < 30s for 1h meeting
- **Reliability**: Graceful degradation if LLM fails
- **Maintainability**: Modular, testable, documented
- **Extensibility**: LLM provider swap without business logic changes
