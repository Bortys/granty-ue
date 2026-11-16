# Granty i dotacje: skill do Claude

Skill do Claude, który szuka otwartych i zapowiedzianych naborów na granty i dotacje oraz przetargów publicznych, sprawdza warunki udziału i oddaje krótką listę z terminami, kwotami i linkami do ogłoszeń. Autor: [Bartosz Sokoliński](https://sokolinski.com).

Obejmuje:

- **programy UE:** Horyzont Europa z EIC, misjami i wspólnymi przedsięwzięciami (np. EuroHPC, CBE, Chips, Clean Hydrogen), Cyfrowa Europa, LIFE, Innovation Fund, CEF, Kreatywna Europa, Erasmus+, CERV i nabory kaskadowe ogłaszane przez projekty UE;
- **obronność i technologie podwójnego zastosowania (dual use):** EDF z EDIP, EUDIS, EIC STEP Defence, NATO DIANA i NATO SPS, nabory obronne w FENG i w programach regionalnych;
- **fundusze europejskie w Polsce:** FENG, FEPW, FERC, FERS, FEnIKS, 16 programów regionalnych, KPO;
- **programy krajowe:** NCBR, NCN, NAWA, FNP, ABM, NFOŚiGW z Funduszem Modernizacyjnym, ARiMR, NIW, ministerstwa i Krajowy Fundusz Szkoleniowy w powiatowych urzędach pracy;
- **źródła lokalne i międzynarodowe:** konkursy ofert samorządów, fundacje, Fundusze EOG, Interreg i Interreg Europe, wspólne konkursy partnerstw europejskich (np. CETP, ERA-NET) z finansowaniem z NCBR albo NCN, Eureka, COST, EIT, ESA, European Urban Initiative, URBACT, Fundusz Wyszehradzki;
- **agendy badawcze i przetargi:** kontrakty i rejestracja dostawców w ESA, EUSPA, CERN (z zapowiedziami przetargów), ESO, EUMETSAT, EU SST, F4E i ECMWF, ośrodki inkubacji ESA BIC, CASSINI, przetargi Komisji i agencji UE (np. EDA), TED z polskimi zamawiającymi i Agencją Uzbrojenia, Biuletyn Zamówień Publicznych, Baza Konkurencyjności, zamówienia przedkomercyjne (PCP).

Instrukcje i odpowiedzi są po polsku.

## Jak działa

1. Pyta, kto składa wniosek i na co: forma prawna, wielkość, region, etap projektu, kwota, termin. U naukowca także rok doktoratu.
2. Przegląda katalog [Kierunek Grant](https://sokolinski.com/granty/): ponad 750 naborów z kilkudziesięciu źródeł, z polskimi tytułami.
3. Pobiera nabory z oficjalnego API wyszukiwania portalu Funding & Tenders. Odsiewa tematy, których terminy minęły, bo portal oznacza jako „otwarte” także tematy z terminami z 2023 roku.
4. Czyta strony instytucji, których brakuje w katalogu i w portalu UE.
5. Przy obronności i dual use sprawdza warunki, które najczęściej odsiewają: kontrolę właścicielską, skład konsorcjum, informacje niejawne, kontrolę eksportu i koncesje.
6. Gdy wnioskodawca może sprzedawać usługi, sprzęt albo prace badawczo-rozwojowe, szuka przetargów w portalu UE i w TED i pokazuje je osobno, bo przetarg to zamówienie, a nie dotacja.
7. Ocenia dopasowanie słowami (mocne, możliwe, słabe) i odpowiada w stałym układzie: najlepiej pasujące nabory, do sprawdzenia, odpadające, od czego zacząć, źródła.

## Co jest w środku

| Plik | Co zawiera |
|---|---|
| `SKILL.md` | instrukcja dla Claude w dziewięciu krokach |
| `scripts/nabory_ue.py` | wyszukiwanie w API Funding & Tenders: polecenia `szukaj`, `temat` i `programy`, także przetargi instytucji UE (`--typ przetargi`) |
| `scripts/przetargi_ted.py` | wyszukiwanie przetargów w API TED: tekst, kody CPV, zamawiający, kraj, termin, zapowiedzi |
| `scripts/katalog_grantow.py` | wyszukiwanie w katalogu Kierunek Grant: tekst, temat, wnioskodawca, zasięg, województwo, termin, rodzaj (nabory, zamówienia agend, konsultacje rynkowe) |
| `references/zrodla-pl.md` | polskie źródła: listy zbiorcze, programy, 16 portali regionalnych, instytucje, samorządy, fundacje |
| `references/zrodla-zagraniczne.md` | programy międzynarodowe spoza portalu UE |
| `references/obronnosc.md` | obronność, bezpieczeństwo i dual use: źródła, polecenia, warunki |
| `references/agendy-i-zamowienia.md` | agendy badawcze jako zamawiający, gdzie szukać przetargów, PCP, warunki udziału |
| `references/api-ft.md` | notatki o API portalu i jego pułapkach |

Skrypty używają tylko biblioteki standardowej Pythona (3.9 lub nowszego), więc niczego nie trzeba instalować. Łączą się z `api.tech.ec.europa.eu`, `api.ted.europa.eu` i `sokolinski.com`.

## Instalacja

- **Claude Code:** skopiuj folder do `~/.claude/skills/granty-ue/` (skill dla ciebie we wszystkich projektach) albo do `.claude/skills/granty-ue/` w repozytorium projektu.
- **claude.ai:** spakuj folder do pliku ZIP (folder `granty-ue` z `SKILL.md` w środku) i dodaj go jako skill w ustawieniach (Customize → Skills). Skrypty potrzebują wykonywania kodu z dostępem do trzech domen wymienionych wyżej. Jeśli środowisko blokuje sieć, skill może korzystać tylko z przeglądarki.

Kilka stron ładuje wyniki skryptem albo blokuje zwykłe pobieranie (wyszukiwarka dotacji, WOD2021, PARP, NCN, NATO DIANA, Eureka, esa-star, e-Zamówienia, Baza Konkurencyjności). Skill czyta je wtedy przez Claude in Chrome, jeśli jest dostępny, a w przeciwnym razie oznacza je jako „do sprawdzenia”.

## Przykłady

Wystarczy zapytać Claude zwykłymi słowami, np. „gdzie dostać dotację na system antydronowy dla małej firmy z Warszawy” albo „jakie są nabory dla fundacji z Lublina, która uczy seniorów”. Skrypty da się też uruchomić samodzielnie z folderu skilla:

```bash
python3 scripts/katalog_grantow.py --temat Bezpieczeństwo --wnioskodawca Firmy Startupy
```

```bash
python3 scripts/katalog_grantow.py --wnioskodawca NGO --zasieg Regionalne --wojewodztwo lubelskie
```

```bash
python3 scripts/nabory_ue.py szukaj --priorytet AI --program HORIZON DIGITAL --status otwarte
```

```bash
python3 scripts/nabory_ue.py szukaj --program EDF ISF
```

```bash
python3 scripts/nabory_ue.py temat HORIZON-EIC-2027-ACCELERATOR-01
```

```bash
python3 scripts/nabory_ue.py szukaj --typ przetargi --tekst satellite
```

```bash
python3 scripts/przetargi_ted.py --tekst 'dron*' 'bezzałog*' UAV --cpv 34711200 35
```

```bash
python3 scripts/przetargi_ted.py --cpv 73 --kraj POL --zapowiedzi
```

## Zastrzeżenia

- To nie jest porada prawna ani finansowa. Przy pomocy publicznej, umowach, kontroli eksportu i koncesjach skill wskazuje, co sprawdzić i u kogo, ale nie ocenia zgodności z prawem.
- Katalog i API to tropy. Terminy, kwoty i warunki potwierdzaj zawsze w ogłoszeniu instytucji, która prowadzi nabór.
- Adresy i fakty w plikach `references/` są sprawdzone 16.11.2026. Programy prac i harmonogramy zmieniają się co rok.
- Klucz `SEDIA` w skrypcie to publiczny klucz, którego używa strona portalu Funding & Tenders. API TED działa bez klucza. Skrypty nie są oficjalnymi narzędziami Komisji Europejskiej ani Urzędu Publikacji UE.
- Przetarg to zamówienie, a nie dotacja. Skill znajduje ogłoszenia i wskazuje warunki udziału, ale nie przygotowuje oferty i nie ocenia jej zgodności z prawem zamówień publicznych.
- Skill niczego nie składa (ani wniosków, ani ofert), nie rejestruje i do nikogo nie pisze. Przygotowuje listę, a decyzję podejmuje człowiek.

## Licencja

Kod i instrukcje są na licencji [MIT](LICENSE). Możesz ich używać, zmieniać je i rozpowszechniać, także komercyjnie. Przy rozpowszechnianiu dołącz informację o autorstwie (Copyright (c) 2026 Bartosz Sokoliński) i treść licencji.

Licencja nie obejmuje danych z katalogu Kierunek Grant, portalu Funding & Tenders ani TED. Należą one do swoich źródeł.

## In English

A Claude skill that finds open and upcoming grant calls: EU programmes (Horizon Europe with EIC, missions and joint undertakings, Digital Europe, LIFE, Innovation Fund, CEF, Creative Europe, Erasmus+, CERV, cascade funding), co-funded European partnership calls, defence and dual-use funding (EDF with EDIP, EUDIS, EIC STEP Defence, NATO DIANA and SPS), EU cohesion funds in Poland, Polish national programmes, local calls and foundations. It also covers contracts with research agencies (ESA, EUSPA, CERN, ESO, F4E) and public tenders from the Funding & Tenders portal and TED, shown separately from grants. It queries the official Funding & Tenders search API, the TED API and the Kierunek Grant catalogue, checks eligibility and returns a short list with deadlines, amounts and links. Instructions and answers are in Polish. Scripts need only the Python standard library. MIT licence.
