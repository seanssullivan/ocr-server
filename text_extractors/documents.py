# Local Imports
from .selectors import extract_text


def extract_document_text(file):
    text = extract_text(file)
    return text
