# Python: `zip(...)`

Ta notatka jest o funkcji `zip(...)` w Pythonie.
Przydaje się wtedy, gdy masz dwie albo więcej list i chcesz przechodzić po ich elementach parami.

W projekcie pojawiło się to przy czytaniu danych formularza w:

- `src/modules/projects/mappers.py`
- `ProjectFormData.from_request_form()`

## 1. Najkrótsza intuicja

`zip(...)` działa jak suwak, który spina kilka list razem według pozycji.

Przykład:

```python
skein_ids = [1, 2, 3]
used_yarn_weights = [50, 20, 80]
```

Po użyciu:

```python
zip(skein_ids, used_yarn_weights)
```

Python widzi pary:

```python
(1, 50)
(2, 20)
(3, 80)
```

Czyli:

- pierwszy element z pierwszej listy z pierwszym elementem z drugiej listy,
- drugi element z pierwszej listy z drugim elementem z drugiej listy,
- trzeci element z pierwszej listy z trzecim elementem z drugiej listy.

## 2. Jak używać `zip(...)` w pętli

Najczęściej używa się `zip(...)` w pętli `for`:

```python
for skein_id, used_yarn_weight in zip(skein_ids, used_yarn_weights):
    print(skein_id, used_yarn_weight)
```

Ten zapis:

```python
for skein_id, used_yarn_weight in ...
```

oznacza:

```text
W każdej parze pierwszy element nazwij skein_id,
a drugi element nazwij used_yarn_weight.
```

Dla danych:

```python
skein_ids = [1, 2, 3]
used_yarn_weights = [50, 20, 80]
```

pętla przejdzie tak:

```text
skein_id = 1, used_yarn_weight = 50
skein_id = 2, used_yarn_weight = 20
skein_id = 3, used_yarn_weight = 80
```

## 3. Po co to przy formularzu

HTML formularz wysyła osobne wartości pól.

Jeśli masz kilka inputów o tej samej nazwie:

```html
<input name="skein_id" value="1">
<input name="skein_id" value="2">
```

to we Flasku możesz pobrać je jako listę:

```python
skein_ids = form.getlist("skein_id", type=int)
```

Jeśli masz też:

```html
<input name="used_yarn_weight" value="50">
<input name="used_yarn_weight" value="20">
```

to możesz pobrać drugą listę:

```python
used_yarn_weights = form.getlist("used_yarn_weight", type=int)
```

Potem `zip(...)` pozwala połączyć te listy w pary:

```python
for skein_id, used_yarn_weight in zip(skein_ids, used_yarn_weights):
    ...
```

Czyli Python czyta to tak:

```text
Pierwszy wybrany motek ma pierwszą wagę zużycia.
Drugi wybrany motek ma drugą wagę zużycia.
Trzeci wybrany motek ma trzecią wagę zużycia.
```

## 4. Ważne: `zip(...)` nie tworzy za Ciebie obiektów

`zip(...)` tylko daje pary wartości.

Jeśli chcesz stworzyć obiekty formularza, musisz zrobić to sama w pętli:

```python
skein_usage = []

for skein_id, used_yarn_weight in zip(skein_ids, used_yarn_weights):
    skein_usage.append(
        ProjectSkeinFormData(
            skein_id=skein_id,
            used_yarn_weight=used_yarn_weight,
        )
    )
```

Najważniejszy szczegół:

```python
ProjectSkeinFormData(...)
```

tworzy nowy obiekt, ale jeśli nie zapiszesz go do listy, to od razu go tracisz.

Dlatego potrzebne jest:

```python
skein_usage.append(...)
```

## 5. Co jeśli listy mają różną długość

`zip(...)` działa tylko do końca najkrótszej listy.

Przykład:

```python
ids = [1, 2, 3]
weights = [50, 20]

for item_id, weight in zip(ids, weights):
    print(item_id, weight)
```

Wynik:

```text
1 50
2 20
```

Para dla `3` nie powstanie, bo druga lista nie ma trzeciego elementu.

Przy formularzach to zwykle jest OK, jeśli inputy powstają parami.
Jeśli formularz może wysłać niepełne dane, wtedy trzeba dodać osobną walidację.

## 6. Najkrótsza wersja do zapamiętania

```python
for first_value, second_value in zip(first_list, second_list):
    ...
```

czytaj jako:

```text
Weź pierwszy element z pierwszej listy i pierwszy element z drugiej listy.
Potem drugi z pierwszej i drugi z drugiej.
Potem trzeci z pierwszej i trzeci z drugiej.
```

W Twoim mapperze:

```python
for skein_id, used_yarn_weight in zip(skein_ids, used_yarn_weights):
    ...
```

czytaj jako:

```text
Dla każdej pary: id motka + zużyta waga,
zbuduj jeden obiekt ProjectSkeinFormData.
```
