# Documentation Guidelines

These rules apply by default. Rules may be added or overridden by project-specific files.

## Documentation Requirements

- Project documentation must be created or updated under `docs/`
- AI-generated tracking documents must go under a dedicated internal directory
- Do not mix client-facing documentation with AI internal tracking

## Documentation Standards

- All documentation must be written in the project's primary language
- Documentation should explain the "why", not just the "what"
- Keep documentation close to the code it describes
- Update documentation whenever code behavior changes

## Client-Side Documentation

When implementing or modifying client-facing features, documentation MUST be created for:

- UI components
- API integrations
- State management logic
- Environment setup
- Deployment procedures
- Client configuration

## Separation of Concerns

- Project documentation is client- or team-facing
- Internal tracking documents are for AI-only use
- Never allow AI to modify client-facing docs without explicit instruction

---

## Documentation Location

Project documentation must be created only in approved directories
defined by the project (e.g. `docs/`, `documentation/`, etc.).

AI must not invent new documentation roots unless there are no documentation directory found.
If no documentation directory is found create `docs/` only at repository root.

---

## Language Rules

Define the language(s) for project documentation.

- All project documentation will be created in **English**

This language rules apply ONLY to project documentation.

They do NOT affect `.kilo/documents/`
unless explicitly stated.

---

## Templates

- Templates under `.kilo/templates/documents/` must be used
- New templates must be referenced in this file

---

## Separation of Concerns

- Project documentation is client- or team-facing
- `.kilo/documents/` is AI internal

---

## Client-Side Documentation Rules

You MUST automatically generate and maintain client-side documentation when implementing or modifying client-facing features.

### Documentation Requirements

- You MUST create documentation for:
  - UI components
  - API integrations
  - State management logic
  - Environment setup
  - Deployment procedures
  - Client configuration

- You MUST organize documentation inside a structured directory.

### Directory Structure

Client-side documentation **MUST** be placed under:

`docs/`

You **MUST** automatically create missing subdirectories when needed.

Recommended structure:

```text
docs/
├── overview.md
├── specifications/
│   ├── architecture.md
│   ├── setup.md
│   └── deployment.md
├── api/
│   └── endpoints.md
├── components/
│   └── <component-name>.md
└── state/
    └── state-management.md
```

### Strict Restrictions

- You MUST NEVER generate, move, or modify files inside:

  client-requirements/

- The `client-requirements/` directory is reserved strictly for raw client-provided materials.
- You MUST treat `client-requirements/` as read-only.

---

# AI Document Model

This file defines the required AI-generated documents used
to plan, execute, verify, and improve work in this repository.

These documents are authoritative and may influence
subsequent task execution.

---

## General Rules

- AI documents must be created under `.kilo/documents/`
- Each directory represents a phase in task execution
- Index prefixes are mandatory and define execution order
- Documents may be updated iteratively
- Later phases may reference earlier phases

---

## Required Document Phases

### 01-plans/

Purpose:
- Capture AI understanding of the request
- Define approach, assumptions, and constraints

Required before:
- Design
- Task breakdown
- Implementation

---

### 02-specifications/

Purpose:
- Define required UI, APIs, behavior, and constraints
- Clarify what must be built

---

### 03-designs/

Purpose:
- Define architecture and implementation details
- File structure, class design, data flow
- Always include Technology Stacks for the project

---

### 04-tasks/

Purpose:
- Break work into executable tasks
- Each task should be verifiable

---

### 05-developments/

Purpose:
- Record execution results
- Summarize completed work

---

### 06-tests/

Purpose:
- Define test plans
- Record test results, failures, and fixes

---

### 07-changes/

Purpose:
- Track changes made after initial planning
- Record why changes occurred

---

### 08-issues/

Purpose:
- Record bugs and issues encountered
- Document countermeasures and lessons learned