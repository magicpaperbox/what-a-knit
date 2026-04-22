const $ = (id) => document.getElementById(id);

const SVG_NS = "http://www.w3.org/2000/svg";

const SYMBOLS = [
  { id: "knit", label: "K on RS, P on WS" },
  { id: "purl", label: "P on RS, K on WS" },
  { id: "ssk", label: "Ssk" },
  { id: "k2tog", label: "k2tog" },
  { id: "yarn_over", label: "YO" },
  { id: "front_marker", label: "START" },
  { id: "no_stitch", label: "no stitch" },
];

const ALLOWED_SYMBOL_IDS = new Set(SYMBOLS.map((symbol) => symbol.id));

const state = {
  rows: 12,
  columns: 12,
  cellSize: 32,
  selectedSymbol: "purl",
  cells: [],
};

const LABEL_MARGIN_LEFT = 34;
const LABEL_MARGIN_BOTTOM = 30;
const LABEL_FONT_SIZE = 12;

function createSvgElement(tagName) {
  return document.createElementNS(SVG_NS, tagName);
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function getSymbol(symbolId) {
  return SYMBOLS.find((symbol) => symbol.id === symbolId);
}

function normalizeCells(rawCells, rows, columns) {
  const normalizedCells = [];
  for (let row = 0; row < rows; row += 1) {
    const sourceRow = Array.isArray(rawCells?.[row]) ? rawCells[row] : [];
    const normalizedRow = [];

    for (let column = 0; column < columns; column += 1) {
      const sourceValue = sourceRow[column];
      normalizedRow.push(ALLOWED_SYMBOL_IDS.has(sourceValue) && sourceValue !== "knit" ? sourceValue : null);
    }

    normalizedCells.push(normalizedRow);
  }

  return normalizedCells;
}

function readSerializedCells(rows, columns) {
  const serializedCells = $("cellsData").value;

  if (!serializedCells) {
    return normalizeCells([], rows, columns);
  }

  try {
    return normalizeCells(JSON.parse(serializedCells), rows, columns);
  } catch (error) {
    return normalizeCells([], rows, columns);
  }
}

function syncSerializedCells() {
  $("cellsData").value = JSON.stringify(state.cells);
}

function resizeCells(rows, columns) {
  const previousCells = state.cells;
  const resizedCells = [];

  for (let row = 0; row < rows; row += 1) {
    const rowCells = [];

    for (let column = 0; column < columns; column += 1) {
      rowCells.push(previousCells[row]?.[column] ?? null);
    }

    resizedCells.push(rowCells);
  }

  state.cells = resizedCells;
}

function drawCellSymbol(symbolId, layer, x, y, cellSize) {
  if (!symbolId || symbolId === "knit") {
    return;
  }

  if (symbolId === "front_marker" || symbolId === "no_stitch") {
    const fillRect = createSvgElement("rect");
    fillRect.setAttribute("x", x + 1);
    fillRect.setAttribute("y", y + 1);
    fillRect.setAttribute("width", Math.max(cellSize - 2, 0));
    fillRect.setAttribute("height", Math.max(cellSize - 2, 0));
    fillRect.setAttribute("fill", symbolId === "front_marker" ? "#39ff14" : "#b9b9b9");
    layer.appendChild(fillRect);
    return;
  }

  if (symbolId === "purl") {
    const dot = createSvgElement("circle");
    dot.classList.add("chart-symbol-fill");
    dot.setAttribute("cx", x + cellSize / 2);
    dot.setAttribute("cy", y + cellSize / 2);
    dot.setAttribute("r", Math.max(cellSize * 0.14, 3));
    layer.appendChild(dot);
    return;
  }

  if (symbolId === "yarn_over") {
    const ring = createSvgElement("circle");
    ring.classList.add("chart-symbol-stroke");
    ring.setAttribute("cx", x + cellSize / 2);
    ring.setAttribute("cy", y + cellSize / 2);
    ring.setAttribute("r", Math.max(cellSize * 0.18, 5));
    ring.setAttribute("fill", "none");
    ring.setAttribute("stroke-width", Math.max(cellSize * 0.07, 2));
    layer.appendChild(ring);
    return;
  }

  if (symbolId === "ssk" || symbolId === "k2tog") {
    const line = createSvgElement("line");
    line.classList.add("chart-symbol-stroke");
    const padding = cellSize * 0.24;

    if (symbolId === "ssk") {
      line.setAttribute("x1", x + padding);
      line.setAttribute("y1", y + padding);
      line.setAttribute("x2", x + cellSize - padding);
      line.setAttribute("y2", y + cellSize - padding);
    } else {
      line.setAttribute("x1", x + padding);
      line.setAttribute("y1", y + cellSize - padding);
      line.setAttribute("x2", x + cellSize - padding);
      line.setAttribute("y2", y + padding);
    }

    line.setAttribute("stroke-width", Math.max(cellSize * 0.07, 2));
    line.setAttribute("stroke-linecap", "round");
    layer.appendChild(line);
  }
}

function buildSymbolPreview(symbolId, size = 32) {
  const preview = createSvgElement("svg");
  preview.setAttribute("viewBox", `0 0 ${size} ${size}`);
  preview.setAttribute("width", size);
  preview.setAttribute("height", size);
  preview.classList.add("chart-symbol-preview");

  const frame = createSvgElement("rect");
  frame.classList.add("chart-preview-frame");
  frame.setAttribute("x", 0.5);
  frame.setAttribute("y", 0.5);
  frame.setAttribute("width", size - 1);
  frame.setAttribute("height", size - 1);
  preview.appendChild(frame);

  drawCellSymbol(symbolId, preview, 0, 0, size);
  return preview;
}

function renderSymbolPalette() {
  const palette = $("symbolPalette");
  const selectedSymbol = getSymbol(state.selectedSymbol);

  palette.innerHTML = "";

  SYMBOLS.forEach((symbol) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "chart-symbol-button";
    button.dataset.symbolId = symbol.id;
    button.setAttribute("aria-label", symbol.label);
    button.setAttribute("title", symbol.label);
    button.setAttribute("role", "listitem");

    if (symbol.id === state.selectedSymbol) {
      button.classList.add("is-active");
      button.setAttribute("aria-pressed", "true");
    } else {
      button.setAttribute("aria-pressed", "false");
    }

    button.appendChild(buildSymbolPreview(symbol.id));

    const label = document.createElement("span");
    label.className = "chart-symbol-button-copy";
    label.textContent = symbol.label;
    button.appendChild(label);

    button.addEventListener("click", () => {
      state.selectedSymbol = symbol.id;
      renderSymbolPalette();
    });

    palette.appendChild(button);
  });

  $("selectedSymbolLabel").textContent = `Selected: ${selectedSymbol.label}`;
}

function renderChart() {
  const svg = $("chart");
  const gridWidth = state.columns * state.cellSize;
  const gridHeight = state.rows * state.cellSize;
  const width = LABEL_MARGIN_LEFT + gridWidth;
  const height = gridHeight + LABEL_MARGIN_BOTTOM;
  const gridOriginX = LABEL_MARGIN_LEFT;
  const gridOriginY = 0;

  svg.setAttribute("width", width.toString());
  svg.setAttribute("height", height.toString());
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.innerHTML = "";

  const labelsLayer = createSvgElement("g");
  const symbolsLayer = createSvgElement("g");
  const gridLayer = createSvgElement("g");
  const hitLayer = createSvgElement("g");
  const border = createSvgElement("rect");

  labelsLayer.classList.add("chart-labels-layer");
  labelsLayer.setAttribute("font-size", LABEL_FONT_SIZE.toString());
  labelsLayer.setAttribute("font-family", "Arial, sans-serif");

  gridLayer.classList.add("chart-grid-layer");
  gridLayer.setAttribute("stroke-width", "1");
  gridLayer.setAttribute("shape-rendering", "crispEdges");

  for (let row = 0; row < state.rows; row += 1) {
    for (let column = 0; column < state.columns; column += 1) {
      const x = gridOriginX + column * state.cellSize;
      const y = gridOriginY + row * state.cellSize;
      drawCellSymbol(state.cells[row][column], symbolsLayer, x, y, state.cellSize);

      const hitRect = createSvgElement("rect");
      hitRect.setAttribute("x", x);
      hitRect.setAttribute("y", y);
      hitRect.setAttribute("width", state.cellSize);
      hitRect.setAttribute("height", state.cellSize);
      hitRect.setAttribute("fill", "transparent");
      hitRect.classList.add("chart-cell-hit");
      hitRect.dataset.row = row.toString();
      hitRect.dataset.column = column.toString();
      hitLayer.appendChild(hitRect);
    }
  }

  for (let column = 0; column <= state.columns; column += 1) {
    const x = gridOriginX + column * state.cellSize;
    const line = createSvgElement("line");
    line.setAttribute("x1", x);
    line.setAttribute("y1", gridOriginY);
    line.setAttribute("x2", x);
    line.setAttribute("y2", gridOriginY + gridHeight);
    gridLayer.appendChild(line);
  }

  for (let row = 0; row <= state.rows; row += 1) {
    const y = gridOriginY + row * state.cellSize;
    const line = createSvgElement("line");
    line.setAttribute("x1", gridOriginX);
    line.setAttribute("y1", y);
    line.setAttribute("x2", gridOriginX + gridWidth);
    line.setAttribute("y2", y);
    gridLayer.appendChild(line);
  }

  for (let column = 0; column < state.columns; column += 1) {
    const label = createSvgElement("text");
    const x = gridOriginX + column * state.cellSize + state.cellSize / 2;
    const y = gridOriginY + gridHeight + 18;
    label.setAttribute("x", x);
    label.setAttribute("y", y);
    label.setAttribute("text-anchor", "middle");
    label.textContent = (column + 1).toString();
    labelsLayer.appendChild(label);
  }

  for (let row = 0; row < state.rows; row += 1) {
    const label = createSvgElement("text");
    const x = gridOriginX - 10;
    const y = gridOriginY + gridHeight - row * state.cellSize - state.cellSize / 2;
    label.setAttribute("x", x);
    label.setAttribute("y", y);
    label.setAttribute("text-anchor", "end");
    label.setAttribute("dominant-baseline", "middle");
    label.textContent = (row + 1).toString();
    labelsLayer.appendChild(label);
  }

  border.setAttribute("x", gridOriginX);
  border.setAttribute("y", gridOriginY);
  border.setAttribute("width", gridWidth);
  border.setAttribute("height", gridHeight);
  border.classList.add("chart-grid-border");
  border.setAttribute("fill", "none");
  border.setAttribute("stroke-width", "2");

  svg.appendChild(labelsLayer);
  svg.appendChild(symbolsLayer);
  svg.appendChild(gridLayer);
  svg.appendChild(border);
  svg.appendChild(hitLayer);
  syncSerializedCells();
}

function handleChartClick(event) {
  const cell = event.target.closest(".chart-cell-hit");

  if (!cell) {
    return;
  }

  const row = Number(cell.dataset.row);
  const column = Number(cell.dataset.column);

  state.cells[row][column] = state.selectedSymbol === "knit" ? null : state.selectedSymbol;
  renderChart();
}

function rebuild() {
  state.rows = clamp(parseInt($("rows").value, 10) || 1, 1, 200);
  state.columns = clamp(parseInt($("columns").value, 10) || 1, 1, 200);
  state.cellSize = clamp(parseInt($("cellSize").value, 10) || 32, 10, 80);

  $("rows").value = state.rows;
  $("columns").value = state.columns;
  $("cellSize").value = state.cellSize;

  resizeCells(state.rows, state.columns);
  renderChart();
}

function handleFormSubmit() {
  rebuild();
}

function init() {
  state.rows = clamp(parseInt($("rows").value, 10) || 12, 1, 200);
  state.columns = clamp(parseInt($("columns").value, 10) || 12, 1, 200);
  state.cellSize = clamp(parseInt($("cellSize").value, 10) || 32, 10, 80);
  state.cells = readSerializedCells(state.rows, state.columns);

  renderSymbolPalette();
  rebuild();

  $("build").addEventListener("click", rebuild);
  $("chart").addEventListener("click", handleChartClick);
  $("chartEditorForm").addEventListener("submit", handleFormSubmit);
}

init();
