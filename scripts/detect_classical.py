import cv2
import numpy as np


def detect_missing_component(ref_img, def_img):
    gray_ref = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    gray_def = cv2.cvtColor(def_img, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray_ref, gray_def)
    diff = cv2.GaussianBlur(diff, (5, 5), 0)

    _, th = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))

    results = []
    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 250:
            continue
        x, y, w, h = cv2.boundingRect(c)
        if w < 15 or h < 15:
            continue
        results.append({
            "type": "missing_component_or_major_mismatch",
            "bbox": (x, y, w, h),
            "score": round(float(area), 2),
            "mask": th
        })
    return results, th


def detect_scratch(ref_img, def_img):
    gray_ref = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    gray_def = cv2.cvtColor(def_img, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray_ref, gray_def)
    diff = cv2.GaussianBlur(diff, (3, 3), 0)

    edges = cv2.Canny(diff, 30, 100)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)

    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=20,
        minLineLength=20,
        maxLineGap=10,
    )

    results = []
    mask = np.zeros_like(gray_ref)

    if lines is not None:
        for ln in lines:
            x1, y1, x2, y2 = ln[0]
            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            angle = abs(np.degrees(np.arctan2(y2 - y1, x2 - x1)))

            if length < 20:
                continue
            if angle < 8 or angle > 85:
                continue

            cv2.line(mask, (x1, y1), (x2, y2), 255, 3)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 30:
            continue
        x, y, w, h = cv2.boundingRect(c)
        aspect = max(w, h) / max(1, min(w, h))
        if aspect < 1.8:
            continue
        results.append({
            "type": "scratch",
            "bbox": (x, y, w, h),
            "score": round(float(area), 2),
            "mask": mask
        })

    return results, mask


def detect_dent_or_blob(ref_img, def_img):
    gray_ref = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    gray_def = cv2.cvtColor(def_img, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray_ref, gray_def)
    diff = cv2.GaussianBlur(diff, (5, 5), 0)

    _, th = cv2.threshold(diff, 28, 255, cv2.THRESH_BINARY)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    results = []
    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 80 or area > 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        aspect = max(w, h) / max(1, min(w, h))
        if aspect > 2.5:
            continue
        results.append({
            "type": "dent_or_blob_defect",
            "bbox": (x, y, w, h),
            "score": round(float(area), 2),
            "mask": th
        })

    return results, th