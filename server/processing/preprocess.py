import cv2
import numpy as np


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
    threshold, binary_image = cv2.threshold(
        blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary_image
