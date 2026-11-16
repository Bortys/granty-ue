# Obronność, bezpieczeństwo i podwójne zastosowanie (dual use)

Adresy i fakty sprawdzone 16.11.2026. Terminy i kwoty sprawdzaj zawsze w bieżącym ogłoszeniu, bo programy obronne zmieniają się szybko.

## Najpierw rozróżnienie

- **Horyzont Europa i EIT** finansują wyłącznie zastosowania cywilne (art. 7 rozporządzenia 2021/695). Wyjątki dotyczą EIC: od 17.06.2026 EIC finansuje też technologie obronne i dual use. EIC Accelerator przyjmuje projekty dual use, jeśli spełniają warunki programu pracy EIC (sprawdź w nim definicję dual use i wymagania co do rynku cywilnego). Osobny nabór EIC STEP Scale Up Defence jest opisany niżej.
- **EDF (Europejski Fundusz Obronny)** finansuje wyłącznie badania i rozwój w dziedzinie obronności. **EDIP** (europejski program przemysłu obronnego) wspiera produkcję i gotowość przemysłu. W portalu UE oba są pod kodem programu EDF, a tematy EDIP mają identyfikatory `EDF-EDIP-…`.
- **Bezpieczeństwo cywilne** (ochrona granic, zarządzanie kryzysowe, cyberbezpieczeństwo, odporność infrastruktury) ma własne programy: Horyzont Europa klaster 3, Cyfrowa Europa (ECCC) i Fundusz Bezpieczeństwa Wewnętrznego (ISF).
- **Kredyt, gwarancja i inwestycja kapitałowa to nie grant.** Przykłady: EIC STEP Scale Up Defence (tylko inwestycja kapitałowa) i NATO Innovation Fund (fundusz venture capital). Kredyt BGK na produkty podwójnego zastosowania to kredyt z premią: dotacja spłaca część jego kapitału, ale najpierw trzeba dostać kredyt w banku. Pokazuj je osobno i oznacz.

## W portalu Funding & Tenders (skrypt `nabory_ue.py`)

| Co | Polecenie | Uwagi |
|---|---|---|
| EDF i EDIP | `szukaj --program EDF` | 16.11.2026: 10 naborów, w tym 7 tematów EDIP z terminem 16.02.2027 (m.in. systemy bezzałogowe i antydronowe, obrona przeciwlotnicza, C5ISR) |
| Tylko EDIP | `szukaj --prefiks EDF-EDIP` | |
| Nabory kaskadowe EDF dla MŚP i startupów | `szukaj --program EDF --typ kaskadowe` | małe kwoty, często bez konsorcjum (16.11.2026 np. BATTLEVERSE i D-STORM) |
| EIC STEP Scale Up Defence | `szukaj --prefiks HORIZON-EIC` | identyfikator `HORIZON-EIC-2027-DEFENCE-01`, termin 1.06.2027; inwestycja kapitałowa, nie dotacja |
| EIC Accelerator dla dual use | `temat HORIZON-EIC-2027-ACCELERATOR-01` | dotacja dla jednego MŚP; warunki dual use w programie pracy EIC |
| Bezpieczeństwo cywilne | `szukaj --prefiks HORIZON-CL3` | 16.11.2026: 21 tematów |
| Cyberbezpieczeństwo | `szukaj --prefiks DIGITAL-ECCC` | 16.11.2026: 11 tematów, w tym `DIGITAL-ECCC-2027-DEPLOY-CYBER-11-DUALUSE` |
| Fundusz Bezpieczeństwa Wewnętrznego | `szukaj --program ISF` | |

**EIC STEP Scale Up Defence.** Rozporządzenie 2025/2653 („defence mini-omnibus”, w mocy od 23.12.2025) rozszerzyło platformę STEP na technologie obronne. Nabór jest dla firm, które pozyskują rundę od 50 do 150 mln EUR i chcą szybko urosnąć w sektorze obronnym. Wybrane firmy dostają wyłącznie inwestycję kapitałową od 10 do 30 mln EUR, bez dotacji. Budżet na 2027 rok to 100 mln EUR. Technologie muszą pasować do 11 priorytetowych obszarów zdolności z wytycznych STEP. Rozwiązania dual use z wiarygodnym modelem biznesowym na rynku cywilnym i obronnym idą do zwykłego naboru STEP Scale Up. Źródło: https://eic.ec.europa.eu/eic-frequently-asked-questions/faqs-eic-strategic-technologies-europe-platform-step-scale-defence-call_en

## Poza portalem UE

| Źródło | Dla kogo i na co | Adres | Jak czytać |
|---|---|---|---|
| EUDIS (program innowacji obronnych UE, finansowany z EDF) | MŚP, startupy i nowi gracze w obronności: akcelerator, hackathony wiosną i jesienią, wyzwania technologiczne, otwarte nabory EDF dla MŚP i technologii przełomowych (granty ryczałtowe), nabory kaskadowe, doradztwo | https://eudis.europa.eu/ | zwykłe pobranie strony działa |
| EUDIS Business Accelerator | startupy i scale-upy z UE i Norwegii; rundy prowadzi operator, w 2026 roku Starburst | https://starburst.aero/news/eudis-business-accelerator-cohort-4-applications-are-now-open/ | termin rundy sprawdzaj na stronie operatora |
| NATO DIANA | akcelerator dla firm z państw NATO rozwijających technologie podwójnego zastosowania, nabory „challenges” zwykle raz w roku | https://www.diana.nato.int/challenges.html | blokuje zwykłe pobieranie, tylko przez Chrome |
| NATO SPS (Science for Peace and Security) | granty na badania, wydarzenia i szkolenia w dziedzinie bezpieczeństwa, z partnerami z państw partnerskich NATO | https://www.nato.int/en/about-us/organization/nato-structure/science-for-peace-and-security-hub | |
| NATO Innovation Fund | fundusz venture capital, nie grant | https://www.nif.fund/ | |
| Punkty kontaktowe EDF | bezpłatne doradztwo przy wnioskach do EDF | https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/support/ncp | w wyszukiwarce wybierz program EDF i Polskę |

## W Polsce

| Źródło | Co | Adres |
|---|---|---|
| Harmonogram FENG | nabory STEP w obronności: inwestycje (PARP) oraz B+R w dwóch ścieżkach (NCBR); 16.11.2026 terminy z harmonogramu z 9.11.2026, ogłoszenie zależy od zmian w programie | https://nowoczesnagospodarka.gov.pl/dokumenty/harmonogram-naborow-w-programie-fundusze-europejskie-dla-nowoczesnej-gospodarki/ |
| Granty na Eurogranty (PARP, FENG 2.12) | dotacja dla MŚP i organizacji badawczych na przygotowanie wniosku do programu UE, w tym do EDF i EDIP | https://www.parp.gov.pl/harmonogram-naborow/grants/granty-na-eurogranty-1 (przez Chrome) |
| FNP First Team (FENG 2.2), nabór dual use | zespoły badawcze w organizacjach badawczych, technologie podwójnego zastosowania | https://www.fnp.org.pl/component/fnp_programs/program/first-team-feng/nabor-2-2026 |
| NCBR | konkursy B+R, w tym obronne i ścieżki STEP | https://www.gov.pl/web/ncbr/platforma-konkursowa/ |
| Programy regionalne | działania dual use i przemysł obronny, 16.11.2026 m.in. w podlaskim, śląskim, opolskim, łódzkim, a w małopolskim, lubuskim, zachodniopomorskim i kujawsko-pomorskim kompetencje i gotowość cywilna | katalog: `katalog_grantow.py --temat Bezpieczeństwo --zasieg Regionalne` |
| BGK (FENG 2.33) | kredyt na wytwarzanie produktów podwójnego zastosowania z premią, która refunduje część kapitału kredytu; najpierw kredyt w banku, więc to nie czysta dotacja | https://www.bgk.pl/produkty/kredyt-na-wytwarzanie-produktow-podwojnego-zastosowania/ |

## Warunki, które w obronności odsiewają najczęściej

Sprawdź je w ogłoszeniu i w programie pracy, zanim polecisz nabór:

1. **Kontrola właścicielska.** W EDF odbiorcy i podwykonawcy nie mogą być kontrolowani przez niestowarzyszone państwo trzecie ani podmiot z takiego państwa (art. 9 rozporządzenia 2021/697). Odstępstwo wymaga gwarancji zatwierdzonych przez państwo siedziby. Inwestor spoza UE w strukturze właścicielskiej to sygnał do sprawdzenia.
2. **Konsorcjum.** W EDF działanie prowadzi zwykle konsorcjum co najmniej trzech kwalifikujących się podmiotów z co najmniej trzech różnych państw członkowskich lub stowarzyszonych (art. 10 rozporządzenia 2021/697). Wyjątki i warunki EDIP podaje program pracy.
3. **Informacje niejawne.** Jeśli temat ma informacje niejawne, sprawdź, czy potrzebne jest świadectwo bezpieczeństwa przemysłowego i poświadczenia dla osób. Wydaje je ABW, a dla jednostek wojskowych SKW (ustawa o ochronie informacji niejawnych). Uzyskanie trwa miesiącami, więc zaznacz to od razu.
4. **Kontrola eksportu.** Towary i technologie dual use podlegają rozporządzeniu (UE) 2021/821, a w Polsce ustawie o obrocie z zagranicą towarami, technologiami i usługami o znaczeniu strategicznym. Przy współpracy z partnerami spoza UE wskaż, że trzeba to sprawdzić.
5. **Koncesja.** Wytwarzanie i obrót technologią o przeznaczeniu wojskowym lub policyjnym wymaga koncesji ministra spraw wewnętrznych. Nabór na wdrożenie produktu wojskowego może tego wymagać od wnioskodawcy.
6. **Etyka i cel cywilny.** W Horyzoncie Europa projekt z zastosowaniem wojskowym odpada. W EDF ocena obejmuje kwestie etyczne opisane w programie pracy.

Punktów 3–5 nie oceniasz sam. Wskaż, co sprawdzić i u kogo (prawnik, ABW lub SKW, departament ministerstwa właściwy dla kontroli obrotu towarami strategicznymi).
