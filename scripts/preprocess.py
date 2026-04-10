import cv2
import numpy as np
from config import MAX_DIM
from utils import resize_keep_aspect


def normalize_image(img):
    img = resize_keep_aspect(img, MAX_DIM)
    return img


def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def get_board_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, np.array([25, 20, 20]), np.array([110, 255, 255]))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = np.zeros(mask.shape, dtype=np.uint8)

    if cnts:
        largest = max(cnts, key=cv2.contourArea)
        cv2.drawContours(out, [largest], -1, 255, thickness=-1)
    else:
        out[:] = 255

    return out