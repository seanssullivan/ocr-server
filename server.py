import cv2
from flask import Flask, redirect, render_template, request
import numpy as np
import pytesseract


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/', methods=['POST'])
def upload_file():
    # check if the post request has a file attached
    if 'image-file' not in request.files:
        return redirect(request.url)

    file = request.files['image-file']

    # if user does not select file, browser may submit an empty string
    if file.filename == '':
        return redirect(request.url)

    # if file type is allowed, process the image for text
    if file and allowed_file(file.filename):
        data = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        
        processed_image = preprocess(image)
        text = pytesseract.image_to_string(processed_image)
        return text


def preprocess(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    grey_scale = hsv_image[..., 2]

    adjustment = int((255 - np.median(grey_scale)) * 0.75)
    adjusted_image = np.where((255 - grey_scale) < adjustment, 255, grey_scale + adjustment)

    blurred_image = cv2.GaussianBlur(adjusted_image, (5, 5), 0)
    threshold, thresholded_image = cv2.threshold(
        blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresholded_image
