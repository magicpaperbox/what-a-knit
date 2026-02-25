const $ = (id) => document.getElementById(id);

function buildGridSvg(rows, columns, cellSize) {
  const svg = $("chart");
  const width = columns * cellSize;
  const height = rows * cellSize;

  svg.setAttribute("width", width.toString());
  svg.setAttribute("height", height.toString());
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);

  svg.innerHTML = "";

  const gridGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
  gridGroup.setAttribute("stroke", "#9aa0a6");
  gridGroup.setAttribute("stroke-width", "1");
  gridGroup.setAttribute("shape-rendering", "crispEdges");

  for (let c = 0; c <= columns; c++) {
    const x = c * cellSize;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", x.toString());
    line.setAttribute("y1", "0");
    line.setAttribute("x2", x.toString());
    line.setAttribute("y2", height.toString());
    gridGroup.appendChild(line);
  }

  for (let r = 0; r <= rows; r++) {
    const y = r * cellSize;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", 0);
    line.setAttribute("y1", y);
    line.setAttribute("x2", width);
    line.setAttribute("y2", y);
    gridGroup.appendChild(line);
  }

  const border = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  border.setAttribute("x", 0);
  border.setAttribute("y", 0);
  border.setAttribute("width", width);
  border.setAttribute("height", height);
  border.setAttribute("fill", "none");
  border.setAttribute("stroke", "#444");
  border.setAttribute("stroke-width", "2");

  svg.appendChild(gridGroup);
  svg.appendChild(border);
}

function rebuild() {
  const rows = parseInt($("rows").value, 10);
  const columns = parseInt($("columns").value, 10);
  const cellSize = parseInt($("cellSize").value, 10);
  buildGridSvg(rows, columns, cellSize);
}

$("build").addEventListener("click", rebuild);

// init
rebuild();