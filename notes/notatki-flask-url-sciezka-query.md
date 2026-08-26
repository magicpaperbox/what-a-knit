# URL, sciezka, dekorator Flask, query params, naglowki i fetch

Te notatki dotycza glownie backendu we Flasku oraz tego, co przegladarka wysyla do aplikacji.

## 1. URL

URL to pelny adres zasobu, ktory wpisujesz albo widzisz w przegladarce.

Przyklad:

```text
http://127.0.0.1:5000/search?q=flask&page=2
```

Ten URL mozna rozbic tak:

```text
http://127.0.0.1:5000/search?q=flask&page=2
[host / adres aplikacji] [path] [query params]

host / adres aplikacji: http://127.0.0.1:5000
path / sciezka URL:     /search
query params:           q=flask&page=2
```

Najprosciej:

```text
URL = caly adres dla przegladarki
```

## 2. Sciezka

Sciezka mowi, gdzie cos jest.

W aplikacji webowej najczesciej spotkasz dwa rodzaje sciezek.

### Sciezka URL

To fragment adresu po domenie / hoscie.

Przyklady:

```text
/
/about
/login
/search
```

Dla pelnego URL-a:

```text
http://127.0.0.1:5000/search?q=flask
```

sciezka URL to:

```text
/search
```

### Sciezka pliku

To miejsce pliku w projekcie albo systemie.

Przyklady:

```text
templates/search.html
static/css/style.css
C:\Users\klaud\project\templates\search.html
```

Wazne rozroznienie:

```text
/search                    -> sciezka URL, czyli adres strony w aplikacji
templates/search.html      -> sciezka pliku, czyli miejsce template w projekcie
```

## 3. Dekorator Flask

To dotyczy backendu.

Dekorator `@app.route()` laczy sciezke URL z funkcja w Pythonie.

Przyklad:

```python
@app.route("/about")
def about():
    return "About page"
```

To znaczy:

```text
Kiedy userka wejdzie na sciezke URL /about,
Flask ma uruchomic funkcje about().
```

W `@app.route()` podajesz zwykle sciezke URL, a nie pelny URL.

Dobrze:

```python
@app.route("/about")
```

Zle:

```python
@app.route("http://127.0.0.1:5000/about")
```

Flask buduje sobie mape:

```text
"/"       -> home()
"/about"  -> about()
"/login"  -> login()
"/search" -> search()
```

Czyli:

```text
path w URL-u wybiera funkcje backendowa
```

## 4. Parametry query

To dotyczy danych z requestu.

Parametry query to czesc URL-a po znaku `?`.

Przyklad:

```text
/search?q=flask&page=2
```

Tutaj:

```text
sciezka URL:   /search
query params:  q=flask&page=2
```

Pojedyncze parametry:

```text
q=flask
page=2
```

Parametry query czesto sluza do:

```text
wyszukiwania: /search?q=flask
filtrowania:  /products?category=books
paginacji:    /posts?page=2
sortowania:   /posts?sort=newest
```

We Flasku odczytujesz je przez `request.args`.

Przyklad:

```python
from flask import request

@app.route("/search")
def search():
    query = request.args.get("q")
    page = request.args.get("page")
    return f"Szukasz: {query}, strona: {page}"
```

Dla URL-a:

```text
/search?q=flask&page=2
```

Flask zobaczy:

```python
request.args.get("q")     # "flask"
request.args.get("page")  # "2"
```

Wazne: `request.args.get("q")` uzywa metody `get()`.

`get()` jest wygodne, bo jezeli parametru nie ma, Flask nie wyrzuci od razu bledu. Zamiast tego dostaniesz `None`, chyba ze ustawisz wartosc domyslna.

Przyklad z wartoscia domyslna:

```python
page = request.args.get("page", "1")
```

## 5. Naglowki requestu

To dotyczy backendu i danych technicznych wyslanych w requescie.

Naglowki requestu to dodatkowe informacje wysylane razem z zadaniem HTTP.

Przyklad uproszczonego requestu:

```text
GET /search?q=flask HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: Chrome
Accept: text/html
```

Tutaj:

```text
GET /search?q=flask HTTP/1.1  -> metoda + sciezka + query params
Host: 127.0.0.1:5000          -> naglowek
User-Agent: Chrome            -> naglowek
Accept: text/html             -> naglowek
```

Naglowki nie sa zwykle widoczne w pasku adresu przegladarki. Przegladarka wysyla je "pod spodem".

Popularne naglowki:

```text
Host            -> do jakiego hosta idzie request
User-Agent      -> jaka przegladarka albo klient wyslal request
Accept          -> jaki typ odpowiedzi klient akceptuje, np. HTML albo JSON
Content-Type    -> jaki typ danych jest wysylany, np. JSON albo formularz
Authorization   -> dane do autoryzacji, np. token
Cookie          -> ciasteczka wyslane z przegladarki
```

### Content-Type

`Content-Type` mowi:

```text
Jaki typ danych jest wysylany w body requestu?
```

Body requestu to glowna tresc wysylana do backendu, na przyklad dane formularza albo JSON.

`Content-Type` jest szczegolnie wazny przy metodach takich jak `POST`, `PUT` i `PATCH`, bo one czesto wysylaja dane w body.

Przyklad requestu z JSON-em:

```text
POST /api/books HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"title": "Flask basics"}
```

To znaczy:

```text
Wysylam dane w formacie JSON.
Backend powinien czytac body jak JSON.
```

We Flasku wtedy czesto uzywasz:

```python
data = request.get_json()
```

Wazna metoda:

```python
request.get_json()
```

Ona probuje odczytac body requestu jako JSON.

Przyklad requestu z klasycznym formularzem:

```text
POST /login HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/x-www-form-urlencoded

email=ala@example.com&password=secret
```

To znaczy:

```text
Wysylam dane jak zwykly formularz HTML.
Backend powinien czytac dane formularza.
```

We Flasku wtedy czesto uzywasz:

```python
email = request.form.get("email")
```

Wazna rzecz:

```text
Content-Type dotyczy tego, co jest wysylane w body.
Przy zwyklym GET czesto nie ma body, wiec Content-Type zwykle nie jest najwazniejszy.
```

### Accept

`Accept` mowi:

```text
Jaki typ odpowiedzi klient chce albo potrafi przyjac?
```

Czyli `Accept` nie opisuje tego, co wysylasz do backendu. Opisuje to, co chcesz dostac z backendu.

Przyklad:

```text
GET /books HTTP/1.1
Host: 127.0.0.1:5000
Accept: text/html
```

To znaczy:

```text
Klient chce dostac HTML, czyli zwykla strone.
```

Inny przyklad:

```text
GET /api/books HTTP/1.1
Host: 127.0.0.1:5000
Accept: application/json
```

To znaczy:

```text
Klient chce dostac JSON, czyli dane, nie gotowa strone HTML.
```

We Flasku mozesz sprawdzac `Accept` przez:

```python
request.headers.get("Accept")
```

Flask ma tez wygodniejsze narzedzie:

```python
request.accept_mimetypes
```

Na poczatku najwazniejsze jest jednak samo rozroznienie:

```text
Content-Type = co wysylam do backendu
Accept       = co chce dostac od backendu
```

We Flasku odczytujesz naglowki przez `request.headers`.

Przyklad:

```python
from flask import request

@app.route("/info")
def info():
    user_agent = request.headers.get("User-Agent")
    return f"Twoja przegladarka: {user_agent}"
```

Tutaj wazna funkcja/metoda to:

```python
request.headers.get("User-Agent")
```

Ona pobiera wartosc naglowka `User-Agent`.

## 6. Porownanie: path, query params, headers

Dla requestu:

```text
GET /search?q=flask&page=2 HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: Chrome
Accept: text/html
```

Mozesz myslec tak:

```text
path:
/search
Mowi: jaka strone / funkcje backendowa chce uruchomic.

query params:
q=flask&page=2
Mowia: z jakimi opcjami, np. wyszukiwanie i numer strony.

headers:
Host, User-Agent, Accept
Mowia: dodatkowe informacje techniczne o requescie.
```

## 7. Content-Type vs Accept

Najprostsza sciaga:

```text
Content-Type:
co jest w body requestu albo response

Accept:
co klient chce dostac w odpowiedzi
```

Przyklad z API:

```text
POST /api/books HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Accept: application/json

{"title": "Flask basics"}
```

Czytamy to tak:

```text
Content-Type: application/json
Wysylam JSON do backendu.

Accept: application/json
Chce dostac JSON z backendu.
```

Przyklad z normalna strona HTML:

```text
GET /books HTTP/1.1
Host: 127.0.0.1:5000
Accept: text/html
```

Czytamy to tak:

```text
Nie wysylam body, tylko prosze o strone.
Accept: text/html oznacza, ze chce dostac HTML.
```

## 8. Body requestu vs body response

To dotyczy kierunku danych.

```text
request:
idzie od przegladarki / klienta do backendu

response:
wraca od backendu do przegladarki / klienta
```

Dlatego `body requestu` to tresc wysylana do serwera.

Przyklad: piszesz posta i klikasz "Opublikuj".

Bardzo uproszczony request moglby wygladac tak:

```text
POST /posts HTTP/1.1
Host: example.com
Content-Type: application/json
Accept: application/json

{"content": "Dzisiaj ucze sie HTTP"}
```

Tutaj body requestu to:

```json
{"content": "Dzisiaj ucze sie HTTP"}
```

Czyli:

```text
tresc posta wysylana do backendu moze byc w body requestu
```

Ale kiedy otwierasz strone i widzisz posty, dane ida w druga strone: od backendu do przegladarki.

Wtedy tresc postow jest czescia odpowiedzi serwera, czyli `body response`.

Przyklad bardzo uproszczonej odpowiedzi JSON:

```text
HTTP/1.1 200 OK
Content-Type: application/json

[
  {"content": "Dzisiaj ucze sie HTTP"},
  {"content": "Flask zaczyna miec sens"}
]
```

Tutaj body response to:

```json
[
  {"content": "Dzisiaj ucze sie HTTP"},
  {"content": "Flask zaczyna miec sens"}
]
```

Najwazniejsze rozroznienie:

```text
Pisze posta i wysylam:
tresc posta jest w body requestu

Otwieram strone i widze posty:
tresc postow jest w body response
```

## 9. Czy kazdy request ma body?

Nie. Nie kazdy request ma body.

Najwazniejszy przyklad to `GET`.

`GET` zwykle sluzy do pobierania danych:

```text
Daj mi cos.
```

Dlatego dane potrzebne do wskazania albo filtrowania zasobu dajesz w URL-u: w path albo query.

Przyklad:

```text
GET /decks/7?mode=learning HTTP/1.1
Host: fishingit.example
```

Rozbijamy to tak:

```text
GET             -> metoda: chce pobrac dane
/decks/7        -> path: chce talie o id 7
?mode=learning  -> query: chce tryb learning
Host: ...       -> naglowek
```

Ten request nie ma body, bo wszystko, co jest potrzebne do wskazania danych, znajduje sie w URL-u.

Praktyczna regula:

```text
GET:
dane wejsciowe w path albo query, bez body

POST:
dane operacji moga byc w body, np. nowa talia

PATCH:
dane operacji moga byc w body, np. zmiana statusu
```

Przyklad `POST` z body:

```text
POST /decks HTTP/1.1
Content-Type: application/json

{"name": "HTTP"}
```

Znaczy:

```text
Utworz nowa talie na podstawie danych z body.
```

Przyklad `PATCH` z body:

```text
PATCH /decks/7 HTTP/1.1
Content-Type: application/json

{"status": "mastered"}
```

Znaczy:

```text
Zmien talie 7 na podstawie danych z body.
```

W JavaScriptowym `fetch()` body dla `GET` i `HEAD` jest niedozwolone.

Zle:

```javascript
fetch("/decks/7", {
  method: "GET",
  body: JSON.stringify({ mode: "learning" })
})
```

Dobrze:

```javascript
fetch("/decks/7?mode=learning")
```

## 10. fetch() vs metody HTTP

To dotyczy JavaScriptu i HTTP.

`fetch()` to funkcja w JavaScripcie.

Jej zadanie:

```text
wyslac request z przegladarki do backendu
```

`GET`, `POST`, `PATCH` to metody HTTP.

Ich zadanie:

```text
powiedziec, jaki rodzaj requestu wysylasz
```

Najkrotsze rozroznienie:

```text
fetch() = narzedzie do wyslania requestu
PATCH   = metoda requestu
```

`fetch()` moze wyslac rozne metody HTTP.

Domyslnie `fetch()` wysyla `GET`:

```javascript
fetch("/decks/7")
```

To znaczy mniej wiecej:

```text
GET /decks/7
```

`fetch()` moze tez wyslac `POST`:

```javascript
fetch("/decks", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ name: "HTTP" })
})
```

To znaczy mniej wiecej:

```text
POST /decks
Content-Type: application/json

{"name": "HTTP"}
```

`fetch()` moze tez wyslac `PATCH`:

```javascript
fetch("/decks/7", {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ status: "mastered" })
})
```

To znaczy mniej wiecej:

```text
PATCH /decks/7
Content-Type: application/json

{"status": "mastered"}
```

Wazne funkcje i pola:

```text
fetch()           -> funkcja JavaScriptu do wysylania requestu
method            -> pole, w ktorym ustawiasz metode HTTP
headers           -> pole, w ktorym ustawiasz naglowki
body              -> pole, w ktorym ustawiasz body requestu
JSON.stringify()  -> funkcja JavaScriptu, ktora zamienia obiekt na tekst JSON
```

Najprosciej:

```text
fetch() samo w sobie nie jest POST ani PATCH.
fetch() moze wyslac GET, POST, PATCH i inne metody.
```

## 11. Routing we Flasku

To dotyczy backendu.

Po otrzymaniu requestu Flask musi zdecydowac:

```text
Ktora funkcja ma obsluzyc ten request?
```

To dopasowanie nazywamy routingiem.

Flask patrzy przede wszystkim na:

```text
1. metode HTTP, np. GET, POST, PATCH
2. sciezke URL, np. /decks/7
```

Przyklad route'u:

```python
@blueprint.get("/decks/<int:deck_id>")
def show_deck(deck_id):
    ...
```

Czytamy to tak:

```text
Jesli przyjdzie request metoda GET
i sciezka bedzie miala ksztalt /decks/liczba,
to uruchom funkcje show_deck().
```

Fragment:

```python
<int:deck_id>
```

znaczy:

```text
w tym miejscu URL-a ma byc liczba calkowita,
a Flask zapisze ja pod nazwa deck_id
```

### Przyklad, ktory pasuje

Request:

```text
GET /decks/7
```

pasuje, bo:

```text
metoda: GET        -> pasuje do @blueprint.get
sciezka: /decks/7  -> pasuje do /decks/<int:deck_id>
deck_id: 7         -> Flask umie odczytac jako int
```

Flask wywola wtedy funkcje mniej wiecej tak:

```python
show_deck(deck_id=7)
```

### Przyklad, ktory nie pasuje przez typ parametru

Request:

```text
GET /decks/abc
```

nie pasuje, bo:

```text
metoda: GET          -> pasuje
sciezka: /decks/abc  -> ksztalt jest podobny
deck_id: abc         -> nie pasuje, bo abc nie jest int
```

Problem jest w tym fragmencie route'u:

```python
<int:deck_id>
```

Flask oczekuje liczby calkowitej, a dostaje tekst `abc`.

### Przyklad, ktory nie pasuje przez metode

Request:

```text
POST /decks/7
```

ma dobra sciezke, ale zla metode dla tego route'u.

Route:

```python
@blueprint.get("/decks/<int:deck_id>")
```

obsluguje `GET`, a request jest `POST`.

Jesli aplikacja nie ma osobnego route'u `POST` dla tej sciezki, Flask nie uruchomi funkcji `show_deck()`.

Najwazniejsze:

```text
Flask wybiera funkcje glownie po metodzie HTTP i sciezce URL.

Body requestu i naglowki moga byc wazne pozniej,
ale najpierw Flask musi znalezc pasujacy route.
```

## 12. Mini-sprawdzenie

Popatrz na URL:

```text
http://127.0.0.1:5000/products?category=books&page=3
```

Pytania:

```text
1. Jaka jest sciezka URL?
2. Jakie sa parametry query?
3. Czy naglowki requestu widac w tym URL-u?
```

Odpowiedzi:

```text
1. /products
2. category=books oraz page=3
3. Nie. Naglowki sa wysylane razem z requestem, ale nie widzisz ich w pasku adresu.
```

Drugie mini-sprawdzenie:

```text
POST /api/products HTTP/1.1
Content-Type: application/json
Accept: application/json

{"name": "Notebook"}
```

Pytania:

```text
1. Co mowi Content-Type?
2. Co mowi Accept?
```

Odpowiedzi:

```text
1. Body requestu jest JSON-em.
2. Klient chce dostac odpowiedz jako JSON.
```

Trzecie mini-sprawdzenie:

```text
POST /posts HTTP/1.1
Content-Type: application/json

{"content": "Hej!"}
```

Pytania:

```text
1. Czy tekst posta jest w request czy response?
2. Czy tekst posta jest w headers czy body?
```

Odpowiedzi:

```text
1. W request, bo wysylasz go do backendu.
2. W body, bo to glowna tresc wysylanych danych.
```

Czwarte mini-sprawdzenie:

```javascript
fetch("/decks/7", {
  method: "PATCH",
  body: JSON.stringify({ status: "mastered" })
})
```

Pytania:

```text
1. Co tutaj jest funkcja JavaScriptu?
2. Co tutaj jest metoda HTTP?
3. Czy `body` jest czescia funkcji `fetch()` czy metoda HTTP?
```

Odpowiedzi:

```text
1. fetch()
2. PATCH
3. body jest polem/opcja przekazana do fetch(), a nie metoda HTTP.
```

Piate mini-sprawdzenie:

Masz route:

```python
@blueprint.get("/decks/<int:deck_id>")
def show_deck(deck_id):
    ...
```

Requesty:

```text
GET /decks/7
GET /decks/abc
POST /decks/7
```

Pytania:

```text
1. Ktory request pasuje?
2. Ktory request nie pasuje przez typ parametru?
3. Ktory request nie pasuje przez metode?
```

Odpowiedzi:

```text
1. GET /decks/7
2. GET /decks/abc, bo abc nie jest int
3. POST /decks/7, bo route obsluguje GET
```

## 13. Najkrotsza sciaga

```text
URL:
pelny adres w przegladarce

sciezka URL / path:
czesc adresu, ktora wybiera route we Flasku

dekorator Flask:
@app.route("/path") laczy path z funkcja backendowa

query params:
dodatkowe dane po ?, np. ?q=flask&page=2

naglowki requestu:
dodatkowe techniczne informacje wysylane z requestem, np. User-Agent, Cookie, Authorization

Content-Type:
co wysylasz w body, np. application/json albo application/x-www-form-urlencoded

Accept:
co chcesz dostac w odpowiedzi, np. text/html albo application/json

body requestu:
dane wysylane do backendu, np. tresc nowego posta

body response:
dane zwracane przez backend, np. lista postow do pokazania na stronie

GET:
pobieranie danych; dane wejsciowe zwykle w path albo query, bez body

POST:
wyslanie danych operacji; body czesto zawiera dane do utworzenia czegos

PATCH:
wyslanie danych operacji; body czesto zawiera dane do zmiany czegos

fetch():
funkcja JavaScriptu do wysylania requestow

method:
opcja w fetch(), ktora ustawia metode HTTP, np. "GET", "POST", "PATCH"

JSON.stringify():
funkcja JavaScriptu, ktora zamienia obiekt na tekst JSON przed wyslaniem w body

routing we Flasku:
dopasowanie requestu do funkcji backendowej

@blueprint.get("/decks/<int:deck_id>"):
route dla metody GET i sciezki /decks/liczba

<int:deck_id>:
dynamiczny fragment sciezki; musi byc int i trafia do funkcji jako deck_id
```
