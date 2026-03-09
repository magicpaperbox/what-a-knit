# Product Requirements Document (PRD): System Zarządzania Projektami Dziewiarskimi

## 1. Cel i Wizja Produktu

Stworzenie aplikacji ułatwiającej dziewiarkom i dziewiarzom kompleksowe zarządzanie swoim hobby. System pozwala na ewidencję posiadanych zasobów (włóczek i narzędzi), tworzenie i katalogowanie wzorów oraz śledzenie postępów w projektach. Unikalną wartością systemu jest wbudowany silnik weryfikacji (Feasibility Engine), który na podstawie posiadanych zasobów weryfikuje i podpowiada, czy dany wzór jest możliwy do zrealizowania, uwzględniając złożone reguły dziewiarskie (np. łączenie cienkich nitek, współdzielenie określonych typów drutów).

## 2. Słownik Pojęć (Domain Vocabulary)

* **Definicja Włóczki (Yarn Definition):** Produkt w katalogu o stałych parametrach: marka, nazwa, **kolor/odcień**, skład, grubość (standardowe kategorie, np. DK, Fingering), waga pełnego motka i jego długość.
* **Motek (Skein / Stash Item):** Fizyczny obiekt w magazynie użytkownika. Stanowi instancję Definicji Włóczki.
* **Narzędzie (Tool):** Fizyczny sprzęt dziewiarski/szydełkowy.
* **Wzór (Pattern):** Instrukcja wykonania dzianiny deklarująca wymagania materiałowe i sprzętowe. Posiada (ownuje) przypisane schematy.
* **Schemat (Chart):** Wizualna, dwuwymiarowa reprezentacja wzoru dziewiarskiego.
* **Projekt (Project):** Konkretna realizacja wzoru lub praca własna, z przypisanymi konkretnymi fizycznymi motkami i narzędziami.
* **Próbka (Gauge):** Liczba oczek i rzędów na kwadracie 10x10 cm.

---

## 3. Zakres Funkcjonalny (Wymagania Systemowe)

### 3.1. Zarządzanie Magazynem Włóczek (Stash)

* **CRUD motków:** Użytkownik może zarządzać fizycznymi motkami w magazynie. Każdy motek opiera się na Definicji Włóczki (która zawiera w sobie informację o kolorze).
* **Śledzenie zużycia (wagowo):** Częściowe zużycie motka w projekcie aktualizuje jego wagę (w gramach). Pozostała długość nici wyliczana jest z proporcji wagi. Resztka (niepełny motek) pozostaje w magazynie jako dostępny zasób.
* **Wielokrotność:** System obsługuje i rozróżnia wiele identycznych motków (tej samej Definicji Włóczki), śledząc stan przypisania każdego z nich osobno.

### 3.2. Zarządzanie Narzędziami (Equipment)

* Rejestracja i inwentaryzacja narzędzi.
* **Typy narzędzi:** Szydełka, Druty proste, Druty na stałej żyłce, Druty wymienne (same końcówki), Druty skarpetkowe (DPN), Odpinane żyłki (kable).
* **Parametry:** Rozmiar (grubość w mm, z opcją podglądu innych jednostek np. US w interfejsie), materiał, długość żyłki (dla narzędzi z żyłką).

### 3.3. Zarządzanie Wzorami i Schematami (Patterns & Charts)

* **Atrybuty Wzoru:** Nazwa, opis, autor, poziom trudności, ocena, kategoria/subkategoria, język, link zewnętrzny, podgląd PDF, zdjęcie główne.
* **Wymagania Wzoru:** Wzór deklaruje zapotrzebowanie na: grubość włóczki, całkowitą długość/wagę włóczki, wymóg wielu kolorów, docelową próbkę (gauge), wymagane narzędzia (z uwzględnieniem min/max długości żyłki).
* **Edytor Schematów (Chart Editor):**
* System zawiera wbudowany edytor HTML pozwalający tworzyć schematy.
* Mechanika: użytkownik podaje wymiary schematu, wybiera symbol i wstawia go w wybraną kratkę (grid).
* Zapis danych: dwuwymiarowa tablica (2D array) po stronie backendu.



### 3.4. Silnik Weryfikacji (Feasibility Engine)

* **Działanie:** Analizuje wymagania wzoru w odniesieniu do zasobów użytkownika i wskazuje, czy oraz z czego projekt da się zrealizować.
* **Złożone reguły:** * Rozpoznaje potrzebę użycia wielu kolorów.
* Obsługuje łączenie dwóch cieńszych nitek (*Yarn held double*), aby zastąpić jedną grubszą włóczkę wymaganą przez wzór.
* Interfejs z silnika jest tylko pomocniczą sugestią – użytkownik tworząc projekt, zachowuje pełną swobodę wyboru (może zignorować ostrzeżenia i przypisać dowolny materiał).



### 3.5. Zarządzanie Projektami (Projects)

* **Konto Projektu:** Możliwość utworzenia na bazie gotowego Wzoru lub jako własny projekt.
* **Śledzenie Postępu:**
* Wyrażone w procentach (0-100%).
* Dziennik projektu: Data startu, data zakończenia, pole notatek, fotograficzny feed postępów (dodawanie zdjęć w czasie trwania).


* **Kalkulator Próbki (Gauge):**
* Projekt pozwala zestawić próbkę wymaganą we wzorze z rzeczywistą próbką zrobioną przez użytkownika.
* System determistycznie podpowiada poprawki (np. "użyj cieńszych drutów", "użyj grubszej włóczki"), jeśli liczba oczek użytkownika nie zgadza się ze wzorem.


* **Statusy:** Zaczęty (Started), W trakcie (In Progress), Ukończony (Finished). Dodatkowy niezależny stan/flaga w przypadku przerwania prac: Spruty (`is_frogged`).

---

## 4. Logika Biznesowa i Reguły Domenowe

1. **Reguła Frogowania (Prucia):**
* Akcja "Froguj" (lub ustawienie statusu `is_frogged` na `true`) zwalnia przypisane narzędzia i natychmiast zwraca powiązane motki z powrotem do dostępnej puli w magazynie. Spruta włóczka zachowuje parametry przypisanej Definicji Włóczki.


2. **Reguły Współdzielenia Narzędzi (Tool Concurrency):**
* **Szydełka:** Narzędzia nielimitowane – można je przypisać do dowolnej liczby równoległych projektów (łatwe wyciągnięcie i powrót do pracy).
* **Druty wymienne (odpinane końcówki):** Mogą być przekładane między różnymi projektami (system zakłada użycie stoperów na zajętych żyłkach).
* **Zasoby blokowane (1:1):** Druty proste, druty na stałej żyłce, druty skarpetkowe (DPN) oraz zajęte odpinane żyłki (kable) przypisane do trwającego projektu są niedostępne dla innych projektów.


3. **Zastępowalność Narzędzi:**
* System pozwala użyć drutów na żyłce w ramach wzoru wymagającego drutów prostych o tej samej grubości (sugestia w Feasibility Engine).



---

## 5. Poza Zakresem MVP (Out of Scope)

* **Autoryzacja i Konta:** Logowanie, zarządzanie sesją użytkowników (do wdrożenia w późniejszym etapie).
* **Kolejkowanie:** Zaawansowane kolejkowanie planów (Queue) i statusy typu Hibernacja.
* **AI Parser:** Zastosowanie asystenta LLM do automatycznego czytania i interpretacji plików wzorów i samodzielnego dedukowania ostatecznych wymiarów. (W MVP kalkulator próbki oparty jest na sztywnej matematyce).
