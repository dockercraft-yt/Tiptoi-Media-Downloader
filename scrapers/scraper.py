from html.parser import HTMLParser
import logging
import os
import sqlite3
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

DB_PATH = os.environ.get("DATABASE_PATH", "data/database.db")
ROOT_URL = "https://service.ravensburger.de/tiptoi%C2%AE/tiptoi%C2%AE_Audiodateien"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class PageParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.links = []
        self.active_link = None
        self.heading_parts = None
        self.title = ""

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and attributes.get("href"):
            self.active_link = {
                "href": attributes["href"],
                "text_parts": [],
                "image_url": None,
            }
        elif tag == "img" and self.active_link:
            image_url = attributes.get("src") or attributes.get("data-src")
            if image_url:
                self.active_link["image_url"] = urljoin(self.base_url, image_url)
        elif tag == "h1":
            self.heading_parts = []

    def handle_data(self, data):
        if self.active_link:
            self.active_link["text_parts"].append(data)
        if self.heading_parts is not None:
            self.heading_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.active_link:
            link = self.active_link
            link["href"] = urljoin(self.base_url, link["href"])
            link["text"] = " ".join(" ".join(link.pop("text_parts")).split())
            self.links.append(link)
            self.active_link = None
        elif tag == "h1" and self.heading_parts is not None:
            if not self.title:
                self.title = " ".join(" ".join(self.heading_parts).split())
            self.heading_parts = None


def fetch_page(url):
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "de-DE,de;q=0.9",
        },
    )
    try:
        with urlopen(request, timeout=60) as response:
            if response.status != 200:
                raise RuntimeError(f"Ravensburger returned HTTP {response.status} for {url}")
            parser = PageParser(response.geturl())
            parser.feed(response.read().decode("utf-8", errors="replace"))
            return parser
    except HTTPError as error:
        raise RuntimeError(f"Ravensburger returned HTTP {error.code} for {url}") from error
    except URLError as error:
        raise RuntimeError(f"Could not fetch {url}: {error.reason}") from error


def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                audio_url TEXT,
                image_url TEXT,
                version TEXT
            )
            """
        )
        conn.execute(
            """
            DELETE FROM media
            WHERE audio_url IS NOT NULL AND audio_url <> ''
              AND id NOT IN (
                  SELECT MIN(id) FROM media
                  WHERE audio_url IS NOT NULL AND audio_url <> ''
                  GROUP BY audio_url
              )
            """
        )
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_media_audio_url
            ON media(audio_url)
            WHERE audio_url IS NOT NULL AND audio_url <> ''
            """
        )
        conn.commit()
    finally:
        conn.close()


def extract_product_links(root_url, links):
    root = urlsplit(root_url)
    path_prefix = root.path.rstrip("/") + "/"
    products = []
    seen_urls = set()

    for link in links:
        title = " ".join(link.get("text", "").split())
        href = link.get("href", "")
        parsed_url = urlsplit(href)
        title_lower = title.lower()

        if parsed_url.netloc != root.netloc or not parsed_url.path.startswith(path_prefix):
            continue
        relative_path = parsed_url.path[len(path_prefix):]
        if len([part for part in relative_path.split("/") if part]) < 2:
            continue
        if "audiodatei" not in title_lower and "audioatei" not in title_lower:
            continue
        if href in seen_urls:
            continue

        seen_urls.add(href)
        products.append({"title": title, "href": href})

    return products


def extract_audio_records(title, links):
    records = []
    for link in links:
        href = link.get("href", "")
        if urlsplit(href).path.lower().endswith(".gme"):
            records.append((title, href, link.get("image_url"), "Standard"))
    return records


def scrape_ravensburger():
    init_db()
    listing = fetch_page(ROOT_URL)
    products = extract_product_links(ROOT_URL, listing.links)
    if not products:
        raise RuntimeError("No product links found; the Ravensburger page structure may have changed")

    logger.info("Found %d product pages", len(products))
    scraped_records = []

    for product in products:
        try:
            article = fetch_page(product["href"])
        except RuntimeError as error:
            logger.warning("Skipping %s: %s", product["href"], error)
            continue

        title = article.title or product["title"]
        records = extract_audio_records(title, article.links)
        if records:
            scraped_records.extend(records)
        else:
            logger.debug("No GME file found on %s", product["href"])

        time.sleep(0.3)

    if not scraped_records:
        raise RuntimeError("No .gme audio links found on the product pages")

    conn = sqlite3.connect(DB_PATH)
    try:
        inserted = 0
        for record in scraped_records:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO media (title, audio_url, image_url, version)
                VALUES (?, ?, ?, ?)
                """,
                record,
            )
            inserted += cursor.rowcount
        conn.commit()
    finally:
        conn.close()

    logger.info(
        "Scraping finished: %d audio files found, %d new rows saved",
        len(scraped_records),
        inserted,
    )


if __name__ == "__main__":
    scrape_ravensburger()
