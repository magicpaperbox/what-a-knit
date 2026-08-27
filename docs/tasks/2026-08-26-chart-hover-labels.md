# Task: Chart Hover Labels

Started: 2026-08-26
Status: in progress

## Goal

Make the chart editor clearly show which row and column the pointer is currently over.

## Current Context

The chart editor already tracks the hovered cell in `state.hoveredRow` and `state.hoveredColumn`.
Hover labels are rendered in SVG by `renderChart()` using a small highlight behind the active row and column numbers.
The highlight is now a real SVG `circle`, not a rounded `rect`, so it looks more circular and avoids the clipped bottom edge.

## Decisions Made

- Hover should work even when the user is only moving the pointer, not painting.
- Row labels need reversed-index comparison because `dataset.row` counts from the top, while chart row labels are displayed from the bottom.
- The visible label marker should be smaller, light green, and borderless.

## Relevant Files

- `static/js/charts.js`
- `static/css/style.css`

## Where We Stopped

`static/js/charts.js` uses `drawLabelHighlight(...)` to draw a light green SVG circle behind the hovered row/column label.
`static/css/style.css` defines the hover label colors through chart label CSS variables.
`node --check static/js/charts.js` passes.

## Next Small Step

Visually test the chart editor in the browser and adjust `LABEL_HIGHLIGHT_RADIUS` if the circles still feel too large or small.

## Open Questions

- Should the app also highlight the entire hovered row/column grid line, or only the row/column numbers?
