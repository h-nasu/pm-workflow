---
description: Convert requirements into executable task breakdowns
agent: planner
---
This workflow turns a requirement into a validated execution plan and a set of implementation-ready tasks.

## Purpose

Use this workflow when the user provides a feature request, bug fix request, refactor goal, or product requirement and wants a clear implementation task list.

## Steps

1. **Understand the Requirement**
   - Read the user requirement carefully
   - Identify goals, scope, assumptions, and constraints
   - List missing information and open questions
   - Determine whether the requirement is simple, moderate, or architecture-impacting

2. **Create Initial Plan**
   - Create a planning document in `01-plans/`
   - Include:
     - Problem Understanding
     - Assumptions
     - Constraints
     - Proposed Approach
     - Risks
     - Open Questions

3. **Check Whether Architecture Work Is Needed**
   - Invoke the architect if any of the following are true:
     - New components or services are required
     - Existing component boundaries will change
     - New API contracts or data models are needed
     - Non-functional requirements are important
     - Cross-cutting concerns exist
     - The planner cannot confidently decompose work without design clarification

4. **Create or Refresh Design**
   - If architecture work is needed, create or update design documents in `03-designs/`
   - Ensure the design defines:
     - Architecture Overview
     - Component Design
     - Data Flow
     - Technology Stack decisions
     - Risks and Mitigations

5. **Create Task Breakdown**
   - Create implementation-ready tasks in `04-tasks/`
   - Each task must include:
     - Task title
     - Objective
     - Inputs / prerequisites
     - Files or modules likely affected
     - Acceptance criteria
     - Dependencies
     - Suggested owner agent
     - Test/verification notes

6. **Assign Tasks to Specialist Agents**
   - Backend tasks → `backend`
   - Frontend tasks → `frontend`
   - Architecture/design tasks → `architect`
   - Documentation tasks → `documentation`
   - QA validation tasks → `qa`
   - Review tasks → `reviewer`

7. **Sequence the Tasks**
   - Order tasks by dependency
   - Prefer small, verifiable increments
   - Separate enabling tasks from implementation tasks
   - Identify tasks that can be done in parallel

8. **Present for Review Before Execution**
   - Output the plan and task list
   - Surface all assumptions, unknowns, and decision points
   - Stop before implementation if key ambiguity remains

## Output Format

### Plan Summary
- Problem Understanding
- Assumptions
- Constraints
- Risks
- Open Questions

### Design Decision
- Architecture needed: yes/no
- If yes: reference design documents created or updated

### Task Breakdown
For each task include:
- ID
- Title
- Owner Agent
- Objective
- Dependencies
- Acceptance Criteria
- Verification

### Execution Order
- Phase 1
- Phase 2
- Phase 3

## Decision Rules

- If the request only changes isolated logic or UI behavior, planner may create tasks directly.
- If the request affects system boundaries, shared contracts, data flow, or scalability, architect must be involved before finalizing tasks.
- Do not create large vague tasks when smaller verifiable tasks are possible.
- Do not begin implementation until the task breakdown is reviewable.

## Exit Criteria

- A plan exists in `01-plans/`
- Architecture impact has been evaluated
- Required design exists in `03-designs/` when needed
- Implementation-ready tasks exist in `04-tasks/`
- Dependencies and acceptance criteria are explicit
