# Jak szukać w kodzie, gdzie zmienić formatowanie wartości

Ta notatka jest o sytuacji typu:

- na stronie widzisz `10.0 x 10.0 cm`
- albo `24.0 sts / 32.0 rows`
- i chcesz znaleźć **w którym miejscu kodu naprawdę warto to zmienić**

Najważniejsza myśl:

- **nie zaczynaj od zgadywania pliku do edycji**
- zacznij od miejsca, które widzisz na stronie
- potem idź po ścieżce danych krok po kroku

---

## 1. Start od template, nie od backendu

Jeśli problem widzisz na ekranie, najpierw znajdź go w HTML/Jinja.

W przykładzie z gauge jest to:

- [templates/patterns/details.html](/mnt/c/Users/klaud/PycharmProjects/what-a-knit/templates/patterns/details.html)

Tam masz np.:

```jinja2
{{ pattern.target_gauge.stitches }} sts /
{{ pattern.target_gauge.rows }} rows
per {{ pattern.target_gauge.width.value }} x {{ pattern.target_gauge.height.value }} cm
```

To jest punkt startowy.

Na tym etapie jeszcze **nie decydujesz, gdzie zmieniać kod**.
Najpierw ustalasz:

- jaka zmienna jest renderowana
- czy jest użyta bezpośrednio
- czy jest użyte `.value`

W tym przykładzie od razu widać różnicę:

- `pattern.target_gauge.stitches`
- `pattern.target_gauge.width.value`

To już podpowiada, że `stitches` i `width` prawdopodobnie **nie są tym samym typem danych**.

---

## 2. Znajdź, skąd template dostaje zmienną

Jeśli w template masz:

```jinja2
{{ pattern.target_gauge.stitches }}
```

to następnym pytaniem jest:

- skąd template dostał `pattern`?

Szukasz więc:

- `render_template('patterns/details.html'`
- albo po prostu nazwy pliku template

W tym projekcie trafiasz do:

- [src/modules/patterns/api.py](/mnt/c/Users/klaud/PycharmProjects/what-a-knit/src/modules/patterns/api.py)

Konkretnie do funkcji `details()`:

```python
@patterns_api.get('/<int:pattern_id>')
def details(pattern_id: int):
    pattern = get_pattern_or_404(PatternId(pattern_id))
    return render_template('patterns/details.html', pattern=pattern)
```

Tu ważna zasada:

- jeśli funkcja tylko pobiera dane i przekazuje je do template,
- to zwykle **nie jest jeszcze miejscem na poprawkę formatowania**

Ta funkcja tylko mówi:

- weź `pattern`
- przekaż go do template

---

## 3. Jeśli trafiasz na "przelotówkę", idź dalej

W [src/modules/patterns/api.py](/mnt/c/Users/klaud/PycharmProjects/what-a-knit/src/modules/patterns/api.py) masz też:

```python
def get_pattern_or_404(pattern_id: PatternId):
    pattern = repo.get_by_id(pattern_id)
    if pattern is None:
        abort(404, f"Pattern id {pattern_id} doesn't exist.")
    return pattern
```

To też jest tylko przelotówka.

Co ona robi:

- woła repozytorium
- sprawdza, czy coś znaleziono
- zwraca obiekt dalej

Jeśli funkcja:

- nie zmienia danych
- nie formatuje danych
- nie buduje napisu

to najczęściej idziesz dalej.

Tutaj kolejnym krokiem jest:

- `repo.get_by_id(...)`

---

## 4. Szukaj miejsca, gdzie obiekt jest składany

To jest najważniejszy krok.

W tym projekcie trafiasz do:

- [src/modules/patterns/repository.py](/mnt/c/Users/klaud/PycharmProjects/what-a-knit/src/modules/patterns/repository.py)

W funkcji `PatternRepository.get_by_id()`:

```python
def get_by_id(self, pattern_id: PatternId) -> Optional[Pattern]:
    ...
    pattern_row = PatternRow(**dict(row))
    gauge_row = self._get_gauge(pattern_row.id)
    return self._row_to_domain(pattern_row, gauge_row)
```

Tutaj bardzo ważny trop to nazwa:

- `_row_to_domain()`

Takie nazwy zwykle oznaczają:

- "zamieniam surowy wiersz z bazy na obiekt Pythona"

I właśnie to miejsce bardzo często odpowiada na pytanie:

- czym naprawdę jest `stitches`
- czym naprawdę jest `width`

---

## 5. Dopiero tutaj sprawdzasz typy danych

W [src/modules/patterns/repository.py](/mnt/c/Users/klaud/PycharmProjects/what-a-knit/src/modules/patterns/repository.py), w `PatternRepository._row_to_domain()`:

```python
gauge = Gauge(
    float(gauge_row.stitches) if gauge_row.stitches is not None else None,
    float(gauge_row.rows) if gauge_row.rows is not None else None,
    width=Centimeters(gauge_row.width_cm) if gauge_row.width_cm is not None else None,
    height=Centimeters(gauge_row.height_cm) if gauge_row.height_cm is not None else None
)
```

To jest kluczowy moment.

Tu widać jasno:

- `stitches` staje się zwykłym `float`
- `rows` stają się zwykłym `float`
- `width` staje się obiektem `Centimeters(...)`
- `height` staje się obiektem `Centimeters(...)`

I dopiero teraz możesz rozsądnie zdecydować, gdzie to poprawić.

---

## 6. Jak z tego wywnioskować miejsce zmiany

### Przypadek A: zwykły `float`

Jeśli wartość kończy jako zwykły `float`, jak:

- `Gauge.stitches`
- `Gauge.rows`

to nie masz osobnej klasy typu `Stitches` albo `Rows`, w której można zrobić `__str__()`.

Wtedy poprawki zwykle szukasz:

- w template
- albo w helperze / właściwości w klasie domenowej

### Przypadek B: obiekt jednostki

Jeśli wartość kończy jako obiekt, jak:

- `Centimeters(...)`
- `Meters(...)`

to bardzo często najlepszym miejscem na formatowanie jest właśnie ta klasa jednostki.

Przykłady z tego projektu:

- [src/modules/units/centimeters.py](/mnt/c/Users/klaud/PycharmProjects/what-a-knit/src/modules/units/centimeters.py)
- [src/modules/units/meters.py](/mnt/c/Users/klaud/PycharmProjects/what-a-knit/src/modules/units/meters.py)

Bo wtedy:

- logika formatowania jest w jednym miejscu
- działa w wielu miejscach aplikacji
- template może po prostu wypisać obiekt

---

## 7. Jak myśleć o tym na przykładzie gauge

### `width` i `height`

W template masz:

```jinja2
{{ pattern.target_gauge.width.value }}
{{ pattern.target_gauge.height.value }}
```

Po przejściu przez repo widzisz, że to są obiekty `Centimeters`.

Wniosek:

- sensowne miejsce poprawki to `Centimeters`
- czyli plik [src/modules/units/centimeters.py](/mnt/c/Users/klaud/PycharmProjects/what-a-knit/src/modules/units/centimeters.py)

### `stitches` i `rows`

W template masz:

```jinja2
{{ pattern.target_gauge.stitches }}
{{ pattern.target_gauge.rows }}
```

Po przejściu przez repo widzisz, że to są zwykłe `float`.

Wniosek:

- samo poprawienie `Centimeters` nic tu nie da
- dla tych pól trzeba szukać innego rozwiązania niż `__str__()` klasy jednostki

---

## 8. Szybka reguła: gdzie raczej NIE poprawiać

### `api.py`

Zwykle nie poprawiasz tam formatowania, jeśli funkcja tylko:

- pobiera dane
- przekazuje je do template

Przykład:

- [src/modules/patterns/api.py](/mnt/c/Users/klaud/PycharmProjects/what-a-knit/src/modules/patterns/api.py), funkcja `details()`

### `get_*_or_404()`

To zwykle nie jest miejsce na formatowanie.
Taka funkcja najczęściej tylko:

- sprawdza istnienie obiektu
- zwraca go dalej

### `repository.py`

Repository to zwykle miejsce do:

- odczytu z bazy
- zapisu do bazy
- składania obiektu domenowego

Repository bardzo pomaga **zrozumieć typy**, ale zwykle nie jest najlepszym miejscem na robienie "ładnego napisu dla użytkownika".

---

## 9. Praktyczny schemat szukania

Gdy widzisz coś brzydko wyświetlonego na stronie:

1. Znajdź dokładny fragment w template.
2. Spisz pełną ścieżkę zmiennej, np. `pattern.target_gauge.width.value`.
3. Znajdź `render_template(...)`, które przekazuje główną zmienną do tego template.
4. Znajdź, skąd ta zmienna pochodzi.
5. Jeśli trafiasz na `repo.get_by_id(...)`, wejdź do repozytorium.
6. Szukaj funkcji typu:
   - `get_by_id`
   - `_row_to_domain`
   - `_to_domain`
   - `from_row`
   - `map_*`
7. Sprawdź, czym kończy się dana wartość:
   - `int`
   - `float`
   - obiekt typu `Meters`, `Centimeters`, itp.
8. Dopiero wtedy wybierz miejsce poprawki.

---

## 10. Dobre hasła do wyszukiwania w projekcie

Kiedy nie wiesz, od czego zacząć, szukaj po tym, co naprawdę widzisz na stronie.

Przykłady dobrych haseł:

- `sts`
- `rows`
- `cm`
- `Gauge:`
- `.value`
- `render_template('patterns/details.html'`
- `target_gauge`
- `actual_gauge`

Szczególnie przydatne:

- `.value`

Bo bardzo często problem "czemu wyświetla się surowa liczba" bierze się właśnie z tego, że template wypisuje `.value`, zamiast korzystać z formatowania obiektu.

---

## 11. Najkrótsza mapa do zapamiętania

- template mówi Ci **co się wyświetla**
- `render_template(...)` mówi Ci **co zostało przekazane**
- repository mówi Ci **z czego to zostało zbudowane**
- domain / units mówi Ci **gdzie najlepiej to sformatować**

Jeśli się gubisz, wróć do tego pytania:

- **czy ja teraz patrzę na miejsce renderowania, miejsce przekazania danych, miejsce budowy obiektu, czy miejsce formatowania?**

To bardzo pomaga nie mieszać warstw.
