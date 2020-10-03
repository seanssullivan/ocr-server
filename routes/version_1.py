# Third-Party Imports
import cv2
from flask import Blueprint, redirect, request
import numpy as np
import pytesseract as pt

# Local Imports
from . import settings


def allowed_ext(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


def preprocess(image):
    """Convert image to greyscale and adjust brightness to facilitate OCR."""
    greyscale_image = convert_to_greyscale(image)
    adjusted_image = adjust_brightness(greyscale_image)
    binary_image = convert_to_binary(adjusted_image)
    return binary_image


def convert_to_greyscale(image):
    greyscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[..., 2]
    return greyscale_image


def adjust_brightness(image):
    adjustment = int((255 - np.median(image)) * 0.75)
    adjusted_image = np.where((255 - image) < adjustment, 255, image + adjustment)
    return adjusted_image


def convert_to_binary(image):
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return binary_image


v1 = Blueprint('v1', __name__, url_prefix='/v1')

@v1.route('/', methods=['POST'])
def upload_file():
    # check if the post request has a file attached
    if 'image-file' not in request.files:
        return redirect(request.url)

    file = request.files['image-file']

    # if user does not select file, browser may submit an empty string
    if file.filename == '':
        return redirect(request.url)

    # if file type is allowed, process the image for text
    if file and allowed_ext(file.filename):
        dtype = request.args.get('dtype') or 'text'

        data = np.frombuffer(file.read(), np.uint8)
        raw_image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        processed_image = preprocess(raw_image)
        
        if dtype == 'text':
            return pt.image_to_string(processed_image)
        
        elif dtype == 'data':
            return pt.image_to_data(processed_image, output_type=pt.Output.STRING)
        
        elif dtype == 'dict':
            return pt.image_to_data(processed_image, output_type=pt.Output.DICT)
            
        elif dtype == 'df':
            return pt.image_to_data(processed_image, output_type=pt.Output.DATAFRAME)
