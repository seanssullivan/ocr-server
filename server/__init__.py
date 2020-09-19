import cv2
from flask import Flask, redirect, render_template, request
import numpy as np
import pytesseract

from . import settings
from .processing import preprocess


def create_app():
    # create and configure the app
    app = Flask(__name__)

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
        if file and allowed(file.filename):
            data = np.frombuffer(file.read(), np.uint8)
            raw_image = cv2.imdecode(data, cv2.IMREAD_COLOR)
            
            processed_image = preprocess(raw_image)
            text = pytesseract.image_to_string(processed_image)
            return text

    return app


def allowed(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS
