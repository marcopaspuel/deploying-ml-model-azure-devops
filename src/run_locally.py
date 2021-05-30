import os
import cv2
from pathlib import Path

from src.detect import detect_and_draw_box

if __name__ == "__main__":
    # Input, Output paths and image format
    IMAGES_PATH = 'images'
    OUTPUTS_PATH = 'images_with_boxes'
    IMAGE_FORMAT = '*.jpg'

    all_img_paths = Path(IMAGES_PATH).rglob(IMAGE_FORMAT)
    for src_img_path in all_img_paths:
        out_file_path = f'{OUTPUTS_PATH}/{str(src_img_path.name)}'
        Path(out_file_path).parent.mkdir(parents=True, exist_ok=True)

        if os.path.exists(out_file_path):
            continue
        input_image = cv2.imread(str(src_img_path))
        output_image, bbox, label, conf = detect_and_draw_box(image=input_image)
        cv2.imwrite(out_file_path, output_image)
