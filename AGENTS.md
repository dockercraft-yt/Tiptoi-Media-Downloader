# Project Agent Instructions

Use these project-specific rules for all code, documentation, and container work. For user-facing overview and legal notes, see [README.md](README.md) and [docs/README.en.md](docs/README.en.md).

## Project Structure

- `app/main.py` implements the FastAPI web app, Jinja2 routes, search, pagination, and SQLite reads. Run it as `uvicorn app.main:app`.
- `app/scraper.py` fetches public product pages and records external `.gme` URLs; it does not download the audio files. Run it as `python -m app.scraper`.
- `app/templates/index.html` contains the page markup and browser-side search and theme behavior.
- `app/static/style.css` owns layout, responsive rules, and the dark/light palettes; `app/static/translations.json` holds the German and English UI texts.
- `docker/Dockerfile` builds the single image used by both services; the build context is the repository root.
- `requirements.txt` pins all Python dependencies.
- `docs/` holds the English README and the synthetic screenshots.
- `compose.yaml` runs the published GHCR image. `compose-dev.yaml` builds the workspace source with `docker/Dockerfile`. Both stay in the repository root because Compose reads `.env` and resolves `./media_data` relative to the Compose file.

## Data and Scraper Invariants

- The database path in both services is `/data/database.db`; both services must mount the same host directory at `/data`.
- Audio URLs are unique. Preserve the unique SQLite index and `INSERT OR IGNORE` behavior when changing ingestion.
- The scraper commits after each product page. Keep commits incremental so a stopped or interrupted run does not discard earlier pages.
- `Found N product pages` is only discovery progress. Use the final `Scraping finished` line and the saved-row count to report ingestion results.
- Scraper image URLs and audio URLs remain external references. Do not add media downloads or commit scraped third-party assets to the repository.

## Docker Workflow

- The default `compose.yaml` uses `ghcr.io/dockercraft-yt/tiptoi-media-downloader:latest`; editing source files does not update that image. Use `compose-dev.yaml` to test workspace changes.
- Both Compose files use `./media_data:/data`. Keep the host directory and database file writable by the selected numeric UID/GID.
- Production Compose passes `${PUID:-1000}:${PGID:-1000}` as the process user. Dev Compose builds the `app` account with matching PUID/PGID build arguments and runs as `app`.
- For a host user other than `1000:1000`, set `PUID` and `PGID` in `.env` and align ownership of `media_data` before starting the services.
- Validate Compose changes with `docker compose -f compose.yaml config` or `docker compose -f compose-dev.yaml config`.
- Build and run local code with `docker compose -f compose-dev.yaml build <service>` and `docker compose -f compose-dev.yaml up -d --no-deps <service>` when a dependent service, especially the scraper, should not be started. A normal `up` can start the scraper because the web service depends on it.
- Do not remove or recreate `media_data` as part of routine testing. It contains the persistent SQLite database.

## Releases and Image Tags

- The `VERSION` file in the repository root is the single source of the release version (plain `X.Y.Z`, no `v`).
- When `VERSION` changes on `main`, `.github/workflows/release.yml` builds and pushes the image as `vX.Y.Z`, then creates the Git tag and GitHub release. It fails if the tag already exists or is lower than the latest release. Do not create release tags by hand.
- `.github/workflows/build.yml` checks that pull requests still build and pushes `latest` on every relevant push to `main`.
- When a change breaks compatibility with older images (for example, renamed modules or changed Compose commands), increase at least the minor version.

## UI and Theme

- Dark mode is the default unless browser `localStorage` explicitly contains `theme=light`.
- Keep the theme control as an icon-only, accessible button: sun in dark mode to activate light mode; crescent moon in light mode to activate dark mode. Maintain its accessible name and tooltip when changing behavior.
- On mobile, keep the title and theme icon in the same header row. When the title wraps, align the icon with its first line and verify narrow widths as well as desktop.
- Keep the German and English READMEs in sync when user-visible features or setup instructions change.

## Branch and Change Workflow

- The shared development branch is `Development`; do not work directly on `main` unless the user asks.
- Do not create additional branches or commits unless explicitly requested.
- Preserve existing user changes. Keep edits scoped to the requested behavior and follow the style of nearby code.
- There is no established automated test suite in the repository. Prefer Docker/Compose checks for runtime changes and browser checks for UI behavior; do not assume host Python is the intended runtime.
- Preserve the project's third-party rights and unofficial-use notices. Use synthetic data for screenshots and examples; do not add copyrighted product artwork or audio.