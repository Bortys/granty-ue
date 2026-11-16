# Polskie źródła naborów: fundusze europejskie, krajowe, lokalne i prywatne

Adresy sprawdzone 15–16.11.2026 (wszystkie odpowiadały). Instytucje zmieniają domeny, a kilka już przekierowuje pod nowe adresy. Jeśli adres nie działa, szukaj nazwy programu na Portalu Funduszy Europejskich, a nie w wyszukiwarce ogólnej.

„Chrome” w kolumnie „Jak czytać” znaczy: strona ładuje wyniki skryptem albo blokuje zwykłe pobieranie, więc czytaj ją przez Claude in Chrome (`get_page_text`).

## Listy zbiorcze

| Źródło | Adres | Jak czytać |
|---|---|---|
| Katalog Kierunek Grant (autora skilla) | https://sokolinski.com/granty/ | skrypt `katalog_grantow.py`; ponad 750 naborów z kilkudziesięciu źródeł |
| Wyszukiwarka dotacji, Portal Funduszy Europejskich | https://funduszeeuropejskie.gov.pl/wyszukiwarka/ | Chrome; programy krajowe i regionalne, filtr po województwie i typie wnioskodawcy |
| Aktualne nabory i miesięczne zestawienia (XLSX: krajowe, regionalne, Interreg) | https://funduszeeuropejskie.gov.pl/aktualne-nabory/ | linki do bieżących plików daje `katalog_grantow.py --raporty`; każdy arkusz ma inne kolumny i jednostki budżetu |
| Nabory, Ministerstwo Funduszy i Polityki Regionalnej | https://www.funduszeunijne.gov.pl/nabory/ | Chrome; stary adres funduszeeuropejskie.gov.pl/nabory przekierowuje tutaj |
| WOD2021, lista naborów w systemie CST2021 | https://wod.cst2021.gov.pl/callForProposals/ | Chrome; tu też składa się wnioski do większości naborów FE 2021–2027 |

## Programy funduszy europejskich 2021–2027 i KPO

| Program | Dla kogo i na co | Adres |
|---|---|---|
| FENG, Fundusze Europejskie dla Nowoczesnej Gospodarki | badania, rozwój i innowacje w firmach, w tym ścieżka SMART i nabory STEP w obronności; operatorzy PARP, NCBR, BGK, FNP | https://nowoczesnagospodarka.gov.pl/ (harmonogram: `/dokumenty/harmonogram-naborow-w-programie-fundusze-europejskie-dla-nowoczesnej-gospodarki/`) |
| FEPW, Fundusze Europejskie dla Polski Wschodniej | firmy i samorządy z województw lubelskiego, podkarpackiego, podlaskiego, świętokrzyskiego i warmińsko-mazurskiego (oraz części mazowieckiego); operator PARP | https://polskawschodnia.gov.pl/ |
| FERC, Fundusze Europejskie na Rozwój Cyfrowy | cyfryzacja, e-usługi publiczne, sieci | https://rozwojcyfrowy.gov.pl/ |
| FERS, Fundusze Europejskie dla Rozwoju Społecznego | kompetencje, rynek pracy, edukacja, włączenie społeczne; nabory MEN osobno, część wniosków w systemie SOWA EFS | https://rozwojspoleczny.gov.pl/, https://efs.men.gov.pl/nabory/, https://sowa2021.efs.gov.pl/ |
| FEnIKS, Fundusze Europejskie na Infrastrukturę, Klimat, Środowisko | energia, klimat, transport, zdrowie, kultura | https://feniks.gov.pl/ |
| Fundusze Europejskie dla Rybactwa | rybactwo i akwakultura, także przez lokalne grupy rybackie | https://rybactwo.gov.pl/ |
| KPO, Krajowy Plan Odbudowy | reformy i inwestycje z instrumentu odbudowy; nabory rozproszone po ministerstwach | https://www.kpo.gov.pl/ |

Każdy program publikuje harmonogram naborów na rok. To najlepsze źródło naborów zapowiedzianych.

## Programy regionalne

Szesnaście programów „Fundusze Europejskie dla [regionu]” prowadzą urzędy marszałkowskie i ich agencje. Zacznij od katalogu (`--zasieg Regionalne --wojewodztwo …`) albo od wyszukiwarki dotacji z filtrem województwa. Portal programu otwieraj przy konkretnym naborze i po harmonogram:

| Województwo | Adres |
|---|---|
| dolnośląskie | https://funduszeuedolnoslaskie.pl/ |
| kujawsko-pomorskie | https://funduszeue.kujawsko-pomorskie.pl/ |
| lubelskie | https://funduszeue.lubelskie.pl/ |
| lubuskie | https://funduszeue.lubuskie.pl/ |
| łódzkie | https://funduszeue.lodzkie.pl/ |
| małopolskie | https://fundusze.malopolska.pl/ |
| mazowieckie | https://funduszeuedlamazowsza.eu/ |
| opolskie | https://funduszeue.opolskie.pl/ |
| podkarpackie | https://funduszeue.podkarpackie.pl/ |
| podlaskie | https://funduszeuepodlaskie.pl/ |
| pomorskie | https://funduszeuepomorskie.pl/ |
| śląskie | https://funduszeue.slaskie.pl/ |
| świętokrzyskie | https://funduszeueswietokrzyskie.pl/ |
| warmińsko-mazurskie | https://funduszeeuropejskie.warmia.mazury.pl/ |
| wielkopolskie | https://funduszeue.wielkopolskie.pl/ |
| zachodniopomorskie | https://funduszeue.wzp.pl/ |

## Instytucje i programy krajowe

| Instytucja | Co prowadzi | Adres | Jak czytać |
|---|---|---|---|
| PARP | nabory dla firm, głównie MŚP, z FENG, FEPW i programów własnych | https://www.parp.gov.pl/harmonogram-naborow | Chrome (Incapsula) |
| NCBR | badania i rozwój: FENG, programy własne i międzynarodowe (np. INNOGLOBO), konkursy obronne | https://www.gov.pl/web/ncbr/platforma-konkursowa/ | Chrome (lista konkursów ładuje się skryptem); strony pojedynczych konkursów na gov.pl czytelne bez przeglądarki |
| NCN | granty na badania podstawowe dla naukowców | https://ncn.gov.pl/bip/konkursy-i-granty/konkursy-w-toku | Chrome |
| NAWA | wymiana i umiędzynarodowienie nauki, m.in. Polskie Powroty | https://www.nawa.gov.pl/programy-nawa/programy-nawa-alias/trwajace | bez przeglądarki |
| FNP, Fundacja na rzecz Nauki Polskiej | programy dla naukowców i zespołów, w FENG m.in. First Team | https://www.fnp.org.pl/ | bez przeglądarki |
| ABM, Agencja Badań Medycznych | badania medyczne i kliniczne | https://abm.gov.pl/ | bez przeglądarki |
| MNiSW | programy ministra, np. Narodowy Program Rozwoju Humanistyki | https://www.gov.pl/web/nauka | bez przeglądarki |
| NFOŚiGW | ochrona środowiska, energia, klimat: programy priorytetowe; wojewódzkie fundusze (WFOŚiGW) mają własne nabory | https://www.gov.pl/web/nfosigw/harmonogram-naborow | bez przeglądarki |
| Fundusz Modernizacyjny (prowadzi NFOŚiGW) | transformacja energetyki: ciepłownictwo, OZE, efektywność energetyczna, przemysł energochłonny (np. program „Przemysł energochłonny – OZE”, ponad 348 mln zł) | https://www.gov.pl/web/funduszmodernizacyjny | bez przeglądarki |
| NCBR, programy międzynarodowe | finansowanie polskich uczestników wspólnych konkursów partnerstw Horyzontu Europa, ERA-NET, Eurostars, CORNET i programów dwustronnych | https://www.gov.pl/web/ncbr/programy--miedzynarodowe | bez przeglądarki |
| NCN, konkursy międzynarodowe | harmonogram konkursów wielostronnych (np. Weave, partnerstwa europejskie) | https://ncn.gov.pl/wspolpraca-zagraniczna/harmonogram-konkursow | Chrome |
| ARiMR | Plan Strategiczny WPR 2023–2027: rolnicy, obszary wiejskie, LEADER przez lokalne grupy działania | https://www.gov.pl/web/arimr/plan-strategiczny-dla-wspolnej-polityki-rolnej-na-lata-2023-2027---dzialania | bez przeglądarki |
| NIW, Narodowy Instytut Wolności | programy dla organizacji pozarządowych, m.in. NOWEFIO i PROO | https://niw.gov.pl/ | bez przeglądarki |
| MKiDN | programy ministra kultury i operatorów | https://www.gov.pl/web/kultura/programy-i-projekty | bez przeglądarki |
| MRPiPS | nabory w polityce społecznej, np. z Funduszu Solidarnościowego | https://www.gov.pl/web/rodzina/nabory | bez przeglądarki |
| KFS, Krajowy Fundusz Szkoleniowy (powiatowe urzędy pracy) | dofinansowanie szkoleń, studiów podyplomowych i egzaminów dla pracodawców i ich pracowników: 80% kosztów, w mikrofirmie (do 10 osób) 100%, najwyżej 300% przeciętnego wynagrodzenia na uczestnika. Wniosek musi spełniać jeden z priorytetów KFS na dany rok. Nabory ogłasza każdy powiatowy urząd pracy osobno, często kilka razy w roku i na kilka dni, z małą pulą (np. około 100 tys. zł). Składa pracodawca zatrudniający na umowę o pracę, więc KFS nie sfinansuje kursów, które organizacja prowadzi dla innych | zasady i priorytety: https://www.gov.pl/web/rodzina/krajowy-fundusz-szkoleniowy; nabory na stronie urzędu pracy właściwego dla siedziby firmy (adres `miasto.praca.gov.pl`, np. https://ostroda.praca.gov.pl/) i w katalogu (`katalog_grantow.py --tekst kształcenia ustawicznego`) | bez przeglądarki |
| ARP, Agencja Rozwoju Przemysłu | konkursy i programy dla przemysłu, np. Dig.IT | https://arp.pl/pl/ | bez przeglądarki |
| BGK | operator instrumentów finansowych i części naborów FENG; głównie finansowanie zwrotne | https://www.bgk.pl/ | bez przeglądarki |

Kto prowadzi który nabór, sprawdzaj w ogłoszeniu. Podział między instytucjami zmienia się między naborami.

## Samorządy i organizacje pozarządowe

Gminy, powiaty i województwa ogłaszają otwarte konkursy ofert na zadania publiczne. Ogłoszenia są w BIP danej jednostki, a wiele samorządów prowadzi nabory w generatorach:

| Źródło | Co | Adres |
|---|---|---|
| eNGO | generator wniosków; każdy samorząd ma własną listę konkursów pod adresem `nazwa.engo.org.pl/konkursy-trwajace` | https://engo.org.pl/ |
| Witkac | generator wniosków z listą konkursów | https://witkac.pl/Contest/ |
| ngo.pl | przegląd konkursów i grantów dla organizacji; tylko trop, daty sprawdzaj u organizatora | https://fundusze.ngo.pl/aktualne |
| BIP gminy lub powiatu | ogłoszenie z regulaminem i załącznikami; oddzielaj konkursy ofert od naborów do komisji konkursowych | adres z ogłoszenia |

## Fundacje i programy firm

Fundacje firmowe ogłaszają rundy grantowe na własnych stronach. Aktualność rundy i regulamin sprawdzaj za każdym razem.

| Fundacja | Adres |
|---|---|
| Fundusz Obywatelski im. Ludwiki i Henryka Wujców | https://www.funduszobywatelski.pl/ |
| Fundacja PZU | https://fundacja.pzu.pl/dotacje |
| Fundacja LOTTO | https://www.fundacjalotto.pl/ |
| Fundacja ORLEN (i programy regionalne, np. ORLEN dla Pomorza) | https://fundacja.orlen.pl/pl |
| Fundacja PKO Banku Polskiego: programy grantowe, np. „Pomagamy z Każdym Krokiem” (wsparcie psychologiczne dzieci i młodzieży; 16.11.2026 nabór do 25.11.2026, granty do 100 tys. zł i lokalne 60–75 tys. zł w 20 miejscowościach) | https://www.fundacjapkobp.pl/ |
| Fundacja Erste: konkursy grantowe dla organizacji pozarządowych, np. „Haki na cyberataki” (edukacja o cyberbezpieczeństwie i oszustwach; granty 50 tys. zł dla fundacji i stowarzyszeń działających co najmniej 2 lata; edycja 2026 zamknięta 16.11.2026) | https://fundacja.erste.pl/ |
| Kaufland, „Lepiej po sąsiedzku”: pieniądze na lokalne inicjatywy sąsiedzkie | https://lepiejposasiedzku.pl/ (Chrome) |

## PFR, uczelnie i agencje rozwoju

Sprawdzaj te źródła bezpośrednio na stronach instytucji. Grupa PFR daje głównie kapitał, akcelerację i kontakty z inwestorami, a pieniądze uczelni trafiają najczęściej do ich własnych pracowników, doktorantów i studentów. Oznaczaj to w odpowiedzi.

| Źródło | Dla kogo i na co | Adres | Jak czytać |
|---|---|---|---|
| Programy Grupy PFR | jedna lista programów PFR, PFR Ventures, PARP, ARP, KUKE i innych instytucji grupy, z filtrami tematów (np. innowacje i akceleracja, ekspansja zagraniczna, finansowanie i doradztwo) | https://grupapfr.pl/programy | Chrome |
| PFR dla startupów | bezpłatne programy: VC Connect (spotkania z funduszami VC i partnerami w ścieżkach sektorowych), Szkoła Pionierów PFR (warsztaty przed akceleracją), program dla technologii podwójnego zastosowania, Science Momentum (akceleracja zespołów naukowych); w aktualnościach także nabory, np. bony badawcze POL-OPENSCREEN | https://startup.pfr.pl/ | Chrome (zwykłe pobieranie zwraca 403) |
| PFR Ventures | fundusz funduszy: nie inwestuje bezpośrednio w firmy, tylko w fundusze VC i PE z programów PFR Starter, PFR Biznest (z aniołami biznesu), PFR Otwarte Innowacje (B+R), PFR KOFFI, PFR CVC, PFR Deep Tech i Starter Science (projekty ze świata nauki). Firma szuka inwestora na liście funduszy z portfela. To inwestycja kapitałowa, nie grant | lista funduszy: https://pfrventures.pl/nasze-portfolio | Chrome |
| PAIH, Polska Agencja Inwestycji i Handlu | Polskie Mosty Technologiczne: grant dla MŚP na wejście na rynki zagraniczne i rozwój eksportu, nabory konkursowe z FENG | https://www.paih.gov.pl/ | bez przeglądarki |
| Konkursy wewnętrzne uczelni badawczych (IDUB) | pracownicy, doktoranci i studenci danej uczelni: mikrogranty, granty dla młodych badaczy, staże. Laureaci II edycji (5.11.2026): AGH, Politechnika Gdańska, Politechnika Śląska, Politechnika Warszawska, Politechnika Wrocławska, UAM, UJ, Uniwersytet Medyczny w Białymstoku, UW i Uniwersytet Wrocławski | strona programu IDUB na stronie uczelni; lista laureatów: https://www.gov.pl/web/nauka/poznalismy-laureatow-ii-edycji-programu-inicjatywa-doskonalosci--uczelnia-badawcza | zwykle bez przeglądarki |
| Centra transferu technologii i spółki celowe uczelni | dla naukowców: granty na prace przedwdrożeniowe (np. w projekcie Science4Business – Nauka dla Biznesu z FENG, na UAM przez UCITT), ochrona patentowa, zakładanie spółek odpryskowych (spin-off); dla firm: bazy technologii, usług badawczych i ekspertów uczelni | strona centrum transferu danej uczelni, np. https://ucitt.amu.edu.pl/ | zwykle bez przeglądarki |
| MNiSW, „Studenckie koła naukowe tworzą innowacje” | projekty kół naukowych; wniosek składa uczelnia, nie samo koło. VI edycja rozstrzygnięta 16.02.2026 | https://www.gov.pl/web/nauka/informacje-o-programie-studenckie-kola-naukowe-tworza-innowacje | bez przeglądarki |
| MNiSW, „Doktorat wdrożeniowy” | doktorant pracuje w firmie i kształci się w szkole doktorskiej, a obok pensji dostaje stypendium ministra; dla firmy to sposób na badania we współpracy z uczelnią. Program ogłaszany co roku wiosną (2026: komunikat z 30.04.2026), rekrutację prowadzą szkoły doktorskie | https://www.gov.pl/web/nauka/doktoraty-wdrozeniowe---czyli-jak-wygrac-trzy-razy | bez przeglądarki |

Część pieniędzy z programów regionalnych rozdają operatorzy projektów grantowych, często regionalne agencje rozwoju. Tak działają np. bony na usługi badawcze dla MŚP (na Dolnym Śląsku projekt „Innowacje dla STEP” Agencji Rozwoju Aglomeracji Wrocławskiej). Ogłoszenia są na stronie operatora i w portalu programu regionalnego.

## Pomoc bez opłat

| Kto | W czym pomaga | Adres |
|---|---|---|
| Krajowy Punkt Kontaktowy Programów Badawczych UE | Horyzont Europa i EIC: wybór tematu, konsultacja wniosku, szukanie partnerów | https://www.kpk.gov.pl/ |
| Punkty Informacyjne Funduszy Europejskich | fundusze krajowe i regionalne: dobór programu, warunki naboru; punkty są w każdym województwie | https://funduszeeuropejskie.gov.pl/skontaktuj-sie/ |
| Punkty kontaktowe programów UE (NCP) | wyszukiwarka punktów kontaktowych dla każdego programu, także EDF | https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/support/ncp |

## Czego tu nie ma

- Programy międzynarodowe spoza portalu UE (Fundusze EOG, Interreg, Eureka, EIT, ESA, Fundusz Wyszehradzki) są w `zrodla-zagraniczne.md`, obronność w `obronnosc.md`, a kontrakty agend badawczych (ESA, CERN, ESO, EUSPA) w `agendy-i-zamowienia.md`.
- Przetargi publiczne (TED, Biuletyn Zamówień Publicznych, Baza Konkurencyjności) to zamówienia, a nie dotacje. Są w `agendy-i-zamowienia.md`.
