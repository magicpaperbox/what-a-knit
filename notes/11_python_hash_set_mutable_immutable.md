# Python: hash, set, mutable, immutable, hashable

Ta notatka jest o podstawach Pythona, które przewijają się u Ciebie w:

- `tests/charts/test_color_chart.py`
- `src/modules/charts/domain.py`

Szczególnie w metodzie `ColorChart.all_colors`, gdzie używany jest `set()`.

## 1. Po co w ogóle są różne typy kolekcji

Python ma kilka podstawowych typów do przechowywania wielu rzeczy naraz:

- `list`
- `tuple`
- `dict`
- `set`

Każdy z nich służy do trochę innego celu.

### `list`

Lista:

- trzyma elementy w kolejności,
- pozwala na duplikaty,
- można ją zmieniać po utworzeniu.

Przykład:

```python
numbers = [1, 2, 2, 3]
numbers.append(4)
```

To jest typ `mutable`.

### `tuple`

Krotka:

- też trzyma elementy w kolejności,
- może mieć duplikaty,
- ale po utworzeniu nie można jej zmieniać.

Przykład:

```python
point = (10, 20)
```

To jest typ `immutable`.

### `dict`

Słownik:

- przechowuje pary `klucz -> wartość`,
- służy do szybkiego znajdowania wartości po kluczu.

Przykład:

```python
person = {"name": "Klaudia", "age": 20}
```

Tutaj:

- `"name"` to klucz,
- `"Klaudia"` to wartość.

### `set`

Zbiór:

- przechowuje tylko unikalne elementy,
- nie przechowuje duplikatów,
- bardzo dobrze nadaje się do sprawdzania, czy coś już istnieje.

Przykład:

```python
colors = {"red", "blue", "red"}
print(colors)  # {"red", "blue"}
```

## 2. Mutable i immutable

### `mutable`

`mutable` znaczy:

- obiekt można zmienić po utworzeniu.

Przykłady:

- `list`
- `dict`
- `set`

```python
numbers = [1, 2]
numbers.append(3)
```

Po `append()` ta sama lista ma nową zawartość.

### `immutable`

`immutable` znaczy:

- obiektu nie można zmienić po utworzeniu.

Przykłady:

- `int`
- `str`
- `tuple`

```python
name = "Ala"
```

Nie możesz zmienić jednego znaku wewnątrz tego stringa. Możesz tylko stworzyć nowy string.

Najprościej:

- `mutable` = można zmieniać,
- `immutable` = nie można zmieniać.

## 3. Co to jest `hash`

`hash` to liczba wyliczana przez funkcję `hash(...)`.

Przykład:

```python
hash("abc")
hash(123)
```

Ta liczba działa jak skrót obiektu.

Python używa jej po to, żeby szybciej:

- sprawdzać, czy element jest w `set`,
- znajdować wartość w `dict`,
- przechowywać elementy w strukturach opartych o hashowanie.

To nie jest "tajemnicza prawda o obiekcie", tylko techniczny skrót potrzebny do szybkiego działania.

## 4. Co znaczy `hashable`

`hashable` znaczy:

- Python umie policzyć `hash(obiekt)`,
- taki obiekt może być użyty jako element `set`,
- taki obiekt może być użyty jako klucz w `dict`.

Przykłady obiektów zwykle `hashable`:

- `int`
- `str`
- `tuple` jeśli w środku też ma tylko rzeczy hashable

Przykład:

```python
hash("red")
hash((1, 2))
```

## 5. Co znaczy `not hashable`

`not hashable` znaczy:

- Python nie pozwala użyć takiego obiektu w `set`,
- Python nie pozwala użyć go jako klucza w `dict`.

Najczęściej `not hashable` są:

- `list`
- `dict`
- `set`

Przykład:

```python
hash([1, 2, 3])  # TypeError
```

Dlaczego?

Bo `list` można zmieniać.
Gdyby dało się jej bezpiecznie używać w `set` albo jako klucza w `dict`, to po zmianie zawartości wszystko mogłoby się "rozjechać".

## 6. Jak to się łączy: mutable, immutable, hashable

Bardzo dobra praktyczna zasada na start:

- rzeczy `immutable` często są `hashable`,
- rzeczy `mutable` zwykle nie są `hashable`.

To nie jest reguła absolutna na 100%, ale w nauce Pythona bardzo pomaga.

Powód jest prosty:

- jeśli obiekt się zmienia,
- to jego "tożsamość logiczna" też może się zmienić,
- a `dict` i `set` potrzebują stabilnych elementów.

## 7. Jak działa `set`

Kiedy dodajesz coś do `set`, Python w uproszczeniu:

1. liczy `hash(elementu)`,
2. wybiera miejsce, gdzie ten element przechować,
3. jeśli wygląda, że podobny element już tam jest, porównuje je jeszcze przez `==`,
4. jeśli to "ten sam" element, nie dodaje duplikatu.

Przykład:

```python
numbers = set()
numbers.add(1)
numbers.add(1)
numbers.add(2)
```

Wynik:

```python
{1, 2}
```

Czyli `set` jest świetny wtedy, gdy chcesz:

- usuwać duplikaty,
- szybko sprawdzać, czy coś już jest.

## 8. Jak działa `dict`

`dict` działa podobnie do `set`, ale zamiast samych elementów przechowuje:

- klucz,
- wartość.

Przykład:

```python
person = {"name": "Klaudia"}
```

Python liczy `hash("name")`, dzięki czemu szybko znajduje wartość `"Klaudia"`.

Dlatego:

- klucz w `dict` musi być `hashable`.

## 9. Co to ma wspólnego z Twoim testem

W pliku `src/modules/charts/domain.py`, w metodzie `ColorChart.all_colors`, masz:

```python
colors = set()
for cell_row in self.cells:
    for cell in cell_row:
        if cell is not None:
            colors.add(cell)
```

To znaczy:

- przechodzisz po wszystkich komórkach wykresu,
- jeśli komórka ma kolor, dodajesz go do `set`,
- jeśli ten sam kolor pojawi się drugi raz, `set` nie doda duplikatu.

Potem:

```python
colors = list(colors)
colors.sort(key=lambda color: color.hex_value)
```

Czyli:

- najpierw używasz `set`, żeby usunąć duplikaty,
- potem zamieniasz wynik na `list`,
- potem sortujesz listę po `color.hex_value`.

To właśnie sprawdza test w `tests/charts/test_color_chart.py`:

- w siatce są dwa razy `blue`,
- ale wynik ma zawierać tylko jedno `blue`,
- i kolory mają być posortowane.

## 10. Dlaczego `Color` może być w `set`

W `src/modules/charts/domain.py` klasa `Color` jest zdefiniowana tak:

```python
@dataclass(frozen=True)
class Color:
    hex_value: str
```

Najważniejsze jest tutaj `frozen=True`.

To oznacza, że obiekt `Color` jest traktowany jak niemutowalny.

Dzięki temu:

- nie powinien zmieniać swojej zawartości po utworzeniu,
- Python może go bezpiecznie hashować,
- można go używać w `set`.

To jest bardzo dobry przykład praktycznego sensu `immutable` i `hashable`.

## 11. Po co są `__hash__` i `__eq__`

Jeśli tworzysz własną klasę, Python musi wiedzieć:

- kiedy dwa obiekty są równe,
- jak policzyć ich hash.

Do tego służą:

- `__eq__(...)`
- `__hash__(...)`

Jeśli dwa obiekty mają być traktowane jako takie same, to:

- `__eq__` powinno zwrócić `True`,
- i oba obiekty powinny mieć ten sam hash.

To jest bardzo ważna zasada:

- jeśli `a == b`, to `hash(a)` i `hash(b)` też muszą być zgodne.

## 12. Najkrótsza wersja do zapamiętania

- `list` = kolejność, duplikaty, mutable
- `tuple` = kolejność, zwykle do stałych danych, immutable
- `dict` = klucz -> wartość, szybkie wyszukiwanie po kluczu
- `set` = unikalne elementy, szybkie sprawdzanie istnienia
- `mutable` = można zmienić po utworzeniu
- `immutable` = nie można zmienić po utworzeniu
- `hashable` = można użyć w `set` i jako klucz w `dict`
- `set` i `dict` działają szybko, bo używają `hash(...)`

## 13. Jedno praktyczne skojarzenie

Jeśli widzisz w kodzie:

```python
colors = set()
```

to najczęściej autor chce jedną z tych rzeczy:

- usunąć duplikaty,
- mieć szybkie sprawdzanie, czy coś już istnieje,
- zbudować zbiór unikalnych wartości.
