import re
import unittest

from pdfminer.layout import LTAnno, LTChar, LTPage, LTTextContainer, LTTextBoxHorizontal, LTTextLineHorizontal

from text_extractors.documents import extract_document_text
from text_extractors.selectors import extract_characters, extract_pages
from text_extractors.selectors import extract_textboxes
from text_extractors.selectors import extract_lines
# from text_extractors.selectors import extract_characters


class TestExtractDocumentText(unittest.TestCase):

    def setUp(self) -> None:
        self.test_file = open('tests/samples/sample_1.pdf', 'rb')

    def test_returns_string(self):
        expected = re.sub(r"[\n\t\s]*", "", """
            It was the best of times, it was the worst of times, it was
            the age of wisdom, it was the age of foolishness, it was
            the epoch of belief, it was the epoch of incredulity, it was
            the season of Light, it was the season of Darkness, it was
            the spring of hope, it was the winter of despair, we had
            everything before us, we had nothing before us, we were
            all going direct to Heaven, we were all going direct the
            other way — in short, the period was so far like the
            present period, that some of its noisiest authorities insisted
            on its being received, for good or for evil, in the superlative
            degree of comparison only.
        """)
        actual = re.sub(r"[\n\t\s]*", "", extract_document_text(self.test_file))
        self.assertEqual(expected, actual)

    def tearDown(self) -> None:
        self.test_file.close()


class TestPDFSelectors(unittest.TestCase):

    def setUp(self) -> None:
        self.test_pdf = open('tests/samples/sample_2.pdf', 'rb')

    def test_extract_pages_from_pdf(self):
        result = extract_pages(self.test_pdf)
        for page in result:
            self.assertIsInstance(page, LTPage)

    def test_extract_textboxes_from_single_pages(self):
        pages = extract_pages(self.test_pdf)
        for page in pages:
            result = extract_textboxes(page)
            for textbox in result:
                self.assertIsInstance(textbox, LTTextBoxHorizontal)

    def test_extract_textboxes_from_multiple_pages(self):
        pages = extract_pages(self.test_pdf)
        result = extract_textboxes(pages)
        for textbox in result:
            self.assertIsInstance(textbox, LTTextBoxHorizontal)

    def test_extract_lines_from_single_textboxs(self):
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            for textbox in textboxes:
                result = extract_lines(textbox)
                for line in result:
                    self.assertIsInstance(line, LTTextLineHorizontal)

    def test_extract_lines_from_multiple_boxes(self):
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            result = extract_lines(textboxes)
            for line in result:
                self.assertIsInstance(line, LTTextLineHorizontal)
    
    def test_extract_lines_from_single_pages(self):
        pages = extract_pages(self.test_pdf)
        for page in pages:
            result = extract_lines(page)
            for line in result:
                self.assertIsInstance(line, LTTextLineHorizontal)
    
    def test_extract_lines_from_multiple_pages(self):
        pages = extract_pages(self.test_pdf)
        result = extract_lines(pages)
        for line in result:
            self.assertIsInstance(line, LTTextLineHorizontal)

    def test_extract_characters_from_single_lines(self):
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            for textbox in textboxes:
                lines = extract_lines(textbox)
                for line in lines:
                    characters = extract_characters(line)
                    for character in characters:
                        self.assertIsInstance(character, LTChar)

    def test_extract_characters_from_multiple_lines(self):
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            for textbox in textboxes:
                lines = extract_lines(textbox)
                characters = extract_characters(lines)
                for character in characters:
                    self.assertIsInstance(character, LTChar)
    
    def test_extract_characters_from_single_textboxes(self):
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            for textbox in textboxes:
                characters = extract_characters(textbox)
                for character in characters:
                    self.assertIsInstance(character, LTChar)

    def test_extract_characters_from_multiple_textboxes(self):
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            characters = extract_characters(textboxes)
            for character in characters:
                self.assertIsInstance(character, LTChar)
    
    def test_extract_characters_from_single_pages(self):
        pages = extract_pages(self.test_pdf)
        for page in pages:
            characters = extract_characters(page)
            for character in characters:
                self.assertIsInstance(character, LTChar)
        
    def test_extract_characters_from_multiple_pages(self):
        pages = extract_pages(self.test_pdf)
        characters = extract_characters(pages)
        for character in characters:
            self.assertIsInstance(character, LTChar)

    def tearDown(self) -> None:
        self.test_pdf.close()
