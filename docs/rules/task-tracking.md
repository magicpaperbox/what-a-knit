# Task Tracking Rules

This document defines how the agent should maintain task memory for this repository.
These rules are mandatory when working in this project.

## Purpose

Task files make it easy to stop and return later without repeating the whole briefing.
They should be readable both for the user and for the agent.

Task tracking is memory, not an implementation plan.
Do not use task files as an excuse to create a plan when the user did not ask for one.

## Location

Task files live in:

```text
docs/tasks/
```

Create one file per meaningful task.
Use an ISO date prefix so files sort chronologically:

```text
docs/tasks/YYYY-MM-DD-short-task-slug.md
```

Example:

```text
docs/tasks/2026-06-01-prepare-agent-docs.md
```

## When To Create A Task File

Create a task file automatically when:

- the user starts a task that will likely span more than one conversation,
- the user explicitly says we should track the task,
- the work involves several files or decisions,
- the current task creates context that would be annoying to repeat tomorrow.

Do not create a task file for tiny one-off questions.

## When To Update A Task File

Update the active task file automatically:

- after an important decision,
- after files are created or changed,
- when the current next step changes,
- before ending a longer work session,
- when the user pauses or switches context,
- when something is blocked and the reason matters.

Keep updates short.
This file is not a transcript.

## Required Task File Structure

Use this structure unless there is a clear reason to adapt it:

```md
# Task: Short Human-Readable Name

Started: YYYY-MM-DD
Status: in progress

## Goal

## Current Context

## Decisions Made

## Relevant Files

## Where We Stopped

## Next Small Step

## Open Questions
```

## What To Write

Write:

- the user-facing goal,
- the current state,
- decisions already made,
- files that matter,
- the exact place where work stopped,
- the next small step,
- open questions or blockers.

## What Not To Write

Do not write:

- long transcripts,
- private speculation about the user,
- implementation plans the user did not request,
- every tiny command that was run,
- vague notes like "continue work" without context.

## Resuming Work

When the user returns to a tracked task:

1. Read `AGENTS.md`.
2. Read this file.
3. Read the relevant task file in `docs/tasks/`.
4. Read the current source files before commenting on code.
5. Continue from the latest concrete context, not from memory alone.
