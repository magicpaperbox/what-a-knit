# Task: Chart Area Selection

Started: 2026-08-27
Status: in progress

## Goal

Add temporary area selection to the chart editor: the user drags over cells, sees the selected rectangle, releases the pointer, and the selected area stays highlighted in the current in-browser state.
The selected area will later drive commands such as bucket fill, copy, paste, cut, recolor, rotate, mirror, and possibly zoom-related drag boxes.

## Current Context

The chart editor already supports hover labels for the current row and column using `state.hoveredRow` and `state.hoveredColumn`.
The chart editor also already has drag painting through pointer events and `state.isPainting`.
Area selection should not immediately paint cells. It should be separate from paint/erase behavior.
The selection must be represented as reusable data, not only as a visual SVG highlight.

## Decisions Made

- Selection should be a temporary frontend state first, not saved to the backend yet.
- The selected area should remain highlighted after releasing the pointer.
- Row and column labels should highlight for the selected rectangle, not only for the currently hovered cell.
- The screenshot is visual reference only; its behavior is not copied exactly because it immediately applies color on release.
- Finished selection should be usable by later commands: bucket fill, copy, paste with overwrite, cut, recolor, rotate, and mirror.
- Copy/paste should likely use a separate chart clipboard state storing a 2D cell matrix copied from the selected area.
- Zoom drag selection should reuse shared rectangle/bounds helper logic where useful, but remain a separate interaction because it should zoom rather than create a persistent edit selection.
- Selection should become active only after the user chooses the Select tool. The default tool should keep the current paint/draw behavior.

## Relevant Files

- `static/js/charts.js`
- `static/css/charts/svg.css`
- `static/css/charts/palette.css`

## Where We Stopped

Do not make selection depend on the future command. Selection should only answer "which rectangle of cells is selected?"
`static/js/charts.js` now has initial selection-related state fields: `selectionStart`, `selectionEnd`, `selectedArea`, and `chartClipboard`, all initialized to `null`.
`static/js/charts.js` now also has a main `TOOLS` entry for `cursor` and a `state.activeTool` initialized to `"cursor"`.
The tool buttons are rendered from `TOOLS` in `static/js/charts.js`. The click handler sets `state.activeTool`, loops over the result of `querySelectorAll(".chart-tool-button")` to remove `is-active` and set `aria-pressed` to `false`, then adds `is-active` and sets `aria-pressed` to `true` on the clicked button.
On 2026-08-31, the non-cursor guard is correctly placed in `handleChartPointerDown`, after the position guard and before painting starts. It sets `state.isPainting = false`, then a nested Select-only condition stores `position` in both `state.selectionStart` and `state.selectionEnd`, and the guard returns without painting. The misplaced guard was removed from `handleChartPointerMove`. Both endpoint assignments have been reviewed and are correct: a new selection initially starts and ends at the clicked cell. Browser behavior has not yet been verified.
Selection dragging is correctly connected: `state.isSelecting` starts as `false`, becomes `true` in the Select branch of `handleChartPointerDown`, gates updates to `state.selectionEnd` in `handleChartPointerMove`, and is reset in `handleChartPointerUp` without clearing the endpoints. The syntax check passed at that stage. The earlier extra indentation in the selection condition has been corrected.
`getSelectionBounds` is correct and does not change `state`. It returns `startPoint: {minRow, minColumn}` and `endPoint: {maxRow, maxColumn}`; preserve this nested result shape. `renderChart` calls the helper and stores the result in `bounds`. The user supplied a console screenshot showing row bounds 0–0 and column bounds 0–3, which describe four cells. Reverse dragging and behavior after release were not independently verified from that screenshot.
The user implemented creation of `selectionRect`, its correct pixel geometry, and the `chart-selection` class inside `if (bounds)` after appending the chart border. The rectangle is now appended to `svg` before the hit layer, and the user confirms selection works. The user explicitly asked the agent to implement CSS only, then requested a more visible matching color. `.chart-selection` in `static/css/charts/svg.css` now uses `--accent-strong` for a raspberry outline in the light theme and a lighter pink outline in the dark theme, plus `--accent-wash-strong` for a translucent pink fill. It retains `stroke-width: 2px` and `pointer-events: none`. The stylesheet is already imported by `static/css/charts.css`. No JavaScript was edited by the agent; the new colors have not been visually verified in the browser.

The user added `renderChart()` after setting `state.selectionEnd` in the Select branch of `handleChartPointerDown` and confirms it works. At the user's request, the agent styled the Tools buttons in `static/css/charts/palette.css`: two equal columns, theme-aware cream/plum backgrounds, a pink active state with a solid inset bottom edge, hover feedback, and a visible keyboard focus outline. Existing JavaScript `.is-active` and `aria-pressed` behavior is unchanged. Browser checks passed for switching the active button, keyboard focus, both themes, and a 375px viewport.

## Next Small Step

The requested Tools styling is complete. The user is resuming selection work and owns the JavaScript implementation. The current step is selected column label highlighting in `renderChart`'s column-label loop: keep hover detection, check that `bounds` exists and `column` lies inclusively between `bounds.startPoint.minColumn` and `bounds.endPoint.maxColumn`, then highlight for hover OR selection using the existing drawing calls. Verify selected column labels remain highlighted after moving the pointer away. Row labels follow as a separate coherent step because their numbering is reversed relative to cell indices.

## Open Questions

- Should copy/paste preserve empty cells as overwrites, or skip empty cells when pasting?
