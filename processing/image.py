# Standard Imports
from functools import reduce

# Third-Party Imports
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


class ImageProcessor:

    def __init__(self, adjustments):
        self._adjustments = adjustments

    def run(self, image):
        return reduce(lambda img, attr: getattr(self, attr)(img), self._adjustments, image)

    @staticmethod
    def to_pil(image):
        if type(image) is not Image:
            rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            arr_img = Image.fromarray(rgb_img)
            return arr_img
    
    @staticmethod
    def to_cv2(image):
        if type(image) is Image:
            arr_img = np.array(image)
            bgr_img = cv2.cvtColor(arr_img, cv2.COLOR_RGB2BGR)
            return bgr_img

    @staticmethod
    def binarize(image):
        if type(image) is Image:
            raise NotImplementedError

        if type(image) is np.ndarray:
            return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        raise TypeError

    @staticmethod
    def brightness(image):
        if type(image) is Image:
            raise NotImplementedError
    
        if type(image) is np.ndarray:
            amount = int((255 - np.median(image)) * 0.75)
            return np.where((255 - image) < amount, 255, image + amount)
    
    @staticmethod
    def edges(image):
        if type(image) is Image:
            return image.filter(ImageFilter.FIND_EDGES)

        if type(image) is np.ndarray:
            return cv2.Canny(image, 100, 200)
        
        raise TypeError

    @staticmethod
    def greyscale(image):
        if type(image) is Image:
            return ImageOps.grayscale(image)
        
        if type(image) is np.ndarray:
            # return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[..., 2]
        
        raise TypeError
    
    @staticmethod
    def gaussian(image):
        if type(image) is Image:
            return image.filter(ImageFilter.GaussianBlur(radius=5))

        if type(image) is np.ndarray:
            return cv2.GaussianBlur(image, (5, 5), 0)
        
        raise TypeError

    @staticmethod
    def invert(image):
        if type(image) is Image:
            ImageOps.invert(image)
        
        if type(image) is np.ndarray:
            return cv2.bitwise_not(image)
        
        raise TypeError

    @staticmethod
    def sharpen(image):
        if type(image) is Image:
            return ImageEnhance.Sharpness(image).enhance(2)
        
        if type(image) is np.ndarray:
            raise NotImplementedError
            
        raise TypeError

    @staticmethod
    def deskew(image):
        if type(image) is Image:
            raise NotImplementedError

        # Reverse foreground and background and binarize image
        binary = ImageProcessor.binarize(image)

        # Use pixel coordinates to compute rotated bounding box
        coords = np.column_stack(np.where(binary > 0))
        angle = cv2.minAreaRect(coords)[-1]

        # adjust angle value
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # rotate image to deskew it
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # Return rotated image
        return rotated
