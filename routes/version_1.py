# Third-Party Imports
from flask import Blueprint, redirect, request

# Local Imports
from text_extractors.images import extract_image_text
from text_extractors.documents import extract_document_text


DOCUMENT_FORMATS = ['pdf']
IMAGE_FORMATS = ['gif', 'jpg', 'jpeg', 'png']


v1 = Blueprint('v1', __name__, url_prefix='/v1/')


@v1.route('/', methods=['POST'])
def upload_file():
    # check if the post request has a file attached
    if 'image-file' not in request.files:
        return redirect(request.url)
    
    file = request.files['image-file']  # attached file

    # if user does not select a file, the browser may submit an empty string
    if file.filename == '':
        return redirect(request.url)

    # get file extension
    ext = file.filename.rsplit('.', 1)[1].lower()

    # get requested response type
    # rtype = request.args.get('response') or 'text'

    # if file extension indicates an image
    if ext in IMAGE_FORMATS:
        text = extract_image_text(file)
        return text

    # if file extension indicates a document
    elif ext in DOCUMENT_FORMATS:
        text = extract_document_text(file)
        return text

    # else file extension does not match an implemented format
    else:
        return redirect(request.url)

