# Notatki: Flask + Jinja2 — Podstawy

## Czym jest Flask?

Flask to **mikro-framework** webowy w Pythonie. "Mikro" oznacza, że daje Ci minimum
potrzebne do postawienia strony internetowej — resztę dobierasz sama wg potrzeb.

Podstawowy plik Flask (`app.py`) wygląda tak:

```python
from flask import Flask, render_template

app = Flask("what a knit")

@app.route('/')
def hello_world():
    return render_template('index.html', title='Moja strona')

if __name__ == '__main__':
    app.run(debug=True)
```

### Co tu się dzieje?

1. `app = Flask("what a knit")` — tworzymy aplikację Flask
2. `@app.route('/')` — mówimy: "gdy ktoś wejdzie na adres `/`, wywołaj funkcję poniżej"
3. `render_template('index.html', ...)` — załaduj plik HTML i przekaż do niego dane
4. `app.run(debug=True)` — uruchom serwer (debug=True = automatyczny restart po zmianach)

### Przepływ danych

```
1. Użytkownik wchodzi na stronę "/"
2. Flask wywołuje funkcję hello_world()
3. Funkcja wywołuje render_template('index.html', yarns=[...])
4. Jinja2 bierze index.html i wstawia dane w odpowiednie miejsca
5. Flask odsyła gotowy HTML do przeglądarki
```

**Ważne:**
- `app.py` = logika, dane, decyzja CO pokazać
- template (HTML) = wygląd, decyzja JAK pokazać
- Dane lecą z app.py → template przez `render_template()`

---

## Czym jest Jinja2?

Jinja2 to **silnik szablonów** (template engine). Pozwala pisać HTML z "dziurami",
w które Flask wstawia dane z Pythona.

### Trzy rodzaje znaczników

| Znacznik   | Do czego                          | Przykład                        |
|------------|-----------------------------------|---------------------------------|
| `{{ }}`    | **Wyświetl wartość** — wstaw tekst | `{{ username }}` → Klaudia     |
| `{% %}`    | **Logika** — if, for, etc.        | `{% if is_logged_in %}`        |
| `{# #}`    | **Komentarz** — ignorowane        | `{# to jest komentarz #}`     |

Wszystko POZA tymi znacznikami to zwykły HTML, który leci na stronę bez zmian.

---

## 1. Wyświetlanie zmiennych: `{{ zmienna }}`

W `app.py` przekazujesz zmienne:
```python
return render_template('index.html',
    username='Klaudia',
    current_date='2026-02-18'
)
```

W template używasz ich przez podwójne klamry:
```html
<p>Witaj, <strong>{{ username }}</strong>!</p>
<p>Dzisiaj jest: {{ current_date }}</p>
```

**Ważne:** Gdybyś nie przekazała `username` w `render_template()`,
a spróbowała użyć `{{ username }}` w template — dostaniesz błąd albo pustą wartość.
Dane NIE przekazują się automatycznie — to Ty decydujesz co wysłać.

---

## 2. Warunki: `{% if %}`

Działają jak `if` w Pythonie, ale owinięte w `{% %}`:

```html
{% if is_logged_in %}
    <p>✅ Jesteś zalogowany!</p>
{% else %}
    <p>❌ Nie jesteś zalogowany.</p>
{% endif %}
```

Można też używać `elif`:

```html
{% if yarn_count > 5 %}
    <p>🎉 Masz dużo włóczek! ({{ yarn_count }} sztuk)</p>
{% elif yarn_count > 0 %}
    <p>📦 Masz trochę włóczek: {{ yarn_count }}</p>
{% else %}
    <p>😢 Nie masz żadnych włóczek.</p>
{% endif %}
```

**Uwaga:** W Pythonie blok kodu kończy się wcięciem.
W Jinja2 musisz jawnie zamknąć blok przez `{% endif %}`.

---

## 3. Pętle: `{% for %}`

Działają jak `for` w Pythonie:

```html
{% for yarn in yarns %}
    <li>{{ yarn.color }} - {{ yarn.weight }}g</li>
{% endfor %}
```

Gdzie `yarns` to lista przekazana z `app.py`:
```python
yarns=[
    {'color': 'Czerwona', 'weight': 100},
    {'color': 'Niebieska', 'weight': 150},
    {'color': 'Zielona', 'weight': 200}
]
```

### Specjalna zmienna `loop`

Wewnątrz pętli masz dostęp do zmiennej `loop`:

- `loop.index` — numer iteracji (od 1)
- `loop.index0` — numer iteracji (od 0)
- `loop.first` — True jeśli to pierwsza iteracja
- `loop.last` — True jeśli to ostatnia iteracja
- `loop.length` — liczba elementów

Przykład:
```html
{% for yarn in yarns %}
    {{ loop.index }}. {{ yarn.color }}
    {% if loop.first %} 👑 (pierwsza!){% endif %}
    {% if loop.last %} 🏁 (ostatnia!){% endif %}
{% endfor %}
```

**Uwaga:** Tak jak `if`, pętla wymaga jawnego zamknięcia: `{% endfor %}`.

---

## 4. Filtry: `{{ zmienna|filtr }}`

Filtry modyfikują wartość przed wyświetleniem. Używa się znaku `|` (pipe):

```html
{{ message }}            →  Witaj w świecie Jinja2!
{{ message|upper }}      →  WITAJ W ŚWIECIE JINJA2!
{{ message|lower }}      →  witaj w świecie jinja2!
{{ message|capitalize }} →  Witaj w świecie jinja2!
{{ message|length }}     →  23 (liczba znaków)
```

Przydatne filtry:
- `upper` / `lower` — zmiana wielkości liter
- `capitalize` — pierwsza litera wielka
- `length` — długość tekstu lub listy
- `default('wartość')` — wartość domyślna jeśli zmienna jest pusta
- `round` — zaokrąglanie liczb

---

## 5. Operacje w szablonie

Możesz wykonywać proste obliczenia bezpośrednio w template:

```html
<p>Masz {{ yarn_count }} włóczek po {{ yarn_weight }}g każda</p>
<p>Razem: {{ yarn_count * yarn_weight }}g włóczki!</p>
```

Ale uwaga — cięższa logika powinna być w `app.py`, nie w template!
Template ma się zajmować **wyświetlaniem**, nie obliczeniami.

---

## 6. Dziedziczenie template i własne bloki na skrypty

To jest bardzo praktyczna rzecz, gdy jedna strona potrzebuje dodatkowego JavaScriptu, a inna nie.

Przykład z `base.html`:

```html
{% block content %}{% endblock %}

<script src="/static/js/theme.js"></script>
{% block scripts %}{% endblock %}
```

Jak to czytać:

- `base.html` definiuje miejsce, które dziecko może później uzupełnić
- `{% block scripts %}` nie ładuje nic samo z siebie
- to jest tylko "gniazdko", w które inny template może wstawić własne skrypty

Po co to jest:

- `theme.js` może zostać globalny dla całej aplikacji
- a konkretna strona może dołożyć swój własny plik JS
- dzięki temu nie wrzucasz wszystkiego do jednego wielkiego `theme.js`

Przykład w template potomnym, np. `templates/patterns/add.html`:

```html
{% block scripts %}
    {{ super() }}
    <script src="/static/js/pattern-form.js"></script>
{% endblock %}
```

### Co robi `{{ super() }}`

To jest bardzo ważne.

`{{ super() }}` znaczy:

- "zachowaj też zawartość tego samego bloku z template rodzica"

Czyli:

- rodzic `base.html` ma w bloku `scripts` swoją zawartość
- dziecko dodaje coś od siebie
- `{{ super() }}` mówi Jinja: nie nadpisuj wszystkiego, tylko dołóż to do tego, co już było

Jak jest teraz:

- dziecko definiuje własny `{% block scripts %}`

Jak powinno być, jeśli chcesz rozszerzyć blok rodzica:

- w środku dajesz `{{ super() }}`
- a dopiero potem swoje dodatkowe `<script ...>`

Dlaczego bez `{{ super() }}` łatwo coś zepsuć:

- jeśli dziecko nadpisze blok i nie użyje `{{ super() }}`, to zawartość z rodzica przepada
- czyli możesz przypadkiem przestać ładować skrypt globalny z `base.html`

Najkrótsza wersja do zapamiętania:

- `{% block scripts %}` = miejsce na skrypty strony
- `{{ super() }}` = zachowaj też to, co było w rodzicu
- dodatkowy `<script src="..."></script>` = doładuj JS tylko dla tej jednej strony

To jest dobry pierwszy krok do porządkowania frontendu:

- kod globalny zostaje globalny
- kod dla jednej strony trafia do osobnego pliku
- template tej strony jawnie mówi, jaki skrypt jest jej potrzebny

---

## FAQ — pytania i odpowiedzi

### Co to `{% raw %}` i `{% endraw %}`?

Mówi Jinja2: "nie ruszaj tego, potraktuj jako zwykły tekst".
Potrzebne tylko gdy chcesz WYŚWIETLIĆ składnię Jinja2 na stronie
(np. w samouczku), zamiast ją wykonać. W normalnej aplikacji raczej nie używasz.

### Co to tag `<code>`?

To zwykły tag HTML — wyświetla tekst czcionką monospace (jak w edytorze kodu).
Nie ma nic wspólnego z pisaniem kodu. To kwestia czysto wizualna:

- `<p>zwykły tekst</p>` → zwykły tekst
- `<code>tekst</code>` → tekst wyświetlony inną czcionką

### Skąd template wie o zmiennych?

Z `render_template()` w `app.py`! Każdy nazwany argument to zmienna:

```python
render_template('index.html',
    title='Moja strona',     # {{ title }} w template
    username='Klaudia',       # {{ username }} w template
    yarns=[...]               # {% for yarn in yarns %} w template
)
```

Nie ma żadnej magii — to Ty jawnie przekazujesz dane z Pythona do HTML-a.

---

## Struktura projektu Flask

```
what-a-knit/
├── app.py              ← główny plik aplikacji (logika, routy)
├── templates/          ← folder na pliki HTML (szablony Jinja2)
│   └── index.html
├── static/             ← folder na pliki statyczne (CSS, obrazki, JS)
├── pyproject.toml      ← konfiguracja projektu i zależności
└── notes/              ← notatki do nauki
```

Flask szuka szablonów w folderze `templates/` i plików statycznych w `static/`.
Te nazwy folderów są konwencją — Flask ich domyślnie szuka.
