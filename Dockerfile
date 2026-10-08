FROM python:3.12-slim

ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION} \
    APP_ENV=docker \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gunicorn.conf.py .
COPY app/ app/

RUN useradd --create-home appuser
USER appuser

EXPOSE 5000
CMD ["gunicorn", "app.main:app"]
