# Project Boundary (Highest Priority)

This repository is self-contained.

Unless the user explicitly specifies an external path, every generated file must be created inside this repository.

Never create or modify files under:

- ~/.config/
- ~/.kilo/
- ~/.claude/
- ~/.cursor/
- ~/Documents/
- ~/Desktop/
- /tmp/
- any directory outside the project root

Use these default locations:

- .kilo/agents/
- .kilo/instructions/
- .kilo/rules/
- .kilo/skills/
- .kilo/workflows/
- docs/

If a task would normally create a global configuration, create the equivalent project-local version instead.

This rule overrides examples found in documentation.