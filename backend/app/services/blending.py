from typing import Tuple
import numpy as np
import cv2


def feather_blend(base_bgr: np.ndarray, patch_rgba: np.ndarray, mask: np.ndarray) -> np.ndarray:
    if patch_rgba.shape[2] == 3:
        alpha = mask.astype(np.float32) / 255.0
    else:
        alpha = patch_rgba[:, :, 3].astype(np.float32) / 255.0
        alpha = alpha * (mask.astype(np.float32) / 255.0)

    alpha = cv2.GaussianBlur(alpha, (21, 21), 0)
    alpha = np.clip(alpha, 0, 1)[..., None]

    patch_bgr = patch_rgba[:, :, :3].astype(np.float32)
    base = base_bgr.astype(np.float32)
    blended = alpha * patch_bgr + (1 - alpha) * base
    return blended.astype(np.uint8)


def color_match(base_bgr: np.ndarray, patch_bgr: np.ndarray, mask: np.ndarray) -> np.ndarray:
    masked = mask > 0
    if masked.sum() == 0:
        return patch_bgr
    base_mean = base_bgr[masked].mean(axis=0)
    patch_mean = patch_bgr[masked].mean(axis=0)
    scale = np.clip(base_mean / (patch_mean + 1e-6), 0.7, 1.3)
    adjusted = np.clip(patch_bgr * scale, 0, 255).astype(np.uint8)
    return adjusted
