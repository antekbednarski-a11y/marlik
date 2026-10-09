# 3. Przypadki testowe do testów manualnych

Trzy katalogi, każdy z innym celem:

| Katalog | Co sprawdza | Liczba przypadków | Jak wykonany na prototypie | Wyniki |
|---|---|---|---|---|
| **A — scenariusze użytkownika** | Czy para jest w stanie zrobić to, po co otwiera aplikację, i czy treść jest prawdziwa i zrozumiała | 109 | Ręcznie: czytanie treści i danych na ekranach; scenariusze wymagające logiki oznaczone jako *Zablokowany* | [`wyniki/katalog-A.csv`](wyniki/katalog-A.csv) |
| **B — interfejs, dostępność, układ** | Mierzalne wymagania: kontrast, rozmiary, semantyka, łamanie, responsywność | 26 przypadków × ekrany × warianty = 1 032 wykonania | Skryptem w Chromium (`narzedzia/sprawdz.mjs`); każdy przypadek ma kroki do ręcznego powtórzenia | [`wyniki/wyniki-B.csv`](wyniki/wyniki-B.csv) |
| **C — przegląd wizualny** | Wrażenie, czytelność, zgodność z intencją — to, czego nie zmierzy skrypt | 32 (16 ekranów × 2 motywy) | Ręcznie: oglądanie zrzutów każdego ekranu w każdym motywie | [`wyniki/katalog-C.csv`](wyniki/katalog-C.csv) |

**Statusy:** *Zaliczony*, *Niezaliczony*, *Nie dotyczy* (na danym ekranie nie ma elementu, który przypadek sprawdza), *Zablokowany* (prototyp nie ma funkcji — przypadek nie został wykonany i nie jest liczony jako wykonany).

**Priorytety (katalog A):** P1 — błąd kosztuje pieniądze, prywatność albo blokuje główne zadanie; P2 — utrudnia codzienne użycie; P3 — dopracowanie.

---

## Katalog B — interfejs, dostępność, układ

Wykonywane na każdym ekranie. Przypadki oznaczone **[kolor]** zależą od motywu i akcentu, więc są wykonywane dla wszystkich 8 wariantów kolorystycznych ekranu (2 motywy × 4 akcenty → 128 wykonań). Pozostałe wykonywane raz na ekran (16 wykonań) albo na ekranach, których dotyczą.

**Narzędzia do ręcznego powtórzenia:** narzędzia deweloperskie przeglądarki (Chrome: *Inspect* → panel *Accessibility* i próbnik kontrastu w *Styles*), dowolny kalkulator kontrastu WCAG, linijka/inspektor rozmiaru elementu, klawiatura (Tab, Shift+Tab).

| ID | Nazwa | Podstawa | Kroki (manualnie) | Oczekiwany wynik |
|---|---|---|---|---|
| TC-B-001 | **[kolor]** Kontrast tekstów na neutralnym tle | WCAG 2.2 — 1.4.3 (AA) | Dla każdego tekstu (poza logotypem i poza tekstami w/na akcencie) odczytaj kolor tekstu i efektywny kolor tła; policz kontrast. | ≥ 4,5:1; dla tekstu ≥ 24 px lub ≥ 18,66 px pogrubionego (700+) ≥ 3:1 |
| TC-B-002 | **[kolor]** Kontrast tekstów w kolorze akcentu i na tle akcentu | WCAG 1.4.3 | Jak wyżej, dla tekstów w kolorze akcentu (linki, aktywna pozycja menu) oraz na tle akcentu (przycisk główny, aktywny chip/zakładka). | j.w. |
| TC-B-003 | **[kolor]** Widoczność obrysu pola formularza | WCAG 1.4.11 | Zmierz kontrast obrysu (lub tła) pola do tła wokół. | ≥ 3:1 |
| TC-B-004 | **[kolor]** Znaczenie kwot nie tylko kolorem | WCAG 1.4.1 | Dla każdej kwoty w kolorze „plus”/„minus” sprawdź, czy ma znak +/−. | Każda barwiona kwota ma znak |
| TC-B-005 | **[kolor]** Kontrast ikon w przyciskach bez tekstu | WCAG 1.4.11 | Dla przycisków z samą ikoną (dzwonek, lupa, +) zmierz kontrast ikony do jej tła. | ≥ 3:1 |
| TC-B-006 | **[kolor]** Przycisk odcina się od tła (heurystyka) | Heurystyka (nie WCAG) | Dla przycisków z tłem/obrysem zmierz kontrast tła lub obrysu przycisku do otoczenia. | ≥ 3:1 — inaczej przycisk wygląda jak tekst |
| TC-B-010 | Rozmiar celów dotykowych | Apple HIG 44 pt, WCAG 2.5.5 (AAA); desktop: WCAG 2.5.8 (AA) | Zmierz każdy przycisk/link/pole. | Telefon ≥ 44×44 px; desktop ≥ 24×24 px |
| TC-B-011 | Nazwa dostępna kontrolek | WCAG 4.1.2 | W panelu *Accessibility* sprawdź *Name* każdej kontrolki. | Każda ma niepustą nazwę |
| TC-B-012 | Stan przełącznika segmentowego (Osobiste/Wspólne) | WCAG 4.1.2 | Sprawdź `aria-pressed`/`aria-selected`/`role="tab"` na przyciskach przełącznika. | Stan wybranej opcji ogłaszany przez czytnik |
| TC-B-013 | Aktywna pozycja nawigacji | WCAG 1.3.1, 1.4.1 | Sprawdź `aria-current` na aktywnej pozycji paska/menu. | Dokładnie jedna pozycja z `aria-current` |
| TC-B-014 | Struktura nagłówków | WCAG 1.3.1 | Wypisz nagłówki h1–h6 w kolejności. | Dokładnie jeden h1, bez przeskoków poziomów |
| TC-B-015 | Język strony | WCAG 3.1.1 | Sprawdź `lang` elementu `<html>`. | `lang="pl"` |
| TC-B-016 | Przejścia i akcje prototypu | Klikalność prototypu | Kliknij każdy link i przycisk. | Każdy prowadzi do ekranu lub wykonuje akcję (link ≠ `#`) |
| TC-B-017 | Treść mieści się w ramce ekranu | Układ | Sprawdź, czy żaden tekst/przycisk nie jest ucięty krawędzią ekranu. | Brak elementów poza ramką |
| TC-B-018 | Treść nie chowa się pod dolnym paskiem (telefon) | Układ | Sprawdź, czy ostatni element treści kończy się nad paskiem nawigacji. | Brak tekstu pod paskiem |
| TC-B-019 | Tekst nie jest ucinany wielokropkiem (szerokość bazowa) | Układ / treść | Poszukaj „…” w nazwach. | Brak uciętych nazw przy szerokości projektu |
| TC-B-020 | Minimalny rozmiar tekstu | Czytelność (praktyka: ≥ 12 px) | Zmierz font każdego tekstu. | Każdy tekst ≥ 12 px |
| TC-B-021 | Render bez błędów | Jakość artefaktu | Otwórz ekran z konsolą przeglądarki. | Brak błędów i pustych pól szablonu `{{…}}` |
| TC-B-022 | Obsługa klawiaturą i widoczny fokus | WCAG 2.1.1, 2.4.7 | Przejdź Tabem przez ekran. | Każda kontrolka osiągalna, fokus widoczny |
| TC-B-023 | Kwota nie łamie się między wierszami | Czytelność kwot | Sprawdź każdą kwotę (`zł`, `€`). | Każda kwota w jednym wierszu |
| TC-B-030 | Szerokość 360 px (typowy Android) | Responsywność | Zwęź ekran telefonu do 360 px. | Nic nie jest ucięte ani pod paskiem |
| TC-B-031 | Szerokość 320 px (najmniejsze iPhone'y) | Responsywność | Zwęź do 320 px. | j.w. |
| TC-B-032 | Tekst powiększony do 130% | Dynamic Type / ustawienia czcionki | Powiększ wszystkie fonty o 30%. | j.w. |
| TC-B-033 | Tekst powiększony do 200% | WCAG 1.4.4 | Powiększ wszystkie fonty o 100%. | j.w. |
| TC-B-034 | Okno desktopu 1024 px | Responsywność | Otwórz ekran desktopowy w oknie 1024 px. | Brak poziomego przewijania |
| TC-B-035 | Okno desktopu 1440 px | Responsywność | Otwórz w oknie 1440 px. | Układ wypełnia okno (brak pustego pasa) |

Pełne wyniki z dowodami (lista elementów, zmierzone wartości) dla każdego z 1 032 wykonań: [`wyniki/wyniki-B.csv`](wyniki/wyniki-B.csv) (do otwarcia w Excelu / Arkuszach) i [`wyniki/wyniki-B.json`](wyniki/wyniki-B.json).

---

## Katalog C — przegląd wizualny

**Procedura (dla każdego ekranu w motywie jasnym i ciemnym, z domyślnym akcentem kierunku):**
1. Obejrzyj ekran jako użytkownik, bez wiedzy o projekcie: co jest najważniejsze? co mogę tu zrobić?
2. Sprawdź łamanie tekstów i kwot, ucięcia na krawędziach, odstępy, wyrównania.
3. Sprawdź, czy stany (aktywna zakładka, zaznaczony portfel, aktywna pozycja menu) są widoczne na pierwszy rzut oka.
4. Sprawdź, czy kolory nie wysyłają sprzecznych sygnałów (np. akcja w kolorze błędu).
5. Zapisz obserwacje; *Niezaliczony*, jeśli znaleziono co najmniej jeden problem z kroków 2–4.

Zrzuty, na których wykonano przegląd: [`zrzuty/`](zrzuty/). Wyniki: [`wyniki/katalog-C.csv`](wyniki/katalog-C.csv).

---

## Katalog A — scenariusze użytkownika (109)

Kolumna *Status na prototypie* to wynik wykonania na obecnej makiecie. Scenariusze *Zablokowane* są gotowe do wykonania na działającej aplikacji. Pełne kroki i dowody: [`wyniki/katalog-A.csv`](wyniki/katalog-A.csv).

### Konto

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-001 | Rejestracja nowej osoby | Otwórz aplikację po raz pierwszy → Załóż konto (e-mail/Apple/Google) | Konto utworzone, przejście do parowania | P1 | ⛔ Zablokowany | Brak ekranu rejestracji w makiecie |
| A-002 | Logowanie istniejącej osoby | Wyloguj → Zaloguj tymi samymi danymi | Widok Głównej z danymi pary | P1 | ⛔ Zablokowany | Brak ekranu logowania |

### Para

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-003 | Zaproszenie partnera kodem/linkiem | Ustawienia → Zaproś partnera → wyślij link | Partner po kliknięciu dołącza do pary; obie osoby widzą te same wspólne dane | P1 | ⛔ Zablokowany | Brak przepływu parowania |
| A-004 | Link zaproszenia wygasa / użyty drugi raz | Użyj tego samego linku na trzecim koncie | Komunikat, że para jest pełna; brak dołączenia | P1 | ⛔ Zablokowany | Brak przepływu parowania |
| A-005 | Rozłączenie pary | Ustawienia → Rozłącz → potwierdź | Jasna informacja, co dzieje się ze wspólnymi danymi i rozliczeniami | P2 | ⛔ Zablokowany | Brak ekranu ustawień |

### Onboarding

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-006 | Pierwsze uruchomienie bez danych (puste stany) | Nowa para bez historii → Główna, Finanse, Migawka | Każdy moduł ma pusty stan z jedną jasną akcją | P2 | ⛔ Zablokowany | Makieta pokazuje tylko stan z danymi (poza kartą inwestycji) |
| A-007 | Zgoda na powiadomienia i aparat | Pierwsze użycie Migawki | Systemowe prośby poprzedzone wyjaśnieniem po polsku | P2 | ⛔ Zablokowany | Brak przepływu |

### Główna

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-010 | Powitanie zalogowanej osoby | Zaloguj się jako Antoś, potem jako Marlenka | Powitanie i perspektywa ('Tobie', 'Ty') zmieniają się zależnie od osoby | P1 | ⛔ Zablokowany | Makieta ma tylko perspektywę Antosia; brak wariantu dla Marlenki |
| A-011 | Data w nagłówku zgodna z kalendarzem | Porównaj 'Czwartek, 24 września' z kalendarzem 2026 | Dzień tygodnia zgodny z datą | P2 | ✅ Zaliczony | 24.09.2026 to czwartek |
| A-012 | Termin najbliższej randki zgodny z kalendarzem | Karta 'Najbliższa randka': 'sob 27.09 · 19:00' | Skrót dnia tygodnia zgodny z datą | P1 | ❌ Niezaliczony | 27.09.2026 to niedziela, nie sobota (przy nagłówku 'Czwartek, 24 września') |
| A-013 | Kwota z Finansów na Głównej zgodna z Finansami | Porównaj kartę 'Finanse' (−13 165 zł) z saldem portfela (−13 165,83 zł) | Ta sama kwota lub poprawnie zaokrąglona | P1 | ❌ Niezaliczony | −13 165,83 zaokrąglone to −13 166; makieta ucina do −13 165 |
| A-014 | Kwota rozliczenia na Głównej zgodna z Finansami | Porównaj '1 416 zł' z '1 416,31 zł' | Ta sama kwota lub poprawnie zaokrąglona | P2 | ✅ Zaliczony | 1 416,31 → 1 416 (poprawne zaokrąglenie) |
| A-015 | Zrozumienie karty Finanse bez wchodzenia w moduł | Pokaż Główną osobie spoza projektu i zapytaj: co znaczy czerwone −13 165 zł? | Osoba wie, czy to dług, wydatki podróży, czy saldo konta | P1 | ❌ Niezaliczony | Karta nie mówi, którego portfela dotyczy ani czym jest kwota; czerwony minus obok 'Marlenka oddaje Tobie' (czyli dobrej wiadomości) daje sprzeczny sygnał |
| A-016 | Status dzisiejszej migawki obu osób | Karta 'Migawka dziś' z chipami 'Ty' i 'Marlenka' | Widać, kto już zrobił dzisiejszą migawkę, a kto nie | P1 | ❌ Niezaliczony | Oba chipy wyglądają identycznie — brak stanu zrobione/niezrobione |
| A-017 | Seria migawek — ryzyko utraty | Karta '62 dni z rzędu' wieczorem, gdy jedna osoba nie zrobiła migawki | Ostrzeżenie o utracie serii i akcja 'Zrób teraz' | P2 | ⛔ Zablokowany | Brak stanu zagrożonej serii |
| A-018 | Znaczenie dużych kafli M / Razem / A | Dotknij każdego kafla; zapytaj użytkownika, czym są | Jasny cel (np. dzisiejsze migawki) i akcja po dotknięciu | P1 | ❌ Niezaliczony | Kafle zajmują ok. 20% ekranu, nie są przyciskami/linkami i nie mają podpisu funkcji; duplikują awatary M/A z nagłówka |
| A-019 | Powiadomienia — informacja o liczbie i treści | Spójrz na dzwonek z kropką; użyj VoiceOver | Liczba nieprzeczytanych lub tekst 'X nowych' także dla czytnika ekranu | P2 | ❌ Niezaliczony | Kropka bez liczby; aria-label 'Powiadomienia' nie mówi o nowych |
| A-020 | Nazwy szybkich akcji zgodne z ekranami docelowymi | Porównaj 'Wydatek' (Główna) z 'Transakcja' (Finanse), 'Randka' z 'Randki' | Ta sama nazwa tej samej czynności w całej aplikacji | P2 | ❌ Niezaliczony | 'Wydatek' vs 'Transakcja' — dwie nazwy jednej akcji |
| A-021 | Szybka akcja Migawka nie dubluje nawigacji | Porównaj szybkie akcje z dolnym paskiem | Szybkie akcje uzupełniają pasek, a nie powtarzają go | P3 | ❌ Niezaliczony | 'Migawka' jest i w szybkich akcjach, i w pasku; 'Zakupy' tylko w szybkich akcjach |
| A-022 | Przejście z karty Finanse do modułu | Dotknij karty 'Finanse' | Otwiera się portfel, którego dotyczy kwota | P1 | ⛔ Zablokowany | Karta nie jest linkiem w makiecie |
| A-023 | Przejście z karty randki do szczegółów | Dotknij 'Kolacja u Kate' | Szczegóły randki z adresem i godziną | P2 | ⛔ Zablokowany | Karta nie jest linkiem; brak ekranu Randki |

### Nawigacja

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-030 | Spójne nazwy pozycji telefon ↔ desktop | Porównaj pasek telefonu z menu desktopu | Te same nazwy tych samych miejsc | P3 | ❌ Niezaliczony | 'Główna' (telefon) vs 'Strona główna' (desktop) |
| A-031 | Dostęp do wszystkich modułów na telefonie | Szukaj na telefonie: Lista życzeń, Słoik wspomnień, Mapa, Ustawienia | Każdy moduł osiągalny w ≤ 2 dotknięciach | P1 | ⛔ Zablokowany | Ukryte pod 'Więcej', którego ekran nie istnieje |
| A-032 | Ten sam zestaw informacji o osobach w nagłówku | Porównaj awatary w nagłówku telefonu (M, A) i desktopu (A) | Spójny nagłówek na obu urządzeniach | P3 | ❌ Niezaliczony | Telefon: M i A; desktop: tylko A |
| A-033 | Powrót z każdego ekranu | Wejdź głęboko (portfel → transakcja) i wróć gestem/przyciskiem | Powrót do poprzedniego miejsca z zachowanym filtrem | P2 | ⛔ Zablokowany | Brak ekranów szczegółów |

### Finanse

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-040 | Salda rozliczeń sumują się do zera | Ty +1 416,31 zł, Marlenka −1 416,31 zł | Suma = 0 | P1 | ✅ Zaliczony | +1 416,31 − 1 416,31 = 0 |
| A-041 | Zdanie rozliczenia zgodne z saldami | 'Marlenka oddaje Tobie 1 416,31 zł' vs salda | Kierunek i kwota zgodne | P1 | ✅ Zaliczony | Ty na plusie, Marlenka na minusie, kwota równa |
| A-042 | 'Wspólne - razem' = suma portfeli | −13 165,83 (Sycylia) + 0,00 (Mieszkanie) | −13 165,83 zł | P2 | ✅ Zaliczony | Zgadza się |
| A-043 | Waluta transakcji vs waluta portfela | Historia w € (−57,00 €), saldo portfela w zł | Widoczny kurs i równowartość w zł przy każdej transakcji w obcej walucie | P1 | ❌ Niezaliczony | Brak kursu i przeliczenia — nie da się sprawdzić, jak € wpływa na saldo w zł |
| A-044 | Saldo portfela da się odtworzyć z historii | Zsumuj pełną historię portfela 'Sycylia 26'' | Suma = −13 165,83 zł | P1 | ⛔ Zablokowany | Widać tylko 6 pozycji; 'Wszystkie' nie prowadzi nigdzie |
| A-045 | Znaczenie ujemnego salda portfela | Zapytaj: co znaczy −13 165,83 zł przy portfelu podróży? | Jednoznaczne: 'wydaliście razem 13 165,83 zł' | P1 | ❌ Niezaliczony | Saldo przedstawione czerwonym minusem jak dług; dla budżetu podróży to suma wydatków — mylące |
| A-046 | Poprawny zapis roku w nazwie | Nazwa portfela 'Sycylia 26'' | 'Sycylia '26' lub 'Sycylia 2026' | P3 | ❌ Niezaliczony | Apostrof po cyfrach zamiast przed nimi (we wszystkich 12 ekranach finansów) |
| A-047 | Rodzaj transakcji zgodny z opisem | 'Oddałem za kolację Kate' — oznaczone 'dzielone', −57,00 € | 'Oddałem' (zwrot) jest rozliczeniem, nie wspólnym wydatkiem — albo opis zmieniony | P2 | ❌ Niezaliczony | Opis sugeruje zwrot pieniędzy, typ 'dzielone' sugeruje wspólny wydatek |
| A-048 | Kierunek rozliczenia w historii | 'Rozliczenie - Marlenka 1 150,00 zł · nie jest wydatkiem' | Widać, kto komu zapłacił (np. 'Marlenka → Ty') | P1 | ❌ Niezaliczony | Kwota bez znaku i bez kierunku |
| A-049 | Sposób podziału wydatku | Pozycja z etykietą 'dzielone' | Widać proporcję (50/50, 70/30, kwotowo) i kto płacił | P2 | ❌ Niezaliczony | 'dzielone' nie mówi kto zapłacił ani w jakiej proporcji |
| A-050 | Filtry historii spójne między ekranami | Desktop: Wszystko/Wydatki/Rozliczenia; Język i elementy: Wszystko/Wydatki/Przychody | Jeden zestaw filtrów | P3 | ❌ Niezaliczony | Dwa różne zestawy |
| A-051 | Jedna akcja 'Rozlicz' na ekranie | Desktop: policz przyciski 'Rozlicz' | Jeden przycisk albo dwa o różnych nazwach i celach | P3 | ❌ Niezaliczony | Dwa identyczne 'Rozlicz' (nagłówek portfela i karta Rozliczenia) |
| A-052 | Inwestycje w kontekście portfela | Desktop, wybrany portfel 'Sycylia 26'' | Moduł inwestycji poza portfelem podróży (np. w Osobiste) | P2 | ❌ Niezaliczony | Pusty stan 'Dodaj inwestycję' wyświetlony przy portfelu wyjazdowym |
| A-053 | Parytet telefon ↔ desktop | Porównaj elementy Finansów na obu urządzeniach | Te same funkcje dostępne na telefonie (choćby głębiej) | P2 | ❌ Niezaliczony | Tylko desktop: lista portfeli, Nowy portfel, filtry historii, inwestycje |
| A-054 | Widoczny wybór Osobiste/Wspólne | Spójrz, która zakładka jest aktywna, w każdym kierunku i motywie | Aktywna zakładka wyraźnie odróżniona | P1 | ❌ Niezaliczony | Miękki natywny i Minimalistyczny: kontrast aktywnej zakładki do tła 1,08–1,21:1 (prawie niewidoczna) |
| A-055 | Główna akcja nie wygląda jak błąd | Porównaj kolor 'Transakcja' z kolorem kwot ujemnych | Kolor akcji wyraźnie inny niż kolor 'minus' | P2 | ❌ Niezaliczony | Domyślne akcenty to odcienie czerwieni: ΔE do koloru minus 7,9 (editorial) – 37,5; przy niebieskim/zielonym/fioletowym 62–125 |
| A-056 | Pole kwoty z klawiaturą numeryczną | Element 'Kwota' w Języku i elementach | inputmode='decimal' i waluta przy polu | P2 | ❌ Niezaliczony | Pole bez type/inputmode i bez waluty |
| A-060 | Dodanie wspólnego wydatku 50/50 | Transakcja → 100 zł, płaci Antoś, podział równo → Zapisz | Antoś +50 zł, Marlenka −50 zł; pozycja w historii obu osób | P1 | ⛔ Zablokowany | Brak formularza transakcji |
| A-061 | Dodanie wydatku z nierównym podziałem | 100 zł, podział 70/30 | Salda 70/30 zgodne z wyborem | P1 | ⛔ Zablokowany | Brak formularza |
| A-062 | Wydatek w obcej walucie | 57 € w portfelu w zł | Kurs z dnia transakcji zapisany; saldo w zł przeliczone | P1 | ⛔ Zablokowany | Brak formularza |
| A-063 | Kwota z przecinkiem i kropką | Wpisz '57,5' i '57.5' | Obie formy akceptowane jako 57,50 | P1 | ⛔ Zablokowany | Brak formularza |
| A-064 | Kwota zero / ujemna / pusta | Wpisz 0, −5, puste → Zapisz | Walidacja z komunikatem po polsku | P1 | ⛔ Zablokowany | Brak formularza |
| A-065 | Bardzo duża kwota | Wpisz 1 000 000,00 | Kwota mieści się w polu, liście i nagłówku bez łamania | P2 | ⛔ Zablokowany | Brak formularza (patrz TC-B-023: już −13 165,83 łamie się na desktopie) |
| A-066 | Edycja transakcji przez drugą osobę | Marlenka edytuje wydatek Antosia | Zmiana widoczna u obojga z informacją kto i kiedy zmienił | P1 | ⛔ Zablokowany | Brak edycji |
| A-067 | Usunięcie transakcji z potwierdzeniem i cofnięciem | Usuń → potwierdź → Cofnij | Salda wracają; dostępne 'Cofnij' | P1 | ⛔ Zablokowany | Brak edycji |
| A-068 | Przelew między osobami | Przelew → Marlenka → Ty 200 zł | Saldo rozliczeń zmniejsza się o 200 zł; pozycja 'nie jest wydatkiem' | P1 | ⛔ Zablokowany | Brak przepływu |
| A-069 | Rozliczenie całości | Rozlicz → potwierdź | Salda = 0; pozycja rozliczenia z kierunkiem i kwotą | P1 | ⛔ Zablokowany | Brak przepływu |
| A-070 | Rozliczenie częściowe | Rozlicz → zmień kwotę na 500 zł | Pozostaje 916,31 zł do oddania | P2 | ⛔ Zablokowany | Brak przepływu |
| A-071 | Nowy portfel wspólny | Nowy portfel → 'Mieszkanie' → waluta PLN | Portfel na liście u obu osób | P2 | ⛔ Zablokowany | Przycisk bez akcji |
| A-072 | Archiwizacja zakończonego portfela | Portfel 'Sycylia' po wyjeździe → Archiwizuj | Znika z listy, dostępny w archiwum, salda zachowane | P3 | ⛔ Zablokowany | Brak funkcji |
| A-073 | Prywatność finansów osobistych | Antoś dodaje wydatek w 'Osobiste' | Marlenka go nie widzi | P1 | ⛔ Zablokowany | Brak logiki widoczności |
| A-074 | Wyszukiwanie transakcji | Szukaj → 'sushi' | Wynik 'Sushi 21.09' | P2 | ⛔ Zablokowany | Przycisk 'Szukaj' bez akcji |
| A-075 | Filtr historii 'Wydatki' | Desktop → Wydatki | Znika 'Rozliczenie - Marlenka' | P2 | ⛔ Zablokowany | Chipy bez akcji |
| A-076 | Pełna historia 'Wszystkie' | Telefon → Historia → Wszystkie | Lista z paginacją/datami grupowanymi | P2 | ⛔ Zablokowany | Link '#' |
| A-077 | Eksport historii (CSV) | Portfel → Eksportuj | Plik CSV z kwotami, walutą, kursami | P3 | ⛔ Zablokowany | Brak funkcji |
| A-078 | Dodanie inwestycji | Dodaj inwestycję → nazwa, kwota, data | Wykres wartości w czasie | P3 | ⛔ Zablokowany | Przycisk bez akcji |
| A-079 | Kategoria i ikona transakcji | Dodaj wydatek 'Szama na lotnisku' | Kategoria wybierana przez użytkownika; ikona zgodna z kategorią | P3 | ⛔ Zablokowany | Brak formularza; w makiecie jedzenie na lotnisku ma ikonę samolotu |

### Migawka

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-090 | Zrobienie dzisiejszej migawki | Migawka → aparat → zdjęcie → Wyślij | Zdjęcie widoczne u obu osób; seria +1 gdy obie zrobią | P1 | ⛔ Zablokowany | Brak ekranu Migawki |
| A-091 | Odmowa dostępu do aparatu | Odmów uprawnień | Wyjaśnienie i link do ustawień systemu | P2 | ⛔ Zablokowany | Brak ekranu |
| A-092 | Utrata serii | Jedna osoba nie robi migawki do północy | Jasny komunikat, zasada serii opisana z góry | P2 | ⛔ Zablokowany | Brak reguł serii w makiecie |
| A-093 | Strefy czasowe w podróży | Osoby w różnych strefach czasowych | Seria liczona wg jasnej reguły (np. strefa pary) | P3 | ⛔ Zablokowany | Brak reguł |
| A-094 | Przegląd archiwum migawek | Migawka → kalendarz/siatka | Przegląd po dniach, oba zdjęcia obok siebie | P3 | ⛔ Zablokowany | Brak ekranu |
| A-095 | Usunięcie własnego zdjęcia | Migawka → zdjęcie → Usuń | Usunięte u obu osób; seria bez zmian lub jasna reguła | P2 | ⛔ Zablokowany | Brak ekranu |

### Randki

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-100 | Zaproponowanie randki | Randka → tytuł, data, miejsce → Zaproponuj | Partner dostaje propozycję do zatwierdzenia | P1 | ⛔ Zablokowany | Brak ekranu Randek |
| A-101 | Zatwierdzenie / odrzucenie propozycji | Partner: Zatwierdź / Odrzuć | Status widoczny u obojga | P1 | ⛔ Zablokowany | Brak ekranu |
| A-102 | Przypomnienie przed randką | Randka za 2 h | Powiadomienie z godziną i miejscem | P2 | ⛔ Zablokowany | Brak ekranu |
| A-103 | Ocena randki po fakcie → Słoik wspomnień | Po randce → Oceń → dodaj zdjęcie | Wspomnienie w Słoiku | P3 | ⛔ Zablokowany | Brak ekranu |
| A-104 | Dodanie do kalendarza systemowego | Randka → Dodaj do kalendarza | Wydarzenie w kalendarzu telefonu | P3 | ⛔ Zablokowany | Brak ekranu |
| A-105 | Data w przeszłości | Zaproponuj randkę na wczoraj | Walidacja lub zapis jako wspomnienie | P3 | ⛔ Zablokowany | Brak formularza |

### Zakupy

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-110 | Dodanie produktu do wspólnej listy | Zakupy → 'mleko' → Dodaj | Pozycja u obu osób w < 2 s | P1 | ⛔ Zablokowany | Brak ekranu Zakupów |
| A-111 | Odhaczenie produktu w sklepie | Dotknij 'mleko' | Przekreślone u obu; łatwe cofnięcie | P1 | ⛔ Zablokowany | Brak ekranu |
| A-112 | Jednoczesna edycja przez dwie osoby | Obie osoby dodają produkty w tej samej chwili | Brak utraty pozycji | P1 | ⛔ Zablokowany | Brak ekranu |
| A-113 | Zakupy → wydatek | Zakończ zakupy → Dodaj jako wydatek | Formularz transakcji z kwotą do uzupełnienia | P3 | ⛔ Zablokowany | Brak ekranu |
| A-114 | Duplikat produktu | Dodaj 'mleko' drugi raz | Podpowiedź o istniejącej pozycji | P3 | ⛔ Zablokowany | Brak ekranu |

### Lista życzeń

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-120 | Dodanie życzenia z linkiem | Lista życzeń → wklej link | Pozycja z miniaturą i ceną | P3 | ⛔ Zablokowany | Brak ekranu |
| A-121 | Ukrycie prezentu przed partnerem | Zarezerwuj życzenie partnera | Partner nie widzi rezerwacji | P2 | ⛔ Zablokowany | Brak ekranu |

### Słoik wspomnień

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-122 | Dodanie wspomnienia | Słoik → Dodaj → tekst + zdjęcie | Wspomnienie widoczne u obu | P3 | ⛔ Zablokowany | Brak ekranu |
| A-123 | Losowanie wspomnienia | Słoik → Losuj | Pokazuje losowe wspomnienie | P3 | ⛔ Zablokowany | Brak ekranu |

### Mapa

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-124 | Miejsca pary na mapie | Mapa | Pinezki randek/wspomnień | P3 | ⛔ Zablokowany | Brak ekranu |
| A-125 | Brak zgody na lokalizację | Odmów lokalizacji | Mapa działa bez pozycji użytkownika | P3 | ⛔ Zablokowany | Brak ekranu |

### Ustawienia

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-130 | Motyw jasny/ciemny/systemowy | Ustawienia → Motyw → Systemowy; przełącz tryb telefonu | Aplikacja podąża za systemem | P2 | ⛔ Zablokowany | Motyw to tylko suwak kanwy; brak ustawienia w aplikacji |
| A-131 | Wybór akcentu nie psuje czytelności | Wybierz każdy z 4 akcentów w każdym motywie | Wszystkie teksty czytelne (WCAG AA) | P1 | ❌ Niezaliczony | Pełny wynik w TC-B-001/002: w 29 z 32 kombinacji (kierunek×motyw×akcent) co najmniej jeden ekran nie spełnia kontrastu; bez błędów tylko Ciepły editorial jasny z zielonym, fioletowym i niebieskim akcentem |
| A-132 | Wylogowanie | Ustawienia → Wyloguj | Powrót do logowania, dane usunięte z urządzenia | P1 | ⛔ Zablokowany | Brak ekranu |
| A-133 | Usunięcie konta i eksport danych (RODO) | Ustawienia → Prywatność → Usuń konto / Pobierz dane | Dane do pobrania; usunięcie z potwierdzeniem i skutkami dla partnera | P1 | ⛔ Zablokowany | Brak ekranu |
| A-134 | Zmiana imienia/zdrobnienia | Ustawienia → Profil → imię 'Antoni' | Zmiana widoczna w powitaniu, rozliczeniach, awatarach | P3 | ⛔ Zablokowany | Brak ekranu |

### Powiadomienia

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-140 | Powiadomienie o nowym wydatku partnera | Marlenka dodaje wydatek | Antoś dostaje powiadomienie z kwotą | P2 | ⛔ Zablokowany | Brak logiki |
| A-141 | Lista powiadomień i oznaczanie przeczytanych | Dzwonek → lista → otwórz | Kropka znika po przeczytaniu | P2 | ⛔ Zablokowany | Przycisk bez akcji |
| A-142 | Wyciszenie kategorii | Ustawienia → Powiadomienia → wyłącz Finanse | Brak powiadomień z Finansów | P3 | ⛔ Zablokowany | Brak ekranu |

### Synchronizacja

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-150 | Dodanie wydatku offline | Tryb samolotowy → dodaj wydatek → włącz sieć | Wydatek zsynchronizowany, bez duplikatu | P1 | ⛔ Zablokowany | Brak logiki |
| A-151 | Konflikt edycji tej samej transakcji | Obie osoby edytują tę samą pozycję offline | Jasna reguła rozwiązania i informacja | P2 | ⛔ Zablokowany | Brak logiki |

### Bezpieczeństwo

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-152 | Blokada aplikacji biometrią | Włącz Face ID → zamknij → otwórz | Wymagana biometria przed pokazaniem finansów | P2 | ⛔ Zablokowany | Brak logiki |
| A-153 | Podgląd w przełączniku aplikacji | Otwórz Finanse → przełącz aplikację | Kwoty zamazane w podglądzie systemu | P3 | ⛔ Zablokowany | Brak logiki |

### Dostępność

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-160 | Dodanie wydatku tylko czytnikiem ekranu | VoiceOver/TalkBack: od Głównej do zapisania wydatku | Każdy krok ogłoszony, stan zakładek i przycisków odczytany | P1 | ⛔ Zablokowany | Brak przepływu; elementy statyczne: patrz TC-B-011/012/013 |
| A-161 | Duży tekst systemowy w działającej aplikacji | Ustaw największy rozmiar tekstu w systemie | Treść przewija się, nic nie jest ucięte | P1 | ⛔ Zablokowany | Makieta ma stałą wysokość i overflow:hidden (patrz TC-B-032/033) |
| A-162 | Redukcja ruchu | Włącz 'Ogranicz ruch' | Brak animacji paralaksy/sprężyn | P3 | ⛔ Zablokowany | Brak animacji do oceny |

### Język

| ID | Scenariusz | Kroki | Oczekiwany wynik | Prio | Status na prototypie | Wynik / dowód |
|---|---|---|---|---|---|---|
| A-170 | Polskie znaki w fontach — Ciepły editorial | Sprawdź ą ę ś ć ż ł ń w nagłówkach i kwotach | Wszystkie znaki z tego samego fontu, bez zastępczych | P2 | ✅ Zaliczony | 'Cześć, Antoś', 'Słoik wspomnień', 'zł' poprawne w Instrument Serif i DM Sans |
| A-171 | Polskie znaki w fontach — Miękki natywny | j.w. | j.w. | P2 | ✅ Zaliczony | Poprawne w Geist |
| A-172 | Polskie znaki w fontach — Żywy i zabawny | j.w. | j.w. | P2 | ✅ Zaliczony | Poprawne w Bricolage Grotesque |
| A-173 | Polskie znaki w fontach — Minimalistyczny | j.w. | j.w. | P2 | ✅ Zaliczony | Poprawne w Geist i Geist Mono |
| A-174 | Treść w perspektywie drugiej osoby | Teksty systemowe ('Marlenka oddaje Tobie', 'Ty') | Formy niezależne od płci odbiorcy | P2 | ✅ Zaliczony | Teksty systemowe neutralne; rodzaj pojawia się tylko w opisie wpisanym przez użytkownika ('Oddałem') |
| A-175 | Rejestr językowy spójny | Porównaj 'Szama na lotnisku' i 'Planujcie wyjścia, zatwierdzajcie propozycje' | Potoczny język użytkownika w danych, spójny ton w interfejsie | P3 | ✅ Zaliczony | Potoczne są tylko dane przykładowe; teksty interfejsu spójne |
| A-176 | Format kwot zgodny z polskim zapisem | Sprawdź separator tysięcy i dziesiętny | Spacja nierozdzielająca jako separator tysięcy, przecinek dziesiętny | P2 | ❌ Niezaliczony | Przecinek OK, ale separator tysięcy to zwykła spacja — kwoty łamią się między wierszami (TC-B-023) |
| A-177 | Nagłówek streak mieści się w jednej linii | Karta 'Migawka dziś' w każdym kierunku | '62 dni z rzędu' w jednej linii | P3 | ❌ Niezaliczony | Łamie się na 2 linie w Miękkim natywnym, Żywym i Minimalistycznym (przy 3-cyfrowej serii będzie gorzej) |
| A-178 | Liczba mnoga dni | Seria 1, 2, 5, 22 dni | '1 dzień', '2 dni', '5 dni', '22 dni' | P3 | ⛔ Zablokowany | Wartość statyczna w makiecie |
