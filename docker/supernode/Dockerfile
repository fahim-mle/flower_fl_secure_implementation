# Flower SuperNode container for insecure validation run.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY config ./config
COPY entrypoint.sh /entrypoint.sh

RUN pip install --no-cache-dir flwr==1.7.0 numpy==1.26.4 \
    && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
