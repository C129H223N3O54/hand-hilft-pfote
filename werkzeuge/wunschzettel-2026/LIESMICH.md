# Wunschzettel-Hintergrund 2026

Dieser Ordner gehört **nicht** zur eigentlichen Website. Er bewahrt Arbeitsdateien auf, damit nichts verloren geht.

- `wunschzettel-hintergrund-2026.png` – fertiges Hintergrundbild (1920 × 1080 px) für die Wunschzettel der Aktion 2026.
- `hintergrund-erzeugen.py` – Python-Skript, mit dem das Bild erzeugt wurde.

## Bild neu erzeugen

Benötigt Python 3 mit `numpy` und `Pillow`:

```
pip install numpy pillow
python hintergrund-erzeugen.py wunschzettel-hintergrund-2026.png
```

Das Skript nutzt einen festen Zufallswert (2026), das Ergebnis ist also jedes Mal dasselbe Bild.
