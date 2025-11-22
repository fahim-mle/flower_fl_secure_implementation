"""Utility helpers to create and load synthetic datasets for SuperNodes."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np


def _dataset_path(client_id: str, data_dir: Path) -> Path:
    sanitized = client_id.replace("/", "_")
    return data_dir / f"{sanitized}_dataset.npz"


def _generate_dataset(path: Path, num_samples: int = 256, num_features: int = 5) -> None:
    rng = np.random.default_rng(seed=abs(hash(path.stem)) % (2**32))
    weights = rng.normal(size=(num_features,), loc=0.0, scale=1.0)
    bias = rng.normal()
    X = rng.normal(size=(num_samples, num_features), loc=0.0, scale=1.0).astype("float32")
    noise = rng.normal(scale=0.05, size=(num_samples,)).astype("float32")
    y = (X @ weights.astype("float32")) + bias + noise
    np.savez(path, X=X, y=y.astype("float32"))


def load_local_dataset(client_id: str, data_directory: str) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    """Return train/test splits, creating synthetic data on first run."""
    data_dir = Path(data_directory)
    data_dir.mkdir(parents=True, exist_ok=True)

    dataset_path = _dataset_path(client_id, data_dir)
    if not dataset_path.exists():
        _generate_dataset(dataset_path)

    with np.load(dataset_path) as data:
        X = data["X"]
        y = data["y"]

    cutoff = int(0.8 * len(X))
    train = (X[:cutoff], y[:cutoff])
    test = (X[cutoff:], y[cutoff:])
    return train, test
