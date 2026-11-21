# Hand hilft Pfote – statische Website

Statischer Nachbau von **hand-hilft-pfote.de** für GitHub Pages.
Reines HTML, CSS und ein kleines JavaScript ohne Framework, ohne Build-Schritt und ohne Jekyll.

**Datenschutz in einem Satz:** Die Seite setzt keine Cookies, nutzt kein Tracking und lädt nichts von fremden Servern. Schriften, Bilder und das Skript liegen alle hier im Repo. Eine Content-Security-Policy in jeder Seite erlaubt nur Inhalte von der eigenen Domain (`'self'`).

---

## Ordnerstruktur

```
/
├── index.html                      Startseite „Über uns“
├── aktuelle-aktion/index.html      Aktuelle Aktion (Weihnachten für Tiere 2026)
├── vergangene-aktionen/
│   ├── index.html                  Chronik 2012 bis heute
│   └── 2025/index.html             Wunschzettel-Galerie 2025 (88 Bilder)
├── impressum/index.html
├── datenschutzerklarung/index.html
├── 404.html                        eigene Fehlerseite
├── assets/
│   ├── css/style.css               gesamtes Design
│   ├── js/main.js                  Handy-Menü + Bild-Großansicht
│   ├── fonts/                      Roboto + Raleway (lokal, woff2)
│   └── img/                        Logo (SVG), Favicons
├── bilder/
│   ├── seiten/                     Titelbilder der Seiten (je 800 und 1600 px breit)
│   ├── team/                       Rebecca, Jan Erik, Bonnie
│   ├── jahre/                      ein Bild pro Jahr für „Vergangene Aktionen“
│   └── aktionen/2025/              Wunschzettel 2025
├── favicon.ico
├── sitemap.xml
├── robots.txt
├── CNAME                           enthält: hand-hilft-pfote.de
└── .nojekyll                       sagt GitHub: kein Jekyll verwenden
```

Die Adressen der Seiten sind dieselben wie bei der alten Strato-Seite (z. B. `/impressum/`, `/datenschutzerklarung/`). Alte Links und Suchmaschinen-Einträge funktionieren also weiter.

---

## Inhalte selbst pflegen

Alle Seiten sind normale HTML-Dateien. Du kannst sie mit jedem Texteditor bearbeiten, zum Beispiel mit **Visual Studio Code** oder **Notepad++**. Nimm bitte nicht Word. In den Dateien zeigen Kommentare wie `<!-- AKTUELLE AKTION – hier pflegen -->` die Stellen, an denen du etwas ändern kannst.

### Gelbe Platzhalter

Alles, was auf der Seite **gelb markiert** in eckigen Klammern steht, z. B. `[PLATZHALTER: Name des Tierheims 2026]`, musst du noch ausfüllen. Ersetze dabei das ganze Stück `<span class="platzhalter">[…]</span>` durch deinen Text. Im Moment gibt es Platzhalter in:

- `aktuelle-aktion/index.html` (Tierheim 2026, Einleitungstext, Wunschzettel)
- `vergangene-aktionen/index.html` (Ergebnis der Aktion 2025)

Mit der Suche nach `platzhalter` in deinem Editor findest du alle Stellen.

### Neue Wunschzettel für die aktuelle Aktion

1. Bilder in den Ordner `bilder/aktionen/2026/` legen. Ideal ist **WebP**, etwa 600 × 338 Pixel. JPG oder PNG gehen auch.
   Dateinamen bitte ohne Leerzeichen und Umlaute, z. B. `wunschzettel-01.webp`.
   *Umwandeln nach WebP unter Windows:* z. B. mit dem kostenlosen Programm „XnConvert“ oder in „Paint.NET“ über *Speichern unter → WebP*.
2. In `aktuelle-aktion/index.html` die Vorlagezeile im Kommentar unter `<ul class="galerie">` kopieren, ohne die Kommentarzeichen `<!--` und `-->` einfügen und Dateiname und Alt-Text anpassen:
   ```html
   <li><a href="../bilder/aktionen/2026/wunschzettel-01.webp"><img src="../bilder/aktionen/2026/wunschzettel-01.webp" width="600" height="338" alt="Bello wünscht sich ein Körbchen" loading="lazy" decoding="async"></a></li>
   ```
   Der **Alt-Text** (`alt="…"`) wird blinden Menschen vorgelesen. Schreib dort kurz, was auf dem Wunschzettel steht.

### Wenn eine Aktion endet (z. B. 2026 ist vorbei)

1. Ordner `vergangene-aktionen/2025/` kopieren und als `vergangene-aktionen/2026/` einfügen. Dort Titel, Untertitel und die Bilderliste anpassen. Am einfachsten kopierst du die `<li>`-Zeilen aus `aktuelle-aktion/index.html`. Achtung: Die Bildpfade beginnen dort mit `../../bilder/…` statt `../bilder/…`.
2. In `vergangene-aktionen/index.html` den obersten Block (2026, „Läuft aktuell“) durch einen normalen Jahresblock ersetzen. Als Vorlage dient der Block von 2024. Ein Jahresbild legst du als `bilder/jahre/2026.webp` ab, ca. 800 px breit.
3. `aktuelle-aktion/index.html` für das neue Jahr umschreiben.
4. In `sitemap.xml` die neue Adresse ergänzen.

### Menü, Kopf- und Fußzeile ändern

Kopfzeile und Fußzeile stehen in allen 7 HTML-Dateien gleich (markiert mit `KOPFZEILE` und `FUSSZEILE`). Wenn du dort etwas änderst, z. B. einen neuen Menüpunkt, musst du das in **jeder** Datei tun. Mit „Suchen und Ersetzen in Dateien“ deines Editors geht das in einem Rutsch.
Hinweis: Die Pfade unterscheiden sich je nach Ordnertiefe (`./`, `../`, `../../`). In `404.html` beginnen sie mit `/`.

### Seite vor dem Hochladen anschauen

Wegen der Sicherheitsregel (CSP) und der Ordner-Adressen funktioniert ein Doppelklick auf `index.html` nur eingeschränkt. Es gibt zwei einfache Wege:
- Einfach committen und pushen. Nach etwa 1 Minute ist die Änderung online.
- Oder lokal: In Visual Studio Code die Erweiterung „Live Server“ installieren und mit Rechtsklick auf `index.html` → *Open with Live Server* öffnen.

---

## Veröffentlichen: Schritt für Schritt

### 1. GitHub Desktop: Repo klonen, Dateien rein, Commit, Push

1. GitHub Desktop öffnen → **File → Clone repository** → Reiter *GitHub.com* → `C129H223N3O54/hand-hilft-pfote` auswählen → Speicherort wählen → **Clone**.
2. Den geklonten Ordner im Windows-Explorer öffnen (in GitHub Desktop: **Repository → Show in Explorer**).
3. **Den gesamten Inhalt** dieses Pakets in den Ordner kopieren, also `index.html`, `CNAME`, `.nojekyll` und alle Unterordner.
   ⚠️ `.nojekyll` beginnt mit einem Punkt. Wenn der Explorer es nicht anzeigt: *Ansicht → Einblenden → Ausgeblendete Elemente*. Die Datei muss mitkopiert werden.
4. Zurück in GitHub Desktop: Links erscheinen jetzt alle neuen Dateien. Unten links bei *Summary* z. B. „Statische Website“ eintragen → **Commit to main**.
5. Oben **Push origin** (bzw. beim allerersten Mal **Publish branch**) klicken.

### 2. GitHub: Pages einschalten

1. Auf github.com das Repo öffnen → **Settings** → links **Pages**.
2. *Build and deployment* → *Source*: **Deploy from a branch**.
3. *Branch*: **main**, Ordner **/ (root)** → **Save**.
4. *Custom domain*: `hand-hilft-pfote.de` eintragen → **Save**. Die Datei `CNAME` im Repo enthält das schon, das Feld sollte also bereits ausgefüllt sein.
5. Nach 1–2 Minuten baut GitHub die Seite. Unter deiner Domain erscheint sie, sobald die DNS-Einträge aus Schritt 3 greifen.

*Empfohlen:* Unter **Settings → Pages** die Domain zusätzlich über dein GitHub-Profil verifizieren (**Profil → Settings → Pages → Add a domain**). Das schützt davor, dass jemand anderes deine Domain in einem eigenen Repo verwendet. GitHub zeigt dir dafür einen TXT-Eintrag, den du bei Strato anlegst.

### 3. Strato: DNS umstellen

Im Strato-Kundenlogin: **Domains → Domainverwaltung → hand-hilft-pfote.de → Zahnrad / DNS-Einstellungen**.

**A-Records** für die Hauptdomain (`hand-hilft-pfote.de`, bei Strato oft „@“ oder leer). Alte A-Records löschen bzw. ersetzen:

| Typ | Wert |
|---|---|
| A | 185.199.108.153 |
| A | 185.199.109.153 |
| A | 185.199.110.153 |
| A | 185.199.111.153 |

**AAAA-Records** (IPv6, optional, aber empfohlen):

| Typ | Wert |
|---|---|
| AAAA | 2606:50c0:8000::153 |
| AAAA | 2606:50c0:8001::153 |
| AAAA | 2606:50c0:8002::153 |
| AAAA | 2606:50c0:8003::153 |

**Subdomain `www`:** CNAME auf `c129h223n3o54.github.io`.
Bei Strato musst du `www` dafür eventuell erst als Subdomain anlegen und dort den CNAME-Eintrag setzen.

⚠️ **MX-Records (E-Mail) nicht anfassen!** Dein Postfach `rebecca@hand-hilft-pfote.de` läuft weiter über Strato.

### 4. HTTPS erzwingen

DNS-Änderungen brauchen meist 15 Minuten bis einige Stunden, in Einzelfällen bis zu 48 Stunden.
Danach in **Settings → Pages** den Haken **Enforce HTTPS** setzen. Ist er noch ausgegraut, wartet GitHub noch auf das Zertifikat. Dann später noch einmal nachsehen.

### 5. Erst dann das alte Strato-Hosting kündigen

Erst wenn `https://hand-hilft-pfote.de` die neue Seite zeigt und das Schloss-Symbol erscheint, das **Webhosting-Paket** („MyWebsite NOW“) bei Strato kündigen.
**Die Domain und das E-Mail-Postfach behalten!** Prüfe beim Kündigen genau, dass nur der Baukasten und das Hosting gekündigt werden. Domain und Mail dürfen nicht mit wegfallen. Frag im Zweifel beim Strato-Support nach, welcher Tarif die Domain und das Postfach enthält.

---

## Prüfung im Browser (Checkliste)

Nach dem Umzug in Chrome, Edge oder Firefox `https://hand-hilft-pfote.de` öffnen und **F12** drücken:

- [ ] **Network-Tab:** Seite mit gedrückter Strg-Taste neu laden (Strg + F5). In der Spalte *Domain* (ggf. per Rechtsklick auf die Spaltenköpfe einblenden) darf **nur `hand-hilft-pfote.de`** stehen. Das gilt auf allen Seiten, auch auf der Galerie.
- [ ] **Application-Tab** (Firefox: *Web-Speicher*): Unter *Cookies* ist für die Domain **nichts** eingetragen, ebenso unter *Local Storage* und *Session Storage*.
- [ ] **Console-Tab:** keine roten Meldungen zu „Content Security Policy“.
- [ ] Am Handy: Menü-Symbol (☰) öffnet und schließt das Menü. In der Galerie öffnet ein Tipp aufs Bild die Großansicht.
- [ ] Eine nicht existierende Adresse aufrufen (z. B. `/test`). Dann erscheint die eigene 404-Seite.
- [ ] `https://www.hand-hilft-pfote.de` leitet auf `https://hand-hilft-pfote.de` weiter.
- [ ] Die Seite läuft über `https://` (Schloss-Symbol).

---

## Abweichungen zum Original

| Was | Original | Jetzt | Warum |
|---|---|---|---|
| Website-Übersetzer | Google Übersetzer nach Zustimmung im Banner | entfernt | lädt Google-Skript; Browser übersetzen heute selbst |
| Cookie-/Consent-Banner | vorhanden, setzte Cookie `gox_cookie_consent` | entfernt | es wird nichts mehr gesetzt, also nicht nötig |
| Tracking-Vorbereitung (pagepulse) | im Baukasten-Skript enthalten, war inaktiv | entfernt | kein Tracking |
| WordPress-Emoji-Skript | konnte bei alten Browsern `s.w.org` laden | entfernt | externe Anfrage |
| Instagram/Twitter | im Baukasten angelegt, aber deaktiviert | entfernt | nicht genutzt |
| Aktuelle Aktion | 2025, nur Galerie | **2026 mit Platzhaltern** | auf deinen Wunsch; 2025 ist abgeschlossen |
| Galerie 2025 | lag unter „Aktuelle Aktion“ | jetzt unter `/vergangene-aktionen/2025/`, verlinkt bei 2025 | 2025 ist abgeschlossen |
| Vergangene Aktionen 2025 | „Läuft aktuell :-)“ | Tierschutzverein Frankfurt am Main + Platzhalter fürs Ergebnis; neuer Eintrag 2026 „Läuft aktuell :-)“ | auf deinen Wunsch |
| Seitentitel im Browser-Tab | „Was wir tun“, „Unterstützen Sie uns“ | passend zur Seite | waren vertauscht/irreführend |
| Fußzeile | Facebook- und Mail-Symbol | zusätzlich E-Mail und Telefon als Text, Telefon-Symbol | Ersatz fürs Kontaktformular, wie gewünscht |
| Telefonnummer | „0160-90114849“ bzw. „016090114849“ | einheitlich „0160 90114849“ | Vereinheitlichung |
| Bilder | JPG/PNG, 25 MB | WebP, 4,3 MB, mit `loading="lazy"` | Ladezeit, gerade am Handy |
| Bilder | ohne Alt-Text | alle mit Alt-Text, Wunschzettel mit dem Wunsch als Text | Barrierefreiheit |
| Logo | PNG | SVG (nachgezeichnet) | scharf auf allen Bildschirmen |
| Schriften | 36 Schnitte von Roboto und Raleway | 5 Schnitte, die tatsächlich genutzt werden | kleiner, schneller |
| Galerie-Großansicht | Baukasten-Lightbox | eigenes kleines Skript, ohne JS öffnet sich das Bild direkt | keine Abhängigkeiten |
| Datenschutzerklärung | Musterformular, Hoster Strato, ohne Aufsichtsbehörde | neu passend zu GitHub Pages, mit HBDI | Setup hat sich geändert |
| Impressum | — | Inhalte 1:1; Hinweis zu den Schriften ergänzt | |
| PayPal | Adresse als Text | unverändert als Text (kein Button, kein Skript) | es gab keinen PayPal-Link; ein paypal.me-Link kann ergänzt werden |

---

## Rechtliches – bitte selbst prüfen

Impressum und Datenschutzerklärung sind sorgfältig an das tatsächliche technische Setup angepasst, **ersetzen aber keine Rechtsberatung**. Bitte selbst oder juristisch prüfen, insbesondere:
- ob das E-Mail-Postfach tatsächlich bei STRATO liegt (Abschnitt 5 der Datenschutzerklärung),
- ob du Spendenquittungen ausstellst oder Spenderdaten länger aufbewahrst (Abschnitt 6),
- das Stand-Datum nach jeder inhaltlichen Änderung der Datenschutzerklärung.

## Lizenzen

- Roboto: Apache License 2.0
- Raleway: SIL Open Font License 1.1
- Fotos: siehe Bildnachweise im Impressum (Unsplash-Lizenz, Pixabay-Lizenz) sowie eigene Fotos.
