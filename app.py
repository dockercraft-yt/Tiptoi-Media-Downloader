from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import math
import os
import sqlite3
from urllib.parse import urlencode

# Configuration
DB_PATH = os.environ.get("DATABASE_PATH", "data/database.db")

os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            audio_url TEXT,
            image_url TEXT,
            version TEXT
        )
    ''')
    cursor.execute(
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
    cursor.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_media_audio_url
        ON media(audio_url)
        WHERE audio_url IS NOT NULL AND audio_url <> ''
        """
    )
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

app = FastAPI(title="Ravensburger Tiptoi Media Downloader")

# Mount static files for images and CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.create_function(
        "CASEFOLD",
        1,
        lambda value: str(value).casefold() if value is not None else "",
        deterministic=True,
    )
    return conn


def get_media_page(search, page, per_page):
    search = search.strip()
    page_size = None if per_page == "all" else int(per_page) if per_page in {"25", "50", "75", "100"} else 25
    where_clause = ""
    parameters = []

    if search:
        escaped_search = search.casefold().replace("!", "!!").replace("%", "!%").replace("_", "!_")
        where_clause = "WHERE CASEFOLD(COALESCE(title, '')) LIKE ? ESCAPE '!'"
        parameters.append(f"%{escaped_search}%")

    conn = get_db_connection()
    try:
        total = conn.execute(
            f"SELECT COUNT(*) FROM media {where_clause}",
            parameters,
        ).fetchone()[0]
        total_pages = max(1, math.ceil(total / page_size)) if page_size else 1
        page = min(max(page, 1), total_pages)
        query = f"SELECT * FROM media {where_clause} ORDER BY title COLLATE NOCASE, id"
        if page_size:
            items = conn.execute(
                f"{query} LIMIT ? OFFSET ?",
                [*parameters, page_size, (page - 1) * page_size],
            ).fetchall()
        else:
            items = conn.execute(query, parameters).fetchall()
    finally:
        conn.close()

    if total_pages <= 7:
        page_numbers = list(range(1, total_pages + 1))
    else:
        start = max(2, page - 2)
        end = min(total_pages - 1, page + 2)
        page_numbers = [1]
        if start > 2:
            page_numbers.append(None)
        page_numbers.extend(range(start, end + 1))
        if end < total_pages - 1:
            page_numbers.append(None)
        page_numbers.append(total_pages)

    start_item = (page - 1) * page_size + 1 if total and page_size else 1 if total else 0
    end_item = start_item + len(items) - 1 if total else 0
    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "page_numbers": page_numbers,
        "start_item": start_item,
        "end_item": end_item,
    }


def page_url(q, per_page, page):
    return f"/?{urlencode({'q': q, 'per_page': per_page, 'page': page})}"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, q: str = "", page: int = 1, per_page: str = "25"):
    results = get_media_page(q, page, per_page)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={**results, "q": q, "page_url": page_url},
    )


@app.get("/api/media")
async def api_media(q: str = "", page: int = 1, per_page: str = "25"):
    results = get_media_page(q, page, per_page)
    return {
        **results,
        "items": [dict(item) for item in results["items"]],
    }

@app.get("/download/{item_id}")
async def download(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT audio_url FROM media WHERE id=?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    
    if item:
        return RedirectResponse(item["audio_url"])
    raise HTTPException(status_code=404, detail="Not found")
