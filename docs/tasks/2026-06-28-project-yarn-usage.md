# Task: Project Yarn Usage

Started: 2026-06-28
Status: in progress

## Goal

Guide the user through implementing a feature where a project can use specific yarn skeins, increasing used yarn in the project decreases available skein weight, and used yarn is visible separately.

## Current Context

- The user wants to write the implementation herself with step-by-step guidance.
- Existing projects can already be connected to patterns through `project_patterns`.
- Existing yarn inventory stores yarn definitions in `yarn` and available skeins in `skein`.
- `Skein.current_weight` currently represents available remaining weight.
- The user added an initial `project_skein_usage` table skeleton with `project_id`, `skein_id`, and `used_weight_grams`.
- The user added `PRIMARY KEY (project_id, skein_id)` to `project_skein_usage`.
- The user added foreign keys from `project_skein_usage.project_id` to `project(id)` and from `project_skein_usage.skein_id` to `skein(id)`.
- The user made `project_skein_usage.used_weight_grams` required with `NOT NULL`.
- The user added `ProjectSkeinUsage` in `src/modules/projects/domain.py` with `skein_id: SkeinId` and `used_weight: Mass`.
- The user added `Project.skein_usages: list[ProjectSkeinUsage]` in `src/modules/projects/domain.py`.
- The user added `ProjectSkeinRow` in `src/modules/projects/repository.py` with fields matching `project_skein_usage`: `project_id`, `skein_id`, and `used_weight_grams`.
- The user added `ProjectRepository._skein_usage_row_to_domain()` to map `ProjectSkeinRow` into `ProjectSkeinUsage`.
- The user added a repository method that reads `project_skein_usage` rows for one project, creates `ProjectSkeinRow` objects, and maps them to `ProjectSkeinUsage`.
- The user started wiring skein usages into `ProjectRepository.get_by_id()` and `_row_to_domain()`.
- The user added `_add_skein_usages()` and wired it into `add()` and `update()`, including cleanup in `update()`.
- The user added deletion cleanup for `project_skein_usage` in `ProjectRepository.delete()`.

## Decisions Made

- Treat this as a cross-module feature touching database, backend/domain/repository, and templates.
- Start from the data model, because project-yarn usage cannot be represented safely only by changing `project.progress_percent`.
- The user wants to support a project consuming several full skeins plus a partial skein, for example 4 full skeins and 20 grams of a fifth skein.
- Store one current total usage row per project-skein pair. The user wants to update a value from e.g. 10 g to 15 g, not store separate 10 g and 5 g usage events.
- Multiple yarn types in one project are supported by storing multiple skein usages, because each `skein_id` points to a `skein`, and each `skein` points to its `yarn_id`.

## Relevant Files

- `src/schema.sql`
- `src/modules/projects/domain.py`
- `src/modules/projects/repository.py`
- `src/modules/projects/mappers.py`
- `src/modules/projects/api.py`
- `src/modules/yarn/domain.py`
- `src/modules/yarn/repository/skein_repository.py`
- `src/modules/yarn/service.py`
- `templates/projects/form.html`
- `templates/projects/details.html`
- `templates/yarn/details.html`

## Where We Stopped

The schema table, domain representation, repository row dataclass, row-to-domain mapper, one-project skein usage query method, `get_by_id()`/`get_all()` wiring, and add/update/delete persistence are in place. The user has moved to `src/modules/projects/mappers.py`; `ProjectSkeinFormData` exists and `ProjectFormData.from_domain()` now maps each `ProjectSkeinUsage` from `project.skein_usages` into a form-data row.

## Next Small Step

In `src/modules/projects/mappers.py`, decide how `ProjectFormData` should represent skein usage rows from forms, then make sure `ProjectFormData.to_domain()` preserves or converts those rows into `Project.skein_usages`.

## Open Questions

- Should the UI record usage by choosing a specific skein, a yarn type, or a grouped skein row?
- Where should the first UI for editing project skein usage live: project details, project edit form, or yarn details?
