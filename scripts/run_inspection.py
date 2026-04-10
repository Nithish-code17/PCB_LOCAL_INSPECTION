from pathlib import Path
import cv2
import numpy as np

from config import (
    REFERENCE_DIR,
    DEFECTIVE_DIR,
    ANNOTATED_DIR,
    MASKS_DIR,
    HEATMAPS_DIR,
    CROPS_DIR,
    REPORTS_DIR,
)
from utils import (
    ensure_output_dirs,
    list_images,
    read_image,
    save_text,
)
from preprocess import normalize_image
from align import align_to_reference
from detect_classical import (
    detect_missing_component,
    detect_scratch,
    detect_dent_or_blob,
)


def draw_results(img, results):
    out = img.copy()
    for i, r in enumerate(results, 1):
        x, y, w, h = r["bbox"]

        if r["type"] == "scratch":
            color = (0, 0, 255)
        elif "missing" in r["type"]:
            color = (255, 0, 0)
        else:
            color = (0, 165, 255)

        cv2.rectangle(out, (x, y), (x + w, y + h), color, 2)
        label = f"{i}: {r['type']}"
        cv2.putText(
            out,
            label,
            (x, max(18, y - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2,
            cv2.LINE_AA,
        )
    return out


def save_mask(path: Path, mask: np.ndarray):
    cv2.imwrite(str(path), mask)


def save_heatmap(path: Path, mask: np.ndarray):
    colored = cv2.applyColorMap(mask, cv2.COLORMAP_JET)
    cv2.imwrite(str(path), colored)


def save_crops(img, results):
    for i, r in enumerate(results, 1):
        x, y, w, h = r["bbox"]
        pad = 20
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(img.shape[1], x + w + pad)
        y2 = min(img.shape[0], y + h + pad)
        crop = img[y1:y2, x1:x2]
        cv2.imwrite(str(CROPS_DIR / f"crop_{i}.png"), crop)


def process_side(side: str):
    ref_folder = REFERENCE_DIR / side
    def_folder = DEFECTIVE_DIR / side

    refs = list_images(ref_folder)
    defs = list_images(def_folder)

    if not refs:
        print(f"[WARN] No reference image found in {ref_folder}")
        return
    if not defs:
        print(f"[WARN] No defective images found in {def_folder}")
        return

    ref_img = normalize_image(read_image(refs[0]))

    for img_path in defs:
        print(f"[INFO] Processing {side}: {img_path.name}")
        def_img = normalize_image(read_image(img_path))
        aligned, align_info = align_to_reference(def_img, ref_img)

        missing_results, missing_mask = detect_missing_component(ref_img, aligned)
        scratch_results, scratch_mask = detect_scratch(ref_img, aligned)
        dent_results, dent_mask = detect_dent_or_blob(ref_img, aligned)

        all_results = scratch_results + missing_results + dent_results

        combined_mask = np.maximum.reduce([missing_mask, scratch_mask, dent_mask])
        annotated = draw_results(aligned, all_results)

        stem = f"{side}_{img_path.stem}"

        cv2.imwrite(str(ANNOTATED_DIR / f"{stem}_annotated.png"), annotated)
        save_mask(MASKS_DIR / f"{stem}_mask.png", combined_mask)
        save_heatmap(HEATMAPS_DIR / f"{stem}_heatmap.png", combined_mask)
        save_crops(aligned, all_results)

        lines = [
            f"Image: {img_path.name}",
            f"Side: {side}",
            f"Alignment: {align_info}",
            f"Total defects: {len(all_results)}",
            ""
        ]

        for i, r in enumerate(all_results, 1):
            lines.append(f"Defect #{i}")
            lines.append(f"  Type : {r['type']}")
            lines.append(f"  Score: {r['score']}")
            lines.append(f"  BBox : {r['bbox']}")
            lines.append("")

        save_text(REPORTS_DIR / f"{stem}_report.txt", "\n".join(lines))


def main():
    ensure_output_dirs([ANNOTATED_DIR, MASKS_DIR, HEATMAPS_DIR, CROPS_DIR, REPORTS_DIR])

    process_side("front")
    process_side("back")

    print("[DONE] Inspection complete.")


if __name__ == "__main__":
    main()