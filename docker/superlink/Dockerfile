# Placeholder Dockerfile for Flower SuperLink service.
FROM python:3.11-slim
WORKDIR /app
COPY config ./config
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
