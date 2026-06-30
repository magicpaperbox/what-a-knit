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
- The user added mapper conversion from `ProjectFormData.skein_usage` to `Project.skein_usages` in `ProjectFormData.to_domain()`.
- The user added parsing of skein usage rows in `ProjectFormData.from_request_form()` with `form.getlist(...)`, `zip(...)`, and `skein_usage.append(ProjectSkeinFormData(...))`.
- The user started the next API/service step and tried to read all skeins from `projects/api.py`; this needs to be redirected toward `YarnService.get_all_skeins()` because available inventory skeins belong to the yarn module, not to `ProjectRepository.get_all()`.
- The user added `YarnService.get_all_skeins() -> list[Skein]`, delegating to the existing `SkeinRepository.get_all()`, and cleaned up the unused `SkeinRepository` import from `projects/api.py`.
- The user imported and instantiated `YarnService` in `projects/api.py`, then passed `available_skeins=yarn_service.get_all_skeins()` to the project form template.
- The user added a first temporary project form UI with `select name="skein_id"` over `available_skeins` and `input name="used_yarn_weight"`.

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

The schema table, domain representation, repository row dataclass, row-to-domain mapper, one-project skein usage query method, `get_by_id()`/`get_all()` wiring, and add/update/delete persistence are in place. The user has moved to `src/modules/projects/mappers.py`; `ProjectSkeinFormData` exists, `ProjectFormData.from_domain()` maps each `ProjectSkeinUsage` from `project.skein_usages` into a form-data row, `ProjectFormData.to_domain()` converts `self.skein_usage` back into `ProjectSkeinUsage` objects, and `ProjectFormData.from_request_form()` now reads `skein_id` plus `used_yarn_weight` lists and converts them into `ProjectSkeinFormData` rows. The project form now receives `available_skeins` and has a first simple select/input pair for submitting skein usage.

## Next Small Step

Next session: manually test creating/editing a project with the temporary skein usage fields, then decide whether to improve the UI or first add a small focused test for mapper/form submission.

## Open Questions

- Should the UI record usage by choosing a specific skein, a yarn type, or a grouped skein row?
- Where should the first UI for editing project skein usage live: project details, project edit form, or yarn details?
