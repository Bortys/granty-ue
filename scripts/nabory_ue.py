#!/usr/bin/env python3
"""Nabory UE z oficjalnego API wyszukiwania portalu Funding & Tenders.

Tylko biblioteka standardowa Pythona, bez instalowania pakietów. Klucz
„SEDIA” jest publiczny: tego samego używa strona portalu w przeglądarce.

Polecenia:
  szukaj   lista otwartych i zapowiedzianych naborów z przyszłym terminem
  temat    szczegóły jednego tematu: budżet, terminy, opis, warunki
  programy słownik programów i priorytetów z liczbą aktualnych naborów

Przykłady:
  python3 nabory_ue.py szukaj --tekst "large language models" --program HORIZON DIGITAL
  python3 nabory_ue.py szukaj --priorytet AI --status otwarte --termin-do 2027-03-31
  python3 nabory_ue.py szukaj --typ kaskadowe --tekst "SME cybersecurity"
  python3 nabory_ue.py szukaj --program EDF ISF        (obronność: EDF z tematami EDIP, Fundusz Bezpieczeństwa Wewnętrznego)
  python3 nabory_ue.py szukaj --typ przetargi --tekst satellite   (zamówienia Komisji i agencji UE, np. EDA, EUSPA, JRC)
  python3 nabory_ue.py temat HORIZON-CL4-2027-01-DIGITAL-EMERGING-01
  python3 nabory_ue.py programy
"""

import argparse
import datetime as dt
import html
import http.client
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import uuid

API = "https://api.tech.ec.europa.eu/search-api/prod/rest"
KLUCZ = "SEDIA"
UA = "granty-ue/1.0 (skill Claude; python-urllib)"
STRONA = 100  # API nie oddaje więcej niż 100 wyników na stronę

TYPY = {"granty": "1", "kaskadowe": "8", "zewnetrzne": "2", "przetargi": "0"}
TYPY_NABOROW = ["1", "8", "2"]  # przetargi nie mają programu, więc nie wchodzą do słownika programów
TYP_NAZWA = {"1": "grant", "8": "kaskadowy", "2": "zewnętrzny", "0": "przetarg"}
STATUSY = {"zapowiedziane": "31094501", "otwarte": "31094502"}
STATUS_NAZWA = {"31094501": "zapowiedziany", "31094502": "otwarty", "31094503": "zamknięty"}


# ---------- komunikacja z API ----------

def _post(endpoint, params, pola):
    granica = uuid.uuid4().hex
    tresc = b""
    for nazwa, wartosc in pola.items():
        tresc += (
            f"--{granica}\r\n"
            f'Content-Disposition: form-data; name="{nazwa}"; filename="blob"\r\n'
            "Content-Type: application/json\r\n\r\n"
        ).encode() + json.dumps(wartosc).encode() + b"\r\n"
    tresc += f"--{granica}--\r\n".encode()
    url = f"{API}/{endpoint}?" + urllib.parse.urlencode({"apiKey": KLUCZ, **params})
    zapytanie = urllib.request.Request(
        url,
        data=tresc,
        method="POST",
        headers={
            "Content-Type": f"multipart/form-data; boundary={granica}",
            "User-Agent": UA,
            "Accept": "application/json",
        },
    )
    ostatni_blad = None
    for proba in range(4):
        try:
            with urllib.request.urlopen(zapytanie, timeout=120) as odp:
                return json.load(odp)
        # OSError obejmuje URLError, TimeoutError i zerwane połączenia (ConnectionResetError),
        # które API zwraca przy kilku równoległych zapytaniach
        except (OSError, http.client.HTTPException, json.JSONDecodeError) as blad:
            ostatni_blad = blad
            time.sleep(2 ** (proba + 1))
    sys.exit(f"Błąd API Funding & Tenders ({endpoint}): {ostatni_blad}")


def _czas_api(d):
    """Format, który API rozumie w filtrze zakresu (sama data jest ignorowana)."""
    return d.strftime("%Y-%m-%dT%H:%M:%S.000+0000")


def _data_z_precyzja(tekst):
    """Parsuje datę i zachowuje informację, czy źródło podało samą datę."""
    if not tekst:
        return None
    tekst = tekst.replace("Z", "+0000")
    formaty = (
        ("%Y-%m-%dT%H:%M:%S.%f%z", False),
        ("%Y-%m-%dT%H:%M:%S%z", False),
        ("%Y-%m-%d", True),
    )
    for wzor, tylko_data in formaty:
        try:
            d = dt.datetime.strptime(tekst, wzor)
            d = d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)
            return d, tylko_data
        except ValueError:
            continue
    return None


def _data(tekst):
    """Zwraca datetime, zachowując dotychczasowy interfejs dla pozostałych pól."""
    wynik = _data_z_precyzja(tekst)
    return wynik[0] if wynik else None


def _pokaz_date(d, z_godzina=True):
    if not d:
        return "brak"
    # Część rekordów ma samą datę (godzina 00:00). Wtedy nie udajemy, że znamy godzinę.
    if not z_godzina or (d.hour, d.minute) == (0, 0):
        return d.strftime("%Y-%m-%d")
    return d.strftime("%Y-%m-%d %H:%M")


def _czy_termin_aktualny(termin, teraz, tylko_data=False):
    """Sprawdza termin; sama data pozostaje ważna do końca dnia UTC."""
    if tylko_data:
        dzis_utc = teraz.astimezone(dt.timezone.utc).date()
        data_utc = termin.astimezone(dt.timezone.utc).date()
        return data_utc >= dzis_utc
    return termin >= teraz


def _typy_dzialan(lista):
    """Skraca nazwy typów działań: bez przedrostka programu, bez powtórzeń."""
    wynik = []
    for t in lista or []:
        t = re.sub(r"\s+", " ", t).strip()
        t = re.sub(r"^(HORIZON|DIGITAL|EDF|LIFE|CEF|EU4H|SMP|ERASMUS|CERV|CREA)( JU)? ", "", t)
        if t not in wynik:
            wynik.append(t)
    return ", ".join(wynik) or None


def slowniki(zapytanie=None):
    """Programy i priorytety z faset API: {kod: (skrót, nazwa, liczba)}."""
    if zapytanie is None:
        zapytanie = {"bool": {"must": [{"terms": {"type": TYPY_NABOROW}}]}}
    dane = _post("facet", {"text": "***"}, {"query": zapytanie, "languages": ["en"]})
    wynik = {}
    for faseta in dane.get("facets", []):
        pozycje = {}
        for v in faseta.get("values", []):
            nazwa = (v.get("value") or "").strip()
            skrot = re.findall(r"\(([^()]+)\)", nazwa)
            skrot = re.sub(r"\s.*", "", skrot[-1].strip()) if skrot else v.get("rawValue")
            pozycje[v.get("rawValue")] = (skrot, nazwa, v.get("count"))
        wynik[faseta.get("name")] = pozycje
    return wynik


def kody_programow(nazwy, programy):
    kody, nieznane = [], []
    po_skrocie = {skrot.upper(): kod for kod, (skrot, _, _) in programy.items()}
    for n in nazwy:
        if n.isdigit():
            kody.append(n)
        elif n.upper() in po_skrocie:
            kody.append(po_skrocie[n.upper()])
        else:
            nieznane.append(n)
    if nieznane:
        dostepne = ", ".join(sorted(po_skrocie))
        sys.exit(f"Nieznany program: {', '.join(nieznane)}. Dostępne skróty: {dostepne}")
    return kody


# ---------- porządkowanie rekordów ----------

def _pole(m, klucz):
    w = m.get(klucz)
    if isinstance(w, list):
        return w[0] if w else None
    return w


def _budzet_tematu(m, identyfikator):
    """Z budgetOverview wyciąga pozycje dotyczące tego tematu."""
    surowe = _pole(m, "budgetOverview")
    if not surowe:
        return []
    try:
        mapa = json.loads(surowe).get("budgetTopicActionMap", {})
    except (json.JSONDecodeError, AttributeError):
        return []
    def _eur(x):
        # Część tematów ma dotację wpisaną w milionach (np. 15 zamiast 15000000).
        # Żaden grant UE nie wynosi poniżej 1000 EUR, więc takie liczby przeliczamy.
        if isinstance(x, (int, float)) and 0 < x < 1000:
            return x * 1_000_000
        return x

    pozycje = []
    for akcje in mapa.values():
        for a in akcje:
            nazwa = a.get("action", "")
            if identyfikator and not nazwa.startswith(identyfikator + " "):
                continue
            pozycje.append({
                "dzialanie": nazwa.split(" - ", 1)[-1],
                "dotacja_min": _eur(a.get("minContribution")),
                "dotacja_max": _eur(a.get("maxContribution")),
                "liczba_grantow": a.get("expectedGrants"),
                "budzet_lacznie": sum(int(x) for x in (a.get("budgetYearMap") or {}).values() if str(x).isdigit()),
                "otwarcie": a.get("plannedOpeningDate"),
                "terminy": a.get("deadlineDates"),
                "model": a.get("deadlineModel"),
            })
    return pozycje


def _kwota(x):
    if x in (None, "", 0):
        return None
    try:
        x = float(x)
    except (TypeError, ValueError):
        return str(x)
    if x >= 1_000_000:
        return f"{x / 1_000_000:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " mln"
    if x >= 1000:
        return f"{x / 1000:.0f} tys."
    return f"{x:.0f}"


def _na_projekt(b):
    if not b:
        return None
    mins = [p["dotacja_min"] for p in b if p["dotacja_min"]]
    maxs = [p["dotacja_max"] for p in b if p["dotacja_max"]]
    if not maxs:
        return None
    lo, hi = min(mins or maxs), max(maxs)
    return f"{_kwota(lo)} EUR" if lo == hi else f"{_kwota(lo)}–{_kwota(hi)} EUR"


def _zamawiajacy(m):
    """Przetarg: nazwy instytucji z cftLeadContractingAuthorityCode, najpierw instytucja prowadząca."""
    surowe = _pole(m, "cftLeadContractingAuthorityCode")
    try:
        lista = json.loads(surowe) if surowe else []
    except json.JSONDecodeError:
        return None
    if not isinstance(lista, list):  # bywa "null"
        return None
    lista = sorted((x for x in lista if isinstance(x, dict)), key=lambda x: not x.get("isLeadAuthority"))
    nazwy = list(dict.fromkeys((x.get("name") or "").strip() for x in lista if x.get("name")))
    if not nazwy:
        return None
    return nazwy[0] + (f" i {len(nazwy) - 1} innych" if len(nazwy) > 1 else "")


def rekord(wynik, teraz, programy):
    m = wynik.get("metadata", {})
    typ = _pole(m, "type")
    identyfikator = _pole(m, "identifier")
    tytul = _pole(m, "title") or ""
    organizator = None
    if typ == "8":  # nabór kaskadowy ogłasza projekt UE, temat to projekt-matka
        tytul = _pole(m, "callTitle") or tytul
        organizator = _pole(m, "projectAcronym")
    zamawiajacy = _zamawiajacy(m) if typ == "0" else None
    terminy = [
        parsed for parsed in (_data_z_precyzja(x) for x in (m.get("deadlineDate") or []))
        if parsed
    ]
    terminy.sort(key=lambda parsed: parsed[0])
    przyszle = [
        termin for termin, tylko_data in terminy
        if _czy_termin_aktualny(termin, teraz, tylko_data)
    ]
    kody = m.get("frameworkProgramme") or []
    program = ", ".join(programy.get(k, (k, k, 0))[0] for k in kody) or ("zamówienie UE" if typ == "0" else "?")
    budzet = _budzet_tematu(m, identyfikator) if typ == "1" else []
    if typ == "1":
        kwota = _na_projekt(budzet)
    elif typ == "0":  # przetarg: szacunkowa wartość całego zamówienia, nie kwota dla jednego wykonawcy
        b = _kwota(_pole(m, "cftEstimatedOverallContractAmount"))
        waluta = _pole(m, "cftEstimatedOverallContractCurrency") or ""
        kwota = f"{b} {waluta} (szacunkowa wartość zamówienia)".replace("  ", " ") if b else None
    else:
        b = _kwota(_pole(m, "budget"))
        kwota = f"{b} {_pole(m, 'currency') or ''} (cały nabór)".replace("  ", " ") if b else None
    tytul = unicodedata.normalize("NFKC", html.unescape(tytul)).strip()
    tresc = " ".join(str(x) for x in [
        tytul, _pole(m, "callTitle"), " ".join(m.get("keywords") or []),
        _pole(m, "descriptionByte"), _pole(m, "description"), _pole(m, "furtherInformation"),
    ] if x)
    tresc = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", html.unescape(re.sub(r"<[^>]+>", " ", tresc)))).lower()
    return {
        "identyfikator": identyfikator,
        "tytul": tytul,
        "typ": TYP_NAZWA.get(typ, typ),
        "status": STATUS_NAZWA.get(_pole(m, "status"), _pole(m, "status")),
        "program": program,
        "nabor": _pole(m, "callIdentifier"),
        "nazwa_naboru": _pole(m, "callTitle") if typ == "1" else None,
        "organizator_kaskady": organizator,
        "zamawiajacy": zamawiajacy,
        "cpv": (m.get("mainCpv") or []) if typ == "0" else [],
        "typ_dzialania": _typy_dzialan(m.get("typesOfAction")),
        "otwarcie": _pokaz_date(_data(_pole(m, "startDate")), False),
        "nastepny_termin": _pokaz_date(przyszle[0]) if przyszle else None,
        "wszystkie_terminy": [_pokaz_date(d) for d, _ in terminy],
        "model_skladania": _pole(m, "deadlineModel"),
        "na_projekt": kwota,
        "budzet": budzet,
        "priorytety": m.get("crossCuttingPriorities") or [],
        "szukanie_partnerow": _pole(m, "allowPartnerSearch") == "true",
        "link": wynik.get("url"),
        "_termin_sort": przyszle[0] if przyszle else None,
        "_waga": wynik.get("weight") or 0,
        "_tresc": tresc,
    }


def _bez_pol_wewnetrznych(r):
    return {k: v for k, v in r.items() if not k.startswith("_")}


def _unikalne_rekordy(wyniki, teraz, programy, widziane=None):
    """Przetwarza stronę wyników i usuwa powtórzenia po unikalnym API reference.

    Nie deduplikuje po URL: różne nabory kaskadowe jednego projektu mogą
    prowadzić do wspólnej strony projektu.
    """
    if widziane is None:
        widziane = set()

    rekordy = []
    for wynik in wyniki:
        pozycja = rekord(wynik, teraz, programy)
        klucz = wynik.get("reference") or (
            pozycja["link"], pozycja["tytul"], pozycja["nastepny_termin"]
        )
        if klucz in widziane:
            continue
        widziane.add(klucz)
        rekordy.append(pozycja)
    return rekordy


# ---------- polecenia ----------

def szukaj(arg):
    teraz = dt.datetime.now(dt.timezone.utc)
    programy = slowniki().get("frameworkProgramme", {})

    zakres = {"gte": _czas_api(teraz.replace(hour=0, minute=0, second=0, microsecond=0))}
    if arg.termin_do:
        koniec = dt.datetime.strptime(arg.termin_do, "%Y-%m-%d").replace(hour=23, minute=59, second=59, tzinfo=dt.timezone.utc)
        zakres["lte"] = _czas_api(koniec)
    warunki = [
        {"terms": {"type": [TYPY[t] for t in arg.typ]}},
        {"terms": {"status": [STATUSY[s] for s in arg.status]}},
        {"range": {"deadlineDate": zakres}},
    ]
    if arg.program:
        warunki.append({"terms": {"frameworkProgramme": kody_programow(arg.program, programy)}})
    if arg.priorytet:
        warunki.append({"terms": {"crossCuttingPriorities": arg.priorytet}})
    zapytanie = {"bool": {"must": warunki}}

    # API szuka dowolnego ze słów i nie zna fraz w cudzysłowie. Słowa z --fraza idą do API,
    # żeby zawęzić kandydatów, a całą frazę sprawdzamy niżej w treści tematu.
    tekst = " ".join(arg.tekst or []).strip()
    tekst = " ".join(x for x in [tekst, " ".join(arg.fraza or [])] if x).strip() or "***"
    sortuj = arg.sortuj or ("trafnosc" if tekst != "***" else "termin")
    pola = {"query": zapytanie, "languages": ["en"]}
    if sortuj == "termin":
        pola["sort"] = {"field": "sortStatus", "order": "ASC"}  # bez sortowania API układa według trafności

    rekordy, widziane, strona, lacznie = [], set(), 1, None
    while True:
        dane = _post("search", {"text": tekst, "pageSize": STRONA, "pageNumber": strona}, pola)
        lacznie = dane.get("totalResults", 0)
        wyniki = dane.get("results", [])
        rekordy.extend(_unikalne_rekordy(wyniki, teraz, programy, widziane))
        if not wyniki or strona * STRONA >= min(lacznie, arg.max_pobran):
            break
        strona += 1

    pobrane = len(rekordy)
    aktualne = [r for r in rekordy if r["_termin_sort"]]
    if arg.prefiks:
        przedrostki = tuple(p.upper() for p in arg.prefiks)
        aktualne = [r for r in aktualne if (r["identyfikator"] or "").upper().startswith(przedrostki)]
    if arg.fraza:
        frazy = [unicodedata.normalize("NFKC", f).lower() for f in arg.fraza]
        aktualne = [r for r in aktualne if all(f in r["_tresc"] for f in frazy)]
    if sortuj == "termin":
        aktualne.sort(key=lambda r: r["_termin_sort"])
    else:
        aktualne.sort(key=lambda r: -r["_waga"])
    pokazane = [_bez_pol_wewnetrznych(r) for r in aktualne[: arg.limit]]

    naglowek = {
        "zrodlo": "API wyszukiwania Funding & Tenders Portal (api.tech.ec.europa.eu, klucz SEDIA)",
        "pobrano": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "zapytanie": {"tekst": " ".join(arg.tekst) if arg.tekst else None, "fraza": arg.fraza, "prefiks": arg.prefiks, "program": arg.program,
                      "priorytet": arg.priorytet, "typ": arg.typ, "status": arg.status, "termin_do": arg.termin_do},
        "sortowanie": sortuj,
        "api_zwrocilo": lacznie,
        "pobrano_rekordow": pobrane,
        "po_filtrach": len(aktualne),
        "pokazano": len(pokazane),
        "uciete_przez_max_pobran": lacznie > arg.max_pobran,
    }
    if arg.json:
        print(json.dumps({"naglowek": naglowek, "nabory": pokazane}, ensure_ascii=False, indent=1))
        return

    print(f"Źródło: {naglowek['zrodlo']}, pobrano {naglowek['pobrano']}.")
    print(f"API zwróciło {lacznie}, po odsianiu nieaktualnych, duplikatów i filtrach: {len(aktualne)}, "
          f"pokazuję {len(pokazane)}, kolejność: {'najbliższy termin' if sortuj == 'termin' else 'trafność'}.")
    if naglowek["uciete_przez_max_pobran"]:
        print(f"Uwaga: pobrano tylko {arg.max_pobran} rekordów. Zawęź zapytanie albo podnieś --max-pobran.")
    print("Godzinę terminu potwierdź na stronie tematu: portal podaje czas brukselski.")
    if "przetargi" in arg.typ:
        print("Przetarg to zamówienie: umowa i wynagrodzenie za wykonanie, nie dotacja. Ofertę składa się "
              "przez eSubmission po zapoznaniu się z dokumentami zamówienia.")
    print()
    if not pokazane:
        print("Brak naborów z przyszłym terminem dla tego zapytania.")
        return
    print("| Następny termin | Status | Program | Identyfikator | Tytuł | Typ | Na projekt | Link |")
    print("|---|---|---|---|---|---|---|---|")
    for r in pokazane:
        tytul = r["tytul"].replace("|", "/")
        if len(tytul) > 90:
            tytul = tytul[:87] + "..."
        if r["organizator_kaskady"]:
            tytul += f" (projekt {r['organizator_kaskady']})"
        if r["zamawiajacy"]:
            tytul += f" (zamawiający: {r['zamawiajacy']})"
        typ = r["typ_dzialania"] or r["typ"] if r["typ"] == "grant" else r["typ"]
        if len(typ) > 60:
            typ = typ[:57] + "..."
        print(f"| {r['nastepny_termin']} | {r['status']} | {r['program']} | {r['identyfikator']} | {tytul} | "
              f"{typ} | {r['na_projekt'] or 'do sprawdzenia'} | {r['link']} |")


def _tekst_z_html(x, limit=None):
    if not x:
        return ""
    x = re.sub(r"(?i)<br\s*/?>", "\n", x)
    x = re.sub(r"(?i)<li[^>]*>", "\n- ", x)
    x = re.sub(r"(?i)</(p|div|h\d|ul|ol|tr)>", "\n", x)
    x = re.sub(r"<[^>]+>", "", x)
    x = html.unescape(x).replace("﻿", "")
    x = re.sub(r"[ \t]+", " ", x)
    x = re.sub(r"\n\s*\n+", "\n\n", x).strip().lstrip('">').strip()  # portal ma tu i ówdzie popsuty HTML
    if limit and len(x) > limit:
        x = x[:limit].rsplit(" ", 1)[0] + f"\n[... ucięte po {limit} znakach, pełna treść: --pelny]"
    return x


def temat(arg):
    teraz = dt.datetime.now(dt.timezone.utc)
    programy = slowniki().get("frameworkProgramme", {})
    zapytanie = {"bool": {"must": [{"terms": {"identifier": [arg.identyfikator]}},
                                   {"terms": {"type": list(TYPY.values())}}]}}
    dane = _post("search", {"text": "***", "pageSize": STRONA, "pageNumber": 1},
                 {"query": zapytanie, "languages": ["en"]})
    wyniki = dane.get("results", [])
    if not wyniki:
        sys.exit(f"Nie znaleziono tematu {arg.identyfikator}. Sprawdź identyfikator w wynikach polecenia szukaj.")
    wyniki.sort(key=lambda w: _pole(w.get("metadata", {}), "type") != "1")
    limit = None if arg.pelny else 4000
    for w in wyniki:
        r = rekord(w, teraz, programy)
        m = w.get("metadata", {})
        if arg.json:
            r = _bez_pol_wewnetrznych(r)
            r["opis"] = _tekst_z_html(_pole(m, "descriptionByte") or _pole(m, "description") or _pole(m, "furtherInformation"))
            r["warunki"] = _tekst_z_html(_pole(m, "topicConditions") or _pole(m, "beneficiaryAdministration"))
            print(json.dumps(r, ensure_ascii=False, indent=1))
            continue
        print(f"# {r['identyfikator']}: {r['tytul']}\n")
        print(f"Pobrano z API Funding & Tenders: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"Rodzaj: {r['typ']}; status w API: {r['status']}; program: {r['program']}")
        if r["nabor"]:
            print(f"Nabór: {r['nabor']}" + (f" ({r['nazwa_naboru']})" if r["nazwa_naboru"] else ""))
        if r["organizator_kaskady"]:
            print(f"Nabór kaskadowy ogłasza projekt: {r['organizator_kaskady']}")
        if r["zamawiajacy"]:
            print(f"Zamawiający: {r['zamawiajacy']}; CPV: {', '.join(r['cpv']) or '?'}")
        print(f"Otwarcie: {r['otwarcie']}; terminy: {', '.join(r['wszystkie_terminy']) or 'brak'}; "
              f"następny: {r['nastepny_termin'] or 'żaden (termin minął)'}; model: {r['model_skladania'] or '?'}")
        if r["typ"] == "przetarg":
            print(f"Wartość: {r['na_projekt'] or 'brak w danych portalu'}. To zamówienie, nie dotacja: "
                  "dokumenty, pytania i oferta przez eSubmission.")
        else:
            print(f"Typ działania: {r['typ_dzialania'] or '?'}; na projekt: {r['na_projekt'] or 'do sprawdzenia'}")
        if r["priorytety"]:
            print(f"Priorytety przekrojowe: {', '.join(r['priorytety'])}")
        if r["typ"] != "przetarg":
            print(f"Szukanie partnerów w portalu: {'tak' if r['szukanie_partnerow'] else 'nie albo brak danych'}")
        print(f"Link: {r['link']}\n")
        if r["budzet"]:
            print("## Budżet tematu\n")
            print("| Działanie | Dotacja na projekt (EUR) | Spodziewana liczba grantów | Budżet łącznie (EUR) | Terminy |")
            print("|---|---|---|---|---|")
            for p in r["budzet"]:
                lo, hi = _kwota(p["dotacja_min"]), _kwota(p["dotacja_max"])
                widelki = (lo or hi or "?") if lo == hi or not (lo and hi) else f"{lo}–{hi}"
                print(f"| {p['dzialanie']} | {widelki} | {p['liczba_grantow'] or '?'} | {_kwota(p['budzet_lacznie']) or '?'} | {', '.join(p['terminy'] or [])} |")
            print()
        opis = _tekst_z_html(_pole(m, "descriptionByte") or _pole(m, "description") or _pole(m, "furtherInformation"), limit)
        warunki = _tekst_z_html(_pole(m, "topicConditions") or _pole(m, "beneficiaryAdministration"), limit)
        if opis:
            print("## Opis (oryginał po angielsku)\n\n" + opis + "\n")
        if warunki:
            print("## Warunki udziału (oryginał po angielsku)\n\n" + warunki + "\n")
        print("-" * 60 + "\n")


def programy_cmd(arg):
    teraz = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    zapytanie = {"bool": {"must": [
        {"terms": {"type": TYPY_NABOROW}},
        {"terms": {"status": list(STATUSY.values())}},
        {"range": {"deadlineDate": {"gte": _czas_api(teraz)}}},
    ]}}
    s = slowniki(zapytanie)
    if arg.json:
        print(json.dumps({k: s.get(k, {}) for k in ("frameworkProgramme", "crossCuttingPriorities")}, ensure_ascii=False, indent=1))
        return
    print("Liczby: nabory otwarte i zapowiedziane z terminem od dziś (granty, kaskadowe, zewnętrzne).\n")
    print("## Programy (użyj skrótu w --program)\n")
    for kod, (skrot, nazwa, ile) in sorted(s.get("frameworkProgramme", {}).items(), key=lambda x: -(x[1][2] or 0)):
        print(f"- {skrot}: {nazwa}, {ile} (kod {kod})")
    print("\n## Priorytety przekrojowe (użyj kodu w --priorytet)\n")
    for kod, (_, nazwa, ile) in sorted(s.get("crossCuttingPriorities", {}).items(), key=lambda x: -(x[1][2] or 0)):
        print(f"- {kod}: {nazwa}, {ile}")


def main():
    p = argparse.ArgumentParser(description="Nabory UE z API Funding & Tenders Portal.")
    sub = p.add_subparsers(dest="polecenie", required=True)

    s = sub.add_parser("szukaj", help="otwarte i zapowiedziane nabory z przyszłym terminem")
    s.add_argument("--tekst", nargs="+", help="słowa kluczowe po angielsku; API szuka dowolnego z nich w całej treści tematu")
    s.add_argument("--fraza", nargs="+", help="frazy, które muszą wystąpić w tytule albo opisie, np. \"language model\"")
    s.add_argument("--prefiks", nargs="+", help="początek identyfikatora, np. HORIZON-EIC albo HORIZON-CL4-2027")
    s.add_argument("--sortuj", choices=["termin", "trafnosc"],
                   help="domyślnie trafność, gdy podano tekst lub frazę, w przeciwnym razie najbliższy termin")
    s.add_argument("--program", nargs="+", help="skróty programów, np. HORIZON DIGITAL LIFE (lista: polecenie programy)")
    s.add_argument("--priorytet", nargs="+", help="priorytety przekrojowe, np. AI DigitalAgenda SocInnov")
    s.add_argument("--typ", nargs="+", choices=list(TYPY), default=["granty", "kaskadowe"],
                   help="granty = tematy programów UE, kaskadowe = małe nabory ogłaszane przez projekty UE, "
                        "zewnetrzne = pomoc zewnętrzna UE (EuropeAid), przetargi = zamówienia Komisji i agencji UE "
                        "(umowa za wynagrodzenie, nie dotacja)")
    s.add_argument("--status", nargs="+", choices=list(STATUSY), default=["otwarte", "zapowiedziane"])
    s.add_argument("--termin-do", help="tylko nabory z terminem najpóźniej tego dnia, RRRR-MM-DD")
    s.add_argument("--limit", type=int, default=40, help="ile pozycji pokazać (domyślnie 40)")
    s.add_argument("--max-pobran", type=int, default=600, help="ile rekordów najwyżej pobrać z API (domyślnie 600)")
    s.add_argument("--json", action="store_true", help="wynik jako JSON z pełnymi polami")
    s.set_defaults(fn=szukaj)

    t = sub.add_parser("temat", help="szczegóły tematu po identyfikatorze")
    t.add_argument("identyfikator", help="np. HORIZON-CL4-2027-01-DIGITAL-EMERGING-01 albo identyfikator przetargu z kolumny Identyfikator")
    t.add_argument("--pelny", action="store_true", help="pełny opis i warunki bez ucinania")
    t.add_argument("--json", action="store_true")
    t.set_defaults(fn=temat)

    g = sub.add_parser("programy", help="słownik programów i priorytetów")
    g.add_argument("--json", action="store_true")
    g.set_defaults(fn=programy_cmd)

    arg = p.parse_args()
    arg.fn(arg)


if __name__ == "__main__":
    main()
