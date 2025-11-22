#!/usr/bin/env bash
set -euo pipefail

SUPERLINK_HOST="${SUPERLINK_HOST:-0.0.0.0}"
SUPERLINK_PORT="${SUPERLINK_PORT:-9091}"
SUPERLINK_ROUNDS="${SUPERLINK_ROUNDS:-3}"

export SUPERLINK_HOST SUPERLINK_PORT SUPERLINK_ROUNDS

exec python -u /app/config/flwr_server_config.py
