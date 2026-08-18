# Testing Guidelines

These rules apply by default. Rules may be added or overridden by project-specific files.

## Test-Driven Development

- Define tests before or alongside implementation
- All new functionality must include test coverage
- Fix failing tests before proceeding

## Test Organization

- Tests should mirror the source code structure
- Group tests by feature or domain
- Use descriptive test names that explain the scenario and expected outcome
- Separate unit tests, integration tests, and end-to-end tests

## Testing Best Practices

- Test behavior, not implementation details
- Keep tests fast and isolated
- Use mocks for external dependencies
- Ensure tests are deterministic and repeatable
- Aim for meaningful coverage, not arbitrary percentage targets

## Failure Handling

- Tests must fail with clear, actionable error messages
- When a test fails, diagnose the root cause before fixing
- Flaky tests should be treated as bugs and fixed immediately