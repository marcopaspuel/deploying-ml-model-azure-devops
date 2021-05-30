import os
import cv2
from pathlib import Path

from src.client_utils import response_from_server, decode_image_from_response

if __name__ == "__main__":
    # Input, Output paths and image format
    IMAGES_PATH = 'assets/images'
    OUTPUTS_PATH = 'assets/images_predicted'
    IMAGE_FORMAT = '*.jpg'

    # Server URL
    BASE_URL = 'http://127.0.0.1:8000'
    ENDPOINT = '/predict'

    # Model Parameters
    MODEL = 'yolov3-tiny'
    CONFIDENCE = '0.5'

    # Construct URL
    url_with_endpoint_no_params = BASE_URL + ENDPOINT
    full_url = url_with_endpoint_no_params + "?model=" + MODEL + "&" + "confidence=" + CONFIDENCE

    # Run predictions on the input path
    all_img_paths = Path(IMAGES_PATH).rglob(IMAGE_FORMAT)
    for src_img_path in all_img_paths:
        out_file_path = f'{OUTPUTS_PATH}/{str(src_img_path.name)}'
        Path(out_file_path).parent.mkdir(parents=True, exist_ok=True)

        if os.path.exists(out_file_path):
            continue
        with open(str(src_img_path), "rb") as image_file:
            prediction = response_from_server(full_url, image_file, verbose=False)
        output_image = decode_image_from_response(prediction)
        cv2.imwrite(out_file_path, output_image)
