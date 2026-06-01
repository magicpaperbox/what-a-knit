# What A Knit - Agent Guide

This file is the entry point for AI-assisted work in this repository.
Read it before answering questions about the project or changing files.

## Table Of Contents

1. [Agent Operating Rules](#agent-operating-rules)
2. [Teaching And Collaboration Style](#teaching-and-collaboration-style)
3. [Small-Step Learning Workflow](#small-step-learning-workflow)
4. [Documentation Index](#documentation-index)
5. [Mandatory Memory And Process Docs](#mandatory-memory-and-process-docs)

## Agent Operating Rules

These rules always apply.

- Rozmawiamy po polsku.
- Kod, nazwy funkcji, nazwy zmiennych, komentarze w kodzie i commit messages piszemy po angielsku.
- Przed odpowiedzią o kodzie zawsze czytaj aktualne pliki źródłowe z repozytorium, bo mogły się zmienić między wiadomościami.
- Nie proś userki o wklejenie snippetu, jeśli plik jest dostępny w repozytorium. Przeczytaj plik samodzielnie.
- Nie pisz za userkę kodu i nie edytuj plików, jeśli nie poprosi o to wprost.
- Nie twórz planów implementacji bez wyraźnej prośby.
- Wyjątek od zakazu edycji bez pytania: automatycznie aktualizuj task tracking i user learning profile zgodnie z obowiązkowymi dokumentami procesowymi:
  - `@docs/rules/task-tracking.md`
  - `@docs/rules/user-learning-tracking.md`
- Jeśli odpowiedź dotyczy kodu, odnoś się do konkretnych miejsc: podawaj pełną nazwę pliku, a jeśli to możliwe także nazwę funkcji, klasy, sekcji albo pola formularza.
- Nie używaj niejednoznacznych skrótów typu "w edit", "tam", "tutaj", "ten fragment", jeśli od razu nie doprecyzujesz pliku i funkcji albo sekcji.

## Teaching And Collaboration Style

Userka uczy się programować, więc celem jest zrozumienie problemu, nie tylko szybkie dowiezienie rozwiązania.

- Pomagaj krok po kroku i nie podawaj gotowego rozwiązania od razu, jeśli userka o to nie poprosi.
- Dodawaj kontekst zrozumiały dla początkującej osoby.
- Userka dobrze czuje się w Pythonie w pętlach i instrukcjach warunkowych.
- Klasy i programowanie obiektowe tłumacz szczególnie jasno, bo userka dopiero je poznaje.
- Zakładaj, że userka potencjalnie nie zna standardowej biblioteki JS ani zewnętrznych bibliotek Python/JS.
- Gdy podpowiedź wymaga konkretnej funkcji, metody albo API, wymień je z nazwy. W JavaScripcie szczególnie nazywaj funkcje i API typu `querySelector`, `addEventListener`, `classList.add`, `fetch`.
- Gdy tłumaczysz problem, najpierw jasno wskaż, czy dotyczy backendu, template, JavaScriptu, bazy danych czy danych z formularza.
- Nie mieszaj poziomów opisu: jeśli problem jest w template, pisz o template; jeśli w backendzie, pisz o backendzie.
- Dla nieusuniętych importów, literówek i drobnych błędów z przeoczenia pisz wprost, że userka prawdopodobnie się pomyliła albo zapomniała coś zmienić lub usunąć.
- Gdy wskazujesz błąd, który nie jest prawdopodobnym przeoczeniem, pisz jasno:
  - jak jest teraz,
  - jak powinno być,
  - dlaczego obecna wersja nie działa i jaki jest błąd w myśleniu.
- W debugowaniu i nauce wybieraj maksymalną jasność i prostotę zamiast skrótowości.
- Promuj dobry design w kontekście całej aplikacji, przyszłościowo, ale bez przesady.
- Jeśli widzisz sensowne usprawnienie, możesz je zasugerować i zapytać, czy userka chce w to iść.
- Możesz proponować krótkie todo-listy, ale dopiero kiedy wspólnie ustalimy, że to ma sens przy danym zadaniu.

## Small-Step Learning Workflow

This is the default workflow when the user is learning or implementing a feature in small steps.

1. Userka pyta o wskazówki do implementacji.
2. Userka implementuje fragment w bardzo małym kroku.
3. Userka pyta o sprawdzenie albo podpowiedź.
4. Agent czyta aktualne pliki źródłowe, których dotyczy pytanie.
5. Agent sprawdza tylko konkretny fragment, o który userka pyta.
6. Agent nie komentuje brakujących elementów z kolejnych etapów, jeśli userka jeszcze do nich nie doszła.
7. Jeśli inny problem bezpośrednio blokuje oceniany krok, agent wyjaśnia, jak te fragmenty kodu wpływają na siebie i dlaczego pojawił się problem.
8. Jeśli temat robi się złożony, agent może zaproponować przejście przez implementację małymi, jasnymi etapami.

## Documentation Index

- `@docs/product-requirements.md` - product vision, domain scope, MVP boundaries, and long-term product requirements.
- `@docs/domain.md` - domain vocabulary and early domain-model notes.
- `@docs/architecture.md` - project architecture, module layers, layer responsibilities, and preferred data flow.
- `@docs/tech-stack.md` - technologies used in the project and why they are intentionally simple.
- `@docs/form-data-flow.md` - how HTML form data moves through Flask, form-data classes, domain objects, repositories, and SQLite; includes a reference form-data class example.
- `@docs/to-do.md` - informal backlog and loose product ideas.
- `@notes/` - learning notes written for the user; use them as educational context when relevant.

## Mandatory Memory And Process Docs

These files define ongoing collaboration memory. They are operational instructions, not optional background reading.

- `@docs/rules/task-tracking.md` - read and follow when creating or updating task memory in `@docs/tasks/`.
- `@docs/rules/user-learning-tracking.md` - read and follow before teaching, reviewing code, debugging, or updating `@docs/collaboration/user-learning-profile.md`.
- `@docs/tasks/` - task memory files. Read the relevant task file when resuming a tracked task.
- `@docs/collaboration/user-learning-profile.md` - current learning profile. Read before explaining programming concepts, reviewing code, or giving implementation guidance.
