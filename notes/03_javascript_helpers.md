# JavaScript: Pomocnicze funkcje (Helpers) i funkcja strzałkowa

Zapis, o który pytasz: 
```javascript
const $ = (id) => document.getElementById(id);
```
To tak zwana **funkcja pomocnicza** (z ang. *helper*). Programiści często dodają ją na samej górze swoich skryptów w czystym JavaScripcie, po to, by zaoszczędzić sobie pisania i uczynić kod czytelniejszym.

Rozbijmy to na czynniki pierwsze!

## Co ten kod dokładnie robi? Krok po kroku

1. `const $`
   Tworzysz nową **stałą** (zmienną, której nie zmienisz w trakcie działania skryptu). Ma ona nazwę `$`. Mimo że znak dolara wygląda groźnie i specyficznie, dla JavaScriptu jest jak każda inna zwykła litera. Równie dobrze mogłabyś napisać `const znajdz = ...`.

2. `= (id) =>`
   To jest nowszy, krótszy sposób zapisu. Tworzymy tzw. **funkcję strzałkową** (*arrow function*). Zapis wyżej po prostu mówi: "przygotuj mi funkcję, która otrzymuje jeden kawałek informacji (argument) oznaczony jako `id`, a z wynikiem zrób to, co wskazuje strzałka `=>`".

3. `document.getElementById(id)`
   To główny bohater całej operacji. Standardowa formułka wbudowana w każdą przeglądarkę, która każe jej przeszukać plik HTML (`document`) w poszukiwaniu jednego konkretnego elementu po jego identyfikatorze `id="..."` (`getElementById`).

Zapis tradycyjny wyglądałby tak i robiłby **dokładnie to samo**:
```javascript
function $(id) {
    return document.getElementById(id);
}
```

## Po co się tego używa? (I dlaczego warto)

Gdy połączysz Front-end z interaktywnością, będziesz w kółko "wyciągać" jakieś wartości ze strony albo ukrywać modale. 

**Wyciąganie okienek bez pomocnika:**
```javascript
let myRows = document.getElementById("rows").value;
let myColumns = document.getElementById("cols").value;
let createButton = document.getElementById("build");

createButton.addEventListener("click", doSomething);
```

**Z pomocnikiem `$()` (naszym skrótem):**
```javascript
let myRows = $("rows").value;
let myColumns = $("cols").value;
let createButton = $("build");

createButton.addEventListener("click", doSomething);
```
Prawda, że od razu widać, gdzie ukrywa się logika i z jakimi okienkami HTML powiązana jest akcja, zamiast gubić się w słowach `document...`? To o wiele "czystszy" kod.

## Kiedy z tego korzystamy?

1. **Gdy budujesz coś mniejszego lub mocno opartego na ID tagów.** Np. w generowaniu map, mini-gierkach w samej przeglądarce czy przyciskach podłączonych do zaawansowanych formularzy kalkulujących koszty, kiedy nie korzystasz z żadnego przepotężnego narzędzia Frontend'owego w stylu React czy Vue (które robią to inaczej pod maską).
2. **Kiedy lubisz porządek.** Ten mechanizm nie zmienia niczego w "backendowej" głębokiej wiedzy, jest w 100% "lukrem składniowym" (syntax sugar). To ma ułatwić życie Tobie jako programiście i przyspieszyć pisanie kodu.

### Ciekawostka o znaku dolara ($)
Sama nazwa `$` wzięła się z popularnego lata temu narzędzia o nazwie `jQuery`. Tam wszystko zaczynało się od dolara. Dzisiaj czysty, współczesny JavaScript (nazywany dumnie "Vanilla JS") potrafi to wszystko sam, ale programiści tak przyzwyczaili używać dolara jako maszynki do zwracania okienek, że wprowadzają sobie taki skrót, żeby nie musieć cofać się w czasie z nawykami pisania.
