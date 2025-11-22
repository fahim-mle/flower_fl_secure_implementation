#!/usr/bin/env bash
set -euo pipefail

SUPERLINK_ADDRESS="${SUPERLINK_ADDRESS:-superlink:9091}"
CLIENT_ID="${CLIENT_ID:-supernode-unknown}"
DATA_DIR="${DATA_DIR:-/data}"

export SUPERLINK_ADDRESS CLIENT_ID DATA_DIR

exec python -u /app/config/flwr_client_config.py
