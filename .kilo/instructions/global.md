# Global Instructions

This file defines how Kilo Code instructions are applied globally across all projects.

## How to Add Project-Specific Documentation

1. Create a `.kilo/instructions/project.md` file in the project root
2. Create a `.kilo/rules/project.md` file for project-specific rules
3. Project-specific files override global ones with the same name
4. Use indexed prefixes (`00-`, `01-`, `02-`) for files that need override ordering

## Instruction Application Order

1. Global instructions (`instructions/global.md`)
2. Project-specific instructions (`instructions/project.md`)
3. Global rules (`rules/*.md`)
4. Project-specific rules (`rules/project.md`)
5. Skills (`skills/*.md`)
6. Workflows (`commands/*.md`)
7. Agents (`agents/*.md`)
8. Project-specific subagents (`agents/subagents/*.md`)

## Safety Principle

Kilo Code should prefer:

- Explicit instructions
- Indexed overrides
- Documented decisions

over assumptions.