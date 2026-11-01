FROM python:3.11-slim AS dependencies
RUN pip install --no-cache-dir --prefix=/install fastapi uvicorn jinja2

FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/data/database.db
COPY --from=dependencies /install /usr/local
WORKDIR /app
COPY app.py ./
COPY scrapers/ ./scrapers/
COPY templates/ ./templates/
COPY static/ ./static/
RUN mkdir -p /data

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
