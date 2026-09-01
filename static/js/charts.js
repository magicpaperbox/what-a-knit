const $ = (id) => document.getElementById(id);

const SVG_NS = "http://www.w3.org/2000/svg";

const TOOLS = [
    {id: "cursor", label: "cursor"},
    {id: "zoom", label: "zoom"},
    {id: "select", label: "select tool"},
    {id: "rotate_selected", label: "rotate selected"}
];

const SYMBOLS = [
    {id: "knit", label: "K on RS, P on WS"},
    {id: "purl", label: "P on RS, K on WS"},
    {id: "ssk", label: "Ssk"},
    {id: "k2tog", label: "k2tog"},
    {id: "yarn_over", label: "YO"},
    {id: "front_marker", label: "START"},
    {id: "no_stitch", label: "no stitch"},
];

const COLOR_TOOLS = [
    {id: "paint", label: "Paint", icon: "/static/icons/paint-brush.png"},
    {id: "erase", label: "Erase", icon: "/static/icons/eraser.png"},
];

const ALLOWED_SYMBOL_IDS = new Set(SYMBOLS.map((symbol) => symbol.id));

const state = {
    rows: 12,
    columns: 12,
    cellSize: 32,
    selectedSymbol: "purl",
    cells: [],
    activeTool: "cursor",
    kind: "symbol",
    colorTool: "paint",
    selectedColor: "#000000",
    isPainting: false,
    hoveredRow: null,
    hoveredColumn: null,
    isSelecting: false,
    selectionStart: null,
    selectionEnd: null,
    selectedArea: null,
    chartClipboard: null,
};

const LABEL_MARGIN_LEFT = 34;
const LABEL_MARGIN_BOTTOM = 30;
const LABEL_FONT_SIZE = 12;
const LABEL_HIGHLIGHT_RADIUS = 11;
const LABEL_HIGHLIGHT_OFFSET_Y = -1;

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

function getSelectionBounds(start, end) {
    if (!start || !end) {
        return null;
    }

    const minRow = Math.min(start.row, end.row);
    const maxRow = Math.max(start.row, end.row);
    const minColumn = Math.min(start.column, end.column);
    const maxColumn = Math.max(start.column, end.column);

    const startPoint = {minRow: minRow, minColumn: minColumn}
    const endPoint = {maxRow: maxRow, maxColumn: maxColumn}

    return {startPoint, endPoint}
}

// Cell state helpers

// resize chart and validate cells
function normalizeCells(rawCells, rows, columns) {
    const normalizedCells = [];

    for (let row = 0; row < rows; row += 1) {
        const sourceRow = Array.isArray(rawCells?.[row]) ? rawCells[row] : [];
        const normalizedRow = [];

        for (let column = 0; column < columns; column += 1) {
            const sourceValue = sourceRow[column];
            if (state.kind === "symbol") {
                normalizedRow.push(ALLOWED_SYMBOL_IDS.has(sourceValue) && sourceValue !== "knit" ? sourceValue : null);
            }
            if (state.kind === "color") {
                normalizedRow.push(typeof sourceValue === "string" && /^#[a-fA-F0-9]{6}$/.test(sourceValue) ? sourceValue : null);
            }
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

function drawLabelHighlight(layer, x, y) {
    const highlight = createSvgElement("circle");
    highlight.classList.add("chart-label-highlight");
    highlight.setAttribute("cx", x.toString());
    highlight.setAttribute("cy", (y + LABEL_HIGHLIGHT_OFFSET_Y).toString());
    highlight.setAttribute("r", LABEL_HIGHLIGHT_RADIUS.toString());
    layer.appendChild(highlight);
}

function drawLabelSelectionBar(layer, x, y, width, height) {
    const highlight = createSvgElement("rect");
    const radius = Math.min(width, height) / 2;
    highlight.classList.add("chart-label-selection-highlight");
    highlight.setAttribute("x", x.toString());
    highlight.setAttribute("y", y.toString());
    highlight.setAttribute("width", width.toString());
    highlight.setAttribute("height", height.toString());
    highlight.setAttribute("rx", radius.toString());
    highlight.setAttribute("ry", radius.toString());
    layer.appendChild(highlight);
}

// Symbol drawing and palette

function drawCellSymbol(symbolId, layer, x, y, cellSize) {
    if (!symbolId || symbolId === "knit") {
        return;
    }

    if (symbolId === "front_marker" || symbolId === "no_stitch") {
        const fillRect = createSvgElement("rect");
        fillRect.setAttribute("x", x + 2);
        fillRect.setAttribute("y", y + 2);
        fillRect.setAttribute("width", Math.max(cellSize - 1, 0).toString());
        fillRect.setAttribute("height", Math.max(cellSize - 1, 0).toString());
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
    fillRect.setAttribute("x", x.toString());
    fillRect.setAttribute("y", y.toString());
    fillRect.setAttribute("width", cellSize.toString());
    fillRect.setAttribute("height", cellSize.toString());
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

    const colorTools = document.createElement("div");
    colorTools.className = "chart-color-tools";

    COLOR_TOOLS.forEach((tool) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "chart-color-tool-button";
        button.dataset.colorTool = tool.id;
        button.setAttribute("aria-label", tool.label);
        button.setAttribute("title", tool.label);
        button.setAttribute("role", "listitem");

        if (tool.id === state.colorTool) {
            button.classList.add("is-active")
            button.setAttribute("aria-pressed", "true");
        } else {
            button.setAttribute("aria-pressed", "false");
        }

        const icon = document.createElement("img");
        icon.className = "chart-color-tool-icon";
        icon.src = tool.icon;
        icon.alt = "";
        icon.setAttribute("aria-hidden", "true");
        button.appendChild(icon);

        const label = document.createElement("span");
        label.className = "chart-color-tool-label";
        label.textContent = tool.label;
        button.appendChild(label);

        button.addEventListener("click", () => {
            state.colorTool = tool.id;
            renderColorPalette()
        });
        colorTools.appendChild(button);
    });

    palette.appendChild(colorTools);

    const colorInput = document.createElement("input");
    colorInput.type = "color";
    colorInput.className = "chart-color-picker";
    colorInput.setAttribute("aria-label", "Pick a color");
    colorInput.value = state.selectedColor;
    colorInput.addEventListener("input", () => {
        state.colorTool = "paint";
        state.selectedColor = colorInput.value;
        paletteSummary.textContent = `Selected: ${state.selectedColor}`;
    });
    colorInput.addEventListener("change", () => {
        renderColorPalette();
    });


    palette.appendChild(colorInput);
    paletteSummary.textContent = `Selected: ${state.selectedColor}`;

    const colorSwatches = document.createElement("div");
    colorSwatches.className = "chart-color-swatches";

    usedColors.forEach((color) => {
        const colorButton = document.createElement("button");
        colorButton.type = "button";
        colorButton.className = "chart-color-button";
        colorButton.setAttribute("aria-label", `Select ${color}`);
        colorButton.setAttribute("title", color);
        colorButton.setAttribute("role", "listitem");

        if (color === state.selectedColor && state.colorTool === "paint") {
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
            state.colorTool = "paint";
            state.selectedColor = color;
            renderColorPalette();
        });
        colorSwatches.appendChild(colorButton);
    });

    if (usedColors.length > 0) {
        palette.appendChild(colorSwatches);
    }
}

// Chart rendering

function renderChart() {
    const gridWidth = state.columns * state.cellSize;
    const gridHeight = state.rows * state.cellSize;
    const width = LABEL_MARGIN_LEFT + gridWidth;
    const height = gridHeight + LABEL_MARGIN_BOTTOM;
    const gridOriginX = LABEL_MARGIN_LEFT;
    const gridOriginY = 0;
    const bounds = getSelectionBounds(state.selectionStart, state.selectionEnd);

    function createSymbolAndHitLayers() {
        const symbolsLayer = createSvgElement("g");
        const hitLayer = createSvgElement("g");

        function createHitRect(x, y, row, column) {
            const hitRect = createSvgElement("rect");
            hitRect.setAttribute("x", x.toString());
            hitRect.setAttribute("y", y.toString());
            hitRect.setAttribute("width", state.cellSize);
            hitRect.setAttribute("height", state.cellSize);
            hitRect.setAttribute("fill", "transparent");
            hitRect.classList.add("chart-cell-hit");
            hitRect.dataset.row = row.toString();
            hitRect.dataset.column = column.toString();
            return hitRect;
        }

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
                hitLayer.appendChild(createHitRect(x, y, row, column));
            }
        }
        return {hitLayer, symbolsLayer};
    }

    function createLabelsLayer(bounds) {
        const labelsLayer = createSvgElement("g");
        labelsLayer.classList.add("chart-labels-layer");
        labelsLayer.setAttribute("font-size", LABEL_FONT_SIZE.toString());
        labelsLayer.setAttribute("font-family", "Arial, sans-serif");
        const columnLabelY = gridOriginY + gridHeight + 18;
        const rowLabelX = gridOriginX - 17;

        if (bounds !== null) {
            const selectionBarX =
                gridOriginX +
                bounds.startPoint.minColumn * state.cellSize +
                state.cellSize / 2 -
                LABEL_HIGHLIGHT_RADIUS;
            const selectionBarY =
                columnLabelY + LABEL_HIGHLIGHT_OFFSET_Y - LABEL_HIGHLIGHT_RADIUS;
            const selectionBarWidth =
                (bounds.endPoint.maxColumn - bounds.startPoint.minColumn) * state.cellSize +
                LABEL_HIGHLIGHT_RADIUS * 2;
            const selectionBarHeight = LABEL_HIGHLIGHT_RADIUS * 2;

            drawLabelSelectionBar(
                labelsLayer,
                selectionBarX,
                selectionBarY,
                selectionBarWidth,
                selectionBarHeight,
            );

            const rowSelectionBarX = rowLabelX - LABEL_HIGHLIGHT_RADIUS;
            const rowSelectionBarY =
                gridOriginY +
                bounds.startPoint.minRow * state.cellSize +
                state.cellSize / 2 +
                LABEL_HIGHLIGHT_OFFSET_Y -
                LABEL_HIGHLIGHT_RADIUS;
            const rowSelectionBarWidth = LABEL_HIGHLIGHT_RADIUS * 2;
            const rowSelectionBarHeight =
                (bounds.endPoint.maxRow - bounds.startPoint.minRow) * state.cellSize +
                LABEL_HIGHLIGHT_RADIUS * 2;

            drawLabelSelectionBar(
                labelsLayer,
                rowSelectionBarX,
                rowSelectionBarY,
                rowSelectionBarWidth,
                rowSelectionBarHeight,
            );
        }

        for (let column = 0; column < state.columns; column += 1) {
            const label = createSvgElement("text");
            const labelText = (column + 1).toString();
            const x = gridOriginX + column * state.cellSize + state.cellSize / 2;
            const y = columnLabelY;

            label.setAttribute("x", x.toString());
            label.setAttribute("y", y.toString());
            label.setAttribute("text-anchor", "middle");
            label.setAttribute("dominant-baseline", "middle");
            label.textContent = labelText;
            const isSelectedColumn =
                bounds !== null &&
                column >= bounds.startPoint.minColumn &&
                column <= bounds.endPoint.maxColumn;

            const isHoveredColumn =
                state.hoveredColumn !== null && column === state.hoveredColumn;

            if (isHoveredColumn && !isSelectedColumn) {
                drawLabelHighlight(labelsLayer, x, y);
            }

            if (isHoveredColumn || isSelectedColumn) {
                label.classList.add("chart-label--hovered");
            }

            labelsLayer.appendChild(label);
        }

        for (let row = 0; row < state.rows; row += 1) {
            const label = createSvgElement("text");
            const labelText = (row + 1).toString();
            const gridRow = state.rows - 1 - row;
            const x = rowLabelX;
            const y = gridOriginY + gridHeight - row * state.cellSize - state.cellSize / 2;
            label.setAttribute("x", x.toString());
            label.setAttribute("y", y.toString());
            label.setAttribute("text-anchor", "middle");
            label.setAttribute("dominant-baseline", "middle");
            label.textContent = labelText;
            const isSelectedRow =
                bounds !== null &&
                gridRow >= bounds.startPoint.minRow &&
                gridRow <= bounds.endPoint.maxRow;

            const isHoveredRow =
                state.hoveredRow !== null && gridRow === state.hoveredRow;

            if (isHoveredRow && !isSelectedRow) {
                drawLabelHighlight(labelsLayer, x, y);
            }

            if (isHoveredRow || isSelectedRow) {
                label.classList.add("chart-label--hovered");
            }

            labelsLayer.appendChild(label);
        }
        return labelsLayer;
    }

    function createGridLayer() {
        const gridLayer = createSvgElement("g");
        gridLayer.classList.add("chart-grid-layer");
        gridLayer.setAttribute("stroke-width", "1");
        gridLayer.setAttribute("shape-rendering", "crispEdges");

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
        return gridLayer;
    }

    function createBorderLayer() {
        const border = createSvgElement("rect");
        border.setAttribute("x", gridOriginX.toString());
        border.setAttribute("y", gridOriginY.toString());
        border.setAttribute("width", gridWidth.toString());
        border.setAttribute("height", gridHeight.toString());
        border.classList.add("chart-grid-border");
        border.setAttribute("fill", "none");
        border.setAttribute("stroke-width", "2");
        return border;
    }

    function createSelectionRect(bounds) {
        if (!bounds) {
            return;
        }
        const selectionRect = createSvgElement("rect");
        selectionRect.setAttribute("x", (gridOriginX + bounds.startPoint.minColumn * state.cellSize).toString());
        selectionRect.setAttribute("y", (gridOriginY + bounds.startPoint.minRow * state.cellSize).toString());
        selectionRect.setAttribute("width", ((bounds.endPoint.maxColumn - bounds.startPoint.minColumn + 1) * state.cellSize).toString())
        selectionRect.setAttribute("height", ((bounds.endPoint.maxRow - bounds.startPoint.minRow + 1) * state.cellSize).toString())
        selectionRect.classList.add("chart-selection");
        return selectionRect;
    }

    const svg = $("chart");
    svg.setAttribute("width", width.toString());
    svg.setAttribute("height", height.toString());
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    svg.innerHTML = "";

    const {hitLayer, symbolsLayer} = createSymbolAndHitLayers();
    svg.appendChild(createLabelsLayer(bounds));
    svg.appendChild(symbolsLayer);
    svg.appendChild(createGridLayer());
    svg.appendChild(createBorderLayer());
    const selectionRect = createSelectionRect(bounds);
    if (selectionRect) {
        svg.appendChild(selectionRect);
    }
    svg.appendChild(hitLayer);

    syncSerializedCells();
}

// User actions

const activeTools = $("chartTools");

TOOLS.forEach((tool) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = tool.label;
    button.className = "chart-tool-button";
    button.dataset.tool = tool.id;
    activeTools.appendChild(button);

    button.addEventListener("click", () => {
        state.activeTool = tool.id;
        const tools = document.querySelectorAll(".chart-tool-button");
        tools.forEach((toolButton) => {
            toolButton.classList.remove("is-active");
            toolButton.setAttribute("aria-pressed", "false");
        });
        button.classList.add("is-active");
        button.setAttribute("aria-pressed", "true");
    });

    if (tool.id === state.activeTool) {
        button.classList.add("is-active");
        button.setAttribute("aria-pressed", "true");
    } else {
        button.setAttribute("aria-pressed", "false");
    }
})


function applyCurrentToolToCell(row, column) {
    if (state.kind === "symbol") {
        state.cells[row][column] = state.selectedSymbol === "knit" ? null : state.selectedSymbol;
    } else {
        if (state.colorTool === "erase") {
            state.cells[row][column] = null;
        } else {
            state.cells[row][column] = state.selectedColor;
        }
    }

    renderChart();
    if (state.kind === "color") {
        renderColorPalette()
    }
}

function getCellPositionFromEvent(event) {
    const cell = event.target.closest(".chart-cell-hit");

    if (!cell) {
        return;
    }

    return {
        row: Number(cell.dataset.row),
        column: Number(cell.dataset.column),
    };
}


function handleChartPointerDown(event) {
    const position = getCellPositionFromEvent(event);

    if (!position) {
        return;
    }

    if (state.activeTool !== "cursor") {
        state.isPainting = false;
        if (state.activeTool === "select") {
            state.isSelecting = true;
            state.selectionStart = position;
            state.selectionEnd = position;
            renderChart();
        }
        return;
    }

    state.isPainting = true;
    applyCurrentToolToCell(position.row, position.column);

}

function handleChartPointerMove(event) {
    const position = getCellPositionFromEvent(event);

    if (!position) {
        return;
    }

    state.hoveredColumn = position.column;
    state.hoveredRow = position.row;

    if (state.isSelecting) {
        state.selectionEnd = position;
    }

    if (state.isPainting) {
        applyCurrentToolToCell(position.row, position.column);
        return;
    }

    renderChart();
}

function handleChartPointerUp() {
    state.isPainting = false;
    state.isSelecting = false;
}

function handleChartPointerLeave() {
    state.hoveredRow = null;
    state.hoveredColumn = null;
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


// Initialization

function init() {
    state.rows = clamp(parseInt($("rows").value, 10) || 12, 1, 200);
    state.columns = clamp(parseInt($("columns").value, 10) || 12, 1, 200);
    state.cellSize = clamp(parseInt($("cellSize").value, 10) || 32, 10, 80);
    const selectedKindInput = document.querySelector('input[name="kind"]:checked');
    if (selectedKindInput) {
        state.kind = selectedKindInput.value;
    }
    state.cells = readSerializedCells(state.rows, state.columns);

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
    $("chart").addEventListener("pointerdown", handleChartPointerDown);
    $("chart").addEventListener("pointermove", handleChartPointerMove);
    $("chart").addEventListener("pointerleave", handleChartPointerLeave);
    document.addEventListener("pointerup", handleChartPointerUp);
    $("chartEditorForm").addEventListener("submit", handleFormSubmit);
}

init();
