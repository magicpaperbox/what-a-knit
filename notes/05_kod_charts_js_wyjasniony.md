# Jak działa kod rysujący kratki (charts.js)? - Krok po Kroku


## Część 1: Użyteczny skrót

```javascript
const $ = (id) => document.getElementById(id);
```
Tworzymy małego pomocnika. Dzięki temu za każdym razem, gdy chcemy złapać jakiś element z naszej strony internetowej po jego ID (np. okienko `<input id="rows">`), zamiast pisać w kółko przydługie słowo `document.getElementById("rows")`, możemy wywołać po prostu `$("rows")`. Zwróci nam to samo okno. Oszczędność czasu i przejrzystość podziękowana na końcu.

---

## Część 2: Odbieranie danych z okienek po kliknięciu głównego "szefa"

```javascript
function rebuild() {
    const rows = parseInt($("rows").value, 10);
    const columns = parseInt($("columns").value, 10);
    const cellSize = parseInt($("cellSize").value, 10);
    
    buildGridSvg(rows, columns, cellSize);
}

$("build").addEventListener("click", rebuild);
```
**`$("build").addEventListener("click", rebuild);`**
Te ostatnia linijka kodu to wyznaczenie szefa "Dozorcy". Łapiemy tag ze strony o `id="build"` (czyli nasz przycisk guzik z różowowego panelu po prawiej tronie "Create") i podpinamy dla niego potajemmie nasłuchiwacza na wypadek kliknięca. Kiedy zaważy wciśnięcie obudzi od góry **Funkcję `rebuild`**

Co wykonuje w środku wywołana funkcja `rebuild()`?
Każde okenko formularza `.value` zapisuje wpisaną rzecz w domyśle użytkownika z klawiatury we właściwości ułożoną jako jako surowy bezwartościowy słowny tekst (tzw String!). np - `"12"`. Aby komputer mógł z tym normalnie pracować matematycznie musisz mu powiedzieć i poprosić go poinformować przez wbudowany u JSa zamek logiczny - hej `parseInt` zamień ten ciąg -  odcyfruj ten ciąg po prawiej - `"12"` - na pełną matematyczną liczbę (używana dziesiąta to podbudowa że posługujemy się bazą ogólnej dziesiętnej wielkość). Gdy już odbierze zapakuje je to w wygodne nowatorskie pudełka `rows`, `columns` i sam kładzie je dla zleceniową do budowy pod przywództwem w wezweiu głównego mistrza - czyli **`buildGridSvg(...)`**.

---

## Część 3: Matematyczny Inżynier - główna funkcja renderująca

Właściwe rysowanie kratek - obśnijmy to rónież warstwa po waesrtwie.

### Przygotowanie głównego płótna obrazu (SVG)

```javascript
function buildGridSvg(rows, columns, cellSize) {
    const svg = $("chart"); // Złap tag "SVG" wyrysowany cicho w domyśle  szablonu
    const width = columns * cellSize; // Policz główną szerokość tablicy (np 10 kolumn * 30 pikseli krateczki)
    const height = rows * cellSize;

    svg.setAttribute("width", width); // Zdefiniowane płótno wyciągnije do HTML tag rozmiar w pixele (na żywio)
    svg.setAttribute("height", height);
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`); // Ustawienie marginesu kamery 
    
    svg.innerHTML = ""; // Ważne wyczyszczenie 
```
Ta sekcja wykonuje proste zadania wyciąga z pustego Tagu ten sam obraz, przelicza jak duży będzie i przypina mu rozmiary na siłę z wyciągoniętymi obliczonaymi wielkościami - oraz ustała z lewego końca startowego górnego (0 0) - ten osłoniety View box obok marginesów z matematyki `${width} i ${height}` - wpychanie i wypinania z szabnlów (Templat Luterals).

W czyszczeniu wewnętrznej zawartość Taggu .innerHTML  podmienia my do pustego. 
To oznacza bez litowania mógła by na starcie tam być namalowania stara pognietiona wektorowa z kratowa linia na podstronie lub od nowa a nałożenue na włącznen - klikem. Wyczyscśmy zeby kratki obok sie z nie namazywaly!.

### Warstwa cienia po wirtualnym powietrzu

```javascript
    const gridGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    gridGroup.setAttribute("stroke", "#9aa0a6"); // Kolor pisaka szary
    gridGroup.setAttribute("stroke-width", "1"); // Wielkość farby (1px cienka)
    gridGroup.setAttribute("shape-rendering", "crispEdges"); // Twarda krawędź
```
Podczas modyfikowania obrazów na wektor (SVG jest innym językiem niż HTML - z rodziny XML!) nie mozna po po rostu wepchać go w zywczajny `.createElement(...)`. Stąd konieczność dodania po cichu tej specyficznie brzmiącej docelowej instyrycji adresnej `.createElementNS` żeby przeglądarka zrozumiała - To będzie obiek z węgla - w tagu z zarysami  G (oznacza Grpupa) żeby można było wszystkie wymalować po woli na nie widoczny folie, i od góry wszystkim powiedzuć: Pomalujcie farbę cienko i bez widocznego wygłańczania.


### Generacja kratek (magia pętli i matematyki pika) 

```javascript
    // Rysowanie linijek dla każdego pionu  dla kolumny (od lewej do prawej krawędzi) 
    for (let c = 0; c <= columns; c++) {
      const x = c * cellSize;
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      // Mówimy dla jednej linii:
      line.setAttribute("x1", x); // Zjedź do odpowiedniego piksela w Powiechznie szerokści (Oś x) i zacznij u samej góry "Y:0" 
      line.setAttribute("y1", 0);
      line.setAttribute("x2", x); // Na dół leć na szerokosći tej samej na Osii i dociągnij na dół Płónka róno we Wysokośći max! 
      line.setAttribute("y2", height);
      gridGroup.appendChild(line); // Schowajemy na przezroczystą folię do grup "g"
    }
```
Podobnie z tą matamtyjką działa ta druga bliźniacza pętla niżej (na "Wiesza" Oś Pionu) – czyli po koleji oblicze sobie 12-to kolkrotnie razy na wysokosć w  pixleach (jaka uzytkownik wskaze) np na `y pos =0 , =32 = 64` itp... a wkładka pod wiersz - mowi narysuj od samego skręjnie rónogo Y: i X u zsamej lewej (0), w podążaj tąż sama kreslać  prosto - naryśuj je na na drugiego brzegu (width) u na końcu tej krawężdzi na foli  ! 


### Dociepanie całej podkłądki

I Ostateczny krtok końcowy z całą paczką w pamięci (grupa wektrowych paczek!) :

```javascript
  svg.appendChild(gridGroup);
  svg.appendChild(border);
}
```
Dopiero i tylko w tey Ostatnich dwóch linijjkach caly wysilek Pętli w pamięści kompuera i farbek  trafi (jak legendarany `screen.blit()`) na żywo - w rzutowane drzewo widome jako podpiecię jako dzieci - wypycha ten gotowy wklejony widocnzy Obraz z SVG  Wszstkim kratką tuż przed Twoje obiektyy oczy! !
