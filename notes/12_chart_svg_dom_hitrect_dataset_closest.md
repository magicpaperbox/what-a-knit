# Chart editor: `hitRect`, `classList`, `dataset`, `closest` i analogia do pygame

Ta notatka dotyczy `static/js/charts.js`, szczegolnie funkcji `renderChart()` i `handleChartClick(event)`.

## 1. Co oznacza `hitRect.classList.add("chart-cell-hit")`

Ten zapis trzeba czytac po kawalku:

```js
hitRect.classList.add("chart-cell-hit");
```

- `hitRect` to zmienna JavaScriptowa.
- Ta zmienna trzyma jeden element SVG typu `rect`.
- `rect` oznacza prostokat.
- W chart editorze ten prostokat jest niewidzialna kratka do klikania.
- `.classList` to lista klas przypietych do tego elementu.
- `.add("chart-cell-hit")` dodaje klase o nazwie `chart-cell-hit`.

Czyli calosc znaczy:

```text
Do tego prostokata SVG dodaj etykiete: chart-cell-hit.
```

To nie jest klasa z Pythona.
To jest klasa HTML/CSS, czyli etykieta na elemencie strony.

Taka klasa moze sluzyc do stylowania w CSS, ale moze tez sluzyc tylko jako znacznik dla JavaScriptu.

W tym miejscu `chart-cell-hit` znaczy:

```text
Ten prostokat jest kratka, ktora mozna kliknac albo pomalowac.
```

## 2. Czy `hitRect` nalezy do SVG?

Tak.

W `static/js/charts.js` ten element powstaje tak:

```js
const hitRect = createSvgElement("rect");
```

Funkcja `createSvgElement("rect")` tworzy element SVG.

To jest podobne do pygame:

```python
pygame.Rect(x, y, width, height)
```

ale z jedna wazna roznica:

- w pygame `pygame.Rect(...)` to obiekt w Pythonie, ktory pomaga liczyc pozycje i kolizje,
- w SVG `rect` to prawdziwy element na stronie, ktory przegladarka moze narysowac i ktory moze dostac klikniecie.

W chart editorze `hitRect` jest takim prostokatem "do trafiania kliknieciem".

## 3. Co to jest `dataset`

`dataset` to miejsce na dodatkowe dane przypiete do elementu HTML/SVG.

W `static/js/charts.js` masz:

```js
hitRect.dataset.row = row.toString();
hitRect.dataset.column = column.toString();
```

To znaczy:

```text
Do tej konkretnej kratki SVG zapisz:
- numer wiersza,
- numer kolumny.
```

Potem, gdy uzytkowniczka kliknie kratke, mozna odczytac:

```js
const row = Number(cell.dataset.row);
const column = Number(cell.dataset.column);
```

Czyli:

```text
Kliknieto prostokat SVG.
Sprawdz, ktory wiersz i ktora kolumne ten prostokat reprezentuje.
Potem zmien state.cells[row][column].
```

Analogia do pygame:

```python
rect = pygame.Rect(x, y, size, size)
cell_info = {"row": row, "column": column, "rect": rect}
```

W JS `dataset` pelni podobna role jak dopisanie informacji `row` i `column` do obiektu kratki.

## 4. Co znaczy `closest(".chart-cell-hit")`

`closest` znaczy "najblizszy", ale nie chodzi o kratke obok na planszy.

To nie jest geometria.
To nie znaczy:

```text
znajdz kratke najblizej kursora
```

`closest(...)` chodzi po drzewie HTML/SVG: od kliknietego elementu w gore do jego rodzicow.

Kod:

```js
const cell = event.target.closest(".chart-cell-hit");
```

czytamy tak:

```text
Wez element, w ktory faktycznie kliknieto: event.target.
Sprawdz, czy ten element sam ma klase chart-cell-hit.
Jesli nie, sprawdz jego rodzica.
Jesli rodzic tez nie, sprawdz kolejnego rodzica.
Idz tak w gore, az znajdziesz element z klasa chart-cell-hit albo dojdziesz do konca.
```

Kropka w `".chart-cell-hit"` jest wazna.

- `"chart-cell-hit"` to zwykly tekst.
- `".chart-cell-hit"` to selektor CSS oznaczajacy: element z klasa `chart-cell-hit`.

To jest ten sam typ zapisu co:

```js
document.querySelector(".form-group");
```

## 5. Co znaczy `rect.chart-cell-hit`

Zapis:

```text
rect.chart-cell-hit
```

oznacza:

```text
element SVG/HTML typu rect, ktory ma klase chart-cell-hit
```

Rozbicie:

- `rect` = typ elementu SVG, prostokat,
- `.chart-cell-hit` = klasa na tym elemencie.

To jest selektor.
Nie tworzy niczego sam z siebie.
To tylko opis:

```text
szukam prostokata z taka klasa
```

## 6. Co to jest `state.cells`

`state.cells` nie jest klasa z Pythona.

W `static/js/charts.js` `state` to zwykly obiekt JavaScriptowy, czyli cos podobnego do slownika w Pythonie.

Masz tam:

```js
const state = {
  rows: 12,
  columns: 12,
  cellSize: 32,
  selectedSymbol: "purl",
  cells: [],
  kind: "symbol",
  selectedColor: "#000000",
  isPainting: false,
};
```

Pythonowa analogia:

```python
state = {
    "rows": 12,
    "columns": 12,
    "cell_size": 32,
    "selected_symbol": "purl",
    "cells": [],
    "kind": "symbol",
    "selected_color": "#000000",
    "is_painting": False,
}
```

`state.cells` to po prostu pole `cells` wewnatrz obiektu `state`.

Pythonowo mozna o tym myslec jak o:

```python
state["cells"]
```

W `state.cells[row][column]` trzymasz prawdziwa wartosc kratki:

- symbol, np. `"purl"`,
- kolor, np. `"#ff0000"`,
- albo `null`, czyli pusta kratka.

## 7. Po co to wszystko w chart editorze

W chart editorze sa dwie warstwy:

```text
state.cells
```

To sa prawdziwe dane chartu w JavaScripcie.

Oraz:

```text
hitRect
```

To jest prostokat SVG, ktory uzytkowniczka moze kliknac.

Most miedzy nimi wyglada tak:

```text
kliknieto hitRect
-> closest(".chart-cell-hit") znajduje kratke
-> dataset.row i dataset.column mowia, ktora to kratka
-> state.cells[row][column] zostaje zmienione
-> renderChart() rysuje chart od nowa
```

## 8. Analogia do pygame

W pygame mozna by myslec tak:

```python
cells_to_click = []

for row in range(rows):
    for column in range(columns):
        rect = pygame.Rect(x, y, cell_size, cell_size)
        cells_to_click.append({
            "rect": rect,
            "row": row,
            "column": column,
        })
```

Potem przy kliknieciu:

```python
for cell in cells_to_click:
    if cell["rect"].collidepoint(mouse_pos):
        row = cell["row"]
        column = cell["column"]
        state_cells[row][column] = selected_symbol
```

W Twoim JS/SVG podobna rola rozklada sie tak:

- `hitRect` jest jak `pygame.Rect`,
- `dataset.row` i `dataset.column` sa jak zapisane `"row"` i `"column"` w slowniku,
- `closest(".chart-cell-hit")` pomaga znalezc klikniety element SVG,
- `state.cells[row][column]` jest jak tabela danych, ktora potem rysujesz.

## 9. Najkrotsza wersja do zapamietania

```text
classList.add(...) = przyklej etykiete do elementu
dataset = zapisz male dane na elemencie
closest(".class-name") = znajdz najblizszy element z taka klasa, idac po HTML/SVG w gore, nie po planszy obok
state.cells = dane chartu, nie klasa z Pythona
hitRect = prostokat SVG, podobny mentalnie do pygame.Rect, ale zyjacy na stronie
```
