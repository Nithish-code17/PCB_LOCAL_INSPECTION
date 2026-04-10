import cv2
import numpy as np
from preprocess import to_gray


def align_to_reference(def_img, ref_img):
    if def_img.shape[:2] != ref_img.shape[:2]:
        def_img = cv2.resize(def_img, (ref_img.shape[1], ref_img.shape[0]))

    gray_ref = to_gray(ref_img).astype(np.float32) / 255.0
    gray_def = to_gray(def_img).astype(np.float32) / 255.0

    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-6)

    try:
        _, warp = cv2.findTransformECC(gray_ref, gray_def, warp, cv2.MOTION_AFFINE, criteria)
        aligned = cv2.warpAffine(
            def_img,
            warp,
            (ref_img.shape[1], ref_img.shape[0]),
            flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
            borderMode=cv2.BORDER_REPLICATE,
        )
        return aligned, {"method": "ecc", "ok": True}
    except cv2.error:
        return def_img, {"method": "resize_only", "ok": False}