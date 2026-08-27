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

## Relevant Files

- `static/js/charts.js`
- `static/css/style.css`

## Where We Stopped

The next work should start in `static/js/charts.js` by adding selection state separate from `state.isPainting`.
Do not make selection depend on the future command. Selection should only answer "which rectangle of cells is selected?"

## Next Small Step

Add frontend state fields for selection start, selection end, the finalized selected area, and a chart clipboard for later copy/paste work.

## Open Questions

- Should selection mode be always active, or should it later become a separate tool beside paint/erase?
- Should copy/paste preserve empty cells as overwrites, or skip empty cells when pasting?
