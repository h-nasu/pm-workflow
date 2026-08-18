# Project Rules

This file contains project-specific rules that override or extend the global rules.

## How This File Works

- This file is read after all `rules/*.md` files in the global framework
- Rules defined here take precedence over global rules
- Use indexed prefixes (`00-`, `01-`, `02-`) when multiple override files are needed

## Project-Specific Rules

Add any project-specific rule overrides here. For example:

- Technology stack constraints
- Testing framework preferences
- Documentation format requirements
- Git branching model
- Deployment pipeline specifics