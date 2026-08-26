# Binary search - notatka

Binary search sluzy do szukania elementu w **posortowanej** liscie.

Najwazniejsza mysl:

```text
Nie sprawdzam elementow po kolei.
Patrze w srodek i wyrzucam polowe listy.
```

## Trzy indeksy

```python
left = 0
right = len(numbers) - 1
middle = (left + right) // 2
```

`left`, `right` i `middle` to **indeksy**, nie wartosci z listy.

Przyklad:

```python
numbers = [2, 5, 8, 12, 16]
```

```text
indeksy:   0  1  2   3   4
wartosci:  2  5  8  12  16
```

Dlatego:

```python
left = 0
right = len(numbers) - 1
```

`len(numbers)` to liczba elementow, a nie ostatni indeks.

## Rytm algorytmu

Zapamietaj:

```text
granice -> srodek -> porownanie -> przesuniecie granicy
```

Albo krocej:

```text
left/right
middle/current
compare
move boundary
```

## Najwazniejsze porownania

Jesli znalezlismy szukana wartosc:

```python
if current == target:
    return middle
```

Jesli wartosc w srodku jest za mala:

```python
elif current < target:
    left = middle + 1
```

Czyli: szukamy bardziej w prawo, wiec przesuwamy lewa granice.

Jesli wartosc w srodku jest za duza:

```python
else:
    right = middle - 1
```

Czyli: szukamy bardziej w lewo, wiec przesuwamy prawa granice.

## Mantra do zapamietania

```text
Za malo?  left idzie w prawo.
Za duzo?  right idzie w lewo.
```

W kodzie:

```python
current < target -> left = middle + 1
current > target -> right = middle - 1
```

## Szkielet funkcji

Najpierw warto nauczyc sie odtwarzac ten ksztalt:

```python
def binary_search(numbers, target):
    left = 0
    right = len(numbers) - 1

    while left <= right:
        middle = (left + right) // 2
        current = numbers[middle]

        if current == target:
            return middle
        elif current < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1
```

## Dlaczego `while left <= right`

Dopoki `left <= right`, istnieje jeszcze fragment listy, w ktorym mozemy szukac.

Gdy `left` minie `right`, to znaczy, ze nie ma juz gdzie szukac.

Wtedy funkcja zwraca:

```python
return -1
```

czyli: nie znaleziono elementu.

## Warunek monotoniczny

Warunek jest **monotoniczny**, jesli jego wynik nie skacze losowo.

Najczesciej wyglada tak:

```text
False False False True True True
```

albo odwrotnie:

```text
True True True False False False
```

Czyli wynik moze zmienic sie raz, ale nie powinien zmieniac sie wiele razy.

Przyklad:

```python
numbers = [2, 5, 8, 12, 16, 23]
target = 12
```

Warunek:

```python
numbers[i] >= target
```

Daje:

```text
2 >= 12   -> False
5 >= 12   -> False
8 >= 12   -> False
12 >= 12  -> True
16 >= 12  -> True
23 >= 12  -> True
```

Czyli:

```text
False False False True True True
```

To jest monotoniczne.

Zly przyklad:

```text
False True False True
```

To nie jest monotoniczne, bo wynik kilka razy zmienia zdanie.

## Dlaczego to ma znaczenie w binary search

Binary search dziala dlatego, ze posortowana lista daje monotoniczne porownania.

Jesli:

```python
current < target
```

to wiemy, ze `current` jest za maly. W posortowanej liscie wszystko po lewej stronie tez bedzie za male albo jeszcze mniejsze.

Dlatego mozemy bezpiecznie zrobic:

```python
left = middle + 1
```

Jesli:

```python
current > target
```

to wiemy, ze `current` jest za duzy. W posortowanej liscie wszystko po prawej stronie tez bedzie za duze albo jeszcze wieksze.

Dlatego mozemy bezpiecznie zrobic:

```python
right = middle - 1
```

Krotka wersja do zapamietania:

```text
Monotoniczny warunek = moge wyrzucic cala polowe naraz.
Niemonotoniczny warunek = binary search nie wie, ktora polowe wyrzucic.
```

## Mini cwiczenie

Dla listy:

```python
numbers = [2, 5, 8, 12, 16, 23, 38]
target = 23
```

Pierwszy srodek:

```python
middle = 3
current = 12
```

Poniewaz:

```python
12 < 23
```

robimy:

```python
left = middle + 1
```

czyli:

```python
left = 4
```
