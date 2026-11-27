# Wunschzettel 2026

Dieser Ordner gehört **nicht** zur eigentlichen Website. Er enthält alles, womit die Wunschzettel der Aktion 2026 erzeugt werden.

| Datei / Ordner | Inhalt |
|---|---|
| `wunschliste-2026.xlsx` | Die Liste vom Tierheim (Name, Wunsch, Preis) plus drei Spalten für die Zettel: **Text auf dem Wunschzettel**, **Preis auf dem Wunschzettel**, **Erfüllt** |
| `fotos/` | Ein Foto pro Tier (verkleinert auf 600 px). Der Dateiname entspricht dem Namen in der Liste, ohne Umlaute und Leerzeichen, z. B. `frau-loewenzahn.jpg` |
| `wunschzettel-erzeugen.py` | Erzeugt die Wunschzettel und trägt die Galerie auf der Seite „Aktuelle Aktion“ ein |
| `wunschzettel-hintergrund-2026.png` | Hintergrundbild (1920 × 1080 px) |
| `hintergrund-erzeugen.py` | Skript, mit dem das Hintergrundbild erzeugt wurde |
| `schriften/` | Schreibschrift *Fondamento Italic* und *Roboto* (beide frei, Lizenz liegt daneben) |

## Einmalig einrichten

Python 3 installieren (z. B. aus dem Microsoft Store), dann in der Eingabeaufforderung:

```
pip install pillow openpyxl
```

## Wunschzettel erzeugen

In diesem Ordner:

```
python wunschzettel-erzeugen.py
```

Das Skript

1. liest `wunschliste-2026.xlsx`,
2. schreibt pro Tier ein Bild nach `bilder/aktionen/2026/` (z. B. `wunschzettel-06-rocky.webp`, 1200 × 675 px),
3. trägt alle Bilder mit Alt-Text in die Galerie von `aktuelle-aktion/index.html` ein (zwischen `WUNSCHZETTEL-START` und `WUNSCHZETTEL-ENDE`).

Danach in GitHub Desktop committen und pushen.

Nur einzelne Tiere neu erzeugen: `python wunschzettel-erzeugen.py --nur Rocky --nur Elly`
Mit `--vorschau` entstehen zusätzlich PNG-Dateien im Ordner `vorschau/`, die nicht ins Repo kommen.

## Typische Änderungen

- **Wunsch erfüllt:** In der Spalte **Erfüllt** `ja` eintragen und das Skript laufen lassen. Der Stempel kommt aus `stempel-wunsch-erfuellt.png` in diesem Ordner (PNG mit transparentem Hintergrund). Fehlt die Datei, meldet das Skript das, und der Zettel bleibt ohne Stempel.
- **Text oder Preis ändern:** Spalte **Text auf dem Wunschzettel** bzw. **Preis auf dem Wunschzettel** anpassen. Ist eine dieser Zellen leer, nimmt das Skript „NAME wünscht sich WUNSCH“ bzw. den Preis aus der Spalte **Preis**.
- **Neues Tier:** Zeile in der Liste ergänzen und ein Foto in `fotos/` legen. Die Reihenfolge der Liste ist die Reihenfolge auf der Seite. Wird ein Tier gestrichen, entfernt das Skript sein Bild beim nächsten vollständigen Lauf.

## Hintergrund neu erzeugen

Benötigt zusätzlich `numpy`:

```
pip install numpy pillow
python hintergrund-erzeugen.py wunschzettel-hintergrund-2026.png
```

Das Skript nutzt einen festen Zufallswert (2026), das Ergebnis ist also jedes Mal dasselbe Bild.
