FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system utilities needed for Playwright and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt \
    && find /usr/local -depth -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true \
    && find /usr/local -type f -name '*.pyc' -delete 2>/dev/null || true

# Install only Playwright Chromium Headless Shell and its Linux system dependencies, then prune redundant files
RUN python -m playwright install --with-deps --only-shell chromium \
    && rm -rf /root/.cache/ms-playwright/chromium-[0-9]* 2>/dev/null || true \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY src ./src
COPY frontend ./frontend
COPY tests ./tests
RUN mkdir -p /app/temp

EXPOSE 8000
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
