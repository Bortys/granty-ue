#!/usr/bin/env python3
"""Przetargi z TED (Tenders Electronic Daily), dziennika zamówień publicznych UE.

API TED v3 pozwala szukać ogłoszeń bez klucza i bez logowania:
POST https://api.ted.europa.eu/v3/notices/search. Tylko biblioteka standardowa Pythona.

W TED są zamówienia powyżej progów unijnych z całej UE: polskich zamawiających
(ministerstwa, wojsko, uczelnie, szpitale, samorządy, spółki), instytucji i agencji UE
(Komisja, EDA, EUSPA, Frontex, F4E, wspólne przedsięwzięcia) i organizacji
międzynarodowych. Zamówień poniżej progów szukaj w Biuletynie Zamówień Publicznych
(e-Zamówienia), a zamówień ESA w esa-star.

Przykłady:
  python3 przetargi_ted.py --tekst dron* antydron* bezzałog*
  python3 przetargi_ted.py --cpv 73 --kraj POL          (usługi badawczo-rozwojowe w Polsce)
  python3 przetargi_ted.py --tekst satellite satelit* --wszystkie-kraje --cpv 35 73
  python3 przetargi_ted.py --zamawiajacy "European Defence Agency" --wszystkie-kraje
  python3 przetargi_ted.py --tekst "sztuczna inteligencja" --zapowiedzi
"""

import argparse
import datetime as dt
import http.client
import json
import re
import sys
import time
import urllib.error
import urllib.request

API = "https://api.ted.europa.eu/v3/notices/search"
UA = "granty-ue/1.0 (skill Claude; python-urllib)"
STRONA = 100
OGLOSZENIA = ["cn-standard", "cn-social", "cn-desg"]  # ogłoszenia o zamówieniu i o konkursie
ZAPOWIEDZI = ["pin-only", "pin-cfc-standard", "pin-cfc-social"]  # wstępne ogłoszenia informacyjne
POLA = [
    "publication-number", "notice-title", "buyer-name", "buyer-country", "notice-type",
    "publication-date", "deadline-receipt-tender-date-lot", "classification-cpv",
    "estimated-value-lot", "estimated-value-cur-lot",
]
TYP_NAZWA = {
    "cn-standard": "ogłoszenie o zamówieniu", "cn-social": "zamówienie na usługi społeczne",
    "cn-desg": "konkurs", "pin-only": "zapowiedź", "pin-cfc-standard": "zapowiedź z zaproszeniem",
    "pin-cfc-social": "zapowiedź z zaproszeniem (usługi społeczne)",
}
JEZYKI = ["pol", "eng", "fra", "deu"]


def _post(zapytanie, strona, limit):
    tresc = json.dumps({"query": zapytanie, "fields": POLA, "page": strona, "limit": limit}).encode()
    req = urllib.request.Request(API, data=tresc, method="POST", headers={
        "Content-Type": "application/json", "Accept": "application/json", "User-Agent": UA})
    ostatni_blad = None
    for proba in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as odp:
                return json.load(odp)
        except urllib.error.HTTPError as blad:
            opis = blad.read().decode("utf-8", "replace")
            if blad.code == 400:  # błąd składni zapytania nie zniknie przy ponowieniu
                try:
                    opis = json.loads(opis).get("message", opis)
                except json.JSONDecodeError:
                    pass
                sys.exit(f"TED odrzucił zapytanie: {opis}\nZapytanie: {zapytanie}")
            ostatni_blad = f"HTTP {blad.code}: {opis[:200]}"
        except (OSError, http.client.HTTPException, json.JSONDecodeError) as blad:
            ostatni_blad = blad
        time.sleep(2 ** (proba + 1))
    sys.exit(f"Błąd API TED: {ostatni_blad}")


def _tekst_wielojezyczny(pole):
    """notice-title i buyer-name to słowniki język → tekst albo lista; wybieramy polski, potem angielski."""
    if not pole:
        return []
    if isinstance(pole, str):
        return [pole]
    if isinstance(pole, list):
        return [str(x) for x in pole]
    for j in JEZYKI + sorted(pole):
        if pole.get(j):
            w = pole[j]
            return w if isinstance(w, list) else [w]
    return []


def _fraza(slowo):
    slowo = slowo.replace('"', "").strip()
    return f'FT~("{slowo}")' if " " in slowo else f"FT~({slowo})"


def zbuduj_zapytanie(arg, od, do):
    warunki = []
    if arg.tekst:
        # API nie rozumie FT~(a AND b): każde słowo osobno, potem OR albo AND
        polaczenie = " AND " if arg.wszystkie else " OR "
        warunki.append("(" + polaczenie.join(_fraza(s) for s in arg.tekst) + ")")
    if arg.cpv:
        kody = []
        for k in arg.cpv:
            k = re.sub(r"\D", "", k)
            if not k:
                sys.exit("Kod CPV to cyfry, np. 73 (badania i rozwój) albo 34711200 (bezzałogowe statki powietrzne).")
            kody.append(f"classification-cpv={k}" if len(k) >= 8 else f"classification-cpv={k}*")
        warunki.append("(" + " OR ".join(kody) + ")")
    if arg.zamawiajacy:
        warunki.append("(" + " OR ".join(f'buyer-name~("{z}")' for z in arg.zamawiajacy) + ")")
    if not arg.wszystkie_kraje:
        kraje = [k.upper() for k in arg.kraj]
        warunki.append(f"buyer-country={kraje[0]}" if len(kraje) == 1 else f"buyer-country IN ({' '.join(kraje)})")
    typy = OGLOSZENIA + (ZAPOWIEDZI if arg.zapowiedzi else [])
    warunki.append(f"notice-type IN ({' '.join(typy)})")
    if not arg.zapowiedzi:
        warunki.append(f"deadline-receipt-tender-date-lot>={od:%Y%m%d}")
    else:
        warunki.append(f"publication-date>={(od - dt.timedelta(days=arg.zapowiedzi_dni)):%Y%m%d}")
    if do:
        warunki.append(f"deadline-receipt-tender-date-lot<={do:%Y%m%d}")
    return " AND ".join(warunki) + " SORT BY publication-date DESC"


def _daty(lista):
    wynik = []
    for x in lista or []:
        try:
            wynik.append(dt.date.fromisoformat(str(x)[:10]))
        except ValueError:
            continue
    return sorted(set(wynik))


def _wartosc(n):
    wartosci = n.get("estimated-value-lot") or []
    waluty = n.get("estimated-value-cur-lot") or []
    suma, waluta = 0.0, None
    for i, w in enumerate(wartosci):
        try:
            suma += float(w)
        except (TypeError, ValueError):
            continue
        waluta = waluta or (waluty[i] if i < len(waluty) else None)
    if not suma:
        return None
    if suma >= 1_000_000:
        kwota = f"{suma / 1_000_000:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " mln"
    elif suma >= 1000:
        kwota = f"{suma / 1000:.0f} tys."
    else:
        kwota = f"{suma:.0f}"
    return f"{kwota} {waluta or ''}".strip()


def rekord(n, od, do):
    numer = n.get("publication-number")
    terminy = _daty(n.get("deadline-receipt-tender-date-lot"))
    przyszle = [d for d in terminy if d >= od and (not do or d <= do)]
    tytuly = _tekst_wielojezyczny(n.get("notice-title"))
    zamawiajacy = list(dict.fromkeys(_tekst_wielojezyczny(n.get("buyer-name"))))
    cpv = list(dict.fromkeys(n.get("classification-cpv") or []))
    typ = n.get("notice-type")
    return {
        "numer": numer,
        "tytul": re.sub(r"\s+", " ", tytuly[0]).strip() if tytuly else "",
        "zamawiajacy": zamawiajacy,
        "kraje": list(dict.fromkeys(n.get("buyer-country") or [])),
        "rodzaj": TYP_NAZWA.get(typ, typ),
        "opublikowano": str(n.get("publication-date") or "")[:10],
        "nastepny_termin": przyszle[0].isoformat() if przyszle else None,
        "wszystkie_terminy": [d.isoformat() for d in terminy],
        "cpv": cpv,
        "szacunkowa_wartosc": _wartosc(n),
        "link": f"https://ted.europa.eu/pl/notice/-/detail/{numer}",
        "_zapowiedz": typ in ZAPOWIEDZI,
    }


def main():
    p = argparse.ArgumentParser(description="Przetargi z TED (API v3, bez klucza).")
    p.add_argument("--tekst", nargs="+", help="słowa do szukania w całej treści ogłoszenia, po polsku i po angielsku; "
                                              "gwiazdka na końcu łapie odmianę (dron*), fraza w cudzysłowie")
    p.add_argument("--wszystkie", action="store_true", help="ogłoszenie musi zawierać wszystkie słowa (domyślnie dowolne)")
    p.add_argument("--cpv", nargs="+", help="początki kodów CPV, np. 73 (badania i rozwój), 35 (sprzęt obronny), "
                                            "72 (usługi IT), 48 (oprogramowanie)")
    p.add_argument("--zamawiajacy", nargs="+", help="nazwa zamawiającego, np. \"European Defence Agency\" "
                                                    "albo \"Agencja Uzbrojenia\"")
    p.add_argument("--kraj", nargs="+", default=["POL"], help="kraj zamawiającego, kod trzyliterowy (domyślnie POL)")
    p.add_argument("--wszystkie-kraje", action="store_true", help="bez filtra kraju (np. instytucje UE w Brukseli)")
    p.add_argument("--od", help="termin składania ofert najwcześniej tego dnia, RRRR-MM-DD (domyślnie dziś)")
    p.add_argument("--termin-do", help="termin składania ofert najpóźniej tego dnia, RRRR-MM-DD")
    p.add_argument("--zapowiedzi", action="store_true",
                   help="dodaj wstępne ogłoszenia informacyjne (zapowiedzi przetargów) z ostatnich dni")
    p.add_argument("--zapowiedzi-dni", type=int, default=60, help="z ilu dni wstecz brać zapowiedzi (domyślnie 60)")
    p.add_argument("--sortuj", choices=["nowe", "termin"], default="nowe",
                   help="nowe = najpierw świeżo opublikowane (domyślnie), termin = najbliższy termin ofert")
    p.add_argument("--limit", type=int, default=25, help="ile pozycji pokazać (domyślnie 25)")
    p.add_argument("--max-pobran", type=int, default=300, help="ile ogłoszeń najwyżej pobrać (domyślnie 300)")
    p.add_argument("--json", action="store_true", help="wynik jako JSON")
    arg = p.parse_args()

    if not (arg.tekst or arg.cpv or arg.zamawiajacy):
        p.error("podaj --tekst, --cpv albo --zamawiajacy, inaczej wyjdą tysiące ogłoszeń")
    od = dt.date.fromisoformat(arg.od) if arg.od else dt.date.today()
    do = dt.date.fromisoformat(arg.termin_do) if arg.termin_do else None
    zapytanie = zbuduj_zapytanie(arg, od, do)

    rekordy, strona, lacznie = [], 1, 0
    while True:
        dane = _post(zapytanie, strona, STRONA)
        lacznie = dane.get("totalNoticeCount", 0)
        notki = dane.get("notices", [])
        rekordy += [rekord(n, od, do) for n in notki]
        if not notki or strona * STRONA >= min(lacznie, arg.max_pobran):
            break
        strona += 1

    # Filtr terminu w API przepuszcza ogłoszenie, gdy pasuje dowolna część zamówienia,
    # a dynamiczne systemy zakupów i umowy ramowe mają terminy sprzed miesięcy. Sprawdzamy jeszcze raz.
    aktualne = [r for r in rekordy if r["nastepny_termin"] or (r["_zapowiedz"] and not do)]
    if arg.sortuj == "termin":
        aktualne.sort(key=lambda r: r["nastepny_termin"] or "9999")
    pokazane = [{k: v for k, v in r.items() if not k.startswith("_")} for r in aktualne[: arg.limit]]

    naglowek = {
        "zrodlo": "TED, API v3 (api.ted.europa.eu/v3/notices/search)",
        "pobrano": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "zapytanie_ted": zapytanie,
        "api_zwrocilo": lacznie,
        "pobrano_ogloszen": len(rekordy),
        "z_przyszlym_terminem": len(aktualne),
        "pokazano": len(pokazane),
        "uciete_przez_max_pobran": lacznie > arg.max_pobran,
    }
    if arg.json:
        print(json.dumps({"naglowek": naglowek, "przetargi": pokazane}, ensure_ascii=False, indent=1))
        return

    print(f"Źródło: {naglowek['zrodlo']}, pobrano {naglowek['pobrano']}.")
    print(f"Zapytanie: {zapytanie}")
    print(f"TED zwrócił {lacznie}, z przyszłym terminem ofert: {len(aktualne)} z {len(rekordy)} pobranych, "
          f"pokazuję {len(pokazane)}, kolejność: {'najbliższy termin' if arg.sortuj == 'termin' else 'najnowsze'}.")
    if naglowek["uciete_przez_max_pobran"]:
        print(f"Uwaga: pobrano tylko {arg.max_pobran} ogłoszeń. Zawęź zapytanie albo podnieś --max-pobran.")
    print("Termin to dzień składania ofert z ogłoszenia (bez godziny). Godzinę i zmiany (sprostowania) "
          "sprawdź w ogłoszeniu i w dokumentach zamówienia.\n")
    if not pokazane:
        print("Brak ogłoszeń z przyszłym terminem dla tego zapytania.")
        return
    print("| Termin ofert | Rodzaj | Kraj | Zamawiający | Tytuł | CPV | Szac. wartość | Link |")
    print("|---|---|---|---|---|---|---|---|")
    for r in pokazane:
        tytul = r["tytul"].replace("|", "/")
        if len(tytul) > 100:
            tytul = tytul[:97] + "..."
        zam = (r["zamawiajacy"][0] if r["zamawiajacy"] else "?").replace("|", "/")
        if len(r["zamawiajacy"]) > 1:
            zam += f" i {len(r['zamawiajacy']) - 1} innych"
        kraje = ", ".join(r["kraje"][:3]) + (" i inne" if len(r["kraje"]) > 3 else "")
        termin = r["nastepny_termin"] or "brak (zapowiedź)"
        print(f"| {termin} | {r['rodzaj']} | {kraje} | {zam} | {tytul} | {', '.join(r['cpv'][:3])} | "
              f"{r['szacunkowa_wartosc'] or 'brak w ogłoszeniu'} | {r['link']} |")


if __name__ == "__main__":
    main()
