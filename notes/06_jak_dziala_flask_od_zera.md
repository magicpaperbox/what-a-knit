# Jak działa Flask — od zera

## Jak działa internet (w wielkim uproszczeniu)

Kiedy wpisujesz adres w przeglądarkę, dzieje się prosta wymiana:

1. **Przeglądarka** wysyła **żądanie** (request) — "daj mi tę stronę!"
2. **Serwer** odbiera żądanie, robi swoją robotę i wysyła **odpowiedź** (response) — gotowy HTML
3. **Przeglądarka** wyświetla otrzymany HTML

To tyle! Internet to pytanie → odpowiedź.

---

## Co robi Flask?

Flask to framework Pythonowy, który stawia **serwer** na Twoim komputerze.
Kiedy uruchamiasz `app.run()`, Flask:

1. ⏳ **Czeka** na żądania od przeglądarki
2. 🔍 **Patrzy** na adres — co przeglądarka chce?
3. 🐍 **Uruchamia** odpowiednią funkcję Pythona
4. 📨 **Odsyła** wynik (HTML) z powrotem do przeglądarki

Flask to jak **kelner** — przeglądarka zamawia danie, Flask idzie do kuchni (Twój kod),
gotuje (wywołuje funkcję) i przynosi danie (HTML) do stolika (przeglądarki).

Lokalnie serwer działa pod adresem `http://localhost:5000`:
- `localhost` = ten komputer
- `5000` = numer portu (drzwi)

---

## Route — adres + funkcja

**Route** łączy adres URL z funkcją Pythona.
Kiedy ktoś wejdzie na dany adres — Flask uruchomi przypisaną funkcję.

```python
@app.route('/')           # adres: strona główna
def index():              # funkcja która się uruchomi
    return "<h1>Witaj!</h1>"  # to zostanie zwrócone do przeglądarki
```

### Ważne:
- `@app.route(...)` to **dekorator** — "naklejka" na funkcję
- W `@` piszesz **nazwę zmiennej** (np. `app`), nie nazwę pliku
- Jeśli ktoś wejdzie na adres, który nie ma route'a → dostanie **404 Not Found**
- `methods=['POST']` — route reaguje na wysłanie formularza, nie na wejście na stronę

---

## Szablony (templates) i render_template

Zamiast pisać HTML w Pythonie, tworzymy osobne pliki HTML w folderze `templates/`:

```python
# app.py
@app.route('/recipes')
def recipes():
    return render_template('recipes.html')
```

- `render_template()` szuka pliku **automatycznie** w folderze `templates/`
- Piszesz tylko nazwę pliku: `'recipes.html'`, NIE `'/templates/recipes.html'`

---

## Przekazywanie zmiennych do szablonu: {{ }}

Możesz przekazać zmienne z Pythona do HTML:

```python
# app.py — wysyłasz zmienne
return render_template('recipes.html', baker='Klaudia', oven_temp=180)
```

```html
<!-- recipes.html — odbierasz zmienne -->
<h1>Przepisy {{ baker }}</h1>
<p>Temperatura: {{ oven_temp }}°C</p>
```

`{{ }}` = **wypisz wartość zmiennej**

Przeglądarka nigdy nie widzi `{{ baker }}` — dostaje gotowe `Przepisy Klaudia`.

---

## Jinja2 — silnik szablonów (to NIE jest Python!)

To co piszesz w szablonach HTML to **Jinja2** — osobny, uproszczony język.
Wygląda podobnie do Pythona, ale ma inną składnię:

### Dwa rodzaje znaczników:
- `{{ }}` — **wypisz** wartość (wyświetl coś)
- `{% %}` — **wykonaj** instrukcję (logika: pętla, if — sama nic nie wyświetla)

### Pętla for:
```html
{% for cake in cakes %}
    <li>{{ cake }}</li>
{% endfor %}              <!-- WAŻNE: trzeba zamknąć! -->
```

### Warunek if:
```html
{% if temp > 200 %}
    <p>🔥 Za gorąco!</p>
{% elif temp > 100 %}
    <p>👍 W sam raz</p>
{% else %}
    <p>🥶 Za zimno!</p>
{% endif %}               <!-- WAŻNE: trzeba zamknąć! -->
```

### Różnica vs Python:
| Python           | Jinja2                          |
|------------------|---------------------------------|
| `for x in y:`   | `{% for x in y %}`             |
| koniec = wcięcie | `{% endfor %}`                  |
| `if x > 5:`     | `{% if x > 5 %}`               |
| koniec = wcięcie | `{% endif %}`                   |

---

## Dziedziczenie szablonów: base.html

**Problem:** Każda strona potrzebuje tego samego nagłówka, menu, stopki.
Kopiowanie tego do każdego pliku = koszmar.

**Rozwiązanie:** Jeden plik bazowy z "dziurą" na treść.

### base.html — wspólna ramka:
```html
<html>
<body>
    <h1>🎂 Lets Bake a Cake!</h1>
    <nav>
        <a href="/">Home</a>
        <a href="/recipes">Przepisy</a>
    </nav>

    {% block content %}
    {% endblock %}         <!-- ← DZIURA na treść -->

    <footer>@ Klaudia 2026</footer>
</body>
</html>
```

### recipes.html — wypełnia dziurę:
```html
{% extends 'base.html' %}    <!-- weź base.html -->
{% block content %}           <!-- wstaw to w dziurę -->
    <h2>Moje przepisy</h2>
    ...
{% endblock %}
```

- `{% extends 'base.html' %}` = "użyj ramki z base.html"
- `{% block content %}` = "a oto moja treść do wstawienia"

---

## Jinja2 vs JavaScript — kto kiedy działa?

```
1. Przeglądarka prosi o stronę
2. 🐍 SERWER (Python + Jinja2) → generuje HTML
   └── {% for %}, {{ }} — działa TUTAJ (jednorazowo)
3. HTML jedzie do przeglądarki
4. 🌐 PRZEGLĄDARKA (JavaScript) → dodaje interaktywność
   └── kliknięcia, animacje — działają TUTAJ (cały czas)
```

Jinja2 = pieczesz tort w kuchni (zanim podasz)
JavaScript = świeczki migające na torcie (po podaniu)

---

## Blueprint — podział aplikacji na moduły

Blueprint to **klasa wbudowana we Flaska**. Pozwala dzielić aplikację na osobne pliki.

```python
# yarn/api.py
from flask import Blueprint
yarn_api = Blueprint('yarn', __name__)

@yarn_api.route('/yarn')
def yarn_list():
    ...
```

```python
# app.py — podłącza moduły
app.register_blueprint(yarn_api)
```

- Blueprint to **pojemnik na routy**
- `register_blueprint()` = podłącz pojemnik do aplikacji
- Efekt taki sam jakby routy były bezpośrednio na `app`, ale **kod jest podzielony na pliki**

---

## Cały przepływ żądania — schemat:

```
Przeglądarka: GET /recipes
       ↓
Flask: "Kto obsługuje /recipes?" → route → funkcja recipes()
       ↓
recipes(): render_template('recipes.html', cakes=[...])
       ↓
Jinja2: base.html + recipes.html + zmiennych → gotowy HTML
       ↓
Flask: odsyła HTML do przeglądarki
       ↓
Przeglądarka: wyświetla stronę + pobiera CSS/JS
```

---

## Minimalna aplikacja Flask (ściągawka):

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name='Klaudia')

if __name__ == '__main__':
    app.run(debug=True)
```

Potrzebna struktura plików:
```
projekt/
├── app.py
├── templates/
│   └── index.html
```
