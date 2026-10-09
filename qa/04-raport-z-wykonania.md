# 4. Raport z wykonania testów

**Obiekt testu:** kanwa *„marlik - kierunki wizualne”* (wersja z 24.09.2026), 16 ekranów, 4 kierunki, 128 wariantów kolorystycznych.
**Data wykonania:** 09.10.2026. **Środowisko:** Chromium 1194 (Playwright 1.56), fonty z Google Fonts wczytane lokalnie w wersjach wskazanych przez kanwę, szerokości 390 px (telefon), 1280 px (desktop), 900 px (język wizualny) + przypadki responsywności.
**Wykonawca:** Claude (AI) — patrz ograniczenia w [02-metodologia.md, M-10](02-metodologia.md#m-10-krytyka-metodologii-tych-testów-i-samego-zlecenia).

## Podsumowanie liczbowe

| | Wykonania | ✅ Zaliczone | ❌ Niezaliczone | Nie dotyczy | ⛔ Zablokowane (niewykonane) |
|---|---:|---:|---:|---:|---:|
| Katalog A — scenariusze użytkownika | 37 | 11 | 26 | — | 72 |
| Katalog B — interfejs, dostępność, układ | 1 032 | 566 | 354 | 112 | — |
| Katalog C — przegląd wizualny | 32 | 2 | 30 | — | — |
| **Razem** | **1 101** | **579** | **410** | **112** | **72** |

- **1 101 wykonań, w tym 989 z werdyktem** (zaliczony/niezaliczony). „Nie dotyczy” to wykonania, w których na danym ekranie nie było sprawdzanego elementu (np. pola formularza poza ekranem „Język i elementy”).
- **72 scenariusze zablokowane nie są liczone jako wykonane** — czekają na prototyp klikalny lub kod.
- **410 niezaliczeń = 38 unikalnych defektów** (11 o wysokiej ważności, 15 średniej, 12 niskiej). Liczba niezaliczeń jest wysoka, bo ten sam defekt występuje na wielu ekranach i wariantach — miarą jakości jest lista defektów poniżej, nie liczba wykonań.

---

## Unikalne defekty

Ważność: **Wysoka** — wpływa na zrozumienie pieniędzy, prywatność, dostępność dla części osób lub blokuje zadanie; **Średnia** — utrudnia; **Niska** — dopracowanie.

| ID | Defekt | Ważność | Gdzie | Dowód | User story |
|---|---|---|---|---|---|
| D-01 | Biały tekst na tle akcentu poniżej 4,5:1 (przycisk „Transakcja”/„Zapisz”, aktywna zakładka/chip) — 2,83:1 (Żywy), 3,4:1 (Natywny), 3,68:1 (Minimalistyczny) | Wysoka | Natywny, Żywy, Minimalistyczny — wszystkie akcenty | TC-B-002 | US-15 |
| D-02 | Akcent jako kolor tekstu (link „Wszystkie”, aktywna pozycja paska) poniżej 4,5:1 — np. 3,77:1 w Ciepłym ciemnym, 2,83:1 w Żywym jasnym | Średnia | Wszystkie kierunki, zwłaszcza motyw ciemny | TC-B-002 | US-15 |
| D-03 | Tekst drugorzędny na kolorowych wypełnieniach poniżej 4,5:1 — menu boczne 4,35:1, „Migawka dziś” 3,8–3,9:1 (Natywny), nieaktywna zakładka 4,31:1 (Minimalistyczny), kafel Finanse 4,48:1 (Żywy) | Średnia | Motyw jasny: Natywny, Żywy, Minimalistyczny | TC-B-001 | US-15 |
| D-04 | Kolory kwot „plus”/„minus” za jasne na jasnym tle — minus 4,13:1 i plus 3,45:1 (Natywny), minus 3,54:1 i plus 3,39:1 (Żywy) | Wysoka | Motyw jasny: Natywny, Żywy | TC-B-001 | US-15 |
| D-05 | Kwota zaznaczonego portfela szara na pomarańczowym (2,1:1) | Średnia | Żywy, desktop | TC-B-002, C-21 | US-15 |
| D-06 | Pole „Kwota” bez widocznego obrysu (1,15:1 i 1,2:1) | Średnia | Natywny, Minimalistyczny | TC-B-003 | US-06 |
| D-07 | Przyciski drugorzędne słabo odcinają się od tła (1,07–1,5:1; heurystyka) | Niska | Ciepły, Natywny, Minimalistyczny | TC-B-006 | — |
| D-08 | Cele dotykowe za małe: zakładki 36 px wysokości, link „Wszystkie” 65×17 px | Średnia | Finanse — telefon, wszystkie kierunki | TC-B-010 | US-18 |
| D-09 | Przełącznik Osobiste/Wspólne bez semantyki stanu (`aria-pressed`/`aria-selected`) | Średnia | 12/12 ekranów z przełącznikiem | TC-B-012 | US-05 |
| D-10 | Aktywna pozycja nawigacji oznaczona tylko kolorem, bez `aria-current` | Średnia | 12/12 ekranów z nawigacją | TC-B-013 | US-19 |
| D-11 | Prototyp bez przejść — wszystkie linki `#`, przyciski bez akcji | Wysoka | 12/16 ekranów | TC-B-016 | M-06 |
| D-12 | Sekcja „Ilustracje” ucięta dolną krawędzią ramki | Niska | 4/4 ekrany „Język i elementy” | TC-B-017, C-07 | US-20 |
| D-13 | Karta inwestycji wychodzi poza ekran (przycisk niewidoczny) | Średnia | Minimalistyczny, desktop | TC-B-017, C-29 | US-20 |
| D-14 | Teksty 11 px (etykiety sekcji, podpisy paska nawigacji) | Średnia | 12/16 ekranów | TC-B-020 | US-17 |
| D-15 | Kwoty łamane między wierszami (`1` / `416 zł`; `-13` / `165,83` / `zł`) — zwykła spacja zamiast nierozdzielającej | Wysoka | Główna ×4, desktop Finanse ×3 | TC-B-023, A-176 | US-02 |
| D-16 | Brak zapasu na większy tekst: przy 130% treść chowa się pod paskiem (8/8 ekranów telefonu), przy 200% 11–19 problemów na ekran; stała wysokość i `overflow: hidden` | Wysoka | Wszystkie ekrany telefonu | TC-B-032, TC-B-033 | US-17 |
| D-17 | Nazwy transakcji ucinane wielokropkiem przy 360/320 px | Niska | Finanse — telefon | TC-B-030, TC-B-031 | US-17 |
| D-18 | Desktop o sztywnej szerokości 1280 px (scroll przy 1024 px, pusty pas przy 1440 px) | Średnia | 4/4 ekrany desktopowe | TC-B-034, TC-B-035 | US-20 |
| D-19 | Dzień tygodnia randki niezgodny z datą („sob 27.09” — w 2026 to niedziela) | Średnia | Główna ×4 | A-012 | US-10 |
| D-20 | Saldo na Głównej obcięte zamiast zaokrąglone (−13 165,83 → −13 165) | Niska | Główna ×4 | A-013 | US-01 |
| D-21 | Suma wydatków wyjazdu pokazana czerwonym minusem jak dług; karta Finanse bez nazwy portfela i znaczenia kwoty | Wysoka | Główna, Finanse — wszystkie | A-015, A-045 | US-01 |
| D-22 | Brak stanu dzisiejszej migawki obu osób (chipy „Ty”/„Marlenka” identyczne) | Wysoka | Główna ×4 | A-016 | US-08 |
| D-23 | Kafle M/Razem/A bez funkcji i podpisu; dublują awatary z nagłówka | Średnia | Główna ×4 | A-018, C-01 | US-09 |
| D-24 | Powiadomienia: kropka bez liczby, etykieta bez informacji o nowych | Niska | Główna, desktop | A-019 | US-11 |
| D-25 | Różne nazwy tej samej rzeczy: „Wydatek”/„Transakcja”, „Główna”/„Strona główna”, dwa zestawy filtrów, dwa „Rozlicz” na ekranie, różne awatary w nagłówku | Średnia | Wszystkie kierunki | A-020, A-030, A-032, A-050, A-051 | US-12 |
| D-26 | Szybkie akcje dublują pasek (Migawka), a Zakupy są tylko w szybkich akcjach | Niska | Główna ×4 | A-021 | US-12 |
| D-27 | Wydatki w € w portfelu w zł bez kursu i przeliczenia | Wysoka | Finanse — wszystkie | A-043 | US-03 |
| D-28 | Błędny zapis roku „Sycylia 26'” (powinno być „’26”) | Niska | Finanse ×12 | A-046 | — |
| D-29 | Historia nie mówi, kto płacił i jak podzielono; rozliczenie bez kierunku; „Oddałem…” oznaczone jako wspólny wydatek | Wysoka | Finanse — wszystkie | A-047, A-048, A-049 | US-04 |
| D-30 | Pusty stan inwestycji przy portfelu wyjazdowym | Niska | Desktop ×4 | A-052 | US-07 |
| D-31 | Funkcje tylko na desktopie (portfele, nowy portfel, filtry, inwestycje); brak ekranu „Więcej” na telefonie | Wysoka | Telefon vs desktop | A-053, A-031 | US-13 |
| D-32 | Aktywna zakładka Osobiste/Wspólne prawie niewidoczna (1,08–1,21:1 do toru) | Wysoka | Natywny, Minimalistyczny (oba motywy) | A-054, C-11, C-12, C-27, C-28 | US-05 |
| D-33 | Domyślny akcent prawie w kolorze „minus” (ΔE 7,9–37,5) — akcja wygląda jak błąd | Średnia | Wszystkie kierunki (domyślne akcenty) | A-055, C-07 | US-16 |
| D-34 | Pole kwoty bez `inputmode="decimal"` i bez waluty | Średnia | Język i elementy ×4 | A-056 | US-06 |
| D-35 | „62 dni z rzędu” łamie się na dwie linie | Niska | Natywny, Żywy, Minimalistyczny | A-177, C-09, C-17, C-25 | — |
| D-36 | Desktop: nieużyta lewa kolumna pod listą portfeli; etykieta „… · 2 OSOBY” przeskakuje do drugiej linii | Niska | Desktop ×4 | C-05, C-13 | US-20 |
| D-37 | W ciemnym motywie kafle M/A ledwo odcinają się od tła | Niska | Ciepły ciemny | C-02 | US-09 |
| D-38 | Font monospace także w słowach („62 dni z rzędu”), nie tylko w liczbach | Niska | Minimalistyczny | C-25 | — |

---

## Wyniki katalogu B według przypadków

| ID | Przypadek | Wykonania | ✅ | ❌ | Nie dotyczy |
|---|---|---:|---:|---:|---:|
| TC-B-001 | Kontrast tekstów na neutralnym tle | 128 | 84 | 44 | 0 |
| TC-B-002 | Kontrast tekstów w/na akcencie | 128 | 25 | 103 | 0 |
| TC-B-003 | Obrys pola formularza | 128 | 16 | 16 | 96 |
| TC-B-004 | Kwoty nie tylko kolorem | 128 | 128 | 0 | 0 |
| TC-B-005 | Kontrast ikon w przyciskach | 128 | 128 | 0 | 0 |
| TC-B-006 | Przycisk odcina się od tła (heurystyka) | 128 | 32 | 96 | 0 |
| TC-B-010 | Cele dotykowe | 16 | 12 | 4 | 0 |
| TC-B-011 | Nazwa dostępna kontrolek | 16 | 16 | 0 | 0 |
| TC-B-012 | Stan przełącznika segmentowego | 16 | 0 | 12 | 4 |
| TC-B-013 | Aktywna pozycja nawigacji | 16 | 0 | 12 | 4 |
| TC-B-014 | Struktura nagłówków | 16 | 16 | 0 | 0 |
| TC-B-015 | Język strony | 16 | 16 | 0 | 0 |
| TC-B-016 | Przejścia i akcje prototypu | 16 | 4 | 12 | 0 |
| TC-B-017 | Treść w ramce ekranu | 16 | 11 | 5 | 0 |
| TC-B-018 | Treść nad dolnym paskiem | 16 | 8 | 0 | 8 |
| TC-B-019 | Brak ucięć wielokropkiem | 16 | 16 | 0 | 0 |
| TC-B-020 | Tekst ≥ 12 px | 16 | 4 | 12 | 0 |
| TC-B-021 | Render bez błędów | 16 | 16 | 0 | 0 |
| TC-B-022 | Klawiatura i fokus | 16 | 16 | 0 | 0 |
| TC-B-023 | Kwota w jednym wierszu | 16 | 9 | 7 | 0 |
| TC-B-030 | Szerokość 360 px | 8 | 5 | 3 | 0 |
| TC-B-031 | Szerokość 320 px | 8 | 4 | 4 | 0 |
| TC-B-032 | Tekst 130% | 8 | 0 | 8 | 0 |
| TC-B-033 | Tekst 200% | 8 | 0 | 8 | 0 |
| TC-B-034 | Desktop 1024 px | 4 | 0 | 4 | 0 |
| TC-B-035 | Desktop 1440 px | 4 | 0 | 4 | 0 |
| **Razem** | | **1032** | **566** | **354** | **112** |

**Co działa dobrze (zaliczone na wszystkich ekranach):** nazwy dostępne wszystkich kontrolek (TC-B-011), struktura nagłówków (TC-B-014), `lang="pl"` (TC-B-015), render bez błędów (TC-B-021), pełna obsługa klawiaturą z widocznym fokusem (TC-B-022), kontrast ikon w przyciskach (TC-B-005), znak +/− przy każdej barwionej kwocie (TC-B-004), brak treści pod dolnym paskiem przy szerokości projektu (TC-B-018). To dobra baza — semantyka HTML w makietach jest staranna.

---

## Porównanie kierunków

| | Ciepły editorial | Miękki natywny | Żywy i zabawny | Minimalistyczny premium |
|---|---|---|---|---|
| Niezaliczone wykonania B (bez „nie dotyczy”) | **70 / 230 (30,4%)** | 109 / 230 (47,4%) | 69 / 230 (30,0%) | 106 / 230 (46,1%) |
| Akcenty bez żadnego błędu kontrastu (jasny / ciemny) | **3 z 4 / 0 z 4** | 0 / 0 | 0 / 0 | 0 / 0 |
| Kontrast aktywnej zakładki do toru (jasny / ciemny) | **13,81 / 12,96** | 1,21 / 1,14 | 2,11–3,61 / 3,09–5,29 | 1,10 / 1,08 |
| Saldo na desktopie w jednej linii | **tak** | nie (2 linie) | nie (2 linie) | nie (3 linie) |
| Biały tekst na przycisku głównym (domyślny akcent) | **≥ 4,5:1** | 3,4:1 | 2,83:1 | 3,68:1 |
| ΔE domyślnego akcentu od koloru „minus” | 7,9 (prawie ten sam) | 16,6 | 33,2 | 16,5 |
| Ucięta treść | ilustracje | ilustracje | ilustracje | ilustracje + karta inwestycji |

**Wniosek.** Najmniej problemów i jedyne warianty w pełni zgodne z kontrastem AA ma **Ciepły editorial w motywie jasnym z akcentem zielonym (`#3E6B5A`), fioletowym (`#7A4E8C`) lub niebieskim (`#2F5D9E`)**. Żywy i zabawny ma podobny odsetek niezaliczeń, ale jego problemy dotyczą najważniejszych elementów (biały tekst na przycisku głównym 2,83:1 przy każdym akcencie; kwoty plus/minus poniżej progu), a niskie liczby zawdzięcza głównie grubym obrysom, które zaliczają heurystykę TC-B-006. Miękki natywny i Minimalistyczny przegrywają przede wszystkim niewidoczną aktywną zakładką Osobiste/Wspólne, czyli elementem, który decyduje o prywatności finansów.

Zastrzeżenie: to porównanie dostępności i poprawności, a nie atrakcyjności. Wybór stylu powinien uwzględnić test z ludźmi (M-07) — ale na podstawie tych danych Ciepły editorial wymaga najmniej pracy, żeby był zgodny i czytelny. Warunek: zmienić domyślną terakotę na zielony lub niebieski (D-33) i poprawić kolor akcentu jako tekstu w motywie ciemnym (D-02).

### Macierz akcentów (czy wariant przechodzi TC-B-001 i TC-B-002 na wszystkich 4 ekranach kierunku)

| Kierunek | Motyw | Akcent 1 | Akcent 2 | Akcent 3 | Akcent 4 |
|---|---|---|---|---|---|
| Ciepły editorial | jasny | ❌ `#B5532E` | ✅ `#3E6B5A` | ✅ `#7A4E8C` | ✅ `#2F5D9E` |
| Ciepły editorial | ciemny | ❌ `#B5532E` | ❌ `#3E6B5A` | ❌ `#7A4E8C` | ❌ `#2F5D9E` |
| Miękki natywny | jasny | ❌ `#E0673C` | ❌ `#2F7BF6` | ❌ `#8A5CF6` | ❌ `#1FA36B` |
| Miękki natywny | ciemny | ❌ `#E0673C` | ❌ `#2F7BF6` | ❌ `#8A5CF6` | ❌ `#1FA36B` |
| Żywy i zabawny | jasny | ❌ `#FF6B3D` | ❌ `#7C5CFF` | ❌ `#10B981` | ❌ `#F43F7A` |
| Żywy i zabawny | ciemny | ❌ `#FF6B3D` | ❌ `#7C5CFF` | ❌ `#10B981` | ❌ `#F43F7A` |
| Minimalistyczny premium | jasny | ❌ `#E4572E` | ❌ `#3B82F6` | ❌ `#A855F7` | ❌ `#16A34A` |
| Minimalistyczny premium | ciemny | ❌ `#E4572E` | ❌ `#3B82F6` | ❌ `#A855F7` | ❌ `#16A34A` |

W motywie ciemnym błąd prawie zawsze dotyczy akcentu użytego jako kolor tekstu (link, aktywna pozycja menu) — rozwiązaniem jest osobny token `accent-text-on-dark` (US-15), a nie rezygnacja z ciemnego motywu.

---

## Wnioski z wykonania

1. **Treść i struktura to większy problem niż styl.** 22 z 26 niezaliczonych scenariuszy użytkownika powtarza się identycznie w każdym kierunku. Zmiana stylu ich nie naprawi — trzeba poprawić treść ekranów (US-01, 03, 04, 08, 12, 13).
2. **Czytelność jest „dziedziczona” po palecie i jednym wzorze.** 259 z 354 niezaliczeń B to przypadki kolorystyczne (TC-B-001/002/003/006). Wynikają głównie z dwóch decyzji: jednego tokenu akcentu w trzech rolach i nie-WCAG-owego wzoru na kolor tekstu. Poprawka w jednym miejscu (US-15) usunie je na wszystkich ekranach.
3. **Liczby wymagają jednego formatera.** Łamanie kwot, obcięcie salda, zły dzień tygodnia i brak kursu to ten sam problem: wartości wpisywane ręcznie zamiast liczone i formatowane (M-04).
4. **Makieta ma dobrą bazę semantyczną.** Nazwy kontrolek, nagłówki, fokus i język są poprawne — warto zachować ten poziom w kodzie.
5. **Najwięcej wiedzy przyniesie odblokowanie scenariuszy.** 72 zablokowane scenariusze (formularz transakcji, migawka, rozliczenie, parowanie) to obszary o najwyższym ryzyku, których nie da się ocenić na statycznej makiecie (M-06).

---

## Jak powtórzyć testy

```bash
# 1. Pobierz pliki kanwy (project/*.dc.html, canvas.json) i fonty Google Fonts (CSS + woff2) do dowolnego katalogu
# 2. Wyrenderuj 128 wariantów:
node qa/narzedzia/render.mjs <katalog project/> <katalog render/> <fonts/all.css>
# 3. Wykonaj katalog B (wymaga Playwright + Chromium):
node qa/narzedzia/sprawdz.mjs <katalog render/> <katalog wyników/>
# 4. Wygeneruj katalog A do CSV:
python3 -I qa/narzedzia/katalog_a.py qa/wyniki/katalog-A.csv
```

Wykonanie katalogu B trwa ok. 30 s. Skrypt działa także na przyszłych wersjach kanwy — może służyć jako test regresji przy każdej zmianie projektu (M-05).
