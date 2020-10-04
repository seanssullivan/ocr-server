# Third-Party Imports
import cv2
import numpy as np
import pytesseract as pt

# Local Imports
from processing.image import ImageProcessor


def extract_image_text(file, rtype='text'):
    data = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    processed_image = process(image)
    
    if rtype == 'text':
        return pt.image_to_string(processed_image)
    
    if rtype == 'data':
        return pt.image_to_data(processed_image, output_type=pt.Output.STRING)
    
    if rtype == 'dict':
        return pt.image_to_data(processed_image, output_type=pt.Output.DICT)
        
    if rtype == 'df':
        return pt.image_to_data(processed_image, output_type=pt.Output.DATAFRAME)


def process(image):
    """Convert image to greyscale and adjust brightness to facilitate OCR."""
    processor = ImageProcessor(['greyscale', 'brightness', 'gaussian', 'binarize'])
    return processor.run(image)
