# User Learning Tracking Rules

This document defines how the agent should maintain the user's learning profile.
These rules are mandatory when working in this repository.

## Purpose

The learning profile helps the agent explain code in a way that fits the user.
It should make future help clearer, more consistent, and less repetitive.

It is not a diary and it is not a psychological profile.

## Location

The learning profile lives here:

```text
docs/collaboration/user-learning-profile.md
```

## When To Read It

Read the learning profile before:

- explaining a programming concept,
- reviewing the user's code,
- giving implementation guidance,
- helping debug a problem,
- deciding how much context to include.

## When To Update It

Update the learning profile automatically when the conversation reveals stable, useful information, such as:

- what the user already understands,
- what the user is currently learning,
- which explanations work well,
- which explanations do not work well,
- recurring confusions,
- topics already explained,
- preferences about workflow.

Do not ask for permission before these small documentation updates.
This is an explicit exception to the general rule "do not edit files unless asked".

## What To Write

Write concise, practical notes that will help future explanations.

Good examples:

- "Comfortable with Python loops and conditionals."
- "Needs extra clarity around classes and object-oriented design."
- "Prefers step-by-step review of small code changes."
- "When explaining JavaScript, name the exact browser API or function."

## What Not To Write

Do not write:

- sensitive personal information,
- guesses about the user's personality,
- emotional interpretation,
- long conversation history,
- praise or criticism,
- anything that would feel uncomfortable if the user opened the file.

## Maintenance

Keep the file short and current.
If information becomes outdated, update or remove it.
Prefer stable learning patterns over one-time observations.

## Required Sections

The profile should contain:

```md
# User Learning Profile

Last updated: YYYY-MM-DD

## Current Comfort Zone

## Currently Learning

## Needs Extra Clarity Around

## Explanation Style That Works Well

## Explanation Style To Avoid

## Already Explained Topics

## Recurring Confusions Or Watch Points
```
