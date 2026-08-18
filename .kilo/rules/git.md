# Git Guidelines

These rules apply by default. Rules may be added or overridden by project-specific files.

## Commit Standards

- Write clear, concise commit messages
- Use imperative mood in commit messages (e.g. "Add feature" not "Added feature")
- Reference issue or ticket numbers when applicable
- Each commit should represent a single logical change

## Branching Strategy

- Use feature branches for new work
- Keep branches short-lived and focused
- Rebase onto the main branch frequently to avoid large merge conflicts
- Never commit directly to the main branch

## Pull Request Guidelines

- Every PR must have a clear description of the change
- PRs should be small and focused on a single concern
- All tests must pass before a PR is merged
- At least one reviewer must approve before merging

## Working with Git

- Pull the latest changes before starting new work
- Resolve merge conflicts immediately
- Do not rewrite published history unless absolutely necessary
- Use tags for releases and important milestones