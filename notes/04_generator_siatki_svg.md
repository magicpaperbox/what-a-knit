# Generator siatki SVG (Chart Creator) – Podsumowanie

W ramach pracy nad funkcjonalnością "Create chart" (generowania kratek do wzorów), omówiliśmy i zastosowaliśmy kilka bardzo ważnych konceptów budowania aplikacji webowych. Poniżej znajduje się ściągawka z najważniejszych lekcji.

## 1. Dobre praktyki w pisaniu CSS (Zasada zamkniętych stylowań)
Na początku style dla nowej strony były napisane dość ogólnie, np.:
```css
button { color: red; }
.row { display: flex; }
svg { display: block; }
```
**Problem:** Gdy te style trafiły do głównego pliku `style.css`, to "zepsułyby" wygląd każdego innego przycisku na całej stronie głównej naszego projektu.
**Dobre rozwiązanie:** Zawsze warto stylować z użyciem unikalnych tzw. "klas (class)". Wszystkim elementom nadaliśmy specyficzne "identyfikatory", np.:
`btn-chart`, `chart-row`, `chart-Inputs-group`, `chart-svg`.
Teraz w CSS modyfikujemy `.btn-chart { ... }` i mamy pewność, że to zadziała tylko na ten jeden, przeznaczony do tego guzik.

## 2. Flexbox, czyli zmagania z układem elementów (CSS)
Zamiast wrzucać wszystkie okienka z boku, posiliłyśmy się magią `Flexboxa`. 
*   **W klasie `.chart-row`:** daliśmy polecenie `flex-direction: column;` – dzięki temu nasze okienka oraz przycisk nie próbują pchać się w jednym rzędzie, lecz ustawiły się gładko pod sobą na zasadzie kolumny.
*   **W klasie `.chart-inputs-group`:** zamknęliśmy trzy konkretne okienka obok siebie z zasadą rozkładu `justify-content: space-evenly;`. Przeglądarka wie teraz, że każdemu oknu ma równomiernie docinać puste wolne miejsce po bokach, żeby całość wyglądała ładnie i gładko po całej szerokości.

## 3. Nowoczesny zapis łączenia ciągów znaków i zmiennych (JS)
Często chcemy połączyć stały tekst wyjściowy z jakimiś wynikami zmiennych z Pythona czy JSa, tak jak w tym konkretnym rzędzie z viewBoxem kamery: 
```javascript
`0 0 ${width} ${height}`
```
Zastosowaliśmy tu **Template Literals**. 
Zamiast pisać powolnie starą, skomplikowaną sklejoną formę `"0 0 " + width + " " + height`, używamy cudownych **backticków (\`...\`)**. Jeśli wpiszesz w nim taką konstrukcję `${...}`, to zamiast brzydkiego rzędu znaków podczas rysowania natychmiast wrzuci w to miejsce obliczoną wcześniej zmienną. Składnia jest elegancka, prosta w odczycie dla programisty i mniej podatna na pomyłki w sklejaniu i dodawaniu pustych spacji znaków!

## 4. Bounding Boxy w rzutowaniu wizji na program, czyli `viewBox` vs `rect`
Bardzo fajne skojarzenie z Pygame! Zastanawialiśmy się, różnicami tego jak wypluwane są piksele na wizję:
*   W Pygame i poleceniu `blit()` wrzucaliśmy stworzony rysunek postaci na ślepo szukając sztywnego miejsca "Kwadratu na głównym monitorze".
*   We właściwości wideo `viewBox="x y szerokść wysokośc"` stosowanej w `<svg>` działaliśmy na samą "kamerach" i obiektywach. Przekazaliśmy dla przeglądarki wykadrowaną wielkość szklanego wizjera. Cała bezkresna folia pliku ze schematem może być wektorowo gigantyczna – viewBox mowi mu **odcięto** – zaciągnij soczewkę od punktu x: 0 i y: 0 aż do punktu w: i h: !

## 5. Praca z drzewem i pętle
Napisany przez nas skrypt, odpalany po przyciśnięciu, zawiera w swym kodzie piękną logikę podziału kratek, napisaną dosłownie pętlami `for`, które wyliczają po kolei szerokość (x i y linii) mnożąc punkty iteracji przez np. ustalony odstęp `32px` od kratki – przypisując w środek każdej kratki nową narysowaną matematycznie współrzędną linii. Oraz mały brudny tip: `svg.innerHTML = ""` błyskawicznie przed zapieczeniem wyrzuca do niszczarki w chmurze stary rysunek przed narysowaniem drugiego na nowym!

## 6. Zawsze pamiętaj podpiąć skrypt do strony!
Na nic pięknie napisany program obsługujący guzik "Create", gdy na stronie szablonu z tym ekranem w ogóle go nie dołączyliśmy...
Aby ożywić nową stronę HTML we "Flasku", na samym dnie kodu, tuż za naszą tablicą przypominamy szablonowi, jak pobrać dedykowany plik skryptu:
```html
<script src="{{ url_for('static', filename='js/charts.js') }}"></script>
```
