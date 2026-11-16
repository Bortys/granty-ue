#!/usr/bin/env python3
"""Przeszukuje katalog naborów Kierunek Grant (sokolinski.com/granty).

Katalog zbiera nabory z wielu źródeł: portalu Funding & Tenders, Portalu Funduszy
Europejskich i miesięcznych zestawień naborów, WOD2021, NCBR, PARP, NFOŚiGW, ARiMR,
NCN, NAWA, NIW, Funduszy EOG, Interreg, eNGO, samorządów, fundacji, NATO i EUDIS.
To trop, a nie źródło ostateczne: termin, kwotę i warunki potwierdza się
w ogłoszeniu organizatora (kolumna Link).

Tylko biblioteka standardowa Pythona.

Przykłady:
  python3 katalog_grantow.py --tekst "sztuczna inteligencja"
  python3 katalog_grantow.py --temat Bezpieczeństwo --wnioskodawca Firmy Startupy
  python3 katalog_grantow.py --zasieg Regionalne --wojewodztwo podlaskie
  python3 katalog_grantow.py --wnioskodawca NGO --termin-do 2027-01-31
  python3 katalog_grantow.py --rodzaj zamowienia --temat Kosmos   (zamówienia ESA, CERN, EUMETSAT, EUSPA)
  python3 katalog_grantow.py --raporty
"""

import argparse
import datetime as dt
import http.client
import json
import sys
import time
import unicodedata
import urllib.error
import urllib.request

ADRES = "https://sokolinski.com/granty/catalog.php"
STRONA = "https://sokolinski.com/granty/"
UA = "granty-ue/1.1 (skill Claude; python-urllib)"
# Pole "kind" w katalogu: brak = finansowanie (grant, dotacja, nagroda), "procurement" = zamówienie,
# "consultation" = konsultacje rynkowe przed zamówieniem. Pole "planned" = termin przybliżony.
RODZAJE = {"finansowanie": "", "zamowienia": "procurement", "konsultacje": "consultation"}
RODZAJ_NAZWA = {"": "nabór", "procurement": "zamówienie", "consultation": "konsultacje rynkowe"}


def pobierz():
    blad = None
    for proba in range(4):
        try:
            req = urllib.request.Request(ADRES, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                t = r.read().decode("utf-8")
            break
        except (OSError, http.client.HTTPException) as e:  # OSError obejmuje URLError i zerwane połączenia
            blad = e
            time.sleep(2 ** (proba + 1))
    else:
        sys.exit(f"Nie udało się pobrać katalogu ({ADRES}): {blad}")
    try:
        return json.loads(t[t.index("{"):t.rindex("}") + 1])
    except ValueError as e:
        sys.exit(f"Katalog ma nieoczekiwany format ({ADRES}): {e}")


def bez_ogonkow(s):
    s = (s or "").replace("ł", "l").replace("Ł", "L")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).casefold()


def data(s):
    try:
        return dt.date.fromisoformat((s or "")[:10])
    except ValueError:
        return None


def budzet(x):
    b, w = x.get("budget"), x.get("currency") or ""
    if not b:
        return ""
    b = float(b)  # w katalogu w milionach
    if b >= 1:
        t = f"{b:,.1f}".replace(",", " ").replace(".0", "").replace(".", ",")
        return f"{t} mln {w}".strip()
    return f"{round(b * 1000):,} tys. {w}".replace(",", " ").strip()


def pasuje_ktorykolwiek(wartosci, szukane):
    wart = [bez_ogonkow(v) for v in wartosci]
    return any(bez_ogonkow(s) in v for s in szukane for v in wart)


def main():
    p = argparse.ArgumentParser(description="Katalog naborów Kierunek Grant (sokolinski.com/granty).")
    p.add_argument("--tekst", nargs="+", help="słowa, które muszą wystąpić wszystkie (tytuł, kod, program, organizator, opis); bez znaczenia wielkość liter i ogonki")
    p.add_argument("--temat", nargs="+", help="np. Bezpieczeństwo, Kosmos, Cyfryzacja, Zdrowie, Energia, Kultura, Sprawy społeczne (wystarczy fragment)")
    p.add_argument("--wnioskodawca", nargs="+", help="np. Firmy, Startupy, NGO, Organizacje badawcze, Samorządy, Naukowcy, Instytucje edukacyjne, Ekonomia społeczna")
    p.add_argument("--zasieg", nargs="+", help="Krajowe, Regionalne, Zagraniczne, Interreg")
    p.add_argument("--wojewodztwo", nargs="+", help="np. podlaskie, mazowieckie (wystarczy fragment); nabory krajowe dołącz osobnym zapytaniem")
    p.add_argument("--program", nargs="+", help="fragment nazwy programu, np. FENG, Horyzont, Interreg, NFOŚiGW, NATO")
    p.add_argument("--zrodlo", nargs="+", help="fragment nazwy źródła, np. NCBR, eNGO, PARP, ARiMR")
    p.add_argument("--od", help="tylko nabory z terminem od tego dnia, RRRR-MM-DD (domyślnie dziś)")
    p.add_argument("--termin-do", help="tylko nabory z terminem najpóźniej tego dnia, RRRR-MM-DD")
    p.add_argument("--bez-terminu", action="store_true", help="dołącz pozycje bez podanego terminu (do sprawdzenia)")
    p.add_argument("--rodzaj", nargs="+", choices=list(RODZAJE),
                   help="finansowanie = granty, dotacje i nagrody; zamowienia = przetargi agend i instytucji "
                        "(zamówienie, nie dotacja); konsultacje = konsultacje rynkowe przed zamówieniem; domyślnie wszystko")
    p.add_argument("--sortuj", choices=["termin", "budzet"], default="termin")
    p.add_argument("--limit", type=int, default=40)
    p.add_argument("--raporty", action="store_true", help="pokaż stan katalogu i linki do oficjalnych zestawień naborów, bez listy")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    k = pobierz()
    stan = data(k.get("snapshot"))
    dzis = dt.date.today()
    od = data(a.od) if a.od else dzis
    do = data(a.termin_do) if a.termin_do else None
    if (a.od and not od) or (a.termin_do and not do):
        sys.exit("Daty podaj w formacie RRRR-MM-DD.")

    naglowek = [f"Źródło: katalog Kierunek Grant ({STRONA}), stan na {k.get('snapshot', '?')}, pobrano {dt.datetime.now():%Y-%m-%d %H:%M}."]
    if stan and (dzis - stan).days > 7:
        naglowek.append(f"Uwaga: katalog ma {(dzis - stan).days} dni. Nowsze nabory mogą w nim nie występować.")
    naglowek.append("To trop: termin, kwotę i warunki potwierdź w ogłoszeniu organizatora (kolumna Link).")

    if a.raporty:
        print("\n".join(naglowek[:2]))
        print(f"\nPozycji w katalogu: {len(k.get('items', []))}.")
        print("\nOficjalne zestawienia naborów z Portalu Funduszy Europejskich (XLSX, co miesiąc):")
        for n, u in (k.get("reports") or {}).items():
            print(f"- {n}: {u}")
        if k.get("portal"):
            print(f"\nPortal: {k['portal']}")
        print("\nŹródła zagraniczne użyte w katalogu:")
        for n, u in (k.get("internationalSources") or {}).items():
            print(f"- {n}: {u}")
        return

    wynik = []
    rodzaje = {RODZAJE[r] for r in a.rodzaj} if a.rodzaj else None
    for x in k.get("items", []):
        if rodzaje is not None and (x.get("kind") or "") not in rodzaje:
            continue
        koniec, start = data(x.get("end")), data(x.get("start"))
        if koniec:
            if koniec < od or (do and koniec > do):
                continue
        elif not a.bez_terminu:
            continue
        if a.tekst:
            tresc = bez_ogonkow(" ".join(str(x.get(pole) or "") for pole in ("title", "originalTitle", "code", "program", "host", "description", "source")))
            if not all(bez_ogonkow(s) in tresc for s in a.tekst):
                continue
        if a.temat and not pasuje_ktorykolwiek(x.get("topics", []), a.temat):
            continue
        if a.wnioskodawca and not pasuje_ktorykolwiek(x.get("audiences", []), a.wnioskodawca):
            continue
        if a.zasieg and not pasuje_ktorykolwiek([x.get("scope", "")], a.zasieg):
            continue
        if a.wojewodztwo and not pasuje_ktorykolwiek([x.get("region", "")], a.wojewodztwo):
            continue
        if a.program and not pasuje_ktorykolwiek([x.get("program", "")], a.program):
            continue
        if a.zrodlo and not pasuje_ktorykolwiek([x.get("source", ""), x.get("host", "")], a.zrodlo):
            continue
        x = dict(x)
        x["status"] = "zapowiedziany" if start and start > dzis else ("otwarty" if koniec else "do sprawdzenia")
        if x.get("planned"):
            x["status"] = "planowany, termin przybliżony"
        x["rodzaj"] = RODZAJ_NAZWA.get(x.get("kind") or "", x.get("kind"))
        wynik.append(x)

    if a.sortuj == "budzet":
        wynik.sort(key=lambda x: -(float(x.get("budget") or 0)))
    else:
        wynik.sort(key=lambda x: (x.get("end") or "9999", x.get("title", "")))
    pokaz = wynik[: a.limit]

    if a.json:
        json.dump({"zrodlo": STRONA, "stan_katalogu": k.get("snapshot"), "znaleziono": len(wynik),
                   "pokazano": len(pokaz), "nabory": pokaz}, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return

    print("\n".join(naglowek))
    ile = {}
    for x in wynik:
        ile[x["rodzaj"]] = ile.get(x["rodzaj"], 0) + 1
    print(f"Pasuje {len(wynik)} z {len(k.get('items', []))} pozycji ("
          + ", ".join(f"{n}: {i}" for n, i in sorted(ile.items())) + f"), pokazuję {len(pokaz)}.")
    if ile.get("zamówienie") or ile.get("konsultacje rynkowe"):
        print("Zamówienie to nie dotacja: zamawiający płaci za wykonanie, a ofertę składa się według dokumentów zamówienia.")
    print()
    if not pokaz:
        return
    print("| Termin | Status | Rodzaj | Zasięg | Program | Tytuł | Organizator | Dla kogo | Budżet | Link |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for x in pokaz:
        zasieg = x.get("scope", "") + (f" ({x['region']})" if x.get("region") else "")
        tytul = (x.get("title") or "").replace("|", "/")
        if len(tytul) > 110:
            tytul = tytul[:107].rsplit(" ", 1)[0] + "..."
        print("| " + " | ".join([
            x.get("end") or "brak", x["status"], x["rodzaj"], zasieg, (x.get("program") or "").replace("|", "/"), tytul,
            (x.get("host") or x.get("source") or "").replace("|", "/")[:60], ", ".join(x.get("audiences", [])) or "do sprawdzenia",
            budzet(x) or "do sprawdzenia", x.get("url", "")]) + " |")


if __name__ == "__main__":
    main()
