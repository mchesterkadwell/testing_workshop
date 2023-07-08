"""
Tests for the view helper functions.
"""
import os

import pytest
from bs4 import BeautifulSoup

# from requests.exceptions import HTTPError
from spacy.tokens import Doc as SpacyDoc

from testing_workshop.exceptions import FileNotFoundAtUrl
from testing_workshop.functions import DigitalLibraryPage, Letter


class TestLetter:
    def test_get_title(self, letter_xml):
        letter = Letter(letter_xml)
        title = letter.get_title()
        assert title == "Letter from  Hooker to Darwin"

    @pytest.mark.skipif("CI" in os.environ, reason="Skip deliberately failing test in CI.")
    def test_get_transcription(self, letter_xml):
        letter = Letter(letter_xml)  # ARRANGE
        transcription = letter.get_transcription()  # noqa: F841 # ACT
        # Exercise 1 - fill in ASSERTION
        assert False


class TestDigitalLibraryPage:
    def test_get_metadata_url_from_digital_library_url(self, page_url_valid, metadata_url_valid):
        page = DigitalLibraryPage(page_url_valid)
        metadata_url = page.get_metadata_url()
        assert metadata_url == "https://services.prod.env.cudl.link/v1/metadata/tei/MS-DAR-00100-00001"

    def test_get_metadata_code_200_returns_text(self, page_url_valid):
        page = DigitalLibraryPage(page_url_valid)
        result = page.get_metadata()
        assert len(result) == 22206

    def test_get_metadata_code_500_raises_exception(self, page_url_invalid):
        page = DigitalLibraryPage(page_url_invalid)
        with pytest.raises(FileNotFoundAtUrl):
            page.get_metadata()

    # Exercise 2 - add test(s) for get_iiif_image_url() here

    # Exercise 5 - add test for expected exception FileNotFoundAtUrl for get_iiif_image_url() here

    # Exercise 6 - refactor parameterized test for expected exceptions for get_iiif_image_url() here


class TestNamedEntityDocument:
    def test_ner_doc_is_instance_of_spacy_doc(self, ner_doc):
        doc = ner_doc.get_doc()
        assert isinstance(doc, SpacyDoc)

    def test_ner_doc_has_ner_tokens(self, ner_doc):
        doc = ner_doc.get_doc()
        assert doc.has_annotation("ENT_IOB")

    # Exercise 6 - refactor this test to use parameterized test inputs
    def test_ner_tokens(self, ner_doc):
        doc = ner_doc.get_doc()
        entities = [{entity.text: entity.label_} for entity in doc.ents]
        assert entities[0] == {"Charles Robert Darwin": "PERSON"}
        assert entities[1] == {"Shrewsbury": "GPE"}
        assert entities[2] == {"12 February 1809": "DATE"}
        assert entities[3] == {"University of Edinburgh Medical School": "ORG"}

    def test_ner_viz_html_returns_entities_div(self, ner_doc):
        soup = BeautifulSoup(ner_doc.ner_viz_html(), features="lxml")
        assert soup.find("div", {"class": "entities"})

    def clean_text_removes_contractions(self, ner_doc):
        clean_text = ner_doc.clean_text("& && &c&c &c   ")
        assert clean_text == "and &and etcetc etc "
