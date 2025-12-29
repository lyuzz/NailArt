from typing import Any, Dict
import cv2
import numpy as np

from app.services.image_io import read_bgr, read_rgba
from app.services.mediapipe_hand import detect_hand
from app.services.nail_geometry import estimate_nail_polys, poly_mask, draw_polys
from app.services.blending import feather_blend, color_match
from app.services.storage import save_image
from app.core.config import DATA_DIR


def tryon(local_path: str, asset: Dict[str, Any], job_id: str) -> Dict[str, Any]:
    image_bgr, _ = read_bgr(local_path)
    hand = detect_hand(image_bgr)
    target_polys = estimate_nail_polys(hand.landmarks)

    nails = {nail["name"]: nail for nail in asset["nails_json"]["nails"]}

    result = image_bgr.copy()
    debug = draw_polys(image_bgr, target_polys)

    for name, target_poly in target_polys.items():
        if name not in nails:
            continue
        nail = nails[name]
        rgba_path = nail["rgba_url"].replace("/static/", "")
        rgba = read_rgba(DATA_DIR / rgba_path)

        canonical_poly = np.array(nail["canonical_poly"], dtype=np.float32)
        target = target_poly.astype(np.float32)
        h_matrix, _ = cv2.findHomography(canonical_poly, target)
        if h_matrix is None:
            continue

        warped = cv2.warpPerspective(
            rgba,
            h_matrix,
            (image_bgr.shape[1], image_bgr.shape[0]),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0, 0),
        )

        mask = poly_mask(image_bgr.shape[:2], target_poly)
        warped_bgr = warped[:, :, :3]
        warped_bgr = color_match(result, warped_bgr, mask)
        warped[:, :, :3] = warped_bgr

        result = feather_blend(result, warped, mask)

    result_url = save_image(result, Path("outputs/tryon") / job_id / "result.jpg")
    debug_url = save_image(debug, Path("outputs/tryon") / job_id / "debug.jpg")

    return {"result_url": result_url, "debug_url": debug_url}
