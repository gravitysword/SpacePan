import cv2
import numpy as np
from io import BytesIO

def numpy_to_png_binary(array):
    _, encoded_image = cv2.imencode('.png', array)
    png_binary_data = encoded_image.tobytes()
    return png_binary_data

