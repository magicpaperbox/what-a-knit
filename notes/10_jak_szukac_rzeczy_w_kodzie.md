# Jak szukać konkretnych rzeczy w kodzie i się nie gubić

To jest notatka o orientowaniu się w kodzie.
Nie o tym, jak napisać rozwiązanie, tylko jak w ogóle znaleźć miejsce, które warto sprawdzić albo zmienić.

Najważniejsza myśl:

- **nie musisz rozumieć całego projektu naraz**
- zwykle wystarczy umieć przejść od objawu do źródła

---

## 1. Najpierw nazwij typ problemu

Zanim zaczniesz szukać, spróbuj nazwać:

- **co dokładnie jest nie tak**
- **w której warstwie to widać**

Przykłady:

- "Na stronie źle wyświetla się tekst" -> zacznij od template
- "Po kliknięciu przycisku coś dzieje się bez przeładowania strony" -> zacznij od JavaScriptu
- "Po wysłaniu formularza zapisują się złe dane" -> zacznij od formularza i `request.form`
- "Z bazy wraca coś dziwnego" -> zacznij od repository
- "Obiekt ma złą logikę" -> zacznij od `domain.py`

To bardzo pomaga, bo od razu zawężasz obszar szukania.

---

## 2. Szukaj po czymś naprawdę konkretnym

Najlepsze hasła do wyszukiwania to zwykle:

- tekst widoczny na stronie
- nazwa pola formularza
- nazwa zmiennej z template
- fragment adresu URL
- nazwa funkcji
- nazwa właściwości

Przykłady dobrych haseł:

- `Gauge:`
- `Add yarn`
- `target_gauge`
- `actual_gauge`
- `name="gauge_rows"`
- `/patterns/`
- `remaining_length`
- `.value`

Słabsze hasła:

- `data`
- `value`
- `pattern`

Bo są za ogólne i dadzą za dużo wyników.

---

## 3. Szukaj od miejsca najbliższego objawowi

Jeśli problem widzisz na stronie, zacznij od tego, co widzi użytkownik.

### Gdy problem jest w wyświetlaniu

Kolejność zwykle jest taka:

1. template
2. `render_template(...)`
3. funkcja route w `api.py`
4. repository
5. domain / units

### Gdy problem jest w formularzu

Kolejność zwykle jest taka:

1. `name=""` w HTML
2. `request.form.get(...)` albo `request.form[...]`
3. mapper / parser formularza
4. obiekt domenowy
5. zapis do repozytorium

### Gdy problem jest po kliknięciu bez przeładowania strony

Kolejność zwykle jest taka:

1. HTML przycisku / elementu
2. plik JavaScript
3. funkcja obsługująca event
4. ewentualnie `fetch(...)` albo zmiana DOM

---

## 4. Śledź jedną wartość, nie cały moduł

To jest jedna z najważniejszych rzeczy.

Zamiast myśleć:

- "Muszę zrozumieć cały plik"

lepiej myśleć:

- "Chcę prześledzić jedną konkretną wartość"

Przykłady:

- skąd bierze się `pattern.target_gauge.stitches`
- skąd bierze się `form_data.full_length`
- gdzie powstaje `remaining_length(yarn)`

To jest dużo lżejsze dla głowy niż próba objęcia wszystkiego naraz.

---

## 5. Zadawaj sobie 3 krótkie pytania

Przy szukaniu bardzo pomagają te pytania:

1. Skąd ta wartość przyszła?
2. W co została zamieniona?
3. Gdzie została użyta albo wyświetlona?

To jest bardzo prosty sposób śledzenia przepływu danych.

---

## 6. Uważaj na miejsca "przelotowe"

Nie każde miejsce, do którego trafisz, jest miejscem dobrej zmiany.

### Miejsca przelotowe

To są miejsca, które głównie:

- przekazują dane dalej
- wołają inną funkcję
- sprawdzają tylko prosty warunek

Przykłady:

- `details()` w `api.py`
- `get_*_or_404()`

Takie miejsca często są dobre do zrozumienia przepływu, ale nie do właściwej poprawki.

### Miejsca decyzyjne

To są miejsca, które:

- budują obiekt
- zmieniają typ
- walidują
- formatują
- zapisują do bazy

To zwykle właśnie tam warto szukać prawdziwej przyczyny albo miejsca poprawki.

---

## 7. Jak rozpoznać ważne funkcje po nazwie

Są nazwy, które bardzo często oznaczają ważne punkty orientacyjne.

Przykłady:

- `details`
- `index`
- `create_*`
- `edit_*`
- `get_by_id`
- `get_all`
- `parse_*_from_form`
- `_row_to_domain`
- `_to_domain`
- `from_row`
- `validate`

Jeśli trafiasz na takie funkcje, często jesteś blisko miejsca, gdzie coś ważnego się dzieje.

---

## 8. Jak korzystać z PyCharm, żeby się szybciej odnajdywać

Najbardziej przydatne narzędzia:

- `Find in Files`
- `Go to Definition`
- `Find Usages`
- `Recent Files`

### `Find in Files`

Używaj, gdy znasz:

- tekst z ekranu
- nazwę zmiennej
- nazwę funkcji

To jest zwykle najlepszy pierwszy krok.

### `Go to Definition`

Używaj, gdy stoisz na:

- nazwie klasy
- nazwie funkcji
- nazwie metody

To pomaga szybko przejść do miejsca definicji.

### `Find Usages`

Używaj, gdy chcesz sprawdzić:

- gdzie coś jest używane
- czy zmiana w jednym miejscu wpłynie też na inne miejsca

To jest bardzo pomocne przy refactorze albo poprawkach "globalnych".

### `Recent Files`

Bardzo przydaje się, gdy krążysz między kilkoma plikami i nie chcesz ich ciągle wyszukiwać od nowa.

---

## 9. Dobra kolejność pytań podczas szukania

Gdy się gubisz, wróć do tej listy:

1. Co dokładnie jest nie tak?
2. Gdzie to widać: backend, template, JavaScript, formularz, baza?
3. Jaki tekst albo jaka zmienna jest z tym związana?
4. Skąd ta zmienna przychodzi?
5. Gdzie zmienia typ albo kształt?
6. Czy poprawka ma być lokalna czy globalna?

To często wystarcza, żeby przestać błądzić.

---

## 10. Nie czytaj wszystkiego

To bardzo częsty problem na początku.

Kiedy próbujesz zrozumieć za dużo naraz, łatwo się zmęczyć i zgubić.

Zamiast:

- czytać cały moduł od góry do dołu

często lepiej:

- znaleźć jeden konkretny objaw
- jedną konkretną zmienną
- jedną ścieżkę przepływu danych

To w zupełności wystarcza, żeby zrobić mały krok do przodu.

---

## 11. Najkrótsza wersja do zapamiętania

- zacznij od objawu
- szukaj po konkretach
- śledź jedną wartość
- odróżniaj miejsca przelotowe od decyzyjnych
- nie próbuj zrozumieć wszystkiego naraz

Jeśli umiesz zrobić tylko to, to już naprawdę dobrze poruszasz się po kodzie.
