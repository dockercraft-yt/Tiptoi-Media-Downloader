# Tiptoi Audio Link Catalog

A private, unofficial web interface for browsing publicly accessible tiptoi® audio entries. The scraper stores titles, preview images, and URLs to `.gme` files in SQLite. The download link then opens the file from its respective provider.

## Important Notes

- This project is **not affiliated with Ravensburger or tiptoi®**, is not supported by them, and is not an official product.
- The project was created exclusively for private, experimental purposes. This does not grant permission to use or redistribute downloaded content.
- To the best of the project's knowledge, Ravensburger currently does not offer official native tiptoi® software for Linux. This independent web interface is not an official replacement.
- The project was created entirely with AI. The code, documentation, and design were AI-generated; no guarantee is made that they have been fully reviewed for technical or legal correctness.
- Trademarks, product names, images, and audio files belong to their respective rights holders. This project does not include or license those materials. Check the applicable terms and rights before using them. Do not publish or distribute content unless you are authorized to do so.

## Features

- Scrapes product titles, preview images, and `.gme` links from the Ravensburger support site.
- Filters titles as you type, including German umlauts.
- Offers page sizes of 25, 50, 75, 100, or all entries.
- Keeps the search and page navigation sticky while scrolling.
- Redirects the download link to the external `.gme` file. The scraper does not store the audio file in SQLite or in the Docker volume.
- Uses SQLite in the persistent Docker volume `media_data` and prevents duplicate audio URLs.

## Screenshots

The screenshots below use synthetic sample records and neutral placeholder artwork. They do not contain Ravensburger images or audio files.

### Desktop

![Desktop view with search, page-size selection, and media cards](docs/screenshots/catalog-desktop.png)

### Search

![Results filtered for Forest](docs/screenshots/catalog-search.png)

### Mobile

![Mobile view with wrapped page navigation](docs/screenshots/catalog-mobile.png)

## Run with Docker Compose

Requirements: Docker Engine and Docker Compose V2.

```sh
docker compose up --build
```

Then open <http://localhost:8000>. Compose starts the web interface and runs the scraper once. Follow the scraper output with:

```sh
docker compose logs -f scraper
```

To run the scraper manually later:

```sh
docker compose run --rm scraper
```

The SQLite file is located at `/data/database.db` inside the container; the named volume `media_data` preserves it when containers are recreated. `docker compose down` removes the containers but keeps the volume. **`docker compose down -v` deletes the volume and the database.**

## Architecture

- **Web:** FastAPI, Jinja2, and local CSS files.
- **Scraper:** Python standard library (`urllib` and `html.parser`); Chromium is not required.
- **Database:** SQLite with unique audio URLs.
- **Container:** Multi-stage Dockerfile; source code is copied into the image, while data is stored separately in the volume.

## License and Rights

No **open-source license file** is currently included for this private, entirely AI-generated project. Without a license, no explicit permission is granted to reuse the project code; the legal status of AI-generated content depends on the specific circumstances and jurisdiction.

If you later decide to make the original project code available for reuse, MIT is a simple option **only for original code that you are legally entitled to license**. Such a license would not grant rights to Ravensburger/tiptoi®, images, audio files, or other third-party content. This is not legal advice.
