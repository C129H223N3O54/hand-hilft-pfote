"""Erzeugt die Wunschzettel für die Weihnachtsaktion 2026.

Liest wunschliste-2026.xlsx, legt jedes Tierfoto aus fotos/ auf den Hintergrund
wunschzettel-hintergrund-2026.png und schreibt pro Tier ein WebP-Bild nach
bilder/aktionen/2026/. Danach trägt es die Galerie in aktuelle-aktion/index.html ein
(zwischen den Markierungen WUNSCHZETTEL-START und WUNSCHZETTEL-ENDE).

Aufruf (in diesem Ordner):
    python wunschzettel-erzeugen.py                 # alle Tiere + Galerie
    python wunschzettel-erzeugen.py --nur Rocky     # nur dieses Tier neu (mehrfach möglich)
    python wunschzettel-erzeugen.py --vorschau      # zusätzlich PNG-Vorschauen in vorschau/

Benötigt Python 3 mit Pillow und openpyxl:  pip install pillow openpyxl
"""
import argparse
import glob
import html
import os
import re
import sys
import unicodedata

from openpyxl import load_workbook
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HIER, "..", ".."))

# ---------------------------------------------------------------- Layout
# Alle Maße beziehen sich auf das 1920 × 1080 px große Hintergrundbild.
FOTO_X, FOTO_Y, FOTO_GROESSE = 100, 115, 600
RAHMEN = 6                               # heller Rand um das Foto
TEXT_X, TEXT_BREITE = 770, 570           # Textblock rechts vom Foto, links vom Baum
TEXT_PT, TEXT_MIN_PT = 60, 46            # einheitliche Größe; kleiner nur, wenn es sonst nicht passt
TEXT_ZEILEN_MAX = 4
TEXT_STRICH = 1                          # macht die schmale Schreibschrift etwas kräftiger
PREIS_Y, PREIS_PT = 948, 42
STEMPEL_MITTE, STEMPEL_HOEHE = (1560, 760), 520   # „Wunsch erfüllt“ unten rechts über dem Baum
AUSGABE_BREITE = 1200                    # Bild auf der Website (doppelt so scharf wie 600 px)

SCHRIFT_TEXT = os.path.join(HIER, "schriften", "Fondamento-Italic.ttf")
SCHRIFT_PREIS = os.path.join(HIER, "schriften", "Roboto-Variable.ttf")
STEMPEL = os.path.join(HIER, "stempel-wunsch-erfuellt.png")
SEITE = os.path.join(REPO, "aktuelle-aktion", "index.html")
BILD_URL = "../bilder/aktionen/2026/"


# ---------------------------------------------------------------- Liste lesen
def dateiname_teil(s):
    s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def schluessel(s):
    """Vergleichswert für Namen: „Shine (the light)“ = „Shine the light“ = shine-the-light.jpg"""
    return dateiname_teil(s).replace("-", "")


def spalte(kopf, name):
    for i, k in enumerate(kopf):
        if k.lower() == name.lower():
            return i
    return None


def lies_liste(pfad):
    ws = load_workbook(pfad, data_only=True).active
    zeilen = list(ws.iter_rows(values_only=True))
    kopf = [str(k).strip() if k else "" for k in zeilen[0]]
    i = {n: spalte(kopf, n) for n in ("Name", "Wunsch", "Preis", "Text auf dem Wunschzettel",
                                      "Preis auf dem Wunschzettel", "Erfüllt")}
    if None in (i["Name"], i["Wunsch"], i["Preis"]):
        sys.exit("Die Liste braucht die Spalten Name, Wunsch und Preis.")

    def wert(z, n):
        k = i[n]
        return str(z[k]).strip() if k is not None and k < len(z) and z[k] is not None else ""

    tiere = []
    for z in zeilen[1:]:
        name = wert(z, "Name")
        if not name:
            continue
        tiere.append({
            "nr": len(tiere) + 1,
            "name": name,
            "text": wert(z, "Text auf dem Wunschzettel") or f"{name} wünscht sich {wert(z, 'Wunsch')}",
            "preis": wert(z, "Preis auf dem Wunschzettel") or preiszeile(wert(z, "Preis")),
            "erfuellt": wert(z, "Erfüllt").lower() in ("ja", "x", "erfüllt", "1"),
            "datei": f"wunschzettel-{len(tiere) + 1:02d}-{dateiname_teil(name)}",
        })
    return tiere


def preiszeile(roh):
    """'6 Dosen - 10,00 Euro' -> '6 Dosen: 10,00 Euro'; ein reiner Betrag bleibt, wie er ist."""
    m = re.match(r"^\s*(.*?)\s*-?\s*(\d+,\d{2}\s*Euro)\s*$", roh)
    if not m:
        return roh
    menge = re.sub(r"^eine?\b", "1", m.group(1).strip(" -"), flags=re.I)
    return f"{menge}: {m.group(2)}" if menge else m.group(2)


def finde_foto(ordner, name):
    for f in os.listdir(ordner):
        stamm, endung = os.path.splitext(f)
        if endung.lower() in (".jpg", ".jpeg", ".png", ".webp") and schluessel(stamm) == schluessel(name):
            return os.path.join(ordner, f)
    return None


# ---------------------------------------------------------------- Zeichnen
def schrift_preis(pt):
    f = ImageFont.truetype(SCHRIFT_PREIS, pt)
    f.set_variation_by_axes([700, 100])      # Gewicht 700 (fett), Breite 100
    return f


def umbrechen(text, schrift, breite):
    """Bricht nach „wünscht sich“ immer um, sonst Wort für Wort. „wünscht sich“ bleibt
    zusammen, lange Wörter mit Bindestrich dürfen am Bindestrich getrennt werden."""
    text = re.sub(r"\b(wünscht|wünschen) sich\b", "\\1\u00a0sich", text)
    teile = re.split(r"(?<=\bsich) +", text, maxsplit=1)
    zeilen = []
    for teil in teile:
        stuecke = []                          # (Text, mit Leerzeichen davor?)
        for wort in teil.split(" "):
            for j, s in enumerate(re.findall(r"[^-]+-(?=.)|[^-]+$|-+$", wort) or [wort]):
                stuecke.append((s, j == 0))
        zeile = ""
        for s, mit_leer in stuecke:
            probe = (zeile + (" " if mit_leer else "") + s) if zeile else s
            if not zeile or schrift.getlength(probe) <= breite:
                zeile = probe
            else:
                zeilen.append(zeile)
                zeile = s
        zeilen.append(zeile)
    return [z.replace("\u00a0", " ") for z in zeilen]


def passender_text(text):
    """Einheitliche Schriftgröße für alle Zettel. Nur wenn der Text dann mehr als
    TEXT_ZEILEN_MAX Zeilen braucht oder ein einzelnes Wort zu breit ist, wird sie kleiner."""
    for pt in range(TEXT_PT, TEXT_MIN_PT - 1, -2):
        f = ImageFont.truetype(SCHRIFT_TEXT, pt)
        zeilen = umbrechen(text, f, TEXT_BREITE)
        if len(zeilen) <= TEXT_ZEILEN_MAX and all(f.getlength(z) <= TEXT_BREITE for z in zeilen):
            return f, zeilen
    return f, zeilen                          # kleinste Größe, notfalls etwas breiter


def mit_schatten(bild, zeichne, unschaerfe, deckkraft, versatz=(0, 0)):
    """Zeichnet die Form als weichen dunklen Schatten ins Bild."""
    maske = Image.new("L", bild.size, 0)
    zeichne(ImageDraw.Draw(maske), 255, versatz)
    maske = maske.filter(ImageFilter.GaussianBlur(unschaerfe)).point(lambda v: int(v * deckkraft))
    bild.paste((0, 0, 0), (0, 0), maske)


def quadrat(foto):
    if foto.mode in ("RGBA", "LA", "P"):
        foto = foto.convert("RGBA")
        foto = Image.alpha_composite(Image.new("RGBA", foto.size, (255, 255, 255, 255)), foto)
    foto = foto.convert("RGB")
    w, h = foto.size
    k = min(w, h)
    foto = foto.crop(((w - k) // 2, (h - k) // 2, (w - k) // 2 + k, (h - k) // 2 + k))
    return foto.resize((FOTO_GROESSE, FOTO_GROESSE), Image.LANCZOS)


def wunschzettel(hintergrund, foto_pfad, tier, stempel=None):
    bild = hintergrund.copy()

    # Foto mit Schatten und hellem Rand
    x0, y0 = FOTO_X - RAHMEN, FOTO_Y - RAHMEN
    x1, y1 = FOTO_X + FOTO_GROESSE + RAHMEN, FOTO_Y + FOTO_GROESSE + RAHMEN
    mit_schatten(bild, lambda d, f, v: d.rectangle([x0 + v[0], y0 + v[1], x1 + v[0], y1 + v[1]], fill=f),
                 unschaerfe=16, deckkraft=0.7, versatz=(8, 12))
    ImageDraw.Draw(bild).rectangle([x0, y0, x1 - 1, y1 - 1], fill=(255, 250, 242))
    bild.paste(quadrat(Image.open(foto_pfad)), (FOTO_X, FOTO_Y))

    # Wunschtext, senkrecht mittig zum Foto
    schrift, zeilen = passender_text(tier["text"])
    abstand = int(schrift.size * 1.18)
    oben = FOTO_Y + FOTO_GROESSE // 2 - (abstand * len(zeilen)) // 2

    def text(d, f, v):
        for i, z in enumerate(zeilen):
            d.text((TEXT_X + v[0], oben + i * abstand + v[1]), z, font=schrift, fill=f,
                   stroke_width=TEXT_STRICH, stroke_fill=f)
    mit_schatten(bild, text, unschaerfe=5, deckkraft=0.85, versatz=(2, 3))
    text(ImageDraw.Draw(bild), (255, 255, 255), (0, 0))

    # Preis unten links
    sp = schrift_preis(PREIS_PT)

    def preis(d, f, v):
        d.text((FOTO_X + v[0], PREIS_Y + v[1]), tier["preis"], font=sp, fill=f)
    mit_schatten(bild, preis, unschaerfe=3, deckkraft=0.8, versatz=(2, 2))
    preis(ImageDraw.Draw(bild), (255, 255, 255), (0, 0))

    # Stempel „Wunsch erfüllt“
    if tier["erfuellt"] and stempel is not None:
        s = stempel.copy()
        s.thumbnail((10_000, STEMPEL_HOEHE), Image.LANCZOS)
        bild.paste(s, (STEMPEL_MITTE[0] - s.width // 2, STEMPEL_MITTE[1] - s.height // 2), s)

    h = round(bild.height * AUSGABE_BREITE / bild.width)
    return bild.resize((AUSGABE_BREITE, h), Image.LANCZOS)


# ---------------------------------------------------------------- Galerie auf der Seite
def galerie_eintragen(tiere):
    if not os.path.exists(SEITE):
        print("Seite nicht gefunden, Galerie nicht eingetragen:", SEITE)
        return
    s = open(SEITE, encoding="utf-8").read()
    start, ende = "<!-- WUNSCHZETTEL-START", "<!-- WUNSCHZETTEL-ENDE -->"
    if start not in s or ende not in s:
        print("Markierungen WUNSCHZETTEL-START/-ENDE fehlen in", SEITE, "– Galerie nicht eingetragen.")
        return
    zeilen = []
    for t in tiere:
        alt = f"{t['text']} ({t['preis']})" + (" – Wunsch erfüllt" if t["erfuellt"] else "")
        url = BILD_URL + t["datei"] + ".webp"
        zeilen.append(f'          <li><a href="{url}"><img src="{url}" width="600" height="338" '
                      f'alt="{html.escape(alt)}" loading="lazy" decoding="async"></a></li>')
    a = s.index(start)
    a = s.index("\n", a) + 1                  # Zeile mit der Start-Markierung bleibt stehen
    b = s.rindex("\n", 0, s.index(ende)) + 1  # Zeile mit der Ende-Markierung bleibt stehen
    neu = s[:a] + "\n".join(zeilen) + "\n" + s[b:]
    if neu != s:
        open(SEITE, "w", encoding="utf-8", newline="\n").write(neu)
        print(f"Galerie in aktuelle-aktion/index.html aktualisiert ({len(tiere)} Wunschzettel).")


# ---------------------------------------------------------------- Ablauf
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--liste", default=os.path.join(HIER, "wunschliste-2026.xlsx"))
    ap.add_argument("--fotos", default=os.path.join(HIER, "fotos"))
    ap.add_argument("--hintergrund", default=os.path.join(HIER, "wunschzettel-hintergrund-2026.png"))
    ap.add_argument("--ausgabe", default=os.path.join(REPO, "bilder", "aktionen", "2026"))
    ap.add_argument("--nur", action="append", help="nur dieses Tier neu erzeugen (Name wie in der Liste)")
    ap.add_argument("--vorschau", action="store_true", help="zusätzlich PNG-Vorschauen in vorschau/")
    a = ap.parse_args()

    alle = lies_liste(a.liste)
    tiere = alle
    if a.nur:
        wahl = {schluessel(n) for n in a.nur}
        tiere = [t for t in alle if schluessel(t["name"]) in wahl]
        if not tiere:
            sys.exit("Kein passender Name in der Liste: " + ", ".join(a.nur))

    hintergrund = Image.open(a.hintergrund).convert("RGB")
    stempel = Image.open(STEMPEL).convert("RGBA") if os.path.exists(STEMPEL) else None
    if stempel is None and any(t["erfuellt"] for t in tiere):
        print("Hinweis: stempel-wunsch-erfuellt.png fehlt – erfüllte Wünsche bekommen noch keinen Stempel.")
    os.makedirs(a.ausgabe, exist_ok=True)
    vorschau = os.path.join(HIER, "vorschau")
    if a.vorschau:
        os.makedirs(vorschau, exist_ok=True)

    fehlt = []
    for t in tiere:
        foto = finde_foto(a.fotos, t["name"])
        if not foto:
            fehlt.append(t["name"])
            continue
        bild = wunschzettel(hintergrund, foto, t, stempel)
        bild.save(os.path.join(a.ausgabe, t["datei"] + ".webp"), "WEBP", quality=86, method=6)
        if a.vorschau:
            bild.save(os.path.join(vorschau, t["datei"] + ".png"))
        print(f"{t['datei']}.webp  –  {t['text']}  |  {t['preis']}" + ("  |  erfüllt" if t["erfuellt"] else ""))

    if fehlt:
        print("Kein Foto gefunden für:", ", ".join(fehlt))
    if not a.nur:                             # alte Dateien entfernen, die nicht mehr zur Liste gehören
        gueltig = {t["datei"] + ".webp" for t in alle}
        for f in glob.glob(os.path.join(a.ausgabe, "wunschzettel-*.webp")):
            if os.path.basename(f) not in gueltig:
                os.remove(f)
                print("entfernt:", os.path.basename(f))
    galerie_eintragen([t for t in alle if t["name"] not in fehlt])


if __name__ == "__main__":
    main()
