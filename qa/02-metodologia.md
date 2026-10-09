# 2. Problemy w metodologii pracy nad marlikiem — i jak je poprawić

Poniżej opisuję problemy w sposobie, w jaki **powstaje** marlik (nie w samych ekranach), znalezione podczas testów. Każdy punkt ma:
**obserwację** (co konkretnie widać w projekcie), **dlaczego to problem** (argument), **poprawkę** i **dlaczego ta poprawka** (argument za rozwiązaniem, nie tylko za zmianą).
Na końcu jest też krytyka metodologii samych tych testów — bo część ograniczeń wynika z tego, jak je zleciliśmy i wykonaliśmy.

---

## M-01. Projektujemy wygląd, zanim zdefiniujemy problem i funkcje

**Obserwacja.** Jedynym artefaktem projektu jest kanwa z czterema kierunkami wizualnymi. Nie ma briefu, listy funkcji, priorytetów ani definicji MVP. Menu desktopu wymienia 9 modułów (Lista życzeń, Słoik wspomnień, Mapa, Inwestycje…), ale tylko 2 mają ekrany (Główna, Finanse). Repozytorium jest puste.

**Dlaczego to problem.** Decyzja o stylu podejmowana bez znajomości zakresu ocenia, jak wyglądają 2 ekrany, a nie czy styl udźwignie 9 modułów, puste stany, formularze, błędy i wykresy. Każda funkcja dodana później będzie „wciskana” w wybrany styl. Bez listy funkcji nie wiadomo też, co testować — dlatego 72 ze 109 scenariuszy użytkownika (66%) jest zablokowanych.

**Poprawka.** Przed dalszym projektowaniem: jednostronicowy brief (dla kogo, jaki problem, czego *nie* robimy) i backlog user stories z priorytetem — punktem startu może być [01-wnioski-i-user-stories.md](01-wnioski-i-user-stories.md). Na tej podstawie zdefiniować MVP, np. Główna + Finanse + Migawka.

**Dlaczego tak.** Brief i backlog kosztują godziny, a zmiana kierunku po zbudowaniu 9 modułów — tygodnie. MVP z 2–3 modułów pozwala dowieźć działającą aplikację, której para realnie używa, zamiast 9 niedokończonych.

---

## M-02. Wybieramy styl przed sprawdzeniem przepływów

**Obserwacja.** 16 ekranów to te same 4 ekrany w 4 stylach — 75% pracy to warianty stylu. Nie ma ani jednego ekranu kluczowej czynności: dodania wydatku, zrobienia migawki, zaproponowania randki, rozliczenia.

**Dlaczego to problem.** Wyniki testów pokazują, że **22 z 26 niezaliczonych scenariuszy użytkownika (katalog A) powtarza się identycznie we wszystkich 4 kierunkach**: mylące czerwone saldo, waluta bez kursu, rozliczenie bez kierunku, brak stanu migawki, różne nazwy tej samej akcji, błędna data. Styl ich nie rozwiązuje ani nie pogarsza — to problemy struktury i treści. Od kierunku zależą tylko 4 (widoczność zakładki, kolor akcentu, kontrast wybranych akcentów, łamanie licznika serii). Wybór między 4 stylami nie usuwa żadnego z pozostałych 22.

**Poprawka.** Kolejność: (1) szare, niskiej wierności szkice 3 głównych przepływów, (2) test na parze (zadania typu: „dodaj wydatek 57 € za kolację, płaciłeś Ty, po połowie”), (3) poprawki, (4) dopiero wtedy styl na sprawdzonej strukturze.

**Dlaczego tak.** Błędy przepływu i treści najtaniej poprawić, zanim obłożymy je stylem — w szarym szkicu zmiana kolejności kroków to minuty, w dopracowanym stylu godziny ×4 kierunki. Styl wybrany na realnych ekranach (formularz, lista, pusty stan) jest też trafniej oceniany niż na dwóch ekranach pokazowych.

---

## M-03. Kierunki nie są porównywane na równych warunkach

**Obserwacja.**
- Kanwa pokazuje Główną **tylko w jasnym**, Finanse na telefonie **tylko w ciemnym** (`dark.default` w `data-props`). Nikt nie oglądał Głównej w ciemnym ani Finansów w jasnym, chyba że ręcznie przełączył suwak — dopiero w testach wyszły problemy widoczne wyłącznie w niewyświetlanych wariantach (C-02, kontrasty TC-B-002 w ciemnym).
- Domyślne akcenty różnią się między kierunkami (terakota, pomarańcz, neon, czerwień), więc porównujemy kolor razem ze stylem.
- Brak kryteriów wyboru: nie zapisano, co ma decydować (czytelność? emocja? „premium”?).

**Dlaczego to problem.** Porównanie, w którym każdy kandydat pokazuje inny zestaw ekranów i kolorów, faworyzuje kierunki o „ładniejszym” domyślnym wariancie, a nie te, które lepiej działają. Bez kryteriów decyzja będzie gustem, a nie oceną.

**Poprawka.**
1. Stała matryca porównawcza: każdy ekran × oba motywy × ten sam typ akcentu, obok siebie. Narzędzie `qa/narzedzia/render.mjs` renderuje ją automatycznie (128 wariantów w kilka sekund).
2. Zapisane kryteria z wagami, np.: czytelność i dostępność (wynik TC-B), zrozumiałość treści (test z parą), dopasowanie do charakteru marki, koszt wdrożenia (np. ilustracje „naklejki” w Żywym są droższe).
3. Ocena każdego kierunku tymi samymi kryteriami — tabela w [raporcie](04-raport-z-wykonania.md#porównanie-kierunków) to pierwszy krok.

**Dlaczego tak.** Matryca usuwa efekt „domyślnego wariantu”, a kryteria spisane *przed* oceną chronią przed racjonalizowaniem wyboru po fakcie.

---

## M-04. Dane w makietach są wpisane ręcznie, nie wyliczane

**Obserwacja.** Daty, dni tygodnia, sumy i zaokrąglenia są wpisane jako tekst w każdym pliku osobno. Skutki: „sob 27.09” przy dacie, która jest niedzielą (A-012); saldo obcięte zamiast zaokrąglone (A-013); kwoty w € bez przeliczenia (A-043); zwykła spacja jako separator tysięcy, przez co kwoty łamią się na 7 z 16 ekranów (TC-B-023). Te same dane są skopiowane w 16 plikach.

**Dlaczego to problem.** Makieta z prawdziwie wyglądającymi danymi „testuje” też treść — a ręcznie wpisane dane ukrywają błędy logiki (nikt nie sprawdzi, czy saldo wynika z historii) i tworzą nowe (literówki w dniu tygodnia). Te same błędy przejdą do kodu, jeśli ktoś przepisze teksty z makiety.

**Poprawka.** Jeden plik danych przykładowych (`docs/dane-przykladowe.json`: osoby, portfele, transakcje z walutą i kursem, randki z datą ISO) oraz wspólne funkcje formatujące (`Intl.NumberFormat('pl-PL')`, `Intl.DateTimeFormat('pl-PL')`), używane zarówno w makietach, jak i w aplikacji.

**Dlaczego tak.** Saldo wyliczane z transakcji samo wykaże niespójności; formatowanie przez standardowe API daje poprawny polski zapis (spacja nierozdzielająca, przecinek) bez pamiętania o nim na każdym ekranie. Jeden plik zmienia się w jednym miejscu.

---

## M-05. Brak systemu projektowego — tokeny kopiowane w 16 plikach, logika kontrastu niezgodna z WCAG

**Obserwacja.**
- Każdy plik ma własną kopię palety i reguł (`const P = …`, `c.btnEdge = …`). Sprawdziłem sumy kontrolne — dziś 4 pliki każdego kierunku są zgodne, ale każda zmiana koloru wymaga 4 identycznych edycji. Kanwa ma `designSystems: []`.
- Kolor tekstu na akcencie liczony jest wzorem `0.299R + 0.587G + 0.114B > 0.62`. To przybliżenie „jasności percepcyjnej”, a nie współczynnik kontrastu WCAG. Skutek: biały tekst na akcencie 2,83–3,68:1 przy wymaganych 4,5:1 (TC-B-002 niezaliczony w 103/128 wariantach).
- Jeden token `accent` służy jednocześnie za tło przycisku, kolor linku na jasnym i na ciemnym tle — fizycznie nie da się go dobrać tak, by działał we wszystkich trzech rolach.

**Dlaczego to problem.** Kopiowane tokeny to przepis na rozjazd przy pierwszej poprawce zrobionej w pośpiechu. Błędny wzór kontrastu sprawia, że *każdy* nowy akcent w ustawieniach może psuć czytelność — a użytkownik nie ma jak się o tym dowiedzieć.

**Poprawka.**
1. Po wyborze kierunku — jeden plik tokenów (`tokens.json`, np. jako Design System na kanwie albo w repo), z którego korzystają makiety i kod.
2. Rozdzielenie akcentu na role: `accent-fill`, `accent-text-on-light`, `accent-text-on-dark`, `on-accent`.
3. `on-accent` wybierany funkcją kontrastu WCAG (wyższy z: biały / prawie czarny), a lista akcentów w ustawieniach filtrowana testem TC-B-001/002.
4. Testy z `qa/narzedzia/` uruchamiane automatycznie przy każdej zmianie (GitHub Actions) — regresja kontrastu nie przejdzie niezauważona.

**Dlaczego tak.** Rola tokenu zamiast koloru pozwala dobrać każdy kolor do jego tła. Automatyczny test zamienia „pamiętajmy o kontraście” w regułę, której nie da się pominąć — a skrypt już istnieje.

---

## M-06. Prototyp jest statyczny — nie da się przetestować zadań

**Obserwacja.** Wszystkie linki prowadzą do `#`, przyciski nie mają akcji (TC-B-016: 12/16 ekranów; 0 przejść między ekranami). Kanwa obsługuje linki prototypowe (`<a href="Finanse.dc.html">` przechodzi do innego ekranu w trybie Play), ale nie są używane.

**Dlaczego to problem.** Test użytkownika polega na zadaniach („rozlicz się z Marlenką”). Bez przejść da się ocenić tylko pierwsze wrażenie — a ono nie mówi, czy ktoś znajdzie „Nowy portfel” albo zrozumie, co robi „Rozlicz”. To główny powód, dla którego 66% scenariuszy jest zablokowanych.

**Poprawka.** Minimum: połączyć istniejące ekrany linkami (pasek nawigacji, karta Finanse → Finanse) i dorysować 3 ekrany zadań: formularz transakcji, ekran migawki, potwierdzenie rozliczenia. Alternatywa: przejść od razu do kodu (np. PWA w repo) dla wybranego kierunku.

**Dlaczego tak.** Kilka połączeń i 3 ekrany odblokowują około 30 scenariuszy z katalogu A (Finanse, Migawka, nawigacja) i pozwalają zrobić prawdziwy test z parą. Jeśli kod jest bliski, prototyp w kodzie daje od razu dane, formatowanie i dostępność — rzeczy, których makieta nie pokaże.

---

## M-07. Brak walidacji z ludźmi — oceniamy sami siebie

**Obserwacja.** Makiety oceniają ich autorzy (para, dla której jest aplikacja) i — w tym raporcie — AI. Nikt spoza projektu nie dostał zadania do wykonania.

**Dlaczego to problem.** Autorzy znają zamysł: wiedzą, że `-13 165 zł` to wydatki wyjazdu, a kafle M/Razem/A to „miejsce na zdjęcia”. Nowa osoba tego nie wie — i właśnie to wychodzi w scenariuszach A-015 i A-018. Ocena ekspercka (w tym moja) znajduje problemy zgodności i spójności, ale nie zastąpi obserwacji, gdzie ktoś realnie się zawiesza.

**Poprawka.** Krótkie testy z zadaniami: 3–5 osób lub par spoza projektu, 15 minut, 3 zadania, zasada „nie podpowiadamy”. Notować, gdzie się zatrzymują i co mówią na głos. Pierwszym uczestnikiem może być Marlenka, bez wcześniejszego tłumaczenia ekranów.

**Dlaczego tak.** Zasada praktyczna z badań użyteczności mówi, że kilka osób na rundę wystarcza do wykrycia większości poważnych problemów, a kolejne rundy (po poprawkach) dają więcej niż jedna duża. Koszt jest mały, a efekt bezpośredni.

---

## M-08. Projekt żyje poza repozytorium — brak wersji, historii i „definition of done”

**Obserwacja.** Kanwa jest poza gitem, repo `marlik` jest puste, nie ma kryteriów akceptacji ani definicji ukończenia. Nie wiadomo, która wersja ekranu jest „obowiązująca” ani kiedy ekran jest gotowy.

**Dlaczego to problem.** Bez historii nie da się wrócić do wcześniejszej decyzji ani wyjaśnić, dlaczego coś zmieniono. Bez kryteriów akceptacji „gotowe” znaczy „podoba mi się”, a testy nie mają do czego się odnieść.

**Poprawka.** Repo jako źródło prawdy:
```
docs/      brief, glosariusz pojęć, user stories z kryteriami akceptacji, dane przykładowe
design/    eksport ekranów (render.mjs) przy każdej wersji kanwy
qa/        przypadki testowe, narzędzia, wyniki (ten katalog)
app/       kod (po wyborze kierunku)
```
Zmiany przez pull requesty; „gotowe” = kryteria akceptacji user story spełnione + testy z `qa/` zaliczone.

**Dlaczego tak.** Repo daje historię i przegląd zmian za darmo, a kryteria akceptacji w user stories łączą projekt z testem — każdy niezaliczony przypadek wskazuje konkretne story do poprawy.

---

## M-09. Dane osobiste w artefaktach projektowych

**Obserwacja.** Makiety zawierają prawdziwe imiona, nazwisko znajomej („Kate”), cel i daty wyjazdu oraz realnie wyglądające kwoty i salda.

**Dlaczego to problem.** Kanwę i repo łatwo udostępnić (link, publiczne repo, zrzut ekranu w portfolio). Dane finansowe i plany podróży to informacje prywatne — także osób trzecich.

**Poprawka.** W artefaktach, które mogą wyjść poza parę, używać fikcyjnych danych z `docs/dane-przykladowe.json` (M-04), a repo trzymać prywatne do czasu ich podmiany.

**Dlaczego tak.** Jedna podmiana w pliku danych (dzięki M-04) usuwa problem ze wszystkich ekranów naraz.

---

## M-10. Krytyka metodologii tych testów (i samego zlecenia)

Rzetelność wymaga wskazania słabych stron również tej pracy.

### M-10a. Liczba przypadków nie jest miarą jakości testów
**Obserwacja.** Zlecenie brzmiało „ponad 500 przypadków”. Wykonałem 1 101 wykonań, ale 1 032 z nich to 26 przypadków z katalogu B uruchomionych na wielu ekranach i wariantach kolorów. **354 niezaliczenia z katalogu B to 18 unikalnych defektów (D-01–D-18), a wszystkie 410 niezaliczeń ze wszystkich katalogów — 38** (lista w [raporcie](04-raport-z-wykonania.md#unikalne-defekty)). Jeden błąd (np. 11 px w dolnym pasku) „niezalicza się” na 12 ekranach.
**Dlaczego to problem.** Cel liczbowy zachęca do mnożenia wariantów zamiast szukania nowych ryzyk; 500 wykonań może sprawdzić jeden ekran 500 razy.
**Poprawka.** Raportować i mierzyć: liczbę **unikalnych defektów** wg ważności, **pokrycie user stories** (każda ma ≥ 1 test akceptacyjny) i **pokrycie przepływów** (ile z kluczowych zadań da się wykonać). Liczbę wykonań traktować jako informację pomocniczą.
**Dlaczego tak.** Te metryki mówią, co realnie wiemy o jakości i czego jeszcze nie wiemy; liczba wykonań mówi głównie o kosztach.

### M-10b. „Testy manualne” wykonane przez AI i skrypt
**Obserwacja.** Katalog B wykonałem skryptem w przeglądarce Chromium (pomiar kontrastu, rozmiarów, przejścia klawiaturą), katalog A — czytając treść ekranów, katalog C — oglądając zrzuty. Nie było prawdziwego człowieka z telefonem w ręku.
**Dlaczego to problem.** Wyniki są powtarzalne i mierzalne, ale nie obejmują: realnej czytelności w słońcu, gestów, wydajności, czytnika ekranu na urządzeniu, zrozumienia przez osoby spoza projektu.
**Poprawka.** Każdy przypadek B ma w katalogu kroki do ręcznego powtórzenia (narzędzia deweloperskie przeglądarki, kalkulator kontrastu), więc można go zweryfikować wyrywkowo. Po zbudowaniu aplikacji: przebieg na fizycznym iPhonie i Androidzie z VoiceOver/TalkBack oraz test z ludźmi (M-07).
**Dlaczego tak.** Automat dobrze wyłapuje regresje mierzalne, człowiek — problemy zrozumienia; potrzebne są obie warstwy.

### M-10c. Testowanie makiety zamiast aplikacji
**Obserwacja.** 72 ze 109 scenariuszy użytkownika jest zablokowanych. Przypadki responsywności (TC-B-030–035) i powiększenia tekstu sprawdzają, „co by się stało, gdyby wdrożyć dokładnie tak, jak narysowano” — kanwa z założenia ma stałe rozmiary.
**Dlaczego to problem.** Część niezaliczeń (np. sztywne 1280 px) to cecha narzędzia, nie decyzja projektowa — trzeba je czytać jako „brakuje specyfikacji zachowania”, a nie „projektant się pomylił”.
**Poprawka.** Do każdego ekranu dopisać, jak ma się zachowywać przy innej szerokości i większym tekście (2–3 zdania), a zablokowane scenariusze A uruchomić ponownie na prototypie klikalnym lub w kodzie.
**Dlaczego tak.** Specyfikacja zachowania to informacja, której programista i tak będzie potrzebował — lepiej, żeby wynikała z decyzji niż z domysłu.

### M-10d. Ograniczenia pomiaru
- Kontrast liczony wzorem WCAG 2.x na kolorach wyliczonych przez Chromium; nie uwzględnia antyaliasingu ani grubości fontu (WCAG 2 nie bierze grubości pod uwagę poza progiem „dużego tekstu”).
- Fonty wczytane lokalnie z Google Fonts w tych samych wersjach, które podaje kanwa; drobne różnice renderowania między przeglądarkami mogą przesunąć łamanie wierszy o kilka pikseli.
- Logotyp „marlik” wyłączony z pomiaru kontrastu (wyjątek WCAG 1.4.3 dla logotypów).
- TC-B-006 (widoczność granic przycisków) to heurystyka, a nie wymóg WCAG — przycisk z etykietą tekstową nie musi mieć obrysu 3:1. Ujęty, bo słabo odcinające się przyciski w Natywnym i Minimalistycznym wyglądają jak tekst, ale jego wynik nie wchodzi do oceny zgodności.
