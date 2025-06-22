import cv2
import numpy as np
from PIL import Image
import os

def preprocess(image_path: str, upscale: int = 3) -> np.ndarray:
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {image_path}")
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"OpenCV가 이미지를 읽지 못했습니다: {image_path}")
    
    if upscale > 1:
        img = cv2.resize(img, None, fx=upscale, fy=upscale, interpolation=cv2.INTER_CUBIC)

    blur = cv2.GaussianBlur(img, (0, 0), 3)
    sharp = cv2.addWeighted(img, 1.5, blur, -0.5, 0)

    _, img_bin = cv2.threshold(
        sharp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    kernel = np.ones((2, 2), np.uint8)
    processed = cv2.morphologyEx(
        img_bin,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1
    )
    return processed

def save_temp(img: np.ndarray, path: str):
    Image.fromarray(img).save(path)
