# 1. Wnioski z testów end-user i propozycje zmian (w formie user stories)

**Co testowano:** kanwa *„marlik - kierunki wizualne”* (stan z 24.09.2026, bez zmian do 09.10.2026) — 16 ekranów w 4 kierunkach wizualnych
(Ciepły editorial, Miękki natywny, Żywy i zabawny, Minimalistyczny premium), każdy w motywie jasnym i ciemnym oraz z 4 kolorami akcentu (128 wariantów).
Repozytorium `marlik` było puste, więc testowałem jedyną istniejącą wersję aplikacji — klikalną wizualnie, ale statyczną makietę.

**Perspektywa:** dwie osoby z pary — Antoś (makieta pokazuje jego widok) i Marlenka — używające aplikacji na telefonie w ciągu dnia i na laptopie przy rozliczeniach.

Każda historia poniżej ma: obserwację z testu (z numerem przypadku jako dowodem), argument, *dlaczego* to ważne dla użytkownika, proponowaną zmianę z uzasadnieniem i kryteria akceptacji, po których poznamy, że zmiana działa.
Numery `A-…`, `TC-B-…`, `C-…` odsyłają do [katalogu przypadków](03-przypadki-testowe.md) i [wyników](wyniki/).

---

## Najważniejsze wnioski (w skrócie)

1. **Pieniądze są pokazane w sposób, który budzi niepokój i bywa sprzeczny.** Czerwone `-13 165 zł` na Głównej obok dobrej wiadomości „Marlenka oddaje Tobie 1 416 zł”, waluty € w portfelu w zł bez kursu, rozliczenie bez kierunku. To najważniejszy obszar aplikacji o wspólnych finansach i jednocześnie najsłabszy w odbiorze.
2. **Kwoty łamią się w połowie liczby** (`1` / `416 zł`, `-13` / `165,83` / `zł`) na 7 z 16 ekranów — bo separatorem tysięcy jest zwykła spacja.
3. **Czytelność zależy od wybranego koloru i motywu.** Bez żadnego błędu kontrastu przechodzą tylko 3 z 32 kombinacji (Ciepły editorial, jasny, akcent zielony / fioletowy / niebieski). Domyślny akcent we wszystkich kierunkach to odcień czerwieni — prawie ten sam co kolor „minus”.
4. **Aktywna zakładka „Osobiste / Wspólne” jest niemal niewidoczna** w dwóch kierunkach (kontrast 1,08–1,21:1) — a od niej zależy, czy patrzysz na swoje, czy wspólne pieniądze.
5. **Główna ma dużo miejsca bez funkcji** (kafle M / Razem / A — ok. 20% ekranu) i za mało informacji o tym, co ważne dziś (czy obie osoby zrobiły migawkę).
6. **Telefon i desktop to dwie różne aplikacje** — inne nazwy, inne funkcje (portfele, filtry, inwestycje tylko na desktopie), desktop o sztywnej szerokości 1280 px.
7. **Najmocniejszy kandydat: Ciepły editorial** — najmniej problemów, kwoty mieszczą się w jednej linii na ekranach Finansów, aktywna zakładka wyraźna (13,8:1), 3 z 4 akcentów bez błędów kontrastu. Warunek: zmienić domyślny akcent z terakoty (ΔE 7,9 od koloru „minus”) na zielony `#3E6B5A` albo niebieski `#2F5D9E`. Szczegóły w [raporcie](04-raport-z-wykonania.md#porównanie-kierunków).

---

## Epik 1: Finanse, którym da się ufać

### US-01 — Rozumiem kartę Finanse na Głównej bez wchodzenia w moduł
> **Jako** Antoś **chcę** z Głównej od razu wiedzieć, ile wydaliśmy w podróży i kto komu ile odda, **aby** nie musieć otwierać Finansów, żeby sprawdzić, czy wszystko gra.

- **Obserwacja:** karta pokazuje czerwone `-13 165 zł` bez nazwy portfela i bez wyjaśnienia, czym ta kwota jest (A-015, A-045). Kwota jest *obcięta*, nie zaokrąglona — `-13 165,83` powinno dać `-13 166` (A-013). Pod spodem dobra wiadomość („Marlenka oddaje Tobie”) w szarym, drobnym tekście.
- **Argument:** czerwony minus w aplikacjach finansowych znaczy „dług / problem”. Tu oznacza sumę wydatków wyjazdu — użytkownik dostaje sygnał alarmowy tam, gdzie nic złego się nie dzieje, a przeocza informację, która go dotyczy (należy mu się 1 416 zł). Obcięcie zamiast zaokrąglenia to drobiazg, ale w module pieniędzy każda niespójność między ekranami podważa zaufanie do liczb.
- **Proponowana zmiana:** karta mówi zdaniem: *„Sycylia ’26 · wydaliście 13 165,83 zł”* w neutralnym kolorze tekstu; wyróżniona linia: *„Marlenka odda Ci 1 416,31 zł”* (albo „Oddajesz Marlence…”). Czerwień tylko dla tego, co faktycznie użytkownik jest winien.
  *Dlaczego tak:* oddziela dwie różne informacje (ile wydaliśmy vs. kto komu), a kolor odpowiada emocji, którą powinna wywołać.
- **Kryteria akceptacji:**
  - Karta zawiera nazwę portfela i czasownik opisujący kwotę („wydaliście”, „zostało”).
  - Kwota na Głównej = kwota w Finansach, zaokrąglona matematycznie (test: 13 165,83 → 13 166).
  - Kolor „minus” użyty wyłącznie dla należności użytkownika.
- **Priorytet:** P1

### US-02 — Kwota nigdy nie rozpada się na dwie linie
> **Jako** użytkownik **chcę** widzieć każdą kwotę w całości, **aby** nie przeczytać „1” zamiast „1 416 zł”.

- **Obserwacja:** `1 416 zł` łamie się na Głównej we wszystkich 4 kierunkach; saldo `-13 165,83 zł` w nagłówku desktopu łamie się na 2 linie (Natywny, Żywy) lub 3 (Minimalistyczny) — TC-B-023, C-01, C-13, C-21, C-29. W kodzie separatorem tysięcy jest zwykła spacja (A-176).
- **Argument:** przy szybkim spojrzeniu oko czyta pierwszą linię — „Marlenka oddaje Tobie 1” to inna informacja niż 1 416 zł. Problem urośnie z każdą większą kwotą (A-065).
- **Proponowana zmiana:** formatowanie przez `Intl.NumberFormat('pl-PL', {style:'currency', currency:'PLN'})` — wstawia spację nierozdzielającą (U+00A0) między tysiącami i przed walutą; dodatkowo `white-space: nowrap` na elementach z kwotą, a duże salda z automatycznym zmniejszaniem fontu.
  *Dlaczego tak:* jedna funkcja formatująca dla całej aplikacji usuwa przyczynę zamiast łatać pojedyncze ekrany i od razu daje poprawny polski zapis.
- **Kryteria akceptacji:** TC-B-023 zaliczony na wszystkich ekranach, także przy kwocie 1 000 000,00 zł i szerokości 320 px.
- **Priorytet:** P1

### US-03 — Wydatek w euro widzę też w złotówkach
> **Jako** Marlenka **chcę** przy wydatku w euro widzieć kurs i równowartość w złotych, **aby** rozumieć, skąd bierze się saldo portfela.

- **Obserwacja:** historia w € (`-57,00 €`), saldo portfela i rozliczenia w zł, bez kursu (A-043). Nie da się sprawdzić, czy saldo jest poprawne (A-044 zablokowany).
- **Argument:** portfel wyjazdowy z założenia miesza waluty. Jeśli użytkownik nie może sam przeliczyć, nie uwierzy w rozliczenie — a to ono decyduje, kto komu przelewa pieniądze.
- **Proponowana zmiana:** każda pozycja w obcej walucie ma drugą linię `≈ 245,10 zł · kurs 4,30 (21.09)`; kurs zapisywany z dnia transakcji, z możliwością ręcznej korekty.
  *Dlaczego kurs z dnia transakcji:* tylko wtedy rozliczenie nie zmienia się samo z dnia na dzień.
- **Kryteria akceptacji:** A-043 i A-062 zaliczone; suma pełnej historii = saldo portfela (A-044).
- **Priorytet:** P1

### US-04 — Z historii wiem, kto komu i ile zapłacił
> **Jako** para **chcemy** przy każdej pozycji widzieć, kto płacił i jak podzieliliśmy koszt, **aby** nie kłócić się o rozliczenia.

- **Obserwacja:** `Rozliczenie - Marlenka 1 150,00 zł` bez znaku i kierunku (A-048); „dzielone” nie mówi, kto płacił ani w jakiej proporcji (A-049); „Oddałem za kolację Kate” — opis zwrotu, oznaczony jako wspólny wydatek (A-047).
- **Argument:** aplikacja do wspólnych finansów ma rozstrzygać wątpliwości, a nie je tworzyć. Brak kierunku przelewu to dokładnie ta informacja, o którą para będzie się dopytywać.
- **Proponowana zmiana:** druga linia pozycji: `Płacił(a): Antoś · po połowie` / `Marlenka → Ty · rozliczenie`; typ transakcji (wydatek / zwrot / przelew) wybierany jawnie w formularzu, a nie zgadywany z opisu.
- **Kryteria akceptacji:** każda pozycja ma płacącego i sposób podziału; rozliczenia mają strzałkę kierunku; A-047–A-049 zaliczone.
- **Priorytet:** P1

### US-05 — Zawsze wiem, czy patrzę na swoje, czy wspólne pieniądze
> **Jako** Antoś **chcę** jednoznacznie widzieć, czy wybrana jest zakładka „Osobiste”, czy „Wspólne”, **aby** nie dodać prywatnego wydatku do wspólnego portfela.

- **Obserwacja:** w Miękkim natywnym i Minimalistycznym aktywna zakładka różni się od tła kontrastem 1,08–1,21:1 (A-054, C-11, C-12, C-27, C-28). Przełącznik nie ma `aria-pressed`/`aria-selected` — czytnik ekranu nie powie, co wybrane (TC-B-012, 12/12 ekranów).
- **Argument:** pomyłka kosztuje tu realne pieniądze i prywatność — wydatek osobisty trafia do partnera (A-073). WCAG 1.4.11 wymaga 3:1 dla stanu komponentu.
- **Proponowana zmiana:** aktywna zakładka z kontrastem ≥ 3:1 do toru przełącznika (jak w Ciepłym editorialu: odwrócone kolory, 13,8:1); w kodzie `role="tablist"` + `aria-selected` albo `aria-pressed`. Dodatkowo nagłówek formularza transakcji powtarza „Dodajesz do: Wspólne · Sycylia ’26”.
- **Kryteria akceptacji:** TC-B-012 zaliczony; kontrast aktywna/nieaktywna ≥ 3:1 w obu motywach.
- **Priorytet:** P1

### US-06 — Pole kwoty działa jak w aplikacji bankowej
> **Jako** użytkownik **chcę** po dotknięciu pola „Kwota” dostać klawiaturę numeryczną z przecinkiem i widzieć walutę, **aby** szybko wpisać wydatek przy kasie.

- **Obserwacja:** pole bez `inputmode`/`type`, bez waluty (A-056); w dwóch kierunkach obrys pola ma kontrast 1,15–1,2:1, czyli pole jest prawie niewidoczne (TC-B-003, C-15, C-31).
- **Argument:** dodanie wydatku to najczęstsza czynność w module finansów; każda sekunda i każdy błąd wpisu się sumują.
- **Proponowana zmiana:** `inputmode="decimal"`, przyrostek waluty (wybieralny), akceptacja „57,5” i „57.5” (A-063), obrys ≥ 3:1.
- **Kryteria akceptacji:** A-056, A-063, TC-B-003 zaliczone.
- **Priorytet:** P2

### US-07 — Inwestycje są tam, gdzie ich szukam
> **Jako** Antoś **chcę** widzieć moduł inwestycji w kontekście swoich oszczędności, **aby** nie mylił mi się z budżetem wyjazdu.

- **Obserwacja:** pusty stan „Nic tu jeszcze nie rośnie / Dodaj inwestycję” stoi obok portfela „Sycylia ’26” (A-052) i jest tylko na desktopie (A-053).
- **Argument:** wyjazd to krótkotrwały budżet, inwestycje to długoterminowe oszczędności — sąsiedztwo sugeruje, że inwestuje się z portfela wyjazdowego.
- **Proponowana zmiana:** inwestycje jako osobna sekcja w „Osobiste” (lub osobna pozycja menu), widoczna także na telefonie.
- **Kryteria akceptacji:** karta inwestycji nie pojawia się przy portfelu wyjazdowym; dostępna na obu urządzeniach.
- **Priorytet:** P3

---

## Epik 2: Główna, która mówi, co ważne dziś

### US-08 — Widzę, kto zrobił dzisiejszą migawkę
> **Jako** Marlenka **chcę** zobaczyć na Głównej, czy Antoś już zrobił dzisiejszą migawkę, i przypomnieć sobie o swojej, **aby** nie stracić 62-dniowej serii.

- **Obserwacja:** chipy „Ty” i „Marlenka” wyglądają identycznie — brak stanu „zrobione / czeka” (A-016); brak stanu zagrożonej serii (A-017).
- **Argument:** seria to mechanizm, który ma codziennie przyciągać do aplikacji. Bez stanu nie wiadomo, czy coś trzeba zrobić — i seria przepada bez ostrzeżenia, co zniechęca bardziej niż jej brak.
- **Proponowana zmiana:** chip z ikoną ✓ i miniaturą zdjęcia dla osoby, która zrobiła migawkę; dla tej, która nie zrobiła — przycisk „Zrób teraz”. Po 20:00 karta zmienia ton: „Zostało 4 h, żeby utrzymać serię”.
- **Kryteria akceptacji:** w każdym z 4 stanów (nikt / tylko Ty / tylko partner / oboje) karta wygląda inaczej i ma właściwą akcję.
- **Priorytet:** P1

### US-09 — Każdy element Głównej czemuś służy
> **Jako** Antoś **chcę**, żeby największe elementy Głównej coś mi mówiły lub do czegoś prowadziły, **aby** nie przewijać, żeby dotrzeć do finansów i randki.

- **Obserwacja:** trzy duże kafle M / Razem / A zajmują ok. 20% ekranu, nie są klikalne i nie mają opisu funkcji; litery M i A dublują awatary z nagłówka (A-018, C-01). Przy tekście 130% szybkie akcje chowają się pod paskiem (TC-B-032).
- **Argument:** pierwszy ekran to najdroższa przestrzeń w aplikacji. Element bez funkcji spycha w dół to, co realnie się zmienia (pieniądze, randka, migawka).
- **Proponowana zmiana:** kafle zamienić na *dzisiejsze migawki* (zdjęcie Marlenki · wspólny kolaż · zdjęcie Antosia) — wtedy łączą się z US-08 i mają sens; w stanie „brak zdjęcia” pokazują przycisk aparatu. Jeśli to nie jest planowane — usunąć i podnieść karty Finanse/Randka.
- **Kryteria akceptacji:** każdy element powyżej szybkich akcji jest klikalny albo pokazuje dane zmienne w czasie; TC-B-032 zaliczony na Głównej.
- **Priorytet:** P2

### US-10 — Daty i dni tygodnia są zawsze poprawne
> **Jako** para **chcemy** ufać datom randek, **aby** nie przyjść w złym dniu.

- **Obserwacja:** nagłówek „Czwartek, 24 września” (2026 — poprawnie), ale „sob 27.09” to w 2026 niedziela (A-011, A-012).
- **Argument:** w makiecie to literówka, ale pokazuje ryzyko: dzień tygodnia wpisywany ręcznie niezależnie od daty. W kalendarzu randek pomyłka dnia to dosłownie nieudana randka.
- **Proponowana zmiana:** dzień tygodnia zawsze generowany z daty (`Intl.DateTimeFormat('pl-PL', {weekday:'short'})`), także w danych przykładowych makiet.
- **Kryteria akceptacji:** A-012 zaliczony; test jednostkowy formatowania dat dla przełomu miesiąca/roku.
- **Priorytet:** P2

### US-11 — Powiadomienia mówią, ile ich jest
> **Jako** użytkownik czytnika ekranu **chcę** usłyszeć „Powiadomienia, 3 nowe”, **aby** wiedzieć, czy warto je otwierać.

- **Obserwacja:** kropka bez liczby, `aria-label="Powiadomienia"` bez informacji o nowych (A-019).
- **Proponowana zmiana:** licznik (do „9+”) i `aria-label` z liczbą.
- **Kryteria akceptacji:** A-019 zaliczony.
- **Priorytet:** P3

---

## Epik 3: Jedna, spójna aplikacja

### US-12 — Ta sama czynność ma tę samą nazwę
> **Jako** użytkownik **chcę**, żeby przycisk „Wydatek” na Głównej i „Transakcja” w Finansach nazywały się tak samo, **aby** nie zastanawiać się, czy to różne rzeczy.

- **Obserwacja:** „Wydatek” vs „Transakcja” (A-020); „Główna” vs „Strona główna” (A-030); filtry „Wydatki/Rozliczenia” vs „Wydatki/Przychody” (A-050); dwa identyczne „Rozlicz” na jednym ekranie (A-051); w nagłówku telefonu dwa awatary, na desktopie jeden (A-032).
- **Argument:** każda różnica nazw to pytanie, które użytkownik musi sobie zadać. W aplikacji używanej codziennie kumuluje się to w poczucie bałaganu.
- **Proponowana zmiana:** słownik pojęć (glosariusz) w repozytorium — jedna nazwa na czynność i miejsce; drugi „Rozlicz” na desktopie zamienić na „Szczegóły rozliczeń” albo usunąć.
  *Dlaczego słownik, a nie poprawki ekran po ekranie:* przy kolejnych ekranach (Randki, Zakupy…) błąd wróci, jeśli nie będzie jednego źródła prawdy.
- **Kryteria akceptacji:** A-020, A-030, A-032, A-050, A-051 zaliczone; glosariusz w `docs/`.
- **Priorytet:** P2

### US-13 — Na telefonie mam wszystko, co na laptopie
> **Jako** Marlenka, która nie używa laptopa, **chcę** na telefonie założyć nowy portfel, przefiltrować historię i dojść do Listy życzeń, **aby** nie być osobą „drugiej kategorii” w parze.

- **Obserwacja:** lista portfeli, „Nowy portfel”, filtry historii i inwestycje tylko na desktopie (A-053); Lista życzeń, Słoik wspomnień, Mapa i Ustawienia ukryte pod „Więcej”, którego ekranu nie ma (A-031).
- **Argument:** aplikacja dla pary działa tylko wtedy, gdy obie osoby mogą zrobić wszystko. Jeśli jedna nie ma laptopa, jej udział w finansach się kończy.
- **Proponowana zmiana:** zaprojektować ekran „Więcej” i ekran „Portfele” na telefon; zasada: funkcja może być na telefonie głębiej, ale nie może jej nie być.
- **Kryteria akceptacji:** macierz funkcji telefon × desktop bez pustych pól; A-031, A-053 zaliczone.
- **Priorytet:** P1

### US-14 — Aplikacja wygląda tak samo dla Antosia i Marlenki
> **Jako** Marlenka **chcę** widzieć „Cześć, Marlenka” i „Oddajesz Antosiowi 1 416,31 zł”, **aby** aplikacja mówiła do mnie, a nie o mnie.

- **Obserwacja:** wszystkie ekrany są z perspektywy Antosia (A-010); u Marlenki zdanie „Marlenka oddaje Tobie” musi zmienić się na „Oddajesz Antosiowi” — wymaga to odmiany imienia (celownik), czego makieta nie przewiduje.
- **Argument:** polska odmiana imion to częste źródło błędów („Oddajesz Antoś”). Lepiej zauważyć to na etapie projektu niż po wdrożeniu.
- **Proponowana zmiana:** każdy ekran z danymi osób projektować w obu perspektywach; w profilu pole „Jak cię odmieniać” (mianownik / dopełniacz / celownik) albo konstrukcje bez odmiany („Do oddania: Ty → Antoś”).
- **Kryteria akceptacji:** każdy ekran Finansów i Głównej ma wariant „Marlenka”; brak nieodmienionych imion.
- **Priorytet:** P2

---

## Epik 4: Czytelność i dostępność dla każdego

### US-15 — Wybrany kolor akcentu nie psuje czytelności
> **Jako** użytkownik, który lubi ciemny motyw i niebieski akcent, **chcę** móc wybrać dowolną opcję z ustawień, **aby** każdy tekst wciąż był czytelny — także w słońcu.

- **Obserwacja:** w 29 z 32 kombinacji (kierunek × motyw × akcent) co najmniej jeden ekran nie spełnia kontrastu WCAG AA (A-131, TC-B-001/002). Najgorsze: biały na pomarańczowym w Żywym (2,83:1), szara kwota na zaznaczonym portfelu (2,1:1). Kolor tekstu na akcencie dobierany jest wzorem jasności „percepcyjnej” `0.299R+0.587G+0.114B > 0.62`, który nie jest miarą kontrastu WCAG.
- **Argument:** ustawienia nie powinny pozwalać na wybór, który psuje aplikację. Użytkownik nie wie, że kontrast to problem — widzi tylko, że „źle się czyta”.
- **Proponowana zmiana:**
  1. Rozdzielić token akcentu na dwa: `accent-fill` (tło przycisku) i `accent-text` (tekst/link na tle) — każdy dobrany pod swoje tło.
  2. Kolor tekstu na akcencie wybierać algorytmem kontrastu WCAG (biały vs. prawie czarny — wyższy kontrast).
  3. Do ustawień wpuszczać tylko akcenty, które w obu motywach przechodzą TC-B-001/002 (skrypt `qa/narzedzia/sprawdz.mjs` to sprawdza automatycznie).
  *Dlaczego tak:* jeden kolor nie może być jednocześnie czytelny jako tekst na jasnym tle, na ciemnym tle i jako tło pod białym tekstem — dwa tokeny rozwiązują to raz na zawsze.
- **Kryteria akceptacji:** TC-B-001 i TC-B-002 zaliczone dla każdego akcentu dostępnego w ustawieniach.
- **Priorytet:** P1

### US-16 — Główna akcja nie wygląda jak ostrzeżenie
> **Jako** Antoś **chcę**, żeby przycisk „Transakcja” nie miał koloru ujemnych kwot, **aby** nie kojarzyć dodawania wydatku z błędem.

- **Obserwacja:** domyślne akcenty wszystkich kierunków to odcienie czerwieni/pomarańczu; odległość barwy od koloru „minus” to ΔE 7,9 (Ciepły editorial — praktycznie ten sam kolor) do 37,5. Przy akcentach niebieskim/zielonym/fioletowym ΔE = 62–125 (A-055, C-07).
- **Argument:** kolor ma w finansach znaczenie; jeśli akcja i strata mają ten sam kolor, kolor przestaje cokolwiek znaczyć.
- **Proponowana zmiana:** domyślny akcent spoza rodziny czerwieni (np. `#3E6B5A` lub `#2F5D9E` w Ciepłym editorialu); czerwień zarezerwowana dla „minus” i akcji destrukcyjnych.
- **Kryteria akceptacji:** ΔE(akcent, minus) ≥ 30 dla każdego dostępnego akcentu.
- **Priorytet:** P2

### US-17 — Działa z dużym tekstem i na mniejszym telefonie
> **Jako** osoba z ustawionym większym tekstem w telefonie **chcę**, żeby nic nie znikało pod dolnym paskiem, **aby** móc korzystać z aplikacji bez okularów.

- **Obserwacja:** przy tekście 130% na wszystkich 8 ekranach telefonu treść chowa się pod paskiem lub jest ucinana (TC-B-032), przy 200% — 11–19 problemów na ekran (TC-B-033). Przy 360 px (typowy Android) i 320 px nazwy transakcji są ucinane (TC-B-030/031). 12 z 16 ekranów używa tekstu 11 px (TC-B-020). Ekrany mają sztywną wysokość 844 px i `overflow: hidden`.
- **Argument:** powiększony tekst systemowy to jedno z najczęściej używanych ustawień dostępności, nie tylko wśród osób słabowidzących; WCAG 1.4.4 wymaga, by treść działała przy 200%. 360 px to bardzo popularna szerokość ekranów Androida — makieta 390 px pokazuje wariant optymistyczny.
- **Proponowana zmiana:** treść przewijana (bez stałej wysokości), dolny pasek przyklejony; minimalny tekst 12 px (etykiety uppercase 11 px → 12–13 px); długie nazwy transakcji zawijane do 2 linii zamiast wielokropka.
- **Kryteria akceptacji:** TC-B-020, TC-B-030–033 zaliczone.
- **Priorytet:** P1

### US-18 — Łatwo trafiam palcem
> **Jako** użytkownik telefonu **chcę** trafiać w zakładki i linki za pierwszym razem, **aby** nie przełączać się przypadkiem między Osobiste i Wspólne.

- **Obserwacja:** zakładki 36 px wysokości, link „Wszystkie” 65×17 px (TC-B-010, 4/4 ekrany Finansów na telefonie).
- **Proponowana zmiana:** min. 44×44 px pola dotyku (zakładki 44 px, link z paddingiem).
- **Kryteria akceptacji:** TC-B-010 zaliczony.
- **Priorytet:** P2

### US-19 — Czytnik ekranu mówi, gdzie jestem
> **Jako** osoba niewidoma **chcę** usłyszeć, która pozycja menu jest aktywna, **aby** wiedzieć, na jakim ekranie jestem.

- **Obserwacja:** aktywna pozycja paska/menu oznaczona tylko kolorem, bez `aria-current` (TC-B-013, 12/12). Pozytywnie: wszystkie przyciski mają nazwy (TC-B-011), fokus klawiatury jest widoczny i obejmuje wszystkie kontrolki (TC-B-022), nagłówki i `lang="pl"` poprawne (TC-B-014/015).
- **Proponowana zmiana:** `aria-current="page"` na aktywnej pozycji + dodatkowy wizualny wskaźnik (pogrubienie/podkreślenie), nie tylko kolor (WCAG 1.4.1).
- **Kryteria akceptacji:** TC-B-013 zaliczony.
- **Priorytet:** P2

### US-20 — Desktop dopasowuje się do okna
> **Jako** Antoś na 13-calowym laptopie **chcę** widzieć cały ekran Finansów bez poziomego przewijania, **aby** wygodnie robić rozliczenia.

- **Obserwacja:** desktop ma sztywne 1280 px — przy 1024 px poziomy scroll, przy 1440 px 160 px pustego pasa (TC-B-034/035). W Minimalistycznym karta inwestycji wychodzi poza ekran (TC-B-017, C-29).
- **Proponowana zmiana:** siatka elastyczna z punktami przełamania (np. < 1100 px — kolumna rozliczeń pod historią).
- **Kryteria akceptacji:** TC-B-017, TC-B-034, TC-B-035 zaliczone.
- **Priorytet:** P3

---

## Priorytety w jednym miejscu

| Priorytet | Historie | Dlaczego najpierw |
|---|---|---|
| **P1** | US-01, 02, 03, 04, 05, 08, 13, 15, 17 | Dotyczą poprawności i zrozumienia pieniędzy, prywatności, czytelności i równego dostępu obu osób — błędy tu kosztują zaufanie albo pieniądze. |
| **P2** | US-06, 09, 10, 12, 14, 16, 18, 19 | Wygoda codziennego użycia i spójność; wpływają na odbiór, rzadziej na poprawność. |
| **P3** | US-07, 11, 20 | Dopracowanie; warto zrobić przy okazji prac nad danym ekranem. |
