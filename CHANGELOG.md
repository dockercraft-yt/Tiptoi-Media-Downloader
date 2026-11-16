# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden in dieser Datei festgehalten.

Das Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), die Versionsnummern folgen [Semantic Versioning](https://semver.org/lang/de/).

## [0.2.0] – unveröffentlicht

> **Achtung beim Update:** Die Python-Module wurden umbenannt, die Container starten jetzt mit `app.main:app` und `python -m app.scraper`. Die neue `compose.yaml` funktioniert deshalb nicht mit älteren Images bis `v0.1.2`. Übernimm `compose.yaml` und `.env.example` aus diesem Release, und setze `VERSION` in deiner `.env` auf `latest` oder `v0.2.0`.

### Hinzugefügt

- Datei `VERSION` als einzige Quelle für die Versionsnummer. Ändert sie sich auf `main`, baut ein Workflow das Image als `vX.Y.Z` und legt Git-Tag und GitHub-Release automatisch an.
- `requirements.txt` mit festen Versionen aller Python-Abhängigkeiten, damit Builds reproduzierbar sind.
- `restart: unless-stopped` für Web und Scraper: Beide Dienste starten nach einem Neustart des Hosts wieder von selbst.
- Dieser Changelog.

### Geändert

- Neue Ordnerstruktur: Python-Code, Templates und statische Dateien liegen in `app/`, das Dockerfile in `docker/`, die englische README in `docs/`.
- Templates und statische Dateien werden relativ zum Code gefunden statt relativ zum Arbeitsverzeichnis.
- Die beiden Image-Workflows sind zu `build.yml` zusammengelegt: Pull Requests werden nur gebaut, Pushes auf `main` als `latest` veröffentlicht.
- `.env.example` nutzt standardmäßig `VERSION=latest` und weist darauf hin, dass der Cron-Zeitplan in UTC gilt.

### Entfernt

- `Dockerfile-dev`, das eine exakte Kopie des `Dockerfile` war. `compose-dev.yaml` baut jetzt mit `docker/Dockerfile`.
- Tag-gesteuerter Image-Workflow. Versionen entstehen nur noch über die Datei `VERSION`.

### Behoben

- Firmenname in beiden READMEs korrigiert („Ravensburger“ statt „Ravensberger“ bzw. „Ravensberg“).
- Tippfehler in der deutschen README („Beispieldaten“, „Einzelfall“).
- README versprach, Datenbank-Pfade ließen sich in der `.env` einstellen. Sie nennt jetzt die tatsächlich verfügbaren Einstellungen.

## [0.1.2] – 2026-11-07

### Hinzugefügt

- Oberfläche auf Deutsch und Englisch. Die Sprache richtet sich nach der Browsersprache.
- Image-Version in Compose über `VERSION` in der `.env` einstellbar.
- `.env.example` mit Cron-Zeitplan, Image-Version und PUID/PGID.

### Geändert

- Pushes auf `main` veröffentlichen kein eigenes `main`-Image-Tag mehr.

### Behoben

- Tippfehler in den READMEs.

## [0.1.1] – 2026-11-07

### Hinzugefügt

- Zeitgesteuerter Scraper: Er läuft beim Start einmal und danach nach dem Cron-Zeitplan aus `SCRAPER_CRON` (Standard: täglich 03:00 UTC).
- `compose-dev.yaml`, um den aktuellen Quellcode lokal als Image zu bauen und zu testen.

### Geändert

- READMEs überarbeitet, neue Screenshots für Hell- und Dunkelmodus auf Desktop und Mobil.

## [0.1.0] – 2026-11-01

Erste Version.

### Hinzugefügt

- Weboberfläche (FastAPI und Jinja2) zum Durchsuchen öffentlich erreichbarer tiptoi®-Audiodateien.
- Suche, die schon während der Eingabe filtert, auch mit deutschen Umlauten.
- Seitengrößen von 25, 50, 75, 100 oder allen Einträgen, mit fixierter Such- und Seitenleiste.
- Hell- und Dunkelmodus (Standard: dunkel), für Mobilgeräte optimiert.
- Scraper ohne zusätzliche Abhängigkeiten, der Titel, Vorschaubild und `.gme`-Link in SQLite speichert. Doppelte Audio-URLs werden verhindert.
- Download-Link, der direkt zur Datei beim Anbieter weiterleitet. Audiodateien werden nicht lokal gespeichert.
- Docker-Image mit mehrstufigem Build, das ohne Root-Rechte läuft und für amd64 und arm64 auf GHCR veröffentlicht wird.
- Docker-Compose-Setup mit getrenntem Web- und Scraper-Dienst.
- READMEs auf Deutsch und Englisch mit Hinweisen zu Rechten und KI-Erstellung.

[0.2.0]: https://github.com/dockercraft-yt/Tiptoi-Media-Downloader/compare/v0.1.2...Development
[0.1.2]: https://github.com/dockercraft-yt/Tiptoi-Media-Downloader/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/dockercraft-yt/Tiptoi-Media-Downloader/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/dockercraft-yt/Tiptoi-Media-Downloader/releases/tag/v0.1.0
