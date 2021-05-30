import io
import os
from pathlib import Path

import cv2
import uvicorn
import numpy as np
import nest_asyncio
from enum import Enum
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

# Assign an instance of the FastAPI class to the variable "app".
# You will interact with your api using this instance.
from detect import detect_and_draw_box

app = FastAPI(title='Deploying a ML Model with FastAPI')


# List available models using Enum for convenience. This is useful when the options are pre-defined.
class Model(str, Enum):
    yolov3tiny = "yolov3-tiny"
    yolov3 = "yolov3"


# By using @app.get("/") you are allowing the GET method to work for the / endpoint.
@app.get("/")
def home():
    return "Congratulations! Your API is working as expected. Now head over to http://localhost:8000/docs."


# This endpoint handles all the logic necessary for the object detection to work.
# It requires the desired model and the image in which to perform object detection.
@app.post("/predict")
def prediction(model: Model, confidence: float, file: UploadFile = File(...)):
    # 1. VALIDATE INPUT FILE
    filename = file.filename
    fileExtension = filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not fileExtension:
        raise HTTPException(status_code=415, detail="Unsupported file provided.")

    # 2. TRANSFORM RAW IMAGE INTO CV2 image

    # Read image as a stream of bytes
    image_stream = io.BytesIO(file.file.read())

    # Start the stream from the beginning (position zero)
    image_stream.seek(0)

    # Write the stream of bytes into a numpy array
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)

    # Decode the numpy array as an image
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # 3. RUN OBJECT DETECTION MODEL

    # Run object detection
    output_image, bbox, label, conf = detect_and_draw_box(image=image, model=model, confidence=confidence)

    # Save it in a folder within the server
    out_file_path = f'assets/images_uploaded/{str(filename)}'
    Path(out_file_path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(f'assets/images_uploaded/{filename}', output_image)

    # 4. STREAM THE RESPONSE BACK TO THE CLIENT

    # Open the saved image for reading in binary mode
    file_image = open(f'assets/images_uploaded/{filename}', mode="rb")

    # Return the image as a stream specifying media type
    return StreamingResponse(file_image, media_type="image/jpeg")


if __name__ == "__main__":
    # Allows the server to be run in this interactive environment
    nest_asyncio.apply()

    # Host depends on the setup you selected (docker or virtual env)
    host = "0.0.0.0" if os.getenv("DOCKER-SETUP") else "127.0.0.1"

    # Spin up the server!
    uvicorn.run(app, host=host, port=8000)
