from pathlib import Path
from typing import Tuple, Union
import os
import numpy as np
from PIL import Image
import cv2
from fastapi import UploadFile

from app.core.config import DATA_DIR, UPLOAD_DIR, STATIC_URL_PREFIX


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_upload(file: UploadFile) -> Tuple[str, str]:
    ensure_dirs()
    filename = Path(file.filename or "upload.jpg").name
    target_path = UPLOAD_DIR / f"{os.getpid()}_{filename}"
    with target_path.open("wb") as f:
        f.write(file.file.read())
    rel_path = target_path.relative_to(DATA_DIR)
    return str(target_path), f"{STATIC_URL_PREFIX}/{rel_path.as_posix()}"


def save_bytes(data: bytes, rel_path: Union[str, Path]) -> str:
    rel_path = Path(rel_path)
    target_path = DATA_DIR / rel_path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("wb") as f:
        f.write(data)
    return f"{STATIC_URL_PREFIX}/{rel_path.as_posix()}"


def save_image(image: Union[np.ndarray, Image.Image], rel_path: Union[str, Path]) -> str:
    rel_path = Path(rel_path)
    target_path = DATA_DIR / rel_path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(image, np.ndarray):
        if image.ndim == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif image.ndim == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        img = Image.fromarray(image)
    else:
        img = image
    img.save(target_path)
    return f"{STATIC_URL_PREFIX}/{rel_path.as_posix()}"


def read_image(path: Union[str, Path]) -> Image.Image:
    return Image.open(path)
