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
  kind: "symbol",
  selectedColor: "#000000",
};

const LABEL_MARGIN_LEFT = 34;
const LABEL_MARGIN_BOTTOM = 30;
const LABEL_FONT_SIZE = 12;

// Shared helpers

function createSvgElement(tagName) {
  return document.createElementNS(SVG_NS, tagName);
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function getSymbol(symbolId) {
  return SYMBOLS.find((symbol) => symbol.id === symbolId);
}

// Cell state helpers

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

function getUsedColors() {
  const colors = new Set();

  for (const row of state.cells) {
    for (const cell of row) {
      if (cell !== null && cell.startsWith("#")) {
        colors.add(cell);
      }
    }
  }

  return Array.from(colors);
}

// Symbol drawing and palette

function drawCellSymbol(symbolId, layer, x, y, cellSize) {
  if (!symbolId || symbolId === "knit") {
    return;
  }

  if (symbolId === "front_marker" || symbolId === "no_stitch") {
    const fillRect = createSvgElement("rect");
    fillRect.setAttribute("x", x + 1);
    fillRect.setAttribute("y", y + 1);
    fillRect.setAttribute("width", Math.max(cellSize - 2, 0).toString());
    fillRect.setAttribute("height", Math.max(cellSize - 2, 0).toString());
    fillRect.setAttribute("fill", symbolId === "front_marker" ? "#39ff14" : "#b9b9b9");
    layer.appendChild(fillRect);
    return;
  }

  if (symbolId === "purl") {
    const dot = createSvgElement("circle");
    dot.classList.add("chart-symbol-fill");
    dot.setAttribute("cx", x + cellSize / 2);
    dot.setAttribute("cy", y + cellSize / 2);
    dot.setAttribute("r", Math.max(cellSize * 0.14, 3).toString());
    layer.appendChild(dot);
    return;
  }

  if (symbolId === "yarn_over") {
    const ring = createSvgElement("circle");
    ring.classList.add("chart-symbol-stroke");
    ring.setAttribute("cx", x + cellSize / 2);
    ring.setAttribute("cy", y + cellSize / 2);
    ring.setAttribute("r", Math.max(cellSize * 0.18, 5).toString());
    ring.setAttribute("fill", "none");
    ring.setAttribute("stroke-width", Math.max(cellSize * 0.07, 2).toString());
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
      line.setAttribute("x2", (x + cellSize - padding).toString());
      line.setAttribute("y2", (y + cellSize - padding).toString());
    } else {
      line.setAttribute("x1", (x + padding).toString());
      line.setAttribute("y1", (y + cellSize - padding).toString());
      line.setAttribute("x2", (x + cellSize - padding).toString());
      line.setAttribute("y2", y + padding);
    }

    line.setAttribute("stroke-width", Math.max(cellSize * 0.07, 2).toString());
    line.setAttribute("stroke-linecap", "round");
    layer.appendChild(line);
  }
}

function buildSymbolPreview(symbolId, size = 32) {
  const preview = createSvgElement("svg");
  preview.setAttribute("viewBox", `0 0 ${size} ${size}`);
  preview.setAttribute("width", size.toString());
  preview.setAttribute("height", size.toString());
  preview.classList.add("chart-symbol-preview");

  const frame = createSvgElement("rect");
  frame.classList.add("chart-preview-frame");
  frame.setAttribute("x", (0.5).toString());
  frame.setAttribute("y", (0.5).toString());
  frame.setAttribute("width", (size - 1).toString());
  frame.setAttribute("height", (size - 1).toString());
  preview.appendChild(frame);

  drawCellSymbol(symbolId, preview, 0, 0, size);
  return preview;
}

function renderSymbolPalette() {
  const palette = $("chartPalette");
  const selectedSymbol = getSymbol(state.selectedSymbol);
  const paletteTitle = $("chartPaletteTitle");
  const paletteSummary = $("chartPaletteSummary");

  palette.innerHTML = "";
  palette.className = "chart-palette chart-palette--symbols";
  paletteTitle.innerHTML = "Symbols";

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

  paletteSummary.textContent = `Selected: ${selectedSymbol.label}`;
}

// Color drawing and palette

function drawCellColor(color, layer, x, y, cellSize) {
  if (color === null || !color.startsWith("#")) {
    return;
  }

  const fillRect = createSvgElement("rect");
  fillRect.setAttribute("x", (x + 1).toString());
  fillRect.setAttribute("y", (y + 1).toString());
  fillRect.setAttribute("width", Math.max(cellSize - 2, 0).toString());
  fillRect.setAttribute("height", Math.max(cellSize - 2, 0).toString());
  fillRect.setAttribute("fill", color);
  layer.appendChild(fillRect);
}

function renderColorPalette() {
  const palette = $("chartPalette");
  const paletteSummary = $("chartPaletteSummary");
  const paletteTitle = $("chartPaletteTitle");
  const usedColors = getUsedColors();

  paletteTitle.innerHTML = "Colors";
  palette.innerHTML = "";
  palette.className = "chart-palette chart-palette--colors";

  const colorInput = document.createElement("input");
  colorInput.type = "color";
  colorInput.className = "chart-color-picker";
  colorInput.setAttribute("aria-label", "Pick a color");
  colorInput.value = state.selectedColor;
  colorInput.addEventListener("input", () => {
    state.selectedColor = colorInput.value;
    paletteSummary.textContent = `Selected: ${state.selectedColor}`;
  });

  palette.appendChild(colorInput);
  paletteSummary.textContent = `Selected: ${state.selectedColor}`;

  usedColors.forEach((color) => {
    const colorButton = document.createElement("button");
    colorButton.type = "button";
    colorButton.className = "chart-color-button";
    colorButton.setAttribute("aria-label", `Select ${color}`);
    colorButton.setAttribute("title", color);
    colorButton.setAttribute("role", "listitem");

    if (color === state.selectedColor) {
      colorButton.classList.add("is-active");
      colorButton.setAttribute("aria-pressed", "true");
    } else {
      colorButton.setAttribute("aria-pressed", "false");
    }

    const colorSwatch = document.createElement("span");
    colorSwatch.className = "chart-color-swatch";
    colorSwatch.style.backgroundColor = color;
    colorButton.appendChild(colorSwatch);

    const colorLabel = document.createElement("span");
    colorLabel.className = "chart-color-button-label";
    colorLabel.textContent = color;
    colorButton.appendChild(colorLabel);

    colorButton.addEventListener("click", () => {
      state.selectedColor = color;
      renderColorPalette();
    });
    palette.appendChild(colorButton);
  });

}

// Chart rendering

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

      if (state.kind === "symbol") {
        drawCellSymbol(state.cells[row][column], symbolsLayer, x, y, state.cellSize);
      }

      if (state.kind === "color") {
        drawCellColor(state.cells[row][column], symbolsLayer, x, y, state.cellSize);
      }

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
    line.setAttribute("x1", x.toString());
    line.setAttribute("y1", gridOriginY.toString());
    line.setAttribute("x2", x.toString());
    line.setAttribute("y2", (gridOriginY + gridHeight).toString());
    gridLayer.appendChild(line);
  }

  for (let row = 0; row <= state.rows; row += 1) {
    const y = gridOriginY + row * state.cellSize;
    const line = createSvgElement("line");
    line.setAttribute("x1", gridOriginX.toString());
    line.setAttribute("y1", y.toString());
    line.setAttribute("x2", (gridOriginX + gridWidth).toString());
    line.setAttribute("y2", y.toString());
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

  border.setAttribute("x", gridOriginX.toString());
  border.setAttribute("y", gridOriginY.toString());
  border.setAttribute("width", gridWidth.toString());
  border.setAttribute("height", gridHeight.toString());
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

// User actions

function handleChartClick(event) {
  const cell = event.target.closest(".chart-cell-hit");

  if (!cell) {
    return;
  }

  const row = Number(cell.dataset.row);
  const column = Number(cell.dataset.column);

  if (state.kind === "symbol") {
    state.cells[row][column] = state.selectedSymbol === "knit" ? null : state.selectedSymbol;
  } else {
    state.cells[row][column] = state.selectedColor;
  }

  renderChart();
  if (state.kind === "color"){
    renderColorPalette()
  }
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

// Initialization

function init() {
  state.rows = clamp(parseInt($("rows").value, 10) || 12, 1, 200);
  state.columns = clamp(parseInt($("columns").value, 10) || 12, 1, 200);
  state.cellSize = clamp(parseInt($("cellSize").value, 10) || 32, 10, 80);
  state.cells = readSerializedCells(state.rows, state.columns);

  const selectedKindInput = document.querySelector('input[name="kind"]:checked');
  if (selectedKindInput) {
    state.kind = selectedKindInput.value;
  }

  if (state.kind === "symbol") {
    renderSymbolPalette();
  }

  if (state.kind === "color") {
    renderColorPalette();
  }

  const kindInputs = document.querySelectorAll('input[name="kind"]');
  kindInputs.forEach((input) => {
    input.addEventListener("change", () => {
      state.kind = input.value;

      if (state.kind === "symbol") {
        renderSymbolPalette();
      } else {
        renderColorPalette();
      }
      renderChart();
    });
  });

  rebuild();

  $("build").addEventListener("click", rebuild);
  $("chart").addEventListener("click", handleChartClick);
  $("chartEditorForm").addEventListener("submit", handleFormSubmit);
}

init();
