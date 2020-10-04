# Third-Party Imports
import cv2
import numpy as np
import pytesseract as pt


def extract_image_text(file, rtype='text'):
    data = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    processed_image = preprocess(image)
    
    if rtype == 'text':
        return pt.image_to_string(processed_image)
    
    if rtype == 'data':
        return pt.image_to_data(processed_image, output_type=pt.Output.STRING)
    
    if rtype == 'dict':
        return pt.image_to_data(processed_image, output_type=pt.Output.DICT)
        
    if rtype == 'df':
        return pt.image_to_data(processed_image, output_type=pt.Output.DATAFRAME)


def preprocess(image):
    """Convert image to greyscale and adjust brightness to facilitate OCR."""
    greyscale_image = convert_to_greyscale(image)
    adjusted_image = adjust_brightness(greyscale_image)
    binary_image = convert_to_binary(adjusted_image)
    return binary_image


def convert_to_greyscale(image):
    greyscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[..., 2]
    return greyscale_image


def adjust_brightness(image, amount=None):
    if not amount:
        amount = int((255 - np.median(image)) * 0.75)

    adjusted_image = np.where((255 - image) < amount, 255, image + amount)
    return adjusted_image


def convert_to_binary(image):
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return binary_image


def detect_edges(image):
    edges = cv2.Canny(image, 100, 200)
    return edges