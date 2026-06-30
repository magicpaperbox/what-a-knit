# HTML form: `name`, `value` i `form.getlist(...)`

Ta notatka jest o przepływie danych z formularza HTML do Flaskowego `request.form`.

W projekcie pojawiło się to przy dodawaniu zużycia motka w:

- `templates/projects/form.html`
- `src/modules/projects/api.py`
- `src/modules/projects/mappers.py`

## 1. Najważniejsza myśl

Formularz HTML wysyła do backendu pary:

```text
nazwa pola -> wartość pola
```

W HTML nazwa pola to atrybut `name`.

Przykład:

```html
<input name="used_yarn_weight" value="20">
```

Po wysłaniu formularza Flask może odczytać:

```python
form.get("used_yarn_weight")
```

i dostanie:

```python
"20"
```

## 2. Do czego służy `id`

`id` identyfikuje element na stronie.

Przykład:

```html
<label for="used_yarn_weight">Used yarn weight:</label>
<input id="used_yarn_weight" name="used_yarn_weight">
```

Tutaj:

- `id="used_yarn_weight"` oznacza: ten konkretny input ma taki identyfikator,
- `for="used_yarn_weight"` oznacza: ten label opisuje element o takim `id`.

`id` pomaga przeglądarce, CSS-owi i JavaScriptowi.
Samo `id` nie decyduje o tym, co trafi do `request.form`.

## 3. Do czego służy `name`

`name` decyduje, pod jaką nazwą wartość zostanie wysłana do backendu.

Przykład:

```html
<input type="number" id="used_yarn_weight" name="used_yarn_weight">
```

Po wysłaniu formularza Flask może odczytać:

```python
form.get("used_yarn_weight")
```

albo, jeśli takich pól może być kilka:

```python
form.getlist("used_yarn_weight", type=int)
```

Najważniejsze:

```text
HTML name="used_yarn_weight"
pasuje do
Python form.getlist("used_yarn_weight")
```

Nazwy muszą być takie same.

## 4. Gdzie wolno dawać `name`

`name` dajemy na elementach formularza, które wysyłają dane.

Najczęstsze przykłady:

```html
<input name="...">
<select name="...">
<textarea name="...">
```

Nie dajemy `name` na zwykłych elementach do układu albo tekstu:

```html
<div>
<p>
<label>
```

Te elementy nie wysyłają wartości do formularza.

## 5. Jak działa `select` i `option`

Przykład z projektu:

```html
<label for="skein_id">Yarn used:</label>
<select id="skein_id" name="skein_id">
    {% for skein in available_skeins %}
        <option value="{{ skein.id.value }}">
            Skein {{ skein.id.value }} - {{ skein.current_weight }}
        </option>
    {% endfor %}
</select>
```

Ten fragment trzeba czytać tak:

```html
<select id="skein_id" name="skein_id">
```

- `id="skein_id"` łączy pole z labelem,
- `name="skein_id"` mówi: wyślij wybraną wartość pod nazwą `skein_id`.

Potem:

```html
<option value="{{ skein.id.value }}">
```

- `value="{{ skein.id.value }}"` mówi: jeśli wybrano tę opcję, wyślij id tego motka.

Tekst między `<option>` i `</option>` jest tylko tekstem widocznym na stronie:

```html
Skein {{ skein.id.value }} - {{ skein.current_weight }}
```

Czyli userka widzi np.:

```text
Skein 3 - 50 g
```

ale backend dostaje np.:

```text
skein_id = 3
```

## 6. Skąd bierze się `available_skeins`

W `src/modules/projects/api.py` przy renderowaniu formularza projektu przekazujesz:

```python
available_skeins=yarn_service.get_all_skeins()
```

To znaczy:

```text
Pobierz wszystkie dostępne motki z YarnService
i daj je template pod nazwą available_skeins.
```

W template możesz potem zrobić:

```html
{% for skein in available_skeins %}
```

To jest pętla Jinja.
Działa podobnie do pętli `for` w Pythonie:

```python
for skein in available_skeins:
    ...
```

## 7. Jak Flask odbiera te pola

W `src/modules/projects/mappers.py` masz:

```python
skein_ids = form.getlist("skein_id", type=int)
used_yarn_weights = form.getlist("used_yarn_weight", type=int)
```

To pasuje do pól HTML:

```html
<select name="skein_id">
<input name="used_yarn_weight">
```

Czyli przepływ wygląda tak:

```text
template:
name="skein_id"
name="used_yarn_weight"

backend:
form.getlist("skein_id", type=int)
form.getlist("used_yarn_weight", type=int)
```

## 8. Dlaczego używamy `getlist(...)`

`form.get(...)` bierze jedną wartość.

`form.getlist(...)` bierze listę wartości o tej samej nazwie.

To jest przydatne, jeśli formularz kiedyś będzie mógł wysłać kilka motków:

```html
<select name="skein_id">...</select>
<input name="used_yarn_weight">

<select name="skein_id">...</select>
<input name="used_yarn_weight">
```

Wtedy Flask może dostać:

```python
skein_ids = [1, 2]
used_yarn_weights = [50, 20]
```

I potem można je połączyć przez:

```python
zip(skein_ids, used_yarn_weights)
```

## 9. Najkrótsza wersja do zapamiętania

```text
id = identyfikator elementu na stronie
for = label wskazuje input/select o takim id
name = nazwa pola wysyłana do Flaskowego request.form
value = konkretna wartość wysyłana po wybraniu opcji albo wpisaniu pola
```

Najważniejsze połączenie:

```text
HTML:
name="skein_id"

Python:
form.getlist("skein_id", type=int)
```

Jeśli te nazwy się nie zgadzają, backend nie znajdzie danych z formularza.
