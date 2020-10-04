# Standard Imports
from io import StringIO

# Third-Party Imports
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams, LTTextContainer, LTChar
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def extract_document_text(file):
    outfp = StringIO()

    parser = PDFParser(file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, outfp, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.create_pages(doc)
    
    for page in pages:
        interpreter.process_page(page)
    
    return outfp.getvalue()
    # return extract_text(file)


# helper functions

# def extract_elements_from_page(pdf_page):
#   return [element for element in pdf_page if isinstance(element, LTTextContainer)]


# def extract_lines_from_element(pdf_element):
#   return [line for line in pdf_element if isinstance(line, LTTextContainer)]


# def extract_lines_from_elements(pdf_elements):
#   lines = []
#   for pdf_element in pdf_elements:
#     lines.extend(extract_lines_from_element(pdf_element))
#   return lines


# def extract_lines_from_page(pdf_page):
#   elements = extract_elements_from_page(pdf_page)
#   lines = extract_lines_from_elements(elements)
#   return lines


# def extract_characters_from_line(pdf_line):
#   return [character for character in pdf_line if isinstance(character, LTChar)]


# def extract_characters_from_lines(pdf_lines):
#   characters = []
#   for pdf_line in pdf_lines:
#     characters.extend(extract_characters_from_line(pdf_line))
#   return characters


# def extract_characters_from_page(pdf_page):
#   lines = extract_lines_from_page(pdf_page)
#   characters = extract_characters_from_lines(lines)
#   return characters


# def extract_characters_from_pages(pages):
#   text_pages = []
#   for page in pages:
#     chars = extract_characters_from_page(page)
#     text_pages.append(chars)
#   return text_pages
