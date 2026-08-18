# Architecture Guidelines

These rules apply by default. Rules may be added or overridden by project-specific files.

## Core Principles

- Prefer simple, maintainable architectures
- Avoid unnecessary abstractions
- Follow existing architectural patterns in the repository
- Changes must not break existing contracts without justification

## Component Design

- Each component should have a single, well-defined responsibility
- Components communicate through well-defined interfaces
- Favor composition over inheritance
- Keep coupling low and cohesion high

## Data Flow

- Define clear data flow between components
- Avoid hidden state and side effects
- Prefer immutable data structures where possible
- Validate data at boundaries (API inputs, external integrations)

## Dependency Management

- Dependencies should be explicit and documented
- Avoid circular dependencies
- External dependencies should be isolated behind interfaces
- Keep the dependency graph acyclic and shallow