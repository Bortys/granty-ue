# Granty i dotacje: skill do Claude

Skill do Claude, który szuka otwartych i zapowiedzianych naborów na granty i dotacje, sprawdza warunki udziału i oddaje krótką listę z terminami, kwotami i linkami do ogłoszeń. Autor: [Bartosz Sokoliński](https://sokolinski.com).

Obejmuje:

- **programy UE:** Horyzont Europa z EIC, Cyfrowa Europa, LIFE, Kreatywna Europa, Erasmus+, CERV i nabory kaskadowe ogłaszane przez projekty UE;
- **obronność i technologie podwójnego zastosowania (dual use):** EDF z EDIP, EUDIS, EIC STEP Defence, NATO DIANA i NATO SPS, nabory obronne w FENG i w programach regionalnych;
- **fundusze europejskie w Polsce:** FENG, FEPW, FERC, FERS, FEnIKS, 16 programów regionalnych, KPO;
- **programy krajowe:** NCBR, NCN, NAWA, FNP, ABM, NFOŚiGW, ARiMR, NIW i ministerstwa;
- **źródła lokalne i międzynarodowe:** konkursy ofert samorządów, fundacje, Fundusze EOG, Interreg, Eureka, EIT, ESA, Fundusz Wyszehradzki.

Instrukcje i odpowiedzi są po polsku.

## Jak działa

1. Pyta, kto składa wniosek i na co: forma prawna, wielkość, region, etap projektu, kwota, termin. U naukowca także rok doktoratu.
2. Przegląda katalog [Kierunek Grant](https://sokolinski.com/granty/): ponad 750 naborów z kilkudziesięciu źródeł, z polskimi tytułami.
3. Pobiera nabory z oficjalnego API wyszukiwania portalu Funding & Tenders. Odsiewa tematy, których terminy minęły, bo portal oznacza jako „otwarte” także tematy z terminami z 2023 roku.
4. Czyta strony instytucji, których brakuje w katalogu i w portalu UE.
5. Przy obronności i dual use sprawdza warunki, które najczęściej odsiewają: kontrolę właścicielską, skład konsorcjum, informacje niejawne, kontrolę eksportu i koncesje.
6. Ocenia dopasowanie słowami (mocne, możliwe, słabe) i odpowiada w stałym układzie: najlepiej pasujące nabory, do sprawdzenia, odpadające, od czego zacząć, źródła.

## Co jest w środku

| Plik | Co zawiera |
|---|---|
| `SKILL.md` | instrukcja dla Claude w ośmiu krokach |
| `scripts/nabory_ue.py` | wyszukiwanie w API Funding & Tenders: polecenia `szukaj`, `temat` i `programy` |
| `scripts/katalog_grantow.py` | wyszukiwanie w katalogu Kierunek Grant: tekst, temat, wnioskodawca, zasięg, województwo, termin |
| `references/zrodla-pl.md` | polskie źródła: listy zbiorcze, programy, 16 portali regionalnych, instytucje, samorządy, fundacje |
| `references/zrodla-zagraniczne.md` | programy międzynarodowe spoza portalu UE |
| `references/obronnosc.md` | obronność, bezpieczeństwo i dual use: źródła, polecenia, warunki |
| `references/api-ft.md` | notatki o API portalu i jego pułapkach |

Skrypty używają tylko biblioteki standardowej Pythona (3.9 lub nowszego), więc niczego nie trzeba instalować. Łączą się z `api.tech.ec.europa.eu` i `sokolinski.com`.

## Instalacja

- **Claude Code:** skopiuj folder do `~/.claude/skills/granty-ue/` (skill dla ciebie we wszystkich projektach) albo do `.claude/skills/granty-ue/` w repozytorium projektu.
- **claude.ai:** spakuj folder do pliku ZIP (folder `granty-ue` z `SKILL.md` w środku) i dodaj go jako skill w ustawieniach (Customize → Skills). Skrypty potrzebują wykonywania kodu z dostępem do dwóch domen wymienionych wyżej. Jeśli środowisko blokuje sieć, skill może korzystać tylko z przeglądarki.

Kilka stron ładuje wyniki skryptem albo blokuje zwykłe pobieranie (wyszukiwarka dotacji, WOD2021, PARP, NCN, NATO DIANA, Eureka). Skill czyta je wtedy przez Claude in Chrome, jeśli jest dostępny, a w przeciwnym razie oznacza je jako „do sprawdzenia”.

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

## Zastrzeżenia

- To nie jest porada prawna ani finansowa. Przy pomocy publicznej, umowach, kontroli eksportu i koncesjach skill wskazuje, co sprawdzić i u kogo, ale nie ocenia zgodności z prawem.
- Katalog i API to tropy. Terminy, kwoty i warunki potwierdzaj zawsze w ogłoszeniu instytucji, która prowadzi nabór.
- Adresy i fakty w plikach `references/` są sprawdzone 16.11.2026. Programy prac i harmonogramy zmieniają się co rok.
- Klucz `SEDIA` w skrypcie to publiczny klucz, którego używa strona portalu Funding & Tenders. Skrypt nie jest oficjalnym narzędziem Komisji Europejskiej.
- Skill niczego nie składa, nie rejestruje i do nikogo nie pisze. Przygotowuje listę, a decyzję podejmuje człowiek.

## Licencja

Kod i instrukcje są na licencji [MIT](LICENSE). Możesz ich używać, zmieniać je i rozpowszechniać, także komercyjnie. Przy rozpowszechnianiu dołącz informację o autorstwie (Copyright (c) 2026 Bartosz Sokoliński) i treść licencji.

Licencja nie obejmuje danych z katalogu Kierunek Grant ani z portalu Funding & Tenders. Należą one do swoich źródeł.

## In English

A Claude skill that finds open and upcoming grant calls: EU programmes (Horizon Europe with EIC, Digital Europe, LIFE, Creative Europe, Erasmus+, CERV, cascade funding), defence and dual-use funding (EDF with EDIP, EUDIS, EIC STEP Defence, NATO DIANA and SPS), EU cohesion funds in Poland, Polish national programmes, local calls and foundations. It queries the official Funding & Tenders search API and the Kierunek Grant catalogue, checks eligibility and returns a short list with deadlines, amounts and links. Instructions and answers are in Polish. Scripts need only the Python standard library. MIT licence.
