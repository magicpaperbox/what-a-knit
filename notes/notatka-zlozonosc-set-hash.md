# Złożoność, `set`, `hash` i podstawowe struktury danych w Pythonie

## 1. Złożoność czasowa

Złożoność czasowa mówi, jak szybko rośnie liczba operacji, kiedy rośnie liczba danych.

Liczbę danych zwykle oznaczamy jako `n`.

```python
numbers = [4, 8, 15, 16]
```

Tutaj `n = 4`.

Jeśli kod bierze tylko pierwszy element:

```python
numbers[0]
```

to jest `O(1)`, bo nie musi przechodzić po całej liście.

Jeśli kod przechodzi po całej liście:

```python
for number in numbers:
    print(number)
```

to jest `O(n)`.

Jeśli kod ma pętlę w pętli:

```python
for first in numbers:
    for second in numbers:
        print(first, second)
```

to jest `O(n²)`, bo robi `n * n` operacji.

## 2. `2n` to nie to samo co `n²`

Dwie pętle jedna po drugiej:

```python
for item in items:
    print(item)

for item in items:
    print(item)
```

To jest około `2n`, czyli w Big O zapisujemy `O(n)`.

Pętla w pętli:

```python
for first in items:
    for second in items:
        print(first, second)
```

To jest `n * n`, czyli `O(n²)`.

Big O pomija stałe:

```text
O(2n) -> O(n)
O(10n) -> O(n)
O(n²) zostaje O(n²)
```

## 3. Czas i pamięć to dwie różne miary

Jeśli mówimy:

```text
Czas: O(n)
Pamięć: O(n)
```

to nie mnożymy tego do `O(n²)`.

To są osobne informacje:

- czas `O(n)` mówi, ile pracy robi program
- pamięć `O(n)` mówi, ile dodatkowego miejsca program potrzebuje

Przykład z `set`:

```python
seen = set()

for number in numbers:
    if number in seen:
        return True

    seen.add(number)

return False
```

Czas: `O(n)`, bo przechodzimy po `numbers` maksymalnie raz.

Pamięć: `O(n)`, bo w `seen` możemy zapisać maksymalnie `n` elementów.

## 4. Jak działa lista

Lista ma kolejność i indeksy:

```python
fruits = ["pear", "banana", "plum", "apple"]
```

Mentalnie:

```text
index 0 -> "pear"
index 1 -> "banana"
index 2 -> "plum"
index 3 -> "apple"
```

Ważne: `"apple"` nie ma indeksu `3` na zawsze. Ona aktualnie znajduje się pod indeksem `3`.

To:

```python
fruits[3] = "kiwi"
```

znaczy: podmień wartość na pozycji `3`.

To:

```python
fruits.insert(1, "kiwi")
```

znaczy: wstaw `"kiwi"` na pozycję `1`, a resztę przesuń.

Szukanie wartości w liście:

```python
"apple" in fruits
```

musi iść po kolei:

```text
pear? nie
banana? nie
plum? nie
apple? tak
```

Dlatego `x in list` to `O(n)`.

## 5. Jak działa `set`

`set` to zbiór unikalnych elementów.

```python
numbers = {1, 2, 2, 3}
```

W secie zostanie:

```python
{1, 2, 3}
```

Cechy `set`:

- nie trzyma duplikatów
- nie ma indeksów jak lista
- nie służy do trzymania kolejności
- bardzo szybko sprawdza, czy element już istnieje

## 6. Co to jest `hash`

`hash` to liczba wyliczona z wartości.

Python ma funkcję wbudowaną `hash()`:

```python
hash("apple")
```

Uproszczona idea:

```text
"apple" -> jakaś liczba
```

`set` używa tej liczby, żeby znaleźć miejsce, gdzie wartość powinna być zapisana.

Bardzo uproszczony model:

```python
index = hash("apple") % table_size
```

Czyli `set` nie pyta:

```text
czy apple jest na miejscu 0?
czy apple jest na miejscu 1?
czy apple jest na miejscu 2?
```

Tylko robi:

```text
policz hash("apple")
hash mówi, gdzie mniej więcej szukać
sprawdź to miejsce
```

Dlatego:

```python
"apple" in some_set
```

jest średnio `O(1)`.

## 7. Kolizja

Czasem dwie różne wartości mogą prowadzić do tego samego miejsca.

To jest kolizja:

```text
hash("apple") -> miejsce 3
hash("grape") -> miejsce 3
```

Wtedy `set` musi sprawdzić dodatkowe miejsce.

Dlatego mówimy, że `set` jest średnio `O(1)`, a nie absolutnie zawsze `O(1)`.

## 8. `set(my_list)`

```python
fruits = ["apple", "banana", "apple"]
unique_fruits = set(fruits)
```

Python nadal przechodzi po liście raz, więc budowanie seta z listy to `O(n)`.

Ale przy każdym elemencie robi szybkie sprawdzenie przez hash:

```text
apple -> policz hash -> dodaj
banana -> policz hash -> dodaj
apple -> policz hash -> już jest, nie dodawaj
```

To nie jest porównywanie każdego elementu z każdym.

## 9. `hashable`

Żeby coś mogło być w `set` albo być kluczem w `dict`, musi być `hashable`.

Działa:

```python
hash("apple")
hash(123)
hash((1, 2))
```

Nie działa:

```python
hash([1, 2])
```

Lista nie jest `hashable`, bo można ją zmienić.

Gdyby lista była w `set`, a potem by się zmieniła, Python mógłby już nie wiedzieć, gdzie jej szukać.

## 10. Porównanie struktur danych

| Struktura | Kolejność | Indeksy | Duplikaty | Szybkie `in` |
|---|---|---|---|---|
| `list` | tak | tak | tak | nie, `O(n)` |
| `tuple` | tak | tak | tak | nie, `O(n)` |
| `set` | nie jak lista | nie | nie | tak, średnio `O(1)` |
| `dict` | pamięta kolejność dodania | nie jak lista | klucze unikalne | po kluczu średnio `O(1)` |

## 11. `dict`

Słownik działa podobnie do seta, ale ma pary `key -> value`.

```python
user = {
    "name": "Klaudia",
    "age": 30,
}
```

Klucze są hashowane.

```python
user["name"]
```

Python nie szuka `"name"` po kolei jak w liście. Liczy hash klucza i znajduje wartość szybko.

## 12. `tuple`

Krotka jest podobna do listy, ale niezmienna:

```python
point = (10, 20)
```

Nie można zrobić:

```python
point[0] = 99
```

Krotka może być `hashable`, jeśli jej zawartość też jest `hashable`.

## 13. Obiekt

Obiekt to inny poziom: grupuje dane i zachowania.

```python
class User:
    pass

user = User()
user.name = "Klaudia"
```

Na początku można myśleć o obiekcie jak o rzeczy z nazwanymi polami.

Pod spodem Python często przechowuje atrybuty obiektu w strukturze podobnej do słownika, ale koncepcyjnie obiekt to nie lista ani set.

## Najważniejsze zdanie

Lista szuka wartości po kolei, a `set` i `dict` używają `hash`, żeby szybko trafić w miejsce, gdzie dana wartość albo klucz powinny się znajdować.
