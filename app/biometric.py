from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class BiometricFeatures:
    # Example aggregated behavioral features (toy)
    avg_key_dwell_ms: float
    avg_key_flight_ms: float
    typing_error_rate: float
    mouse_avg_speed: float
    mouse_pause_rate: float

def to_vector(f: BiometricFeatures) -> np.ndarray:
    # Keep ordering fixed!
    return np.array([
        f.avg_key_dwell_ms,
        f.avg_key_flight_ms,
        f.typing_error_rate,
        f.mouse_avg_speed,
        f.mouse_pause_rate
    ], dtype=np.float32)

def normalize(vec: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    # Simple standardization placeholder. In production:
    # - fit scaler on historical legit sessions per population
    # - version your scaler
    mean = vec.mean()
    std = vec.std()
    return (vec - mean) / (std + eps)

def cosine_similarity(a: np.ndarray, b: np.ndarray, eps: float = 1e-8) -> float:
    return float(np.dot(a, b) / ((np.linalg.norm(a) * np.linalg.norm(b)) + eps))