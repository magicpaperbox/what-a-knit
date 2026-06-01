# Task: Prepare Agent Docs

Started: 2026-06-01
Status: ready for review

## Goal

Prepare the repository so future AI-assisted work starts with less briefing and better shared context.

## Current Context

The repository already had `AGENTS.md`, product/domain docs, learning notes, and a small Flask/SQLite/plain-JavaScript application structure.

The user wants `AGENTS.md` to stay as the main entry point with the most important collaboration and learning rules, while detailed project/process documentation lives in `docs/`.

## Decisions Made

- Keep collaboration rules and learning workflow directly in `AGENTS.md`.
- Make `AGENTS.md` a table of contents for deeper docs.
- Keep most project documentation in English.
- Keep user-facing collaboration and learning rules in Polish where that makes them clearer.
- Add mandatory process docs:
  - `docs/rules/task-tracking.md`
  - `docs/rules/user-learning-tracking.md`
- Track longer tasks in `docs/tasks/` using ISO-date filenames.
- Track stable learning preferences in `docs/collaboration/user-learning-profile.md`.
- `docs/form-data-flow.md` should include a practical reference example of a form-data class with its core methods, not only a conceptual data-flow description.
- `AGENTS.md` should avoid duplicated rules. It now separates:
  - operating rules,
  - teaching and collaboration style,
  - small-step learning workflow,
  - documentation index,
  - mandatory memory/process docs.

## Relevant Files

- `AGENTS.md`
- `docs/architecture.md`
- `docs/tech-stack.md`
- `docs/form-data-flow.md`
- `docs/rules/task-tracking.md`
- `docs/rules/user-learning-tracking.md`
- `docs/collaboration/user-learning-profile.md`
- `docs/tasks/2026-06-01-prepare-agent-docs.md`

## Where We Stopped

Initial documentation structure has been created.
`docs/form-data-flow.md` has been updated with a concrete `PatternFormData` reference example and route usage snippets.
`AGENTS.md` has been reorganized to remove duplicated rules and make headings consistent.

## Next Small Step

Review whether the structure and wording match the user's preferred collaboration style.

## Open Questions

- Should any section in `AGENTS.md` be shorter or stricter?
- Should task files stay in English, or should they be written in Polish for easier daily use?
