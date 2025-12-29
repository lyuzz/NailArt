from typing import Dict, List, Any
from pathlib import Path
import cv2
import numpy as np

from app.services.image_io import read_bgr, rgb_to_bgr
from app.services.mediapipe_hand import detect_hand
from app.services.nail_geometry import estimate_nail_polys, poly_mask, draw_polys
from app.services.storage import save_image
from app.core.config import OUTPUT_EXTRACT_DIR


def extract_nails(local_path: str, job_id: str) -> Dict[str, Any]:
    image_bgr, _ = read_bgr(local_path)
    hand = detect_hand(image_bgr)
    polys = estimate_nail_polys(hand.landmarks)

    output_dir = OUTPUT_EXTRACT_DIR / job_id
    output_dir.mkdir(parents=True, exist_ok=True)

    nails: List[Dict[str, Any]] = []
    for name, poly in polys.items():
        mask = poly_mask(image_bgr.shape[:2], poly)
        x, y, w, h = cv2.boundingRect(poly.astype(np.int32))
        cropped = image_bgr[y : y + h, x : x + w]
        cropped_mask = mask[y : y + h, x : x + w]
        rgba = cv2.cvtColor(cropped, cv2.COLOR_BGR2BGRA)
        rgba[:, :, 3] = cropped_mask

        rgba_url = save_image(rgba, Path("outputs/extract") / job_id / f"{name}.png")
        mask_url = save_image(cropped_mask, Path("outputs/extract") / job_id / f"{name}_mask.png")

        canonical_poly = (poly - np.array([x, y], dtype=np.float32)).tolist()
        nails.append(
            {
                "name": name,
                "rgba_url": rgba_url,
                "mask_url": mask_url,
                "canonical_poly": canonical_poly,
                "meta": {"bbox": [int(x), int(y), int(w), int(h)]},
            }
        )

    preview = draw_polys(image_bgr, polys)
    preview_url = save_image(preview, Path("outputs/extract") / job_id / "preview.jpg")

    nails_json = {"nails": nails}
    suggested_asset = {
        "owner_type": "user",
        "title": f"Extracted {job_id}",
        "type": "set5",
        "preview_url": preview_url,
        "nails_json": nails_json,
    }

    return {
        "preview_url": preview_url,
        "nails": [
            {"name": nail["name"], "rgba_url": nail["rgba_url"], "mask_url": nail["mask_url"]}
            for nail in nails
        ],
        "suggested_asset": suggested_asset,
        "nails_json": nails_json,
    }
