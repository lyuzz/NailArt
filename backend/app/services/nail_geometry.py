from typing import Dict, List, Tuple
import numpy as np
import cv2

Finger = Tuple[int, int, int]

FINGER_INDICES: Dict[str, Finger] = {
    "thumb": (4, 3, 2),
    "index": (8, 7, 6),
    "middle": (12, 11, 10),
    "ring": (16, 15, 14),
    "pinky": (20, 19, 18),
}


def _finger_poly(landmarks: List[Tuple[int, int]], tip: int, dip: int, pip: int) -> np.ndarray:
    tip_pt = np.array(landmarks[tip], dtype=np.float32)
    dip_pt = np.array(landmarks[dip], dtype=np.float32)
    pip_pt = np.array(landmarks[pip], dtype=np.float32)
    direction = tip_pt - dip_pt
    norm = np.linalg.norm(direction) + 1e-6
    direction /= norm
    perp = np.array([-direction[1], direction[0]], dtype=np.float32)
    width = np.linalg.norm(dip_pt - pip_pt) * 0.6
    length = np.linalg.norm(tip_pt - dip_pt) * 0.9

    center = dip_pt + direction * (length * 0.5)
    half_w = width * 0.5
    half_l = length * 0.5

    p1 = center - direction * half_l + perp * half_w
    p2 = center - direction * half_l - perp * half_w
    p3 = center + direction * half_l - perp * half_w
    p4 = center + direction * half_l + perp * half_w

    return np.stack([p1, p2, p3, p4], axis=0)


def estimate_nail_polys(landmarks: List[Tuple[int, int]]) -> Dict[str, np.ndarray]:
    polys: Dict[str, np.ndarray] = {}
    for name, (tip, dip, pip) in FINGER_INDICES.items():
        polys[name] = _finger_poly(landmarks, tip, dip, pip)
    return polys


def poly_mask(image_shape: Tuple[int, int], poly: np.ndarray) -> np.ndarray:
    mask = np.zeros(image_shape, dtype=np.uint8)
    pts = poly.astype(np.int32)
    cv2.fillPoly(mask, [pts], 255)
    return mask


def draw_polys(image: np.ndarray, polys: Dict[str, np.ndarray], labels: bool = True) -> np.ndarray:
    out = image.copy()
    for name, poly in polys.items():
        pts = poly.astype(np.int32)
        cv2.polylines(out, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        if labels:
            center = pts.mean(axis=0).astype(int)
            cv2.putText(out, name, tuple(center), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    return out
