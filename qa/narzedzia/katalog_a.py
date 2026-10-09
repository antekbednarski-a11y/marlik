"""Katalog A — scenariusze funkcjonalne użytkownika końcowego (testy manualne).

Każdy wiersz to przypadek testowy pisany pod docelową, działającą aplikację. Kolumna
"status_prototyp" to wynik wykonania na obecnym prototypie (kanwa "marlik - kierunki wizualne"):
  Zaliczony / Niezaliczony  – dało się wykonać na makiecie (treść, dane, spójność),
  Zablokowany               – makieta nie ma tej funkcji / logiki, więc nie da się wykonać.
Zablokowane NIE są liczone jako wykonane.

Użycie: python3 -I katalog_a.py <plik wyjściowy .csv>
"""
import csv
import sys

P1, P2, P3 = "P1", "P2", "P3"
OK, FAIL, BLOCK = "Zaliczony", "Niezaliczony", "Zablokowany"

# (id, moduł, tytuł, kroki, oczekiwany wynik, priorytet, status, wynik / dowód)
CASES = [
    # --- Konto, para, onboarding ---
    ("A-001", "Konto", "Rejestracja nowej osoby", "Otwórz aplikację po raz pierwszy → Załóż konto (e-mail/Apple/Google)", "Konto utworzone, przejście do parowania", P1, BLOCK, "Brak ekranu rejestracji w makiecie"),
    ("A-002", "Konto", "Logowanie istniejącej osoby", "Wyloguj → Zaloguj tymi samymi danymi", "Widok Głównej z danymi pary", P1, BLOCK, "Brak ekranu logowania"),
    ("A-003", "Para", "Zaproszenie partnera kodem/linkiem", "Ustawienia → Zaproś partnera → wyślij link", "Partner po kliknięciu dołącza do pary; obie osoby widzą te same wspólne dane", P1, BLOCK, "Brak przepływu parowania"),
    ("A-004", "Para", "Link zaproszenia wygasa / użyty drugi raz", "Użyj tego samego linku na trzecim koncie", "Komunikat, że para jest pełna; brak dołączenia", P1, BLOCK, "Brak przepływu parowania"),
    ("A-005", "Para", "Rozłączenie pary", "Ustawienia → Rozłącz → potwierdź", "Jasna informacja, co dzieje się ze wspólnymi danymi i rozliczeniami", P2, BLOCK, "Brak ekranu ustawień"),
    ("A-006", "Onboarding", "Pierwsze uruchomienie bez danych (puste stany)", "Nowa para bez historii → Główna, Finanse, Migawka", "Każdy moduł ma pusty stan z jedną jasną akcją", P2, BLOCK, "Makieta pokazuje tylko stan z danymi (poza kartą inwestycji)"),
    ("A-007", "Onboarding", "Zgoda na powiadomienia i aparat", "Pierwsze użycie Migawki", "Systemowe prośby poprzedzone wyjaśnieniem po polsku", P2, BLOCK, "Brak przepływu"),
    # --- Główna ---
    ("A-010", "Główna", "Powitanie zalogowanej osoby", "Zaloguj się jako Antoś, potem jako Marlenka", "Powitanie i perspektywa ('Tobie', 'Ty') zmieniają się zależnie od osoby", P1, BLOCK, "Makieta ma tylko perspektywę Antosia; brak wariantu dla Marlenki"),
    ("A-011", "Główna", "Data w nagłówku zgodna z kalendarzem", "Porównaj 'Czwartek, 24 września' z kalendarzem 2026", "Dzień tygodnia zgodny z datą", P2, OK, "24.09.2026 to czwartek"),
    ("A-012", "Główna", "Termin najbliższej randki zgodny z kalendarzem", "Karta 'Najbliższa randka': 'sob 27.09 · 19:00'", "Skrót dnia tygodnia zgodny z datą", P1, FAIL, "27.09.2026 to niedziela, nie sobota (przy nagłówku 'Czwartek, 24 września')"),
    ("A-013", "Główna", "Kwota z Finansów na Głównej zgodna z Finansami", "Porównaj kartę 'Finanse' (−13 165 zł) z saldem portfela (−13 165,83 zł)", "Ta sama kwota lub poprawnie zaokrąglona", P1, FAIL, "−13 165,83 zaokrąglone to −13 166; makieta ucina do −13 165"),
    ("A-014", "Główna", "Kwota rozliczenia na Głównej zgodna z Finansami", "Porównaj '1 416 zł' z '1 416,31 zł'", "Ta sama kwota lub poprawnie zaokrąglona", P2, OK, "1 416,31 → 1 416 (poprawne zaokrąglenie)"),
    ("A-015", "Główna", "Zrozumienie karty Finanse bez wchodzenia w moduł", "Pokaż Główną osobie spoza projektu i zapytaj: co znaczy czerwone −13 165 zł?", "Osoba wie, czy to dług, wydatki podróży, czy saldo konta", P1, FAIL, "Karta nie mówi, którego portfela dotyczy ani czym jest kwota; czerwony minus obok 'Marlenka oddaje Tobie' (czyli dobrej wiadomości) daje sprzeczny sygnał"),
    ("A-016", "Główna", "Status dzisiejszej migawki obu osób", "Karta 'Migawka dziś' z chipami 'Ty' i 'Marlenka'", "Widać, kto już zrobił dzisiejszą migawkę, a kto nie", P1, FAIL, "Oba chipy wyglądają identycznie — brak stanu zrobione/niezrobione"),
    ("A-017", "Główna", "Seria migawek — ryzyko utraty", "Karta '62 dni z rzędu' wieczorem, gdy jedna osoba nie zrobiła migawki", "Ostrzeżenie o utracie serii i akcja 'Zrób teraz'", P2, BLOCK, "Brak stanu zagrożonej serii"),
    ("A-018", "Główna", "Znaczenie dużych kafli M / Razem / A", "Dotknij każdego kafla; zapytaj użytkownika, czym są", "Jasny cel (np. dzisiejsze migawki) i akcja po dotknięciu", P1, FAIL, "Kafle zajmują ok. 20% ekranu, nie są przyciskami/linkami i nie mają podpisu funkcji; duplikują awatary M/A z nagłówka"),
    ("A-019", "Główna", "Powiadomienia — informacja o liczbie i treści", "Spójrz na dzwonek z kropką; użyj VoiceOver", "Liczba nieprzeczytanych lub tekst 'X nowych' także dla czytnika ekranu", P2, FAIL, "Kropka bez liczby; aria-label 'Powiadomienia' nie mówi o nowych"),
    ("A-020", "Główna", "Nazwy szybkich akcji zgodne z ekranami docelowymi", "Porównaj 'Wydatek' (Główna) z 'Transakcja' (Finanse), 'Randka' z 'Randki'", "Ta sama nazwa tej samej czynności w całej aplikacji", P2, FAIL, "'Wydatek' vs 'Transakcja' — dwie nazwy jednej akcji"),
    ("A-021", "Główna", "Szybka akcja Migawka nie dubluje nawigacji", "Porównaj szybkie akcje z dolnym paskiem", "Szybkie akcje uzupełniają pasek, a nie powtarzają go", P3, FAIL, "'Migawka' jest i w szybkich akcjach, i w pasku; 'Zakupy' tylko w szybkich akcjach"),
    ("A-022", "Główna", "Przejście z karty Finanse do modułu", "Dotknij karty 'Finanse'", "Otwiera się portfel, którego dotyczy kwota", P1, BLOCK, "Karta nie jest linkiem w makiecie"),
    ("A-023", "Główna", "Przejście z karty randki do szczegółów", "Dotknij 'Kolacja u Kate'", "Szczegóły randki z adresem i godziną", P2, BLOCK, "Karta nie jest linkiem; brak ekranu Randki"),
    # --- Nawigacja ---
    ("A-030", "Nawigacja", "Spójne nazwy pozycji telefon ↔ desktop", "Porównaj pasek telefonu z menu desktopu", "Te same nazwy tych samych miejsc", P3, FAIL, "'Główna' (telefon) vs 'Strona główna' (desktop)"),
    ("A-031", "Nawigacja", "Dostęp do wszystkich modułów na telefonie", "Szukaj na telefonie: Lista życzeń, Słoik wspomnień, Mapa, Ustawienia", "Każdy moduł osiągalny w ≤ 2 dotknięciach", P1, BLOCK, "Ukryte pod 'Więcej', którego ekran nie istnieje"),
    ("A-032", "Nawigacja", "Ten sam zestaw informacji o osobach w nagłówku", "Porównaj awatary w nagłówku telefonu (M, A) i desktopu (A)", "Spójny nagłówek na obu urządzeniach", P3, FAIL, "Telefon: M i A; desktop: tylko A"),
    ("A-033", "Nawigacja", "Powrót z każdego ekranu", "Wejdź głęboko (portfel → transakcja) i wróć gestem/przyciskiem", "Powrót do poprzedniego miejsca z zachowanym filtrem", P2, BLOCK, "Brak ekranów szczegółów"),
    # --- Finanse: odczyt i spójność ---
    ("A-040", "Finanse", "Salda rozliczeń sumują się do zera", "Ty +1 416,31 zł, Marlenka −1 416,31 zł", "Suma = 0", P1, OK, "+1 416,31 − 1 416,31 = 0"),
    ("A-041", "Finanse", "Zdanie rozliczenia zgodne z saldami", "'Marlenka oddaje Tobie 1 416,31 zł' vs salda", "Kierunek i kwota zgodne", P1, OK, "Ty na plusie, Marlenka na minusie, kwota równa"),
    ("A-042", "Finanse", "'Wspólne - razem' = suma portfeli", "−13 165,83 (Sycylia) + 0,00 (Mieszkanie)", "−13 165,83 zł", P2, OK, "Zgadza się"),
    ("A-043", "Finanse", "Waluta transakcji vs waluta portfela", "Historia w € (−57,00 €), saldo portfela w zł", "Widoczny kurs i równowartość w zł przy każdej transakcji w obcej walucie", P1, FAIL, "Brak kursu i przeliczenia — nie da się sprawdzić, jak € wpływa na saldo w zł"),
    ("A-044", "Finanse", "Saldo portfela da się odtworzyć z historii", "Zsumuj pełną historię portfela 'Sycylia 26''", "Suma = −13 165,83 zł", P1, BLOCK, "Widać tylko 6 pozycji; 'Wszystkie' nie prowadzi nigdzie"),
    ("A-045", "Finanse", "Znaczenie ujemnego salda portfela", "Zapytaj: co znaczy −13 165,83 zł przy portfelu podróży?", "Jednoznaczne: 'wydaliście razem 13 165,83 zł'", P1, FAIL, "Saldo przedstawione czerwonym minusem jak dług; dla budżetu podróży to suma wydatków — mylące"),
    ("A-046", "Finanse", "Poprawny zapis roku w nazwie", "Nazwa portfela 'Sycylia 26''", "'Sycylia '26' lub 'Sycylia 2026'", P3, FAIL, "Apostrof po cyfrach zamiast przed nimi (we wszystkich 12 ekranach finansów)"),
    ("A-047", "Finanse", "Rodzaj transakcji zgodny z opisem", "'Oddałem za kolację Kate' — oznaczone 'dzielone', −57,00 €", "'Oddałem' (zwrot) jest rozliczeniem, nie wspólnym wydatkiem — albo opis zmieniony", P2, FAIL, "Opis sugeruje zwrot pieniędzy, typ 'dzielone' sugeruje wspólny wydatek"),
    ("A-048", "Finanse", "Kierunek rozliczenia w historii", "'Rozliczenie - Marlenka 1 150,00 zł · nie jest wydatkiem'", "Widać, kto komu zapłacił (np. 'Marlenka → Ty')", P1, FAIL, "Kwota bez znaku i bez kierunku"),
    ("A-049", "Finanse", "Sposób podziału wydatku", "Pozycja z etykietą 'dzielone'", "Widać proporcję (50/50, 70/30, kwotowo) i kto płacił", P2, FAIL, "'dzielone' nie mówi kto zapłacił ani w jakiej proporcji"),
    ("A-050", "Finanse", "Filtry historii spójne między ekranami", "Desktop: Wszystko/Wydatki/Rozliczenia; Język i elementy: Wszystko/Wydatki/Przychody", "Jeden zestaw filtrów", P3, FAIL, "Dwa różne zestawy"),
    ("A-051", "Finanse", "Jedna akcja 'Rozlicz' na ekranie", "Desktop: policz przyciski 'Rozlicz'", "Jeden przycisk albo dwa o różnych nazwach i celach", P3, FAIL, "Dwa identyczne 'Rozlicz' (nagłówek portfela i karta Rozliczenia)"),
    ("A-052", "Finanse", "Inwestycje w kontekście portfela", "Desktop, wybrany portfel 'Sycylia 26''", "Moduł inwestycji poza portfelem podróży (np. w Osobiste)", P2, FAIL, "Pusty stan 'Dodaj inwestycję' wyświetlony przy portfelu wyjazdowym"),
    ("A-053", "Finanse", "Parytet telefon ↔ desktop", "Porównaj elementy Finansów na obu urządzeniach", "Te same funkcje dostępne na telefonie (choćby głębiej)", P2, FAIL, "Tylko desktop: lista portfeli, Nowy portfel, filtry historii, inwestycje"),
    ("A-054", "Finanse", "Widoczny wybór Osobiste/Wspólne", "Spójrz, która zakładka jest aktywna, w każdym kierunku i motywie", "Aktywna zakładka wyraźnie odróżniona", P1, FAIL, "Miękki natywny i Minimalistyczny: kontrast aktywnej zakładki do tła 1,08–1,21:1 (prawie niewidoczna)"),
    ("A-055", "Finanse", "Główna akcja nie wygląda jak błąd", "Porównaj kolor 'Transakcja' z kolorem kwot ujemnych", "Kolor akcji wyraźnie inny niż kolor 'minus'", P2, FAIL, "Domyślne akcenty to odcienie czerwieni: ΔE do koloru minus 7,9 (editorial) – 37,5; przy niebieskim/zielonym/fioletowym 62–125"),
    ("A-056", "Finanse", "Pole kwoty z klawiaturą numeryczną", "Element 'Kwota' w Języku i elementach", "inputmode='decimal' i waluta przy polu", P2, FAIL, "Pole bez type/inputmode i bez waluty"),
    # --- Finanse: operacje (docelowa aplikacja) ---
    ("A-060", "Finanse", "Dodanie wspólnego wydatku 50/50", "Transakcja → 100 zł, płaci Antoś, podział równo → Zapisz", "Antoś +50 zł, Marlenka −50 zł; pozycja w historii obu osób", P1, BLOCK, "Brak formularza transakcji"),
    ("A-061", "Finanse", "Dodanie wydatku z nierównym podziałem", "100 zł, podział 70/30", "Salda 70/30 zgodne z wyborem", P1, BLOCK, "Brak formularza"),
    ("A-062", "Finanse", "Wydatek w obcej walucie", "57 € w portfelu w zł", "Kurs z dnia transakcji zapisany; saldo w zł przeliczone", P1, BLOCK, "Brak formularza"),
    ("A-063", "Finanse", "Kwota z przecinkiem i kropką", "Wpisz '57,5' i '57.5'", "Obie formy akceptowane jako 57,50", P1, BLOCK, "Brak formularza"),
    ("A-064", "Finanse", "Kwota zero / ujemna / pusta", "Wpisz 0, −5, puste → Zapisz", "Walidacja z komunikatem po polsku", P1, BLOCK, "Brak formularza"),
    ("A-065", "Finanse", "Bardzo duża kwota", "Wpisz 1 000 000,00", "Kwota mieści się w polu, liście i nagłówku bez łamania", P2, BLOCK, "Brak formularza (patrz TC-B-023: już −13 165,83 łamie się na desktopie)"),
    ("A-066", "Finanse", "Edycja transakcji przez drugą osobę", "Marlenka edytuje wydatek Antosia", "Zmiana widoczna u obojga z informacją kto i kiedy zmienił", P1, BLOCK, "Brak edycji"),
    ("A-067", "Finanse", "Usunięcie transakcji z potwierdzeniem i cofnięciem", "Usuń → potwierdź → Cofnij", "Salda wracają; dostępne 'Cofnij'", P1, BLOCK, "Brak edycji"),
    ("A-068", "Finanse", "Przelew między osobami", "Przelew → Marlenka → Ty 200 zł", "Saldo rozliczeń zmniejsza się o 200 zł; pozycja 'nie jest wydatkiem'", P1, BLOCK, "Brak przepływu"),
    ("A-069", "Finanse", "Rozliczenie całości", "Rozlicz → potwierdź", "Salda = 0; pozycja rozliczenia z kierunkiem i kwotą", P1, BLOCK, "Brak przepływu"),
    ("A-070", "Finanse", "Rozliczenie częściowe", "Rozlicz → zmień kwotę na 500 zł", "Pozostaje 916,31 zł do oddania", P2, BLOCK, "Brak przepływu"),
    ("A-071", "Finanse", "Nowy portfel wspólny", "Nowy portfel → 'Mieszkanie' → waluta PLN", "Portfel na liście u obu osób", P2, BLOCK, "Przycisk bez akcji"),
    ("A-072", "Finanse", "Archiwizacja zakończonego portfela", "Portfel 'Sycylia' po wyjeździe → Archiwizuj", "Znika z listy, dostępny w archiwum, salda zachowane", P3, BLOCK, "Brak funkcji"),
    ("A-073", "Finanse", "Prywatność finansów osobistych", "Antoś dodaje wydatek w 'Osobiste'", "Marlenka go nie widzi", P1, BLOCK, "Brak logiki widoczności"),
    ("A-074", "Finanse", "Wyszukiwanie transakcji", "Szukaj → 'sushi'", "Wynik 'Sushi 21.09'", P2, BLOCK, "Przycisk 'Szukaj' bez akcji"),
    ("A-075", "Finanse", "Filtr historii 'Wydatki'", "Desktop → Wydatki", "Znika 'Rozliczenie - Marlenka'", P2, BLOCK, "Chipy bez akcji"),
    ("A-076", "Finanse", "Pełna historia 'Wszystkie'", "Telefon → Historia → Wszystkie", "Lista z paginacją/datami grupowanymi", P2, BLOCK, "Link '#'"),
    ("A-077", "Finanse", "Eksport historii (CSV)", "Portfel → Eksportuj", "Plik CSV z kwotami, walutą, kursami", P3, BLOCK, "Brak funkcji"),
    ("A-078", "Finanse", "Dodanie inwestycji", "Dodaj inwestycję → nazwa, kwota, data", "Wykres wartości w czasie", P3, BLOCK, "Przycisk bez akcji"),
    ("A-079", "Finanse", "Kategoria i ikona transakcji", "Dodaj wydatek 'Szama na lotnisku'", "Kategoria wybierana przez użytkownika; ikona zgodna z kategorią", P3, BLOCK, "Brak formularza; w makiecie jedzenie na lotnisku ma ikonę samolotu"),
    # --- Migawka ---
    ("A-090", "Migawka", "Zrobienie dzisiejszej migawki", "Migawka → aparat → zdjęcie → Wyślij", "Zdjęcie widoczne u obu osób; seria +1 gdy obie zrobią", P1, BLOCK, "Brak ekranu Migawki"),
    ("A-091", "Migawka", "Odmowa dostępu do aparatu", "Odmów uprawnień", "Wyjaśnienie i link do ustawień systemu", P2, BLOCK, "Brak ekranu"),
    ("A-092", "Migawka", "Utrata serii", "Jedna osoba nie robi migawki do północy", "Jasny komunikat, zasada serii opisana z góry", P2, BLOCK, "Brak reguł serii w makiecie"),
    ("A-093", "Migawka", "Strefy czasowe w podróży", "Osoby w różnych strefach czasowych", "Seria liczona wg jasnej reguły (np. strefa pary)", P3, BLOCK, "Brak reguł"),
    ("A-094", "Migawka", "Przegląd archiwum migawek", "Migawka → kalendarz/siatka", "Przegląd po dniach, oba zdjęcia obok siebie", P3, BLOCK, "Brak ekranu"),
    ("A-095", "Migawka", "Usunięcie własnego zdjęcia", "Migawka → zdjęcie → Usuń", "Usunięte u obu osób; seria bez zmian lub jasna reguła", P2, BLOCK, "Brak ekranu"),
    # --- Randki ---
    ("A-100", "Randki", "Zaproponowanie randki", "Randka → tytuł, data, miejsce → Zaproponuj", "Partner dostaje propozycję do zatwierdzenia", P1, BLOCK, "Brak ekranu Randek"),
    ("A-101", "Randki", "Zatwierdzenie / odrzucenie propozycji", "Partner: Zatwierdź / Odrzuć", "Status widoczny u obojga", P1, BLOCK, "Brak ekranu"),
    ("A-102", "Randki", "Przypomnienie przed randką", "Randka za 2 h", "Powiadomienie z godziną i miejscem", P2, BLOCK, "Brak ekranu"),
    ("A-103", "Randki", "Ocena randki po fakcie → Słoik wspomnień", "Po randce → Oceń → dodaj zdjęcie", "Wspomnienie w Słoiku", P3, BLOCK, "Brak ekranu"),
    ("A-104", "Randki", "Dodanie do kalendarza systemowego", "Randka → Dodaj do kalendarza", "Wydarzenie w kalendarzu telefonu", P3, BLOCK, "Brak ekranu"),
    ("A-105", "Randki", "Data w przeszłości", "Zaproponuj randkę na wczoraj", "Walidacja lub zapis jako wspomnienie", P3, BLOCK, "Brak formularza"),
    # --- Zakupy ---
    ("A-110", "Zakupy", "Dodanie produktu do wspólnej listy", "Zakupy → 'mleko' → Dodaj", "Pozycja u obu osób w < 2 s", P1, BLOCK, "Brak ekranu Zakupów"),
    ("A-111", "Zakupy", "Odhaczenie produktu w sklepie", "Dotknij 'mleko'", "Przekreślone u obu; łatwe cofnięcie", P1, BLOCK, "Brak ekranu"),
    ("A-112", "Zakupy", "Jednoczesna edycja przez dwie osoby", "Obie osoby dodają produkty w tej samej chwili", "Brak utraty pozycji", P1, BLOCK, "Brak ekranu"),
    ("A-113", "Zakupy", "Zakupy → wydatek", "Zakończ zakupy → Dodaj jako wydatek", "Formularz transakcji z kwotą do uzupełnienia", P3, BLOCK, "Brak ekranu"),
    ("A-114", "Zakupy", "Duplikat produktu", "Dodaj 'mleko' drugi raz", "Podpowiedź o istniejącej pozycji", P3, BLOCK, "Brak ekranu"),
    # --- Lista życzeń, Słoik, Mapa ---
    ("A-120", "Lista życzeń", "Dodanie życzenia z linkiem", "Lista życzeń → wklej link", "Pozycja z miniaturą i ceną", P3, BLOCK, "Brak ekranu"),
    ("A-121", "Lista życzeń", "Ukrycie prezentu przed partnerem", "Zarezerwuj życzenie partnera", "Partner nie widzi rezerwacji", P2, BLOCK, "Brak ekranu"),
    ("A-122", "Słoik wspomnień", "Dodanie wspomnienia", "Słoik → Dodaj → tekst + zdjęcie", "Wspomnienie widoczne u obu", P3, BLOCK, "Brak ekranu"),
    ("A-123", "Słoik wspomnień", "Losowanie wspomnienia", "Słoik → Losuj", "Pokazuje losowe wspomnienie", P3, BLOCK, "Brak ekranu"),
    ("A-124", "Mapa", "Miejsca pary na mapie", "Mapa", "Pinezki randek/wspomnień", P3, BLOCK, "Brak ekranu"),
    ("A-125", "Mapa", "Brak zgody na lokalizację", "Odmów lokalizacji", "Mapa działa bez pozycji użytkownika", P3, BLOCK, "Brak ekranu"),
    # --- Ustawienia, motyw ---
    ("A-130", "Ustawienia", "Motyw jasny/ciemny/systemowy", "Ustawienia → Motyw → Systemowy; przełącz tryb telefonu", "Aplikacja podąża za systemem", P2, BLOCK, "Motyw to tylko suwak kanwy; brak ustawienia w aplikacji"),
    ("A-131", "Ustawienia", "Wybór akcentu nie psuje czytelności", "Wybierz każdy z 4 akcentów w każdym motywie", "Wszystkie teksty czytelne (WCAG AA)", P1, FAIL, "Pełny wynik w TC-B-001/002: w 29 z 32 kombinacji (kierunek×motyw×akcent) co najmniej jeden ekran nie spełnia kontrastu; bez błędów tylko Ciepły editorial jasny z zielonym, fioletowym i niebieskim akcentem"),
    ("A-132", "Ustawienia", "Wylogowanie", "Ustawienia → Wyloguj", "Powrót do logowania, dane usunięte z urządzenia", P1, BLOCK, "Brak ekranu"),
    ("A-133", "Ustawienia", "Usunięcie konta i eksport danych (RODO)", "Ustawienia → Prywatność → Usuń konto / Pobierz dane", "Dane do pobrania; usunięcie z potwierdzeniem i skutkami dla partnera", P1, BLOCK, "Brak ekranu"),
    ("A-134", "Ustawienia", "Zmiana imienia/zdrobnienia", "Ustawienia → Profil → imię 'Antoni'", "Zmiana widoczna w powitaniu, rozliczeniach, awatarach", P3, BLOCK, "Brak ekranu"),
    # --- Powiadomienia ---
    ("A-140", "Powiadomienia", "Powiadomienie o nowym wydatku partnera", "Marlenka dodaje wydatek", "Antoś dostaje powiadomienie z kwotą", P2, BLOCK, "Brak logiki"),
    ("A-141", "Powiadomienia", "Lista powiadomień i oznaczanie przeczytanych", "Dzwonek → lista → otwórz", "Kropka znika po przeczytaniu", P2, BLOCK, "Przycisk bez akcji"),
    ("A-142", "Powiadomienia", "Wyciszenie kategorii", "Ustawienia → Powiadomienia → wyłącz Finanse", "Brak powiadomień z Finansów", P3, BLOCK, "Brak ekranu"),
    # --- Synchronizacja, offline, bezpieczeństwo ---
    ("A-150", "Synchronizacja", "Dodanie wydatku offline", "Tryb samolotowy → dodaj wydatek → włącz sieć", "Wydatek zsynchronizowany, bez duplikatu", P1, BLOCK, "Brak logiki"),
    ("A-151", "Synchronizacja", "Konflikt edycji tej samej transakcji", "Obie osoby edytują tę samą pozycję offline", "Jasna reguła rozwiązania i informacja", P2, BLOCK, "Brak logiki"),
    ("A-152", "Bezpieczeństwo", "Blokada aplikacji biometrią", "Włącz Face ID → zamknij → otwórz", "Wymagana biometria przed pokazaniem finansów", P2, BLOCK, "Brak logiki"),
    ("A-153", "Bezpieczeństwo", "Podgląd w przełączniku aplikacji", "Otwórz Finanse → przełącz aplikację", "Kwoty zamazane w podglądzie systemu", P3, BLOCK, "Brak logiki"),
    # --- Dostępność end-to-end ---
    ("A-160", "Dostępność", "Dodanie wydatku tylko czytnikiem ekranu", "VoiceOver/TalkBack: od Głównej do zapisania wydatku", "Każdy krok ogłoszony, stan zakładek i przycisków odczytany", P1, BLOCK, "Brak przepływu; elementy statyczne: patrz TC-B-011/012/013"),
    ("A-161", "Dostępność", "Duży tekst systemowy w działającej aplikacji", "Ustaw największy rozmiar tekstu w systemie", "Treść przewija się, nic nie jest ucięte", P1, BLOCK, "Makieta ma stałą wysokość i overflow:hidden (patrz TC-B-032/033)"),
    ("A-162", "Dostępność", "Redukcja ruchu", "Włącz 'Ogranicz ruch'", "Brak animacji paralaksy/sprężyn", P3, BLOCK, "Brak animacji do oceny"),
    # --- Język i treść ---
    ("A-170", "Język", "Polskie znaki w fontach — Ciepły editorial", "Sprawdź ą ę ś ć ż ł ń w nagłówkach i kwotach", "Wszystkie znaki z tego samego fontu, bez zastępczych", P2, OK, "'Cześć, Antoś', 'Słoik wspomnień', 'zł' poprawne w Instrument Serif i DM Sans"),
    ("A-171", "Język", "Polskie znaki w fontach — Miękki natywny", "j.w.", "j.w.", P2, OK, "Poprawne w Geist"),
    ("A-172", "Język", "Polskie znaki w fontach — Żywy i zabawny", "j.w.", "j.w.", P2, OK, "Poprawne w Bricolage Grotesque"),
    ("A-173", "Język", "Polskie znaki w fontach — Minimalistyczny", "j.w.", "j.w.", P2, OK, "Poprawne w Geist i Geist Mono"),
    ("A-174", "Język", "Treść w perspektywie drugiej osoby", "Teksty systemowe ('Marlenka oddaje Tobie', 'Ty')", "Formy niezależne od płci odbiorcy", P2, OK, "Teksty systemowe neutralne; rodzaj pojawia się tylko w opisie wpisanym przez użytkownika ('Oddałem')"),
    ("A-175", "Język", "Rejestr językowy spójny", "Porównaj 'Szama na lotnisku' i 'Planujcie wyjścia, zatwierdzajcie propozycje'", "Potoczny język użytkownika w danych, spójny ton w interfejsie", P3, OK, "Potoczne są tylko dane przykładowe; teksty interfejsu spójne"),
    ("A-176", "Język", "Format kwot zgodny z polskim zapisem", "Sprawdź separator tysięcy i dziesiętny", "Spacja nierozdzielająca jako separator tysięcy, przecinek dziesiętny", P2, FAIL, "Przecinek OK, ale separator tysięcy to zwykła spacja — kwoty łamią się między wierszami (TC-B-023)"),
    ("A-177", "Język", "Nagłówek streak mieści się w jednej linii", "Karta 'Migawka dziś' w każdym kierunku", "'62 dni z rzędu' w jednej linii", P3, FAIL, "Łamie się na 2 linie w Miękkim natywnym, Żywym i Minimalistycznym (przy 3-cyfrowej serii będzie gorzej)"),
    ("A-178", "Język", "Liczba mnoga dni", "Seria 1, 2, 5, 22 dni", "'1 dzień', '2 dni', '5 dni', '22 dni'", P3, BLOCK, "Wartość statyczna w makiecie"),
]


def main(out):
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "modul", "tytul", "kroki", "oczekiwany_wynik", "priorytet", "status_prototyp", "wynik_dowod"])
        for row in CASES:
            w.writerow(row)
    by = {}
    for c in CASES:
        by[c[6]] = by.get(c[6], 0) + 1
    print(f"{len(CASES)} przypadków:", by)


if __name__ == "__main__":
    main(sys.argv[1])
