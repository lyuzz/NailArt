from pathlib import Path

import cv2
import numpy as np

from app.services.extraction_pipeline import extract_nails
from app.services.tryon_pipeline import tryon
from app.services.mediapipe_hand import HandResult


def fake_hand(image_bgr):
    h, w = image_bgr.shape[:2]
    points = []
    for idx in range(21):
        x = int(w * (0.2 + (idx % 5) * 0.15))
        y = int(h * (0.2 + (idx // 5) * 0.15))
        points.append((x, y))
    return HandResult(handedness="Right", landmarks=points)


def _write_placeholder_images(tmp_path: Path) -> tuple[Path, Path]:
    hand = np.full((256, 256, 3), (220, 200, 180), dtype=np.uint8)
    cv2.circle(hand, (128, 128), 60, (200, 180, 160), 4)
    hand_path = tmp_path / "sample_hand.jpg"
    cv2.imwrite(str(hand_path), hand)

    nail = np.full((256, 256, 3), (60, 20, 120), dtype=np.uint8)
    cv2.rectangle(nail, (80, 80), (176, 176), (255, 255, 255), 3)
    nail_path = tmp_path / "sample_nail.jpg"
    cv2.imwrite(str(nail_path), nail)

    return hand_path, nail_path


def test_pipelines_smoke(monkeypatch, tmp_path):
    monkeypatch.setattr("app.services.mediapipe_hand.detect_hand", fake_hand)
    sample_hand, sample_nail = _write_placeholder_images(tmp_path)
    result = extract_nails(str(sample_hand), "job_smoke_extract")

    assert result["preview_url"]
    assert len(result["nails"]) == 5

    asset = {
        "nails_json": result["nails_json"],
    }

    output = tryon(str(sample_nail), asset, "job_smoke_tryon")
    assert "result_url" in output
    assert "debug_url" in output

    result_path = Path("backend/data") / output["result_url"].replace("/static/", "")
    debug_path = Path("backend/data") / output["debug_url"].replace("/static/", "")
    assert result_path.exists()
    assert debug_path.exists()
