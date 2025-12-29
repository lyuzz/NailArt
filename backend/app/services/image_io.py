from pathlib import Path
from typing import Tuple
import numpy as np
import cv2

from app.utils.errors import ImageReadError


def read_bgr(path: str) -> Tuple[np.ndarray, Tuple[int, int]]:
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise ImageReadError(f"Failed to read image: {path}")
    h, w = img.shape[:2]
    return img, (w, h)


def read_rgba(path: str) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ImageReadError(f"Failed to read image: {path}")
    if img.shape[2] == 3:
        alpha = np.full((img.shape[0], img.shape[1], 1), 255, dtype=img.dtype)
        img = np.concatenate([img, alpha], axis=2)
    return img


def bgr_to_rgb(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def rgb_to_bgr(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
