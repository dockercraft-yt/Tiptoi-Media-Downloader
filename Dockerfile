FROM python:3.11-slim AS dependencies
RUN pip install --no-cache-dir --prefix=/install fastapi uvicorn jinja2 apscheduler==3.11.0

FROM python:3.11-slim AS runtime
ARG PUID=1000
ARG PGID=1000
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/data/database.db
COPY --from=dependencies /install /usr/local
WORKDIR /app
COPY app.py ./
COPY scrapers/ ./scrapers/
COPY templates/ ./templates/
COPY static/ ./static/
RUN groupadd --gid "${PGID}" app \
    && useradd --uid "${PUID}" --gid "${PGID}" --no-create-home --shell /usr/sbin/nologin app \
    && mkdir -p /data \
    && chown app:app /data

USER app
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
