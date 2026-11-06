# Tiptoi Media Downloader

🌐 [English](README.en.md)

Eine private, inoffizielle Weboberfläche zum Durchsuchen öffentlich erreichbarer tiptoi®-Audioeinträge. Dieser Katalog dient als benutzerfreundliche Schnittstelle, um Inhalte zu finden und über die entsprechenden Anbieter zu öffnen.

## Wichtige Hinweise

- Dieses Projekt ist **nicht mit Ravensberger oder tiptoi® verbunden, wird nicht von ihnen unterstützt und ist kein offizielles Produkt**.
- Das Projekt wurde ausschließlich für private, experimentelle Zwecke erstellt. Eine Nutzung oder Weitergabe heruntergeladener Inhalte wird damit nicht erlaubt.
- Da Ravensberger derzeit keine offizielle native tiptoi®-Software für Linux anbietet, dient diese unabhängige Weboberfläche als Alternative.
- Das Projekt wurde mithilfe von KI erstellt. Code, Dokumentation und Gestaltung wurden KI-generiert; eine vollständige fachliche oder rechtliche Prüfung wird nicht zugesichert.
- Marken, Produktnamen, Bilder und Audiodateien gehören ihren jeweiligen Rechteinhabern. Dieses Projekt enthält und lizenziert diese Inhalte nicht.

## Funktionen

- **Einfaches Browsen:** Durchsuche den Katalog nach Produkten und finde die dazugehörigen `.gme`-Links.
- **Intelligente Suche:** Filtere Ergebnisse in Echtzeit während der Eingabe (inklusive deutscher Umlaute).
- **Anpassbare Ansicht:** Wähle zwischen verschiedenen Seitengrößen (25, 50, 75, 100 oder allen).
- **Modernes Design:** Automatischer Start im Darkmode mit einem praktischen Switch für den Wechsel zwischen hellem und dunklem Thema.
- **Mobiloptimiert:** Die Oberfläche ist so gestaltet, dass sie auch auf Mobilgeräten (Smartphone/Tablet) gut bedienbar ist.
- **Direkte Verknüpfung:** Der Link führt dich direkt zum entsprechenden Anbieter; die Audiodateien werden nicht lokal gespeichert.

## Screenshots

Die folgenden Screenshots verwenden synthetische Beispildaten und neutrale Platzhaltergrafiken. Sie enthalten keine Ravensberger-Bilder oder Audiodateien.

| Startseite   |      Suche      |
|:----------:|:-------------:|
| <img src="docs/screenshots/catalog-desktop_dark_light.png" alt="Desktopansicht mit Suchleiste, Seitenauswahl und Medienkarten" width="600">|<img src="docs/screenshots/catalog-desktop_dark_light_search.png" alt="Nach Forest gefilterte Treffer" width="600">  |
| <img src="docs/screenshots/catalog-mobile_dark_light.png" alt="Mobile Ansicht mit umbrochener Seitennavigation" width="200">| <img src="docs/screenshots/catalog-mobile_dark_light_search.png" alt="Mobile Ansicht mit umbrochener Seitennavigation" width="200">  |

## Start mit Docker Compose

Das System lässt sich einfach über Docker Compose starten.

**Voraussetzung:** Docker Engine und Docker Compose V2 müssen installiert sein.

1. **Installation:**
   ```bash
   git clone <Repository-URL>
   cd Tiptoi-Media-Downloader
   mv .env.example .env
   ```
2. **Start:**
   ```bash
   docker compose up -d
   ```
   Nach dem Start ist die Weboberfläche unter `http://localhost:8000` erreichbar. Der Scraper wird beim Start einmal direkt ausgeführt und dann auch nach einem festgelegten Zeitplan.

*Für Fortgeschrittene: Details zu Cron-Einstellungen, Datenbank-Pfaden oder spezifischen Identifikatoren können in der `.env` Datei angepasst werden.*

## Lizenz und Rechte

Für dieses private, vollständig KI-erstellte Projekt wird derzeit **keine Open-Source-Lizenz** mitgeliefert. Ohne Lizenz wird keine ausdrückliche Erlaubnis zur Weiterverwendung des Projektcodes erteilt; die konkrete Rechtslage für KI-generierte Inhalte hängt vom Einzelfund und der Rechtsordnung ab.
