# 02 - Baza danych (Flask-SQLAlchemy) i formularze

## HTML Select (dropdown)

### Podstawowy select
Zamiast `<input type="text">` można użyć `<select>` – rozwijaną listę opcji:
```html
<select id="type" name="type">
    <option value="sweater">Sweater</option>
    <option value="hat">Hat</option>
    <option value="socks">Socks</option>
</select>
```

**WAŻNE:** `<select>` ZASTĘPUJE `<input>` – nie dodajemy obu naraz!

### Placeholder w select
Select nie ma atrybutu `placeholder`. Zamiast tego dodajemy specjalny `<option>` na początku:
```html
<option value="" disabled selected hidden>Choose a category...</option>
```
- `disabled` – nie można tego wybrać z listy
- `selected` – wyświetla się domyślnie
- `hidden` – nie pokazuje się po rozwinięciu listy

### Dynamiczne opcje zależne od wyboru
Np. subcategory zależy od wybranej category – do tego potrzeba **JavaScript**!
- Python/Jinja2 działa na SERWERZE (przed wyświetleniem strony)
- JavaScript działa w PRZEGLĄDARCE (reaguje na akcje użytkownika)
- Dane mogą pochodzić z Pythona, ale interakcja wymaga JS

---

## SQL vs MySQL vs SQLite

- **SQL** = JĘZYK zapytań do baz danych (jak Python jest językiem programowania)
- **MySQL** = PROGRAM bazy danych (wymaga instalacji serwera)
- **SQLite** = PROGRAM bazy danych (wbudowany w Pythona! Dane w jednym pliku .db)
- Składnia SQL jest prawie identyczna w obu

Dla małych projektów i nauki → **SQLite** (zero instalacji, `import sqlite3`)

---

## Flask-SQLAlchemy (ORM)

ORM (Object-Relational Mapping) = sposób pracy z bazą danych przez klasy Pythona
zamiast pisania SQL ręcznie. Używany wszędzie w branży!

### Instalacja
```bash
uv add flask-sqlalchemy
```

### Konfiguracja w app.py
```python
from flask_sqlalchemy import SQLAlchemy

app = Flask("what a knit")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knit.db'  # plik bazy
db = SQLAlchemy(app)  # obiekt "łącznika" z bazą
```

### Tworzenie modelu (klasy = tabela w bazie)
```python
class Pattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)       # unikalne ID, baza nadaje automatycznie
    name = db.Column(db.String(100), nullable=False)    # tekst, max 100 znaków, wymagane
    type = db.Column(db.String(50))                     # tekst, opcjonalne
    subtype = db.Column(db.String(50))
    difficulty = db.Column(db.Integer)                   # liczba całkowita
    notes = db.Column(db.String(500))
```

Typy kolumn:
- `db.Integer` – liczba całkowita
- `db.String(100)` – tekst (max 100 znaków)
- `nullable=False` – pole wymagane (nie może być puste)
- `primary_key=True` – unikalny identyfikator, baza sama nadaje numery

### Tworzenie bazy danych (pliku .db)

**Jednolinijkowa komenda (POLECANA!):**
```bash
uv run python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Done!')"
```

Albo interaktywnie w Pythonie:
```bash
uv run python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...                          # <-- pusty Enter żeby zamknąć blok with!
>>> exit()
```

Plik bazy pojawi się w: `instance/knit.db`

### ⚠️ Jak wydostać się z terminala Python:
- `exit()` – normalne wyjście
- `Ctrl+C` – przerwanie (jeśli coś się zawiesiło)
- `Ctrl+Z` + Enter – wymuszone wyjście z Pythona (Windows)
- Jeśli widzisz `...` – jesteś w bloku, wciśnij pusty Enter żeby go zamknąć

### ⚠️ Po zmianie modelu (dodaniu/usunięciu kolumn):
1. Usuń stary plik bazy: `del instance\knit.db`
2. Stwórz bazę ponownie (komenda wyżej)
3. Dane zostaną utracone! (w przyszłości migracje to rozwiążą)

---

## Operacje na bazie danych (CRUD)

### Dodawanie rekordu (Create)

```python
new_pattern = Pattern(
    name=request.form['name'],
    type=request.form['type'],
    subtype=request.form['subtype'],
    notes=request.form['notes']
)
db.session.add_straight_needles(new_pattern)  # dodaj do sesji
db.session.commit()  # ZAPISZ! (jak kliknięcie "Save")
```
Po `commit()` obiekt dostaje swoje `id`: `new_pattern.id`

### Odczyt wszystkich rekordów (Read)
```python
patterns = Pattern.query.all()  # zwraca listę obiektów Pattern
```

### Odczyt jednego rekordu po ID
```python
pattern = db.get_or_404(Pattern, pattern_id)  # znajdź lub pokaż błąd 404
```

---

## Ważne zasady

### Linki do rekordów – używaj ID z bazy, nie indeksu pętli!
```html
<!-- ŹLE (stare, listowe podejście): -->
<a href="/pattern/{{ loop.index0 }}">

<!-- DOBRZE (bazodanowe podejście): -->
<a href="/pattern/{{ pattern.id }}">
```
ID z bazy jest STAŁE – nie zmienia się nawet po usunięciu innych rekordów.

### request.form['nazwa'] musi odpowiadać atrybutowi name="" w HTML
```html
<input name="notes">          <!-- HTML -->
```
```python
request.form['notes']          # Python – musi być identyczne!
```

### Przepływ danych (jednokierunkowy!)
```
Python (dane) → render_template() → Jinja2 (wkleja w HTML) → Przeglądarka
```
Python wysyła dane i "zapomina". Nie ma ciągłej komunikacji.

---

## TODO na później
- [ ] Usunąć zakomentowaną starą listę `patterns` z app.py
- [ ] Dodać `instance/` do `.gitignore`
- [ ] Dynamiczne dropdowny (SUBCATEGORIES dict → Jinja2 pętla)
- [ ] Ostylować `<select>` w CSS
- [ ] JavaScript do zależnych dropdownów (subcategory zależy od category)
