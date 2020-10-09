# Standard Imports
from io import StringIO
from typing import Generator

# Third-Party Imports
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTPage, LTTextContainer, LTTextBoxHorizontal, LTTextLineHorizontal, LTChar, LTAnno
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def main():
    with open('tests/samples/sample_2.pdf', 'rb') as doc:
        pages = extract_pages(doc)
        print(type(pages))
        print(isinstance(pages, Generator))
        # for page in pages:
        #     print(isinstance(page, LTTextContainer))


def extract_text(file):
    """Extract text from a PDF document using pdfminer.six.
    
    While we could just use extract_text() from pdfminer.high_level,
    the more verbose solution provides the opportunity to extend and
    customize the process later."""

    parser = PDFParser(file)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()

    with StringIO() as output:
        device = TextConverter(rsrcmgr, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)

        return output.getvalue()


def extract_pages(file):
    """Extract pages from a PDF document using pdfminer.six.
    
    While we could just use extract_pages() from pdfminer.high_level,
    the more verbose solution provides the opportunity to extend and
    customize the process later."""

    parser = PDFParser(file)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        yield layout


def extract_textboxes(element):
    """Selector function to extract instances of LTTextBoxHorizontal from LTPage objects."""
    if isinstance(element, LTPage):
        for textbox in element:
            if isinstance(textbox, LTTextBoxHorizontal):
                yield textbox

    elif isinstance(element, Generator):
        for page in element:
            yield from extract_textboxes(page)

    else:
        raise TypeError


def extract_lines(element):
    """Selector function to extract instances of LTTextLineHorizontal from LTTextBoxHorizontal objects."""
    if isinstance(element, LTTextBoxHorizontal):
        for line in element:
            if isinstance(line, LTTextLineHorizontal):
                yield line

    elif isinstance(element, Generator):
        for obj in element:
            yield from extract_lines(obj)

    elif type(element) in [LTTextContainer, LTPage]:
        for textbox in extract_textboxes(element):
            yield from extract_lines(textbox)

    else:
        raise TypeError


def extract_characters(element):
    """Selector function to extract instances of LTChar from LTTextLineHorizontal objects."""
    if isinstance(element, LTTextLineHorizontal):
        for char in element:
            if isinstance(char, LTChar):
                yield char

    elif isinstance(element, Generator):
        for obj in element:
            yield from extract_characters(obj)

    elif type(element) in [LTTextBoxHorizontal, LTTextContainer, LTPage]:
        for line in extract_lines(element):
            yield from extract_characters(line)

    else:
        raise TypeError


if __name__ == "__main__":
    main()
