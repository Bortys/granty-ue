# Agendy badawcze, organizacje międzynarodowe i zamówienia publiczne

Adresy i fakty sprawdzone 16.11.2026. Czytaj, gdy wnioskodawca może sprzedawać usługi, sprzęt albo prace badawczo-rozwojowe albo gdy pytanie dotyczy ESA, CERN, przetargów lub zamówień.

## Przetarg to nie dotacja

W grancie wnioskodawca proponuje projekt, a instytucja dokłada do niego część kosztów. W zamówieniu zamawiający opisuje, czego potrzebuje, i płaci wykonawcy za wykonanie. Ocenia warunki udziału (doświadczenie, referencje, obroty, zespół) i kryteria oferty (cena, jakość, termin). Prawa do wyników określa umowa.

Pokazuj przetargi w osobnej tabeli z dopiskiem „zamówienie, nie dotacja”. Skill znajduje ogłoszenia i sprawdza podstawowe warunki. Oferty nie przygotowuje i nie ocenia jej zgodności z ustawą Prawo zamówień publicznych (Pzp).

## Agendy i organizacje badawcze

Kupują głównie od firm z państw członkowskich. Polska należy do ESA, CERN i ESO, a jako państwo UE uczestniczy też w agendach unijnych (EUSPA, F4E). Rejestracja dostawcy to pierwszy krok, często zanim pojawi się ogłoszenie, bo część zaproszeń trafia tylko do zarejestrowanych firm.

| Organizacja | Co kupuje albo finansuje | Jak wejść | Adres | Jak czytać |
|---|---|---|---|---|
| ESA, Europejska Agencja Kosmiczna | kontrakty przemysłowe (studia, rozwój technologii, sprzęt, usługi) i otwarte nabory propozycji; dla firm od startupów po integratorów systemów | rejestracja w esa-star; ogłoszenia w esa-star Publication (od 23.03.2021 zamiast EMITS), ich polskie streszczenia w katalogu Kierunek Grant (`katalog_grantow.py --rodzaj zamowienia --program ESA`) | https://www.esa.int/business/business-with-esa, portal: https://doing-business.sso.esa.int/, ogłoszenia: https://esastar-publication-ext.sso.esa.int/ | esa-star tylko przez Chrome; nabory dofinansowania czytaj w wierszu niżej, bez przeglądarki |
| ESA Space Solutions (dawniej Business Applications, BASS) | dofinansowanie bez oddawania udziałów, od 60 tys. do ponad 3 mln EUR na działanie, dla usług i produktów opartych na danych albo technologiach kosmicznych, z każdej branży (także rolnictwo, finanse i ubezpieczenia): Kick-starts (nabór zawsze otwarty, wnioski oceniane partiami), studia wykonalności i projekty pilotażowe, Growth Projects dla rozwiązań z sukcesem na pierwszym rynku, nabory tematyczne z terminami | pełny wniosek wymaga pisemnej zgody delegacji krajowej (Written Authorisation); każdy nabór podaje listę krajów, z których firmy mogą dostać pieniądze; kontakty do polskiej delegacji (ministerstwo rozwoju i POLSA) są na stronie delegacji | lista naborów: https://business.esa.int/funding, zasady: https://business.esa.int/how-to-apply, delegacje: https://business.esa.int/national-delegations | bez przeglądarki; tu bierz otwarte nabory ESA dla firm |
| ESA BIC (ośrodki inkubacji ESA) | startupy z technologią kosmiczną albo jej zastosowaniem na Ziemi: wsparcie techniczne i biznesowe oraz 50 tys. EUR bez oddawania udziałów na rozwój produktu i własności intelektualnej | zgłoszenie do konkretnego ośrodka; sprawdź na liście, gdzie działa najbliższy | https://commercialisation.esa.int/esa-business-incubation-centres/ | bez przeglądarki |
| POLSA, Polska Agencja Kosmiczna | krajowe informacje o programach ESA i udziale Polski | | https://polsa.gov.pl/ | bez przeglądarki |
| EUSPA, agencja programu kosmicznego UE (Galileo, EGNOS) | przetargi i granty, m.in. na usługi i zastosowania nawigacji satelitarnej | przetargi w portalu UE (`nabory_ue.py szukaj --typ przetargi`) i w TED, granty w portalu UE | https://www.euspa.europa.eu/opportunities/procurement-grants/procurement, https://www.euspa.europa.eu/opportunities | bez przeglądarki |
| CASSINI, inicjatywa przedsiębiorczości kosmicznej UE | hackathony, wyzwania z nagrodami pieniężnymi, akcelerator, kojarzenie z firmami; fundusz CASSINI (1 mld EUR) inwestuje przez fundusze VC, to nie grant | zgłoszenia do konkretnych wydarzeń | https://www.cassini.eu/cassini-initiative | bez przeglądarki |
| CERN | zamówienia dla firm z państw członkowskich i stowarzyszonych; webinaria dla firm bez doświadczenia z CERN | rejestracja dostawcy na stronie | https://business-with-cern.web.cern.ch/ | bez przeglądarki |
| CERN, zapowiedzi przetargów | przetargi o wartości powyżej 200 tys. CHF, zanim zostaną rozesłane: badania rynku (Market Survey), zaproszenia do przetargu i zapytania cenowe. Zwykle odpowiadać mogą tylko firmy, których dostawy i usługi pochodzą z państwa członkowskiego CERN. Udział zgłasza się mailem na adres z ogłoszenia. 16.11.2026: 47 pozycji (24 badania rynku, 23 zapowiedzi) | zgłoszenie zainteresowania mailem; badanie rynku to zwykle pierwszy krok do zaproszenia | strona: https://forthcoming-ms.cern.ch/ (aplikacja w JS, przez Chrome); te same dane jako JSON bez przeglądarki: https://procurement-api.cern.ch/procurement/forthcoming/detailed (pola `reference`, `title`, `status`, `contract_type`, `cost_range`, `next_step_expected`, `source_url`) | API bez przeglądarki |
| ESO, Europejskie Obserwatorium Południowe | przetargi w państwach członkowskich ESO; uczestników wybiera się głównie z bazy dostawców i przez krajowych łączników przemysłowych (Industrial Liaison Officers) | rejestracja w bazie dostawców ESO | https://www.eso.org/public/industry/ | bez przeglądarki |
| F4E (Fusion for Energy) | zamówienia na europejski wkład w ITER i badania nad syntezą jądrową | rejestracja w portalu przemysłowym | https://industryportal.f4e.europa.eu/ | bez przeglądarki |
| EUMETSAT, Europejska Organizacja Eksploatacji Satelitów Meteorologicznych | przetargi na usługi, dane i systemy satelitarne, także szkolenia i wsparcie użytkowników | system przetargowy EUMITS: bieżące i planowane zaproszenia do przetargu, rejestracja do pobierania dokumentów | https://eumits.eumetsat.int/pub/pub_citt_list.jsf | lista bieżących przetargów bez przeglądarki (numer, tytuł, data otwarcia i zamknięcia) |
| EU SST, europejskie partnerstwo śledzenia obiektów w przestrzeni kosmicznej | zamówienia na obserwacje i śledzenie śmieci kosmicznych (np. stacje laserowe, czujniki), ogłaszane przez krajowe agencje partnerstwa, w Polsce przez POLSA (BIP i platforma zakupowa) | tabela postępowań i odnośniki do portali zamówień państw partnerstwa | https://www.eusst.eu/about-us/procurement | bez przeglądarki; postępowania są też w TED |
| ECMWF, Europejskie Centrum Prognoz Średnioterminowych | przetargi na usługi i sprzęt dla centrum prognoz pogody | | https://www.ecmwf.int/en/about/suppliers | bez przeglądarki |
| EDA, Europejska Agencja Obrony | przetargi obronne, często umowy ramowe | przetargi w portalu UE (`nabory_ue.py szukaj --typ przetargi`) i w TED (`przetargi_ted.py --zamawiajacy "European Defence Agency" --wszystkie-kraje`) | strona eda.europa.eu blokuje zwykłe pobieranie | przez Chrome |

Firma bez historii z ESA zaczyna zwykle od Kick-startu albo naboru tematycznego ESA Space Solutions i od rozmowy z polską delegacją o zgodzie na finansowanie. Kontrakty z przetargów w esa-star przychodzą później.

ESA stosuje zasadę zwrotu geograficznego: kontrakty trafiają do firm z państw członkowskich mniej więcej w proporcji do wkładu tych państw w programy ESA. Dla firmy z Polski znaczy to, że szanse zależą od programów, w których Polska ma składkę. Pytaj o to POLSA.

Nie sprawdzono 16.11.2026: strona zamówień EuroHPC (zwracała 404) i Open Space Innovation Platform ESA (wymaga logowania). Ich przetargi szukaj w TED (`przetargi_ted.py --tekst ... --wszystkie-kraje`) i w portalu UE.

## Gdzie szukać przetargów

| Źródło | Co tam jest | Narzędzie | Adres |
|---|---|---|---|
| Katalog Kierunek Grant, pozycje „zamówienie” i „konsultacje rynkowe” | zamówienia agend przetłumaczone na polski: 16.11.2026 było ich ponad 110, m.in. 88 z ESA (z esa-star) oraz pozycje z CERN, EUMETSAT, EUSPA, EU SST i ECMWF. Opis pozycji ESA mówi, czy Polska jest na liście państw wskazanych dla postępowania | `katalog_grantow.py --rodzaj zamowienia konsultacje`; opis w `--json`, pole `description` | https://sokolinski.com/granty/ |
| TED (Tenders Electronic Daily) | zamówienia powyżej progów unijnych z całej UE: polskich zamawiających (ministerstwa, wojsko, uczelnie, szpitale, samorządy, spółki), instytucji i agencji UE, organizacji międzynarodowych; także zapowiedzi przetargów (wstępne ogłoszenia informacyjne) i ogłoszenia o udzieleniu zamówienia | `scripts/przetargi_ted.py` (API v3 bez klucza) | https://ted.europa.eu/en/ (strony ogłoszeń przez Chrome) |
| Portal Funding & Tenders, zakładka przetargów | przetargi Komisji i agencji UE (np. EDA, EUSPA, SatCen, JRC) z dokumentami, pytaniami i składaniem ofert przez eSubmission | `nabory_ue.py szukaj --typ przetargi`, szczegóły: `temat <identyfikator>` | https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/calls-for-tenders |
| e-Zamówienia, Biuletyn Zamówień Publicznych | polskie zamówienia od 130 000 zł netto do progów unijnych | Chrome | https://ezamowienia.gov.pl/mo-client-board/bzp/list |
| Baza Konkurencyjności | zamówienia beneficjentów funduszy UE (firm, uczelni, organizacji), którzy kupują w projektach według zasady konkurencyjności, np. usługi badawcze, szkolenia, doradztwo, sprzęt | Chrome | https://bazakonkurencyjnosci.funduszeeuropejskie.gov.pl/ |
| Agencja Uzbrojenia | zamówienia sprzętu wojskowego i usług dla Sił Zbrojnych RP, inicjowanie prac badawczo-rozwojowych, umowy offsetowe | ogłoszenia powyżej progów w TED: `przetargi_ted.py --zamawiajacy "Agencja Uzbrojenia"` (16.11.2026: 321 ogłoszeń, w większości o udzieleniu zamówienia) | opis zadań: https://www.gov.pl/web/obrona-narodowa/agencja-uzbrojenia, strona AU: https://www.wojsko-polskie.pl/au/ (przez Chrome) |

Poniżej 130 000 zł netto ustawy Pzp się nie stosuje. Zamawiający ogłaszają wtedy zapytania ofertowe na swoich stronach i platformach zakupowych, więc takich zamówień nie znajdzie żaden zbiorczy serwis.

W obronności część zakupów nie trafia do publicznych ogłoszeń, bo ustawa przewiduje wyłączenia ze względu na bezpieczeństwo państwa. Przed przetargiem zamawiający może też prowadzić wstępne konsultacje rynkowe z firmami (w dawnej ustawie: dialog techniczny). Dlatego w obronności liczy się także kontakt z Agencją Uzbrojenia i śledzenie jej strony, a nie tylko wyszukiwarki.

### Jak szukać w TED

- `--tekst` szuka w całej treści ogłoszenia. Podawaj słowa po polsku i po angielsku, z gwiazdką na odmianę: `--tekst 'dron*' 'bezzałog*' 'UAV'`. W powłoce zsh gwiazdkę bierz w apostrofy. Fraza w cudzysłowie działa: `--tekst "sztuczna inteligencja"`.
- Tekst łapie też ogłoszenia, w których słowo pada przy okazji (np. ubezpieczenie dronów w przetargu na ubezpieczenie floty). Zawężaj kodem CPV: 73 (usługi badawcze i rozwojowe), 72 (usługi informatyczne), 48 (oprogramowanie i systemy informatyczne), 35 (sprzęt bezpieczeństwa i obronny), 34711200 (bezzałogowe statki powietrzne).
- Domyślnie kraj zamawiającego to Polska. Instytucje UE mają siedziby w Belgii, Luksemburgu, Hiszpanii i innych krajach, więc dla nich dodaj `--wszystkie-kraje`.
- `--zapowiedzi` dodaje wstępne ogłoszenia informacyjne. Zapowiedź nie ma terminu ofert, ale daje czas na przygotowanie i pokazuje plany zamawiającego.
- Skrypt odsiewa ogłoszenia, których terminy minęły. Filtr TED przepuszcza ogłoszenie, gdy pasuje dowolna część zamówienia, a dynamiczne systemy zakupów i umowy ramowe mają terminy sprzed miesięcy.
- Termin w tabeli to dzień składania ofert bez godziny. Godzinę i sprostowania sprawdzaj w ogłoszeniu i w dokumentach zamówienia.

## Zamówienia innowacyjne (PCP i PPI)

- **Zamówienie przedkomercyjne (PCP):** zamawiający kupuje prace badawczo-rozwojowe etapami (projekt, prototyp, testy) od kilku wykonawców naraz, zanim rozwiązanie trafi na rynek. Dla firmy z technologią to kontrakt na rozwój produktu z pierwszym klientem. W Polsce PCP ogłasza NCBR. 16.11.2026 w TED były jego zapowiedzi z kodem 73100000 (np. „PCP AUDITORIA”): `przetargi_ted.py --zamawiajacy "Narodowe Centrum Badań i Rozwoju" --zapowiedzi --zapowiedzi-dni 365`.
- **Zamówienie rozwiązań innowacyjnych (PPI):** zamawiający kupuje rozwiązanie nowe na rynku, często jako pierwszy klient.
- **Granty UE dla zamawiających:** tematy Horyzontu Europa typu „Pre-commercial Procurement” dają dotację konsorcjum zamawiających publicznych na wspólne PCP. Firma wchodzi później jako wykonawca w ich przetargu. W portalu mają tag `InnovationProcurement`: `nabory_ue.py szukaj --priorytet InnovationProcurement` (16.11.2026: 6 tematów). Dla samorządu, szpitala albo uczelni to grant, a dla firmy zapowiedź przyszłego przetargu.

## Warunki, które w przetargach odsiewają

Sprawdź je w ogłoszeniu i w dokumentach zamówienia, zanim polecisz przetarg:

1. **Warunki udziału.** Doświadczenie (referencje z podobnych zamówień), osoby z określonymi kwalifikacjami, sprzęt, sytuacja finansowa (obroty, ubezpieczenie). Firma bez referencji często odpada. Może wtedy wejść jako podwykonawca, w konsorcjum albo polegać na zasobach innego podmiotu, jeśli dokumenty na to pozwalają.
2. **Oświadczenia o braku podstaw wykluczenia.** W Polsce powyżej progów unijnych to JEDZ (Jednolity Europejski Dokument Zamówienia). Instytucje UE mają własne wzory oświadczeń w dokumentach przetargu.
3. **Wadium.** Zabezpieczenie oferty w pieniądzu albo gwarancji, jeśli zamawiający go wymaga. Gwarancję trzeba załatwić przed terminem ofert.
4. **Czas.** Od ogłoszenia do terminu ofert mija zwykle kilka tygodni. Pytania do zamawiającego mają własny, wcześniejszy termin, a sprostowania potrafią zmienić termin i wymagania.
5. **Obronność.** Informacje niejawne, świadectwo bezpieczeństwa przemysłowego i koncesja: `obronnosc.md`.
6. **Organizacje międzynarodowe.** ESA, CERN i ESO kupują w państwach członkowskich. Firma z siedzibą poza nimi zwykle nie dostanie zaproszenia. Dokumenty są po angielsku.

Punktów 1–3 nie oceniasz za wykonawcę. Wskaż, co sprawdzić w dokumentach, a ocenę zostaw jemu i jego prawnikowi.
