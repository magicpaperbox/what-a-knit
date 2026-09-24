# Task: Project Yarn Usage

Started: 2026-06-28
Status: in progress

## Goal

Guide the user through implementing project yarn planning: reserve specific owned skeins for planned projects, record when reserved skeins are actually used, remove reserved resources from the available pool, and restore used yarn when a project is frogged.

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
- On 2026-09-07, the user made this feature the current priority because she needs to plan not-yet-started projects and know whether the remaining unreserved yarn is sufficient.
- The desired workflow now distinguishes assigning/reserving a skein from actually consuming it through a later "Use skein" action.
- Frogging a project should return its yarn to the available pool.
- The current implementation does not yet represent this distinction: `project_skein_usage` and `ProjectSkeinUsage` store only used weight, while the project form immediately asks for used weight.
- The current "Frog project" button posts to the project delete route, so it deletes the project instead of performing a reversible frog operation.
- The user does not want to select technical physical skein IDs in the project form. She wants to select a yarn definition (the owned yarn kind), enter the required weight in grams, and have the system report whether enough unreserved inventory exists.
- One project can require several yarn definitions, so the project form must eventually support multiple yarn requirement rows.
- The current dropdown is not informative because `_render_project_form()` passes bare `Skein` objects and `templates/projects/form.html` renders only `skein.id` and `skein.current_weight`; a `Skein` contains only `yarn_id` and does not itself contain the yarn brand, name, or color.

## Decisions Made

- Treat this as a cross-module feature touching database, backend/domain/repository, and templates.
- Start from the data model, because project-yarn usage cannot be represented safely only by changing `project.progress_percent`.
- The user wants to support a project consuming several full skeins plus a partial skein, for example 4 full skeins and 20 grams of a fifth skein.
- Store one current total usage row per project-skein pair. The user wants to update a value from e.g. 10 g to 15 g, not store separate 10 g and 5 g usage events.
- Multiple yarn types in one project are supported by storing multiple skein usages, because each `skein_id` points to a `skein`, and each `skein` points to its `yarn_id`.
- Reservation and consumption are separate business states. Reserving yarn for a planned project must make it unavailable to other project plans without pretending it has already been used.
- Consumption must preserve enough information to restore the consumed yarn if the project is frogged.
- Define the state transitions and ownership rules before extending the temporary form UI.
- A project yarn requirement and a physical skein allocation are different concepts: the user chooses `YarnId` plus required grams, while the system later chooses one or more matching `SkeinId` records.
- Keep the user-facing requirement separate from the system-facing allocation so multiple yarn definitions and availability checks remain clear.
- The user clarified the intended knitting meaning: the pattern declares the material need; on the project she only assigns matching yarn from stash. `PatternRequirements` exists in `src/modules/patterns/domain.py` but is commented out on `Pattern`, so a pattern cannot yet supply grams or yarn kind to the project form. `ProjectYarnRequirement` remains the project-side stash assignment (`YarnId` plus grams). A Jinja `{% if initial_selected_patterns %}` cannot wait for the live pattern picker, because Jinja renders before that JavaScript selection happens.
- On 2026-09-23 the user paused copying the edit-form display onto Used yarn. Using a skein is usually the whole remaining skein. A typed weight is only the exception, when part of the skein is left over. The screen should also show how much has already been used. Do not treat the current Used yarn weight input as the final interaction.

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

The schema table, domain representation, repository row dataclass, row-to-domain mapper, one-project skein usage query method, `get_by_id()`/`get_all()` wiring, and add/update/delete persistence are in place. `ProjectSkeinFormData` maps the submitted `skein_id` and `used_yarn_weight`, and the project form receives `available_skeins`. This earlier implementation models immediate usage but does not yet model the newly clarified reservation-first workflow. The user has added `ProjectYarnRequirement`, `Project.yarn_requirements`, the `project_yarn_requirement` table, and complete repository read/create/update/delete handling. `delete()` now correctly cleans `project_gauge`, `project_patterns`, `project_yarn_requirement`, and `project_skein_usage` once each before deleting the project. `ProjectYarnRequirementFormData` exists in `src/modules/projects/mappers.py`. `ProjectFormData` has a `yarn_requirements` list. `from_domain()` and `to_domain()` now convert between `ProjectYarnRequirement` and `ProjectYarnRequirementFormData`, including `yarn_requirements=` on the `Project(...)` call. Imports for `ProjectYarnRequirement` and `YarnId` are in place. The form-data layer now round-trips yarn requirements. `_render_project_form()` now passes `available_yarns`. The Booked yarn group in `templates/projects/form.html` restores one requirement on edit. The Used yarn controls stay temporary. On 2026-09-23 the user agreed not to copy the `selected` / `value` display onto them, because consumption will be a later action: the normal case takes the skein's whole remaining weight, a typed weight appears only for a partial use, and grams already used are shown rather than retyped.

`details()` in `src/modules/projects/api.py` loads `yarns` in the same order as `project.yarn_requirements`. The Booked yarn row in `templates/projects/details.html` prints `requirement.required_weight.grams` and `yarns[loop.index0].name` in one loop. The user confirmed that this works. One booked-yarn row now round-trips through the form, edit view, and project details. Stash quantity is not shown yet.

`YarnService.get_stash_yarn_weight()` starts from `Mass(0)` and returns `Mass`. `details()` builds a `weight` list by calling it with each `requirement.yarn_id`, in the same order as `yarns`. The Booked yarn row in `templates/projects/details.html` does not print that list yet.

## Next Small Step

In that same loop in `templates/projects/details.html`, print `weight[loop.index0].grams` beside the yarn name. That is the shelf total for the booked yarn only.

## Open Questions

- Should the UI record usage by choosing a specific skein, a yarn type, or a grouped skein row?
- Where should the first UI for editing project skein usage live: project details, project edit form, or yarn details?
- Should the first "Use skein" implementation consume the skein's entire current weight, or must it support partial use such as 20 g from a skein immediately?
- When a project is finished rather than frogged, should an unused remainder be released automatically while the consumed amount stays deducted?
