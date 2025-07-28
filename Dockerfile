FROM python:3.11-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /install

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install/packages \
                --no-cache-dir \
                -f https://download.pytorch.org/whl/cpu/torch_stable.html \
                -r requirements.txt && \
    find /install/packages -type d -name '__pycache__' -exec rm -rf {} + && \
    find /install/packages -type f -name '*.pyc' -delete && \
    find /install/packages -type d -name 'tests' -exec rm -rf {} + && \
    rm -rf /root/.cache /install/packages/**/*.dist-info

FROM python:3.11-slim-bookworm

RUN adduser --disabled-password --gecos '' appuser
USER appuser

WORKDIR /app

COPY --chown=appuser:appuser app/main.py ./main.py
COPY --chown=appuser:appuser app/config.py ./config.py
COPY --chown=appuser:appuser app/embedding_utils.py ./embedding_utils.py
COPY --chown=appuser:appuser app/output_builder.py ./output_builder.py
COPY --chown=appuser:appuser app/pdf_processor.py ./pdf_processor.py
COPY --chown=appuser:appuser app/ranking.py ./ranking.py

COPY --from=builder /install/packages /usr/local

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
