# QA marlika — testy end-user prototypu (09.10.2026)

Testy aplikacji marlik z perspektywy użytkownika końcowego (para: Antoś i Marlenka), wykonane na jedynej istniejącej wersji aplikacji — kanwie projektowej *„marlik - kierunki wizualne”* (16 ekranów, 4 kierunki wizualne, motyw jasny/ciemny, 4 akcenty).

## Dokumenty

| Plik | Zawartość |
|---|---|
| [01-wnioski-i-user-stories.md](01-wnioski-i-user-stories.md) | Wnioski i propozycje zmian jako 20 user stories — każda z obserwacją, argumentem, uzasadnioną poprawką i kryteriami akceptacji |
| [02-metodologia.md](02-metodologia.md) | 10 problemów w metodologii pracy (w tym krytyka samych tych testów) — z argumentacją problemu i poprawki |
| [03-przypadki-testowe.md](03-przypadki-testowe.md) | Katalogi przypadków testowych do testów manualnych: A (109 scenariuszy użytkownika), B (26 przypadków UI/dostępności), C (przegląd wizualny) |
| [04-raport-z-wykonania.md](04-raport-z-wykonania.md) | Wyniki: 1 101 wykonań, 38 unikalnych defektów, porównanie kierunków, wnioski |
| [wyniki/](wyniki/) | Surowe wyniki: `katalog-A.csv`, `wyniki-B.csv` / `.json` (1 032 wykonania z dowodami), `katalog-C.csv` |
| [zrzuty/](zrzuty/) | 32 zrzuty ekranów (każdy ekran w jasnym i ciemnym motywie, domyślny akcent), na których wykonano przegląd |
| [narzedzia/](narzedzia/) | Skrypty: render wariantów z kanwy, wykonanie katalogu B, generator katalogu A |

## W skrócie

- **1 101 wykonań** (989 z werdyktem): ✅ 579 · ❌ 410 · nie dotyczy 112. Dodatkowo **72 scenariusze zablokowane** — prototyp nie ma tych funkcji; nie są liczone jako wykonane.
- **38 unikalnych defektów** — 11 o wysokiej ważności. Najważniejsze: kwoty łamane w połowie liczby, czerwony minus dla sumy wydatków wyjazdu, waluta € bez kursu, rozliczenia bez kierunku, brak stanu dzisiejszej migawki, niewidoczna aktywna zakładka Osobiste/Wspólne (2 kierunki), za niski kontrast przy 29 z 32 kombinacji motyw × akcent.
- **Najmniej problemów: Ciepły editorial** — jedyny z wariantami w pełni zgodnymi z kontrastem WCAG AA (motyw jasny, akcent zielony/fioletowy/niebieski). Warunek: zmienić domyślny akcent (terakota jest prawie identyczna z kolorem „minus”).
- **Główny problem metodologii:** projektujemy styl przed treścią i przepływami — 22 z 26 niezaliczonych scenariuszy użytkownika występuje identycznie we wszystkich 4 kierunkach, więc wybór stylu ich nie rozwiąże.

## Ograniczenia

Testy wykonał Claude (AI): katalog B skryptem w Chromium, katalogi A i C przez czytanie treści i oglądanie zrzutów. To nie zastępuje testu z ludźmi ani na fizycznych urządzeniach — szczegóły w [02-metodologia.md, M-10](02-metodologia.md#m-10-krytyka-metodologii-tych-testów-i-samego-zlecenia).

## Powtórzenie testów

Instrukcja w [04-raport-z-wykonania.md](04-raport-z-wykonania.md#jak-powtórzyć-testy). Skrypty działają na każdej kolejnej wersji kanwy, więc mogą służyć jako test regresji.
