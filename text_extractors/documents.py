# Local Imports
from .selectors import extract_text


def main():
    with open('tests/samples/sample_2.pdf', 'rb') as doc:
            text = extract_document_text(doc)
            print(text)


def extract_document_text(file):
    text = extract_text(file)
    return text


if __name__ == "__main__":
    main()
