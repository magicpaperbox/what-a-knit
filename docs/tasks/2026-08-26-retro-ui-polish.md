# Task: Retro UI Polish

Started: 2026-08-26
Status: in progress

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
- `templates/projects/details.html`
- `templates/yarn/details.html`
- `templates/patterns/details.html`
- `templates/tools/details.html`
- `templates/base.html`
- `static/js/theme.js`
- `docs/collaboration/user-learning-profile.md`

## Where We Stopped

Global CSS variables were updated for contrast and a more coherent retro palette. Contrast checks for the main text, label, link, nav, and button color pairs are above 4.5:1. The latest CSS pass reduced visual heaviness across typography, section spacing, inputs, buttons, tables, and chart controls while preserving the retro/cozy direction.

The CSS has also been cleaned after those changes: duplicate `.section`, `body`, `.page-shell`, and skein child-row overrides were consolidated, and unused old shadow/nav/title-tab tokens were removed.

The palette cleanup replaced several one-off colors that were visually inconsistent: mint chart buttons, cool gray cancel buttons, orange trash buttons, and scattered hardcoded pink table states now use shared retro palette tokens.

The detail heading/back-link layout was adjusted after visual review: the title tab lost its bottom rounding/shadow and overlaps the section by only the border width, while the back control uses the title-tab border color and sits closer to the tab baseline.

The yarn list now has a dedicated `.resource-list--yarn` and `.yarn-card` variant. The list width is capped and centered, and yarn cards with images use a compact text-left/image-right layout on narrow screens, then get more image width and spacing from the 640px breakpoint upward. The yarn grid uses `auto-fill`, not `auto-fit`, so a single yarn card does not stretch across the whole row.

Dark mode is now restored before first paint: `templates/base.html` runs a small inline script in `<head>` before `static/css/style.css`, and the theme class lives on `<html>` as `html.dark`. `static/js/theme.js` now uses `document.documentElement`, and the dark-mode selectors in `static/css/style.css` were updated accordingly.

## Next Small Step

Visually inspect the changed screens in the browser, especially the yarn list with many cards, detail pages, list pages with tables/cards, and the chart editor in light and dark mode.

## Open Questions

- Whether the light mode palette feels retro enough or should lean more pastel/candy.
- Whether chart editor controls should keep stronger playful shadows or be softened like the rest of the app.
