# API wyszukiwania portalu Funding & Tenders

Notatki do utrzymania skryptu `scripts/nabory_ue.py`. Stan sprawdzony 15.11.2026. Czytaj, gdy skrypt zwraca błąd albo dziwne wyniki.

## Punkty dostępu

- Wyszukiwanie: `POST https://api.tech.ec.europa.eu/search-api/prod/rest/search?apiKey=SEDIA&text=...&pageSize=...&pageNumber=...`
- Fasety (słowniki z liczbami): `POST https://api.tech.ec.europa.eu/search-api/prod/rest/facet?apiKey=SEDIA&text=***`

Klucz `SEDIA` jest publiczny, używa go strona portalu. Treść żądania to `multipart/form-data` z polami JSON:

- `query`: zapytanie w stylu Elasticsearch, `{"bool": {"must": [...], "must_not": [...]}}` z warunkami `terms`, `range`, `exists`;
- `languages`: `["en"]`;
- `sort`: np. `{"field": "sortStatus", "order": "ASC"}`. Bez tego pola wyniki są ułożone według trafności (pole `weight`).

`text=***` oznacza wszystko. Większe strony niż 100 wyników API przycina do 100.

## Kody

| Pole | Wartość | Znaczenie |
|---|---|---|
| `type` | `0` | przetarg instytucji UE (`--typ przetargi`, domyślnie pomijany) |
| | `1` | temat grantowy programu UE |
| | `2` | zaproszenie do składania wniosków w pomocy zewnętrznej (EuropeAid, Prospect) |
| | `8` | nabór kaskadowy, ogłaszany przez projekt UE (wsparcie dla stron trzecich) |
| `status` | `31094501` | zapowiedziany |
| | `31094502` | otwarty |
| | `31094503` | zamknięty |
| `frameworkProgramme` | np. `43108390` | Horizon Europe; pełny słownik daje faseta `frameworkProgramme` (polecenie `programy`) |
| `crossCuttingPriorities` | np. `AI`, `DigitalAgenda` | tagi przekrojowe, słownik w fasecie o tej nazwie |

EDIP nie ma osobnego kodu programu. Jego tematy są pod `frameworkProgramme` EDF (`44181033`) i mają identyfikatory `EDF-EDIP-…` (stan 16.11.2026).

## Pułapki

1. **Status bywa nieaktualny.** Setki rekordów ze statusem „otwarty” mają wszystkie terminy w przeszłości. Filtr: `{"range": {"deadlineDate": {"gte": "RRRR-MM-DDT00:00:00.000+0000"}}}`. Działa tylko pełny znacznik czasu. Sama data (`2026-11-15`) jest po cichu ignorowana i zwraca wszystko.
2. **Pola są listami.** `deadlineDate` ma kilka wartości przy naborach z wieloma terminami odcięcia. Zakres w filtrze spełnia rekord, który ma choć jeden termin w zakresie, więc następny termin trzeba wybrać po stronie skryptu.
3. **Godzina.** Terminy mają często 17:00 z oznaczeniem `+0000`, a część rekordów samą datę (00:00). Portal pokazuje terminy w czasie brukselskim. Skrypt nie przelicza stref, a przy 00:00 pokazuje samą datę. Godzinę potwierdzaj na stronie tematu.
4. **Wyszukiwanie tekstowe łapie dowolne ze słów** i nie obsługuje fraz w cudzysłowie (zwraca zero wyników). Frazę sprawdza skrypt w treści rekordu (`--fraza`).
5. **Nabory kaskadowe mają identyfikator i adres projektu-matki.** Jeden projekt potrafi mieć kilkanaście osobnych naborów z tym samym `identifier` i tym samym `url` (strona projektu z listą jego naborów). Tytuł naboru jest w `callTitle`, organizator w `projectAcronym`. Powtórki odsiewa się po polu `reference`, które jest unikalne dla rekordu. Odsiewanie po `url` gubi prawdziwe nabory.
6. **Budżet.** U tematów grantowych w `budgetOverview` (tekst JSON): `budgetTopicActionMap` z pozycjami `action`, `minContribution`, `maxContribution`, `expectedGrants`, `budgetYearMap`, `deadlineDates`. Mapa obejmuje cały nabór, więc pozycje tematu wybiera się po początku nazwy `action` („IDENTYFIKATOR - …”). Część tematów ma `minContribution` i `maxContribution` wpisane w milionach (np. `15` przy `budgetYearMap` 15 000 000); skrypt przelicza wartości poniżej 1000. U naborów kaskadowych i zewnętrznych jest pole `budget` (cały nabór) i czasem `currency`.
7. **Treść.** Opis tematu w `descriptionByte`, warunki w `topicConditions` (HTML, miejscami popsuty). U naborów kaskadowych opis w `description` i `furtherInformation`, warunki w `beneficiaryAdministration`.
8. **Rekordy bez terminu** (`must_not exists deadlineDate`) to w praktyce stare ogłoszenia EuropeAid. Skrypt je pomija.
9. **Przetargi (`type` 0)** mają zamawiającego w `cftLeadContractingAuthorityCode` (tekst JSON z listą instytucji i polem `isLeadAuthority`), szacunkową wartość w `cftEstimatedOverallContractAmount` i `cftEstimatedOverallContractCurrency`, kody CPV w `mainCpv`, numer postępowania w `callIdentifier`, a link do strony przetargu (`.../tender-details/ID`) w `url`. Pole `caName` to zwykle tytuł, nie zamawiający. Przetargi zapowiedziane i zaproszenia do wyrażenia zainteresowania (`-EXA`) często nie mają `deadlineDate`, więc filtr terminu je pomija. Stan 16.11.2026.
10. **Strony tematów** (`.../topic-details/ID`) są aplikacją ładowaną skryptem. Zwykłe pobranie strony zwraca pustą powłokę. Treść bierz z API, a dokumenty naboru otwieraj w przeglądarce.
