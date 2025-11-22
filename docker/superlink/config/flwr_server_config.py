"""Flower SuperLink configuration for insecure validation run."""

from __future__ import annotations

import logging
import os

import flwr as fl


def start_superlink() -> None:
    """Start a minimal Flower server binding to env-provided address."""
    host = os.getenv("SUPERLINK_HOST", "0.0.0.0")
    port = os.getenv("SUPERLINK_PORT", "9091")
    num_rounds = int(os.getenv("SUPERLINK_ROUNDS", "3"))
    server_address = f"{host}:{port}"

    logging.info("Starting SuperLink on %s for %s rounds", server_address, num_rounds)

    strategy = fl.server.strategy.FedAvg(
        fraction_fit=1.0,
        fraction_evaluate=1.0,
        min_fit_clients=2,
        min_evaluate_clients=2,
        min_available_clients=2,
    )

    fl.server.start_server(
        server_address=server_address,
        config=fl.server.ServerConfig(num_rounds=num_rounds),
        strategy=strategy,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    start_superlink()
