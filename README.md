# Tiptoi Audio-Link-Katalog

[English](README.en.md)

Eine private, inoffizielle Weboberfläche zum Durchsuchen öffentlich erreichbarer tiptoi®-Audioeinträge. Der Scraper speichert Titel, Vorschaubild und die URL zur `.gme`-Datei in SQLite. Der Download-Link öffnet anschließend die Datei beim jeweiligen Anbieter.

## Wichtige Hinweise

- Dieses Projekt ist **nicht mit Ravensburger oder tiptoi® verbunden, wird nicht von ihnen unterstützt und ist kein offizielles Produkt**.
- Das Projekt wurde ausschließlich für private, experimentelle Zwecke erstellt. Eine Nutzung oder Weitergabe heruntergeladener Inhalte wird damit nicht erlaubt.
- Nach Kenntnisstand des Projekts bietet Ravensburger derzeit keine offizielle native tiptoi®-Software für Linux an. Diese unabhängige Weboberfläche ist kein offizieller Ersatz dafür.
- Das Projekt wurde vollständig mithilfe von KI erstellt. Code, Dokumentation und Gestaltung wurden KI-generiert; eine vollständige fachliche oder rechtliche Prüfung wird nicht zugesichert.
- Marken, Produktnamen, Bilder und Audiodateien gehören ihren jeweiligen Rechteinhabern. Dieses Projekt enthält und lizenziert diese Inhalte nicht. Prüfe vor Nutzung die geltenden Bedingungen und Rechte. Veröffentliche oder verteile keine Inhalte, zu deren Weitergabe du nicht berechtigt bist.

## Funktionen

- Scrapt Produktnamen, Vorschaubilder und `.gme`-Links von der Ravensburger-Service-Seite.
- Filtert Titel direkt während der Eingabe, auch mit deutschen Umlauten.
- Bietet Seitengrößen von 25, 50, 75, 100 oder allen Einträgen.
- Zeigt eine sticky Such- und Seitennavigation.
- Startet standardmäßig im Darkmode. Ein Icon-Button mit Sonne und Mondsichel wechselt das Theme; die Auswahl wird im Browser gespeichert.
- Richtet den Theme-Button auf Mobilgeräten neben der ersten Titelzeile aus.
- Leitet den Download-Link direkt zur externen `.gme`-Datei weiter. Der Scraper lädt die Audiodatei nicht herunter und speichert sie weder in SQLite noch unter `/data`.
- Speichert Scraper-Treffer nach jeder Produktseite in SQLite und verhindert doppelte Audio-URLs.
- Verwendet `./media_data` als persistenten Host-Bind-Mount für die Datenbank.

## Screenshots

Die folgenden Screenshots verwenden synthetische Beispieldaten und neutrale Platzhaltergrafiken. Sie enthalten keine Ravensburger-Bilder oder Audiodateien.

### Desktop

![Desktopansicht mit Suchleiste, Seitenauswahl und Medienkarten](docs/screenshots/catalog-desktop.png)

### Suche

![Nach Forest gefilterte Treffer](docs/screenshots/catalog-search.png)

### Mobil

![Mobile Ansicht mit umbrochener Seitennavigation](docs/screenshots/catalog-mobile.png)

## Start mit Docker Compose

Voraussetzung: Docker Engine und Docker Compose V2. Das Standard-Compose verwendet das veröffentlichte GHCR-Image; lokale Quellcodeänderungen sind erst mit einem neuen Image enthalten. Beide Dienste mounten `./media_data` nach `/data` und verwenden standardmäßig UID/GID `1000:1000`.

Lege bei Bedarf eine `.env` im Projektverzeichnis mit den IDs des Host-Benutzers an:

```dotenv
PUID=1000
PGID=1000
SCRAPER_CRON="0 3 * * *"
```

Passe die Werte an, falls `id -u` oder `id -g` andere IDs ausgibt. Der Ordner `media_data` und eine vorhandene `database.db` müssen für diese IDs schreibbar sein. Unter Linux kannst du den Besitz bei Bedarf so korrigieren:

```sh
sudo chown -R "$(id -u):$(id -g)" media_data
```

### Veröffentlichtes Image

```sh
docker compose up -d
```

Öffne anschließend <http://localhost:8000>. Compose startet die Weboberfläche und führt den Scraper einmal direkt sowie danach nach dem Zeitplan aus. `SCRAPER_CRON` verwendet ein fünfstelliges Cron-Muster in UTC und ist standardmäßig auf täglich um 03:00 UTC gesetzt. Du kannst den Wert in `.env` anpassen. Die Scraper-Ausgabe lässt sich mit folgendem Befehl verfolgen:

```sh
docker compose logs -f scraper
```

Für einen späteren manuellen Einmallauf ohne Zeitplan:

```sh
docker compose run --rm -e SCRAPER_CRON= scraper
```

Die SQLite-Datei liegt auf dem Host unter `media_data/database.db` und im Container unter `/data/database.db`. `docker compose down` entfernt die Container, lässt den Bind-Mount und die Datenbank bestehen. Zum Löschen der Datenbank muss die Datei im Host-Verzeichnis bewusst entfernt werden.

### Lokale Entwicklung

`compose-dev.yaml` baut den Workspace-Code mit `Dockerfile-dev` und startet die Container als Benutzer `app` mit den konfigurierten PUID/PGID-Werten:

```sh
docker compose -f compose-dev.yaml up -d --build
```

Da das Dev-Compose den Scraper als Abhängigkeit des Webservices startet, kann auch ein Web-Neustart einen Scrape auslösen. Nur den Webservice ohne Abhängigkeiten neu bauen und starten:

```sh
docker compose -f compose-dev.yaml build web
docker compose -f compose-dev.yaml up -d --no-deps web
```

Der Scraper protokolliert gefundene Produktseiten, Audio-Links und neu gespeicherte Zeilen getrennt. `Found ... product pages` bedeutet noch nicht, dass die Produkte bereits in SQLite stehen. Treffer werden nach jeder Produktseite committed; bei einem Abbruch bleiben bereits gespeicherte Treffer erhalten. Doppelte Audio-URLs werden ignoriert.

## Architektur

- **Web:** FastAPI, Jinja2 und lokale CSS-Dateien.
- **Scraper:** Python-Standardbibliothek (`urllib` und `html.parser`) sowie APScheduler für den Cron-Zeitplan; Chromium ist nicht erforderlich.
- **Datenbank:** SQLite mit eindeutiger Audio-URL.
- **Container:** `compose.yaml` verwendet das veröffentlichte Image; `compose-dev.yaml` baut den lokalen Quellcode. Beide verwenden einen Host-Bind-Mount für die SQLite-Datei.

## Lizenz und Rechte

Für dieses private, vollständig KI-erstellte Projekt wird derzeit **keine Open-Source-Lizenzdatei** mitgeliefert. Ohne Lizenz wird keine ausdrückliche Erlaubnis zur Weiterverwendung des Projektcodes erteilt; die konkrete Rechtslage für KI-generierte Inhalte hängt vom Einzelfall und der Rechtsordnung ab.

Falls der eigene Projektcode später bewusst zur Wiederverwendung freigegeben werden soll, ist MIT eine einfache Option **nur für den Originalcode, an dem eine Lizenz erteilt werden darf**. Eine solche Lizenz würde weder Rechte an Ravensburger/tiptoi® noch an Bildern, Audio-Dateien oder sonstigen Drittinhalten gewähren. Dies ist keine Rechtsberatung.
