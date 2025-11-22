"""Flower SuperNode client configuration for insecure validation."""

from __future__ import annotations

import logging
import os
import time
from typing import Dict, List, Tuple

import flwr as fl
import numpy as np

from dataset_loader import load_local_dataset


class LinearRegressionClient(fl.client.NumPyClient):
    """Minimal NumPy-based client for demonstration purposes."""

    def __init__(self, client_id: str, data_dir: str, epochs: int = 5, lr: float = 0.01) -> None:
        self.client_id = client_id
        self.epochs = epochs
        self.lr = lr

        (self.x_train, self.y_train), (self.x_test, self.y_test) = load_local_dataset(client_id, data_dir)
        num_features = self.x_train.shape[1]
        self.weights = np.zeros(num_features, dtype="float32")
        self.bias = np.zeros(1, dtype="float32")

    def get_parameters(self, config: Dict[str, str]) -> List[np.ndarray]:
        return [self.weights, self.bias]

    def _set_parameters(self, parameters: List[np.ndarray]) -> None:
        self.weights = parameters[0].astype("float32")
        self.bias = parameters[1].astype("float32")

    def fit(self, parameters: List[np.ndarray], config: Dict[str, str]) -> Tuple[List[np.ndarray], int, Dict[str, float]]:
        self._set_parameters(parameters)
        for _ in range(self.epochs):
            self._train_epoch()
        loss = self._loss(self.x_train, self.y_train)
        metrics = {"train_loss": float(loss)}
        return self.get_parameters(config), len(self.y_train), metrics

    def evaluate(self, parameters: List[np.ndarray], config: Dict[str, str]) -> Tuple[float, int, Dict[str, float]]:
        self._set_parameters(parameters)
        loss = self._loss(self.x_test, self.y_test)
        return float(loss), len(self.y_test), {"test_loss": float(loss)}

    def _train_epoch(self) -> None:
        preds = self.x_train @ self.weights + self.bias
        error = preds.reshape(-1) - self.y_train
        grad_w = self.x_train.T @ error / len(self.x_train)
        grad_b = np.mean(error)
        self.weights -= self.lr * grad_w.astype("float32")
        self.bias -= self.lr * grad_b.astype("float32")

    def _loss(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        preds = x @ self.weights + self.bias
        error = preds.reshape(-1) - y
        return np.mean(error**2)


def connect_with_retry(client: fl.client.Client, server_address: str, max_backoff: int = 30) -> None:
    """Attempt to connect to the SuperLink until successful."""
    backoff = 2
    while True:
        try:
            fl.client.start_numpy_client(server_address=server_address, client=client)
            break
        except Exception as err:  # pragma: no cover - runtime logging
            logging.warning("Client %s failed to connect (%s). Retrying in %ss", client.client_id, err, backoff)
            time.sleep(backoff)
            backoff = min(backoff * 2, max_backoff)


def main() -> None:
    client_id = os.getenv("CLIENT_ID", "supernode-unknown")
    data_dir = os.getenv("DATA_DIR", "/data")
    server_address = os.getenv("SUPERLINK_ADDRESS", "superlink:9091")

    logging.info("Starting client %s targeting %s", client_id, server_address)
    client = LinearRegressionClient(client_id=client_id, data_dir=data_dir)
    connect_with_retry(client, server_address)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    main()
