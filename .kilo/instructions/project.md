# Project Instructions

This file contains project-specific instructions that override or extend the global instructions.

## How This File Works

- This file is read after `instructions/global.md`
- Rules defined here take precedence over global rules with the same name
- Use indexed prefixes (`00-`, `01-`, `02-`) when multiple override files are needed

## Project-Specific Overrides

Add any project-specific instruction overrides here. For example:

- Coding standards specific to this project
- Architecture patterns specific to this project
- Toolchain or framework preferences
- Team conventions or naming patterns

## Adding New Project Rules

1. Create rule files in `rules/project.md`
2. Create skill files in `skills/`
3. Create subagent files in `agents/subagents/`
4. Reference them in this file for discoverability