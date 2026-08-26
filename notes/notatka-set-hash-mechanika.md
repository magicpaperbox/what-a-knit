# Mechanika `set` i `hash` w Pythonie

Ta notatka tłumaczy, jak `set` znajduje elementy szybko: przez `hash`, wewnętrzną tabelę, przeliczanie hasha na miejsce, obsługę kolizji i powiększanie tabeli.

## 1. `set` nie działa jak lista

Lista trzyma elementy po kolei:

```python
fruits = ["apple", "banana", "kiwi", "plum"]
```

Mentalnie:

```text
index 0 -> apple
index 1 -> banana
index 2 -> kiwi
index 3 -> plum
```

Gdy robimy:

```python
"plum" in fruits
```

Python musi sprawdzać po kolei:

```text
apple? nie
banana? nie
kiwi? nie
plum? tak
```

Dlatego szukanie wartości w liście to `O(n)`.

`set` działa inaczej. Nie szuka po kolei. Używa wewnętrznej tabeli i funkcji `hash()`.

## 2. Wewnętrzna tabela seta

Załóżmy, że `set` ma pod spodem 8 technicznych miejsc:

```text
index:  0       1       2       3       4       5       6       7
      [     ] [     ] [     ] [     ] [     ] [     ] [     ] [     ]
```

To nie są indeksy dla programistki. Nie można zrobić:

```python
my_set[2]
```

Te miejsca są tylko wewnętrzną organizacją seta.

## 3. Co robi `hash()`

`hash()` zamienia wartość na liczbę.

```python
hash("plum")
hash(10)
```

Uproszczona idea:

```text
"plum" -> 77
10 -> 10
```

To nie znaczy, że `hash("plum")` naprawdę zawsze wynosi `77`. To tylko liczba do nauki mechanizmu.

Ważne jest to:

```text
ta sama wartość daje ten sam hash w trakcie działania programu
```

Czyli jeśli przy dodawaniu `"plum"` hash prowadził do jakiegoś miejsca, to przy szukaniu `"plum"` Python znowu trafi w to samo miejsce startowe.

## 4. Jak hash zmienia się w miejsce w tabeli

Hash może być dużą liczbą, na przykład:

```text
hash("plum") = 77
```

Ale tabela ma tylko 8 miejsc:

```text
0 1 2 3 4 5 6 7
```

Python potrzebuje sposobu, żeby z liczby `77` zrobić numer od `0` do `7`.

Do zrozumienia mechanizmu wystarczy myśleć o operatorze `%`, czyli reszcie z dzielenia:

```python
77 % 8
```

Liczymy:

```text
8 * 9 = 72
77 - 72 = 5
```

Czyli:

```text
77 % 8 = 5
```

Wniosek:

```text
"plum" zaczyna szukanie od miejsca 5
```

## 5. Dlaczego `%` działa

Jeśli tabela ma 8 miejsc, to `% 8` zawsze da wynik od `0` do `7`.

```text
0 % 8 = 0
1 % 8 = 1
7 % 8 = 7
8 % 8 = 0
9 % 8 = 1
77 % 8 = 5
100 % 8 = 4
```

Dlatego mechanizm można zapamiętać tak:

```text
wartość -> hash -> reszta z dzielenia -> miejsce startowe w tabeli
```

Dla naszego przykładu:

```text
"plum" -> 77 -> 77 % 8 -> 5
```

## 6. Dodawanie elementu do seta

Załóżmy, że mamy pusty set:

```python
numbers = set()
numbers.add(10)
```

Dla liczb całkowitych można na początku myśleć, że hash jest bliski samej liczbie:

```text
hash(10) = 10
```

Tabela ma 8 miejsc:

```text
10 % 8 = 2
```

`10` trafia do miejsca `2`:

```text
index:  0       1       2       3       4       5       6       7
      [     ] [     ] [ 10  ] [     ] [     ] [     ] [     ] [     ]
```

## 7. Co jeśli miejsce jest zajęte

Dodajemy kolejną liczbę:

```python
numbers.add(18)
```

Uproszczony hash:

```text
hash(18) = 18
18 % 8 = 2
```

`18` też chce zacząć od miejsca `2`.

Ale miejsce `2` jest już zajęte przez `10`.

Set sprawdza:

```text
czy 18 == 10?
nie
```

To znaczy, że to nie jest duplikat. To jest kolizja.

Set szuka innego wolnego miejsca według swojej wewnętrznej reguły. W uproszczonym modelu możemy powiedzieć, że sprawdza dalej i znajduje miejsce `3`:

```text
index:  0       1       2       3       4       5       6       7
      [     ] [     ] [ 10  ] [ 18  ] [     ] [     ] [     ] [     ]
```

Kolizja nie jest błędem. To normalna sytuacja.

## 8. Co jeśli dodamy duplikat

Teraz robimy:

```python
numbers.add(10)
```

Set liczy:

```text
hash(10) = 10
10 % 8 = 2
```

Idzie do miejsca `2` i widzi:

```text
tam już jest 10
```

Sprawdza:

```text
czy 10 == 10?
tak
```

Więc nie dodaje drugi raz.

Dlatego w secie nie ma duplikatów.

## 9. Hash sam nie wystarcza do rozpoznania duplikatu

Dwie różne wartości mogą mieć ten sam hash albo mogą po `%` trafić w to samo miejsce.

Przykład:

```text
hash(10) = 10
10 % 8 = 2

hash(18) = 18
18 % 8 = 2
```

Obie liczby startują od miejsca `2`, ale nie są tym samym:

```text
10 == 18
```

daje:

```text
False
```

Dlatego set używa dwóch rzeczy:

```text
hash mówi, gdzie zacząć szukać
== mówi, czy to naprawdę ta sama wartość
```

## 10. Trzy sytuacje przy `add()`

Gdy robisz:

```python
some_set.add(value)
```

set robi mentalnie:

```text
1. policz hash(value)
2. przelicz hash na miejsce startowe
3. sprawdź to miejsce
```

Potem są trzy możliwości:

```text
miejsce puste
-> wpisz element

miejsce zajęte przez tę samą wartość
-> duplikat, nie dodawaj

miejsce zajęte przez inną wartość
-> kolizja, szukaj innego miejsca
```

## 11. Co jeśli dodamy czwarty element

Załóżmy, że mamy już:

```text
index:  0       1       2       3       4       5       6       7
      [     ] [ 9   ] [ 10  ] [ 18  ] [     ] [     ] [     ] [     ]
```

Dodajemy:

```python
numbers.add(26)
```

Uproszczony hash:

```text
hash(26) = 26
26 % 8 = 2
```

Miejsce `2` jest zajęte przez `10`, więc set pyta:

```text
czy 26 == 10?
nie
```

To kolizja.

Set szuka dalej według swojej reguły. Jeśli miejsce `3` też jest zajęte, może znaleźć wolne miejsce `4`:

```text
index:  0       1       2       3       4       5       6       7
      [     ] [ 9   ] [ 10  ] [ 18  ] [ 26  ] [     ] [     ] [     ]
```

## 12. Co gdy tabela robi się za pełna

Gdy w tabeli jest za dużo elementów, set zaczyna mieć więcej kolizji.

Wtedy Python powiększa tabelę.

Przykład:

```text
stara tabela: 8 miejsc
nowa tabela: 16 miejsc
```

Potem Python układa elementy od nowa, bo zmienił się rozmiar tabeli.

Wcześniej:

```text
26 % 8 = 2
```

Po powiększeniu:

```text
26 % 16 = 10
```

Czyli element może trafić w inne techniczne miejsce.

To dlatego `set` nie ma indeksów dla programistki. Jego wewnętrzne miejsca mogą się zmieniać.

## 13. Co się dzieje przy usuwaniu

Gdy robisz:

```python
numbers.remove(10)
```

set:

```text
1. liczy hash(10)
2. przelicza hash na miejsce startowe
3. znajduje 10
4. usuwa 10
```

Przy kolizjach Python musi uważać, żeby późniejsze szukanie innych elementów nadal działało. Dlatego wewnętrznie może zostawić specjalny ślad po usuniętym miejscu, zamiast traktować je jak zwykłe puste miejsce.

Nie musisz pamiętać szczegółów tego śladu. Ważna intuicja:

```text
usuwanie też korzysta z hasha, żeby zacząć szukanie w dobrym miejscu
```

## 14. Dlaczego elementy seta muszą być `hashable`

Element w secie musi mieć stabilny hash.

Działa:

```python
{1, 2, 3}
{"apple", "banana"}
{(1, 2), (3, 4)}
```

Nie działa:

```python
{[1, 2]}
```

Lista nie jest `hashable`, bo można ją zmienić:

```python
items = [1, 2]
items.append(3)
```

Gdyby lista była w secie i zmieniła się po dodaniu, set mógłby już nie wiedzieć, gdzie jej szukać.

## 15. Czy sam `set` jest `hashable`

Zwykły `set` nie jest `hashable`, bo jest zmienialny.

To daje błąd:

```python
hash({1, 2, 3})
```

Ale `set` używa hashy swoich elementów.

Najważniejsze rozróżnienie:

```text
set używa hashy elementów
ale zwykły set sam nie jest hashable
```

Jeśli potrzebujemy niezmiennego seta, można użyć `frozenset`:

```python
frozenset({1, 2, 3})
```

## 16. Cena za szybkość

Lista trzyma elementy ciasno po kolei:

```text
[apple][banana][kiwi][plum]
```

Set trzyma większą tabelę, często z pustymi miejscami:

```text
[puste][plum][puste][banana][kiwi][puste][apple][puste]
```

Te puste miejsca są ceną za szybkie szukanie.

Dlatego:

```text
lista: zwykle mniej pamięci, wolniejsze szukanie po wartości
set: zwykle więcej pamięci, szybsze szukanie po wartości
```

Oba mogą mieć pamięć `O(n)`, ale `set` zwykle ma większy narzut.

## Najważniejszy model do zapamiętania

```text
wartość
-> hash(wartość)
-> hash % liczba_miejsc
-> miejsce startowe w tabeli
-> sprawdzenie, czy miejsce jest puste, zajęte przez duplikat albo zajęte przez inną wartość
```

Dla przykładu:

```text
26
-> hash(26) = 26
-> 26 % 8 = 2
-> sprawdź miejsce 2
-> jeśli zajęte przez inną wartość, szukaj kolejnego miejsca
```

To jest powód, dla którego `set` zwykle nie przechodzi po wszystkich elementach po kolei.
