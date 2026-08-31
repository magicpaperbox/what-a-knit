# Task: Retro UI Polish

Started: 2026-08-26
Status: completed

## Goal

Refine the app UI so it stays playful and slightly retro, while improving readability, contrast, and visual hierarchy.

## Current Context

The current UI direction is intentionally not generic SaaS. It should keep the cozy knitting identity, rounded shapes, pink/purple palette, and retro feel.

Recent work focused on detail pages and global CSS:

- Added back-link controls to detail views.
- Moved the back-link into the detail page header next to the title.
- Softened heavy borders and offset shadows into lighter elevation.
- Adjusted palette variables for better contrast and coherence.
- Lightened the overall CSS rhythm: smaller fixed heading sizes, softer section/card spacing, thinner inputs, calmer buttons, and less heavy table/chart controls.
- Cleaned CSS after the styling pass by consolidating duplicate base rules, removing unused design tokens, and deleting redundant table/mobile overrides.
- Normalized odd one-off colors by adding shared tokens for accent washes, neutral buttons, danger text/buttons, icon controls, chart secondary buttons, and footer text.
- Refined detail-page heading composition: the title now behaves more like a folder tab attached to the details panel, and the back button is aligned as a related outline control instead of a detached floating square.
- Adjusted the yarn inventory list so yarn cards use a dedicated scan-friendly variant with text on the left and yarn images on the right at wider breakpoints.
- Fixed the dark-mode navigation flash by applying the saved theme to `<html>` before the main stylesheet loads, then updating dark-mode CSS selectors from `body.dark` to `html.dark`.
- Refined the expanded skein subtable: the nested rows now use a lighter outline, a subtle divider between child records, and clearer parent-child hierarchy.
- Flattened the desktop navigation item interaction style: hover/active states now use flat fills and borders instead of per-item soft shadows, dark mode active navigation has a visible border, and the nav shell keeps a soft shadow to separate the panel from the page.
- Strengthened the skein table trash action so it uses the same danger color family as the "Frog yarn" delete button instead of the softer secondary danger background.
- Reworked the trash icon artwork to use a lighter body, softer pink accents, two front slats, and a stronger outline so it stays readable on the darker danger button background.
- Manual visual inspection passed on 2026-08-28. The UI polish work was committed as `e3e1768 more css and ui`.

## Decisions Made

- Keep the back-link as a small icon control next to the page title, not as a floating decorative button.
- Preserve the retro style with outlines, soft corners, pink/lavender/plum colors, and small green/yellow accents.
- Use softer elevation variables instead of strong offset shadows for large UI surfaces.
- Separate link colors from button accent colors with `--link` and `--link-hover`.
- Prefer contrast-safe button backgrounds so white button text remains readable.
- Use breakpoint-based text sizes instead of viewport-scaled font sizes, so headings do not grow too aggressively on large screens.
- Keep inventory-style yarn cards left-aligned for scanning instead of centering every card; use the photo as a right-side visual anchor.

## Relevant Files

- `static/css/style.css`
- `templates/yarn/index.html`
- `templates/yarn/details.html`
- `templates/projects/details.html`
- `templates/patterns/details.html`
- `templates/tools/details.html`
- `templates/base.html`
- `static/js/theme.js`
- `static/css/components/tables.css`
- `static/css/responsive/mobile.css`
- `static/css/responsive/768.css`
- `static/css/responsive/1024.css`
- `docs/collaboration/user-learning-profile.md`

## Where We Stopped

Global CSS variables were updated for contrast and a more coherent retro palette. Contrast checks for the main text, label, link, nav, and button color pairs are above 4.5:1. The latest CSS pass reduced visual heaviness across typography, section spacing, inputs, buttons, tables, and chart controls while preserving the retro/cozy direction.

The CSS has also been cleaned after those changes: duplicate `.section`, `body`, `.page-shell`, and skein child-row overrides were consolidated, and unused old shadow/nav/title-tab tokens were removed.

The palette cleanup replaced several one-off colors that were visually inconsistent: mint chart buttons, cool gray cancel buttons, orange trash buttons, and scattered hardcoded pink table states now use shared retro palette tokens.

The detail heading/back-link layout was adjusted after visual review: the title tab lost its bottom rounding/shadow and overlaps the section by only the border width, while the back control uses the title-tab border color and sits closer to the tab baseline.

The yarn list now has a dedicated `.resource-list--yarn` and `.yarn-card` variant. The list width is capped and centered, and yarn cards with images use a compact text-left/image-right layout on narrow screens, then get more image width and spacing from the 640px breakpoint upward. The yarn grid uses `auto-fill`, not `auto-fit`, so a single yarn card does not stretch across the whole row.

Dark mode is now restored before first paint: `templates/base.html` runs a small inline script in `<head>` before `static/css/style.css`, and the theme class lives on `<html>` as `html.dark`. `static/js/theme.js` now uses `document.documentElement`, and the dark-mode selectors in `static/css/style.css` were updated accordingly.

The desktop navigation panel now leans flatter and more retro: `static/css/responsive/768.css` removes the hover and active nav item shadows, adds a visible active border in dark mode, uses a slower hover transition, and replaces the desktop nav shell's gradient/blur/radial glow with a flat panel background while keeping a soft outer shell shadow for separation.

The expanded skein child-row styling was softened after visual review: the pink nested group now uses `--rose-divider` between records, and the outer rose outline was reduced from 2px to 1px across desktop and mobile breakpoints. `templates/yarn/details.html` now marks every top-level skein record with `skein-parent-row`, so single skeins and grouped parent rows share the same wrapped row styling. On desktop, an expanded parent row becomes the top part of one outlined parent-and-children package; the child rows stay as real table rows and use a subtle timeline-style connector with dots in the first column, closer to a nested comment thread without breaking column alignment. The desktop table columns were adjusted so the child label no longer collides with the weight column, parent row counts align more closely with the child-row dots, and text cells are vertically centered without moving action buttons.

The skein table delete icon now uses the same stronger danger background as the main delete buttons, so destructive actions stand out while staying in the app's existing palette.

The trash icon artwork was updated after the stronger danger background made the old mostly-pink icon too low-contrast. A later pass simplified the front from three slats to two and softened the hot-pink accents for better tiny-size readability.

The changed screens were visually checked in the browser and the user confirmed everything works. The UI polish pass is considered complete.

## Next Small Step

No active UI polish step. If the design is revisited later, open a new small polish task for that specific area.

## Open Questions

- None for this completed polish pass.
