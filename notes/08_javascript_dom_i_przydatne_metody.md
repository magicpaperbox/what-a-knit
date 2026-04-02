# JavaScript: DOM i przydatne metody w praktyce

To nie jest lista "wszystkich specjalnych funkcji JavaScriptu", bo czegoś takiego sensownie nie da się zamknąć w jednej krótkiej notatce.
To jest **ściąga z najczęstszych rzeczy**, które pojawiają się w zwykłym JS w projekcie takim jak Twój.

Najważniejsza myśl:

- JavaScript bardzo często robi 3 rzeczy:
- znajduje elementy w HTML,
- reaguje na akcje użytkownika,
- zmienia coś na stronie.

## 1. Szukanie elementów w HTML

### Ważne: czym jest selektor CSS i czemu pojawia się w JavaScripcie

To jest jedno z najbardziej mylących miejsc na początku frontendu.

Selektor CSS to po prostu **sposób wskazania elementu na stronie**.

Przykłady selektorów:

- `input`
- `#status`
- `.form-group`
- `[name="pattern_id"]`

Najważniejsze:

- selektor CSS **nie oznacza od razu stylowania**,
- to jest po prostu język opisu elementu,
- CSS używa go do stylowania,
- JavaScript może używać tego samego zapisu do wyszukiwania elementów.

Czyli:

- w CSS:

```css
input {
    border: 1px solid red;
}
```

tu `input` mówi:
"styluj wszystkie inputy"

- w JS:

```js
document.querySelector("input");
```

tu `input` mówi:
"znajdź pierwszy input"

To nie znaczy, że JavaScript "używa CSS-a do wyglądu".
To znaczy tylko, że JavaScript używa **składni selektorów CSS jako języka wyszukiwania**.

Czy musisz mieć plik CSS, żeby tego używać?

- nie,
- możesz w ogóle nie pisać stylów,
- ale i tak `querySelector(...)` nadal używa selektorów.

Najprościej:

- HTML = co jest na stronie,
- CSS = jak to wygląda,
- JS = co z tym robimy,
- selektor CSS = sposób powiedzenia, **który element mamy na myśli**.

### 5 najczęstszych selektorów, które warto znać do JS

#### `#id`

Znaczy:

- element o konkretnym `id`

```js
document.querySelector("#status");
```

To odpowiada HTML:

```html
<select id="status"></select>
```

#### `.class`

Znaczy:

- element z daną klasą

```js
document.querySelector(".form-group");
```

#### `input`

Znaczy:

- element o takim tagu

```js
document.querySelector("input");
```

#### `[name="pattern_id"]`

Znaczy:

- element, który ma atrybut `name="pattern_id"`

```js
document.querySelector('[name="pattern_id"]');
```

#### `input[name="pattern_id"][value="7"]`

Znaczy:

- `input`
- który ma `name="pattern_id"`
- i jednocześnie ma `value="7"`

To jest właśnie przykład selektora po atrybutach.

U Ciebie taki zapis przydaje się wtedy, gdy chcesz sprawdzić:

- czy w kontenerze istnieje już hidden input dla konkretnego patternu

Czyli:

```js
hiddenInputContainer.querySelector(`input[name="pattern_id"][value="${pattern.id}"]`);
```

Jak to czytać:

- w `hiddenInputContainer`
- znajdź input
- o `name="pattern_id"`
- i `value` równym `pattern.id`

### Backticki i `${...}`

To też Ci się właśnie przydało.

Backticki to taki zapis:

```js
`tekst`
```

To też jest string, czyli tekst, ale specjalny.
Pozwala wstawiać wartości zmiennych do środka.

Przykład:

```js
const name = "Klaudia";
const text = `Hello ${name}`;
```

Wynik:

```js
Hello Klaudia
```

Czyli:

- `${...}` znaczy: "wstaw tutaj wartość"

W Twoim przykładzie:

```js
`input[name="pattern_id"][value="${pattern.id}"]`
```

jeśli `pattern.id` ma wartość `7`, to finalnie robi się z tego:

```js
input[name="pattern_id"][value="7"]
```

### Jak czytać taki zapis w `querySelector(...)`

To jest dokładnie ten typ zapisu, na którym łatwo się zgubić:

```js
hiddenInputContainer.querySelector(`input[name="pattern_id"][value="${pattern.id}"]`);
```

Rozbijmy to bardzo wolno.

#### `hiddenInputContainer`

To jest zmienna JavaScriptowa, która wskazuje na konkretny element HTML.

W Twoim przypadku:

- to jest kontener `div`,
- w środku którego trzymasz hidden inputy z wybranymi patternami.

Czyli:

- "szukaj w tym konkretnym miejscu"

#### `.querySelector(...)`

To jest metoda JavaScriptu, która znaczy:

- "znajdź pierwszy element pasujący do opisu"

Czyli:

- nie szukasz po całej stronie,
- tylko wewnątrz `hiddenInputContainer`.

#### Tekst w środku `querySelector(...)`

To:

```js
`input[name="pattern_id"][value="${pattern.id}"]`
```

jest po prostu **opisem elementu, którego szukasz**.

Ten opis składa się z trzech części.

#### `input`

Znaczy:

- szukam elementu typu `<input>`

#### `[name="pattern_id"]`

Znaczy:

- ten input ma mieć atrybut `name="pattern_id"`

Czyli nie byle jaki input, tylko taki konkretny.

#### `[value="${pattern.id}"]`

Znaczy:

- ten input ma mieć atrybut `value` równy aktualnemu `pattern.id`

Jeśli:

```js
pattern.id === 7
```

to ten fragment:

```js
[value="${pattern.id}"]
```

zamienia się na:

```js
[value="7"]
```

#### Całość razem

```js
input[name="pattern_id"][value="7"]
```

znaczy:

- znajdź input
- który ma `name="pattern_id"`
- i jednocześnie ma `value="7"`

#### Uwaga na spację

Te dwa zapisy nie znaczą tego samego:

```js
input[name="pattern_id"][value="7"]
```

oraz

```js
input[name="pattern_id"] [value="7"]
```

Pierwszy zapis znaczy:

- jeden element `input`,
- który ma oba atrybuty naraz

Drugi zapis ze spacją znaczy:

- element `[value="7"]`,
- który jest w środku czegoś pasującego do `input[name="pattern_id"]`

Czyli:

- bez spacji = jeden element z dwoma warunkami,
- ze spacją = relacja rodzic / dziecko albo przodek / potomek.

W praktyce:

- jeśli chcesz opisać jeden element z kilkoma atrybutami, nie dawaj tam spacji.

#### Po co to jest w Twoim kodzie

To jest potrzebne, żeby sprawdzić:

- czy w kontenerze istnieje już hidden input dla tego patternu

Czyli myślowo:

- "czy ten pattern już został wybrany?"

Jeśli taki input już istnieje:

```js
if (existingHiddenInput) {
    return;
}
```

to kończysz funkcję i nie dodajesz duplikatu.

### Najkrótsza wersja do zapamiętania

W zapisie:

```js
hiddenInputContainer.querySelector(`input[name="pattern_id"][value="${pattern.id}"]`)
```

- `hiddenInputContainer` = gdzie szukam
- `querySelector(...)` = znajdź pierwszy pasujący element
- `input` = jakiego typu elementu szukam
- `[name="pattern_id"]` = z jakim atrybutem
- `[value="${pattern.id}"]` = z jaką konkretną wartością

### `!!` czyli zamiana wartości na `true` albo `false`

To jest częsty skrót w JavaScripcie.

Przykład:

```js
const existingHiddenInput = hiddenInputContainer.querySelector(
    `input[name="pattern_id"][value="${pattern.id}"]`
);

return !!existingHiddenInput;
```

Jak to czytać:

- `querySelector(...)` zwraca element albo `null`
- element jest traktowany jako wartość "prawdziwa"
- `null` jest traktowane jako wartość "fałszywa"

Jeden wykrzyknik `!` oznacza negację:

- `!true` daje `false`
- `!false` daje `true`

Ale można go też użyć do zamiany różnych wartości na zwykłe `true` albo `false`.

Przykład:

```js
!existingHiddenInput
```

To da:

- `false`, jeśli element istnieje
- `true`, jeśli `existingHiddenInput` jest `null`

Drugi wykrzyknik odwraca to jeszcze raz:

```js
!!existingHiddenInput
```

Czyli finalnie:

- `true`, jeśli element istnieje
- `false`, jeśli element nie istnieje

Najkrócej:

- `!coś` = odwróć
- `!!coś` = zamień na czyste `true` albo `false`

W Twoim kodzie:

```js
return !!existingHiddenInput;
```

to znaczy:

- zwróć `true`, jeśli hidden input istnieje
- zwróć `false`, jeśli hidden input nie istnieje

To jest krótszy zapis tego samego co:

```js
if (existingHiddenInput) {
    return true;
}

return false;
```

### `id`, `class`, atrybut` w HTML - czym one są, a czym nie są

To jest miejsce, gdzie bardzo łatwo się pomylić, bo te słowa istnieją też w innych kontekstach.

#### `id` w HTML

Przykład:

```html
<input id="status">
```

Tutaj `id` znaczy:

- unikalna nazwa elementu na stronie

To nie jest:

- `id` rekordu z bazy danych,
- automatycznie numer,
- coś backendowego.

W selektorze:

```js
#status
```

to znaczy:

- element z `id="status"`

#### `class` w HTML

Przykład:

```html
<div class="form-group"></div>
```

Tutaj `class` znaczy:

- grupa / etykieta elementu,
- coś, po czym można element stylować albo znaleźć.

To nie jest:

- klasa z Pythona,
- definicja obiektu,
- programowanie obiektowe.

W selektorze:

```js
.form-group
```

to znaczy:

- element z klasą `form-group`

#### Atrybut w HTML

Przykład:

```html
<input type="hidden" name="pattern_id" value="7">
```

Tutaj atrybutami są:

- `type`
- `name`
- `value`

Czyli:

- `type="hidden"` to atrybut i jego wartość,
- `name="pattern_id"` to atrybut i jego wartość,
- `value="7"` to atrybut i jego wartość.

To nie jest:

- indeks listy,
- zmienna z Pythona,
- coś specjalnego z backendu.

#### `[]` w selektorze

W zapisie:

```js
[name="pattern_id"]
```

kwadratowe nawiasy nie znaczą:

- "weź element listy"

Tylko znaczą:

- "szukaj elementu po atrybucie"

Czyli:

- w Pythonie `lista[0]` = pierwszy element listy
- w selektorze CSS `[name="pattern_id"]` = element z atrybutem `name="pattern_id"`

To są dwie różne rzeczy, tylko używają tego samego znaku.

### Najkrótsza ściąga

- `#status` = po `id`
- `.form-group` = po klasie
- `[name="pattern_id"]` = po atrybucie
- `input` = po tagu HTML

### `document.getElementById("nazwa")`

Szuka **jednego elementu po `id`**.

```js
const statusSelect = document.getElementById("status");
```

Kiedy używać:

- gdy element ma konkretne `id="status"`,
- gdy chcesz znaleźć dokładnie jeden element.

Jak to czytać:

- `document` = cała strona HTML,
- `getElementById(...)` = "daj mi element o takim id".

### `document.querySelector("selektor")`

Szuka **pierwszego elementu**, który pasuje do selektora CSS.

```js
const form = document.querySelector(".project-form");
const input = document.querySelector('input[type="date"]');
```

Kiedy używać:

- gdy chcesz szukać po klasie, typie inputa, atrybucie itd.,
- gdy wystarczy pierwszy pasujący element.

### `document.querySelectorAll("selektor")`

Szuka **wszystkich pasujących elementów**.

```js
const steppers = document.querySelectorAll(".number-stepper");
```

Wynik to nie jest jeden element, tylko lista elementów.

Kiedy używać:

- gdy takich elementów na stronie jest kilka,
- gdy chcesz coś zrobić z każdym z nich.

### `element.querySelector(...)`

To samo co wyżej, ale nie szukasz w całym dokumencie, tylko **wewnątrz jednego konkretnego elementu**.

```js
const input = stepper.querySelector('input[type="number"]');
```

To jest bardzo ważne.

Jak jest teraz:

- `document.querySelector(...)` szuka w całej stronie,
- `stepper.querySelector(...)` szuka tylko w środku tego jednego wrappera.

## 2. Przechodzenie po wielu elementach

### `forEach(...)`

`forEach` wykonuje jakąś funkcję dla każdego elementu listy.

```js
steppers.forEach(function (stepper) {
    console.log(stepper);
});
```

Jak to czytać:

- "dla każdego elementu z listy zrób to, co jest w środku".

To jest bardzo podobne do:

```python
for stepper in steppers:
    print(stepper)
```

Kiedy używać:

- gdy masz kilka elementów i chcesz do każdego dodać podobną logikę.

## 3. Reagowanie na kliknięcie i inne akcje

### `addEventListener("click", ...)`

To mówi przeglądarce:
"gdy wydarzy się kliknięcie, uruchom ten kod".

```js
button.addEventListener("click", function () {
    console.log("klik");
});
```

Najczęstsze zdarzenia:

- `"click"` - kliknięcie,
- `"input"` - zmiana wpisywanej wartości,
- `"change"` - zmiana wartości pola,
- `"submit"` - wysłanie formularza.

### `dispatchEvent(...)`

To jest sposób na **ręczne wywołanie zdarzenia** na elemencie.

```js
input.dispatchEvent(new Event("input", { bubbles: true }));
input.dispatchEvent(new Event("change", { bubbles: true }));
```

Jak to czytać:

- `new Event("input")` = utwórz nowe zdarzenie typu `"input"`,
- `dispatchEvent(...)` = wyślij to zdarzenie do elementu.

Po co się tego używa:

- gdy zmieniasz coś w JS, a nie ręcznie przez użytkownika,
- ale chcesz, żeby inne fragmenty kodu zachowały się tak, jak przy normalnej zmianie pola.

Przykład z Twojego kodu:

- klikasz własny przycisk `+` albo `-`,
- JS zmienia `input.value`,
- ale sama zmiana `input.value` nie zawsze oznacza jeszcze, że inne listenery się uruchomią,
- więc `dispatchEvent(...)` mówi:
  "hej, potraktuj to tak, jakby użytkownik naprawdę zmienił wartość pola".

Ważne:

- `dispatchEvent(...)` nie zmienia wartości sam z siebie,
- on tylko wysyła informację o zdarzeniu.

Najprościej:

- `addEventListener(...)` = nasłuchuję na zdarzenie,
- `dispatchEvent(...)` = ręcznie to zdarzenie wywołuję.

### `setInterval(...)` i `clearInterval(...)`

To są funkcje do **powtarzania czegoś co jakiś czas**.

```js
const intervalId = setInterval(function () {
    console.log("działam co chwilę");
}, 250);
```

To znaczy:

- uruchom tę funkcję,
- potem powtarzaj ją co `250` milisekund,
- czyli około 4 razy na sekundę.

Po co się tego używa:

- do animacji,
- do odświeżania czegoś co chwilę,
- do sytuacji typu:
  "dopóki trzymam przycisk, zwiększaj wartość".

`setInterval(...)` zwraca identyfikator, który trzeba sobie zapisać:

```js
const intervalId = setInterval(...);
```

Potem możesz to zatrzymać:

```js
clearInterval(intervalId);
```

Najprościej:

- `setInterval(...)` = zacznij powtarzać,
- `clearInterval(...)` = przestań powtarzać.

### `setTimeout(...)` i `clearTimeout(...)`

To są funkcje do **opóźnienia wykonania czegoś jeden raz**.

```js
const timeoutId = setTimeout(function () {
    console.log("uruchomię się później");
}, 300);
```

To znaczy:

- poczekaj `300` milisekund,
- uruchom funkcję raz.

To nie jest powtarzanie.
To jest tylko jedno opóźnione wykonanie.

Jeśli chcesz to anulować przed wykonaniem:

```js
clearTimeout(timeoutId);
```

Najprościej:

- `setTimeout(...)` = zrób coś później, raz,
- `clearTimeout(...)` = anuluj to czekanie.

### Różnica między `setTimeout` a `setInterval`

- `setTimeout(...)` - jedno opóźnione wykonanie,
- `setInterval(...)` - powtarzanie co jakiś czas.

### Przykład z przytrzymywaniem przycisku

Jeśli chcesz, żeby po przytrzymaniu `+` wartość zmieniała się dalej, to często łączy się obie rzeczy:

1. `setTimeout(...)`
   żeby po krótkiej chwili zacząć auto-powtarzanie,
2. `setInterval(...)`
   żeby potem zmieniać wartość co np. `250 ms`,
3. `clearTimeout(...)` i `clearInterval(...)`
   żeby zatrzymać to po puszczeniu przycisku.

Czyli myślowo:

- klikam i trzymam,
- od razu robi się pierwszy krok,
- po chwili startuje powtarzanie,
- puszczam przycisk,
- wszystko się zatrzymuje.

## 4. Czytanie i zmienianie danych w elementach

### `.value`

Pobiera albo ustawia wartość pola formularza.

```js
const currentValue = input.value;
input.value = "10";
```

Używamy dla:

- `input`,
- `select`,
- `textarea`.

### `.textContent`

Zmienia zwykły tekst w elemencie.

```js
resultElement.textContent = pattern.name;
```

To jest bezpieczniejsze niż `innerHTML`, jeśli chcesz wstawić sam tekst.

### `.innerHTML`

Wstawia HTML jako tekst do zinterpretowania przez przeglądarkę.

```js
resultsContainer.innerHTML = "";
```

U Ciebie to się przydaje np. do wyczyszczenia kontenera.

Uwaga:

- do prostego tekstu zwykle lepiej używać `textContent`,
- `innerHTML` jest mocniejsze, ale łatwiej nim namieszać.

## 5. Tworzenie i dodawanie elementów

### `document.createElement("div")`

Tworzy nowy element HTML w pamięci.

```js
const resultElement = document.createElement("div");
```

To jeszcze nie pokazuje go na stronie.

### `appendChild(...)`

Dodaje element jako dziecko do innego elementu.

```js
resultsContainer.appendChild(resultElement);
```

Dopiero wtedy nowy element trafia na stronę.

### `.remove()`

Usuwa element z HTML.

```js
selectedElement.remove();
```

### `.children`, `.length` i `.childElementCount`

To są rzeczy przydatne, gdy chcesz sprawdzić:

- czy element ma dzieci,
- ile elementów jest w środku,
- czy kontener jest pusty.

#### `.children`

Zwraca dzieci-elementy danego elementu.

```js
selectedPatternsContainer.children
```

To znaczy:

- "daj mi elementy, które są w środku tego kontenera"

#### `.children.length`

Pozwala policzyć, ile tych dzieci jest.

```js
selectedPatternsContainer.children.length
```

Przykład:

- `0` = nic nie ma w środku,
- `1` = jest jedno dziecko,
- `2` = są dwa dzieci itd.

#### `.childElementCount`

To jeszcze prostszy sposób na policzenie dzieci-elementów.

```js
selectedPatternsContainer.childElementCount
```

To znaczy dokładnie:

- ile elementów-dzieci ma ten kontener

Przykład:

```js
if (selectedPatternsContainer.childElementCount > 0) {
    console.log("są wybrane patterny");
}
```

Najprościej:

- `.children` = same dzieci,
- `.children.length` = liczba dzieci,
- `.childElementCount` = też liczba dzieci, tylko od razu.

Do prostego pytania:

- "czy ten kontener jest pusty?"

bardzo wygodne jest właśnie:

```js
selectedPatternsContainer.childElementCount
```

### `style.display`

To jest prosty sposób na pokazanie albo ukrycie elementu w JavaScripcie.

Przykłady:

```js
selectedPatternsLabel.style.display = "none";
```

To znaczy:

- ukryj element

```js
selectedPatternsLabel.style.display = "block";
```

To znaczy:

- pokaż element jako blok

Najprościej:

- `"none"` = schowaj
- `"block"` = pokaż

To nie znaczy, że:

- `block` jest dosłownie słowem "pokaż"

To znaczy tylko:

- `display` opisuje sposób wyświetlania elementu,
- `none` = w ogóle go nie wyświetlaj,
- `block` = wyświetlaj go jako element blokowy.

Czyli:

- `none` chowa element,
- `block` przywraca go do normalnego widoku jako `div` / blok.

To jest ważne, bo:

- `block` nie jest jedyną możliwą wartością "widocznego" elementu,
- są też np. `inline`, `flex`, `grid`,
- ale dla zwykłego `div` bardzo często `block` jest po prostu sensownym sposobem pokazania go z powrotem.

To się przydaje, gdy:

- chcesz coś ukryć na starcie,
- albo pokazywać dopiero wtedy, gdy spełniony jest jakiś warunek

Przykład:

```js
if (selectedPatternsContainer.childElementCount === 0) {
    selectedPatternsLabel.style.display = "none";
} else {
    selectedPatternsLabel.style.display = "block";
}
```

## 6. Atrybuty i dane dodatkowe

### `getAttribute("nazwa")`

Pobiera wartość atrybutu HTML.

```js
const savedSubtype = subcategorySelect.getAttribute("data-selected");
```

### `removeAttribute("nazwa")`

Usuwa atrybut z elementu.

```js
subcategorySelect.removeAttribute("data-selected");
```

### `data-*`

To własne dane w HTML.

Przykład:

```html
<button data-stepper-action="increment">+</button>
```

Tutaj:

- `data-stepper-action` to własny atrybut,
- można go potem wyszukiwać w JS.

## 7. Przydatne rzeczy na stringach

### `.includes(...)`

Sprawdza, czy tekst zawiera dany fragment.

```js
pattern.name.toLowerCase().includes(query);
```

Przykład:

- `"sweter".includes("we")` daje `true`
- `"sweter".includes("xy")` daje `false`

### `.split(...)`

Dzieli tekst na kawałki.

```js
"0.5".split(".");
```

Wynik:

```js
["0", "5"]
```

### `.length`

Mówi, ile czegoś jest.

Dla tekstu:

```js
"abc".length // 3
```

Dla listy:

```js
[10, 20, 30].length // 3
```

## 8. Zamiana typów

### `String(...)`

Zamienia coś na tekst.

```js
String(12); // "12"
```

### `Number(...)`

Zamienia coś na liczbę.

```js
Number("12"); // 12
Number("0.5"); // 0.5
```

Uwaga:

- jeśli tekst nie wygląda jak liczba, możesz dostać `NaN`.

### `Number.isNaN(...)`

Sprawdza, czy wynik jest `NaN`.

```js
Number.isNaN(currentValue)
```

To jest zabezpieczenie:

- "czy ta wartość naprawdę jest liczbą?"

## 9. Przydatne rzeczy do liczb

### `Math.max(a, b)`

Zwraca większą z dwóch wartości.

```js
Math.max(3, 7); // 7
```

### `Math.min(a, b)`

Zwraca mniejszą z dwóch wartości.

```js
Math.min(3, 7); // 3
```

U Ciebie to jest używane do pilnowania zakresu `min` / `max`.

### `.toFixed(n)`

Formatuje liczbę do określonej liczby miejsc po przecinku.

```js
(1.234).toFixed(1); // "1.2"
(1).toFixed(1); // "1.0"
```

Uwaga:

- wynik `toFixed(...)` jest tekstem, a nie liczbą.

## 10. Funkcja w środku funkcji

W JS bardzo często spotkasz taki zapis:

```js
button.addEventListener("click", function () {
    updateInput(1);
});
```

To znaczy:

- przekazujesz funkcję jako argument do innej funkcji.

Czyli nie:

- "uruchom to teraz",

tylko:

- "zachowaj tę funkcję i uruchom ją później, gdy będzie kliknięcie".

## 11. `return`

`return` kończy działanie funkcji i oddaje wynik.

```js
function add(a, b) {
    return a + b;
}
```

Ale czasem `return` oznacza po prostu:

- "przerwij i wyjdź stąd".

Przykład:

```js
if (!input) {
    return;
}
```

To znaczy:

- jeśli nie ma inputa, kończymy i nic więcej nie robimy.

## 12. `const` i `let`

### `const`

Używasz, gdy nie chcesz później przypisywać nowej wartości do zmiennej.

```js
const input = document.getElementById("status");
```

### `let`

Używasz, gdy wartość ma się zmieniać.

```js
let result = value;
```

Najprościej:

- `const` - domyślny wybór,
- `let` - gdy naprawdę chcesz coś później zmieniać.

## 13. Najczęstszy schemat w praktyce

Bardzo dużo kodu frontendowego wygląda tak:

1. znajdź element,
2. dodaj nasłuchiwanie na zdarzenie,
3. odczytaj wartość,
4. przelicz coś,
5. zaktualizuj HTML.

Przykład:

```js
const button = document.getElementById("save");
const input = document.getElementById("name");

button.addEventListener("click", function () {
    const text = input.value;
    console.log(text);
});
```

## 14. Co warto zapamiętać na teraz

Jeśli masz czuć, że ogarniasz podstawy JS do pracy z formularzem, to na ten moment najważniejsze są:

- `getElementById`
- `querySelector`
- `querySelectorAll`
- `forEach`
- `addEventListener`
- `value`
- `textContent`
- `createElement`
- `appendChild`
- `remove`
- `includes`
- `split`
- `length`
- `Number`
- `String`
- `return`

## 15. Ważna uwaga

To nie są "specjalne funkcje JavaScriptu" w jednym sensie.
W tej notatce są wymieszane:

- funkcje,
- metody,
- właściwości,
- atrybuty HTML,
- i kilka ważnych pojęć.

To normalne.
Przy nauce frontendu zwykle poznaje się je razem, bo razem pracują.
