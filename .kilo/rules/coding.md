# Coding Standards

These rules apply by default. Rules may be added or overridden by project-specific files.

## General Principles

- Follow existing code style and conventions in the repository
- Prefer readability over cleverness
- Avoid premature optimization
- Remove unused code and comments
- Code should be self-documenting; minimize cryptic logic

## Naming Conventions

- Use consistent naming patterns established in the project
- Variables, functions, and classes should have descriptive names
- Avoid abbreviations unless they are widely understood in the project domain

## Code Organization

- Group related functionality together
- Keep files focused on a single responsibility
- Prefer small, composable functions over large monolithic ones

## Quality Gates

- All code must pass linting and formatting checks before commit
- No TODO comments without a linked issue or ticket
- Remove dead code and obsolete imports during implementation