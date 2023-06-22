"""
Helper functions to use in views.
"""
from pathlib import Path
from urllib.parse import urljoin, urlparse

import en_core_web_sm
import requests
from bs4 import BeautifulSoup
from spacy import displacy

from .exceptions import FileNotFoundAtUrl

# We only want the ner pipeline, so we can disable the rest to save resources.
nlp = en_core_web_sm.load(disable=["tok2vec", "tagger", "parser", "senter", "attribute_ruler", "lemmatizer"])

DIGITAL_LIBRARY_URL_PREFIX = "https://cudl.lib.cam.ac.uk/view/"
METADATA_URL_PREFIX = "https://services.prod.env.cudl.link/v1/metadata/tei/"


class Letter:
    """
    The content and metadata of a Darwin letter in Cambridge Digital Library.
    """

    def __init__(self, xml):
        self.xml = xml
        self.tree = BeautifulSoup(xml, features="xml")
        self._set_title()
        self._set_transcription()

    def _set_title(self):
        self._title = self.tree.title.text

    def get_title(self):
        return self._title

    def _set_transcription(self):
        self._transcription = self.tree.find(type="transcription").text.strip()

    def get_transcription(self):
        return self._transcription


class DigitalLibraryPage:
    """
    The page of an item in Cambridge Digital Library.
    """

    def __init__(self, url):
        self.digital_library_url_prefix = DIGITAL_LIBRARY_URL_PREFIX
        self.metadata_url_prefix = METADATA_URL_PREFIX
        self.url = url
        self._set_metadata_url()

    def _set_metadata_url(self):
        url = urlparse(self.url)
        path = Path(url.path)
        item_id = path.parts[-1] if len(path.parts) == 3 else path.parts[-2]
        self._metadata_url = urljoin(self.metadata_url_prefix, item_id)

    def get_metadata_url(self):
        return self._metadata_url

    def get_metadata(self):
        """Return a string of metadata available at the metadata URL of the page's item."""
        response = requests.get(self.get_metadata_url())
        if response.status_code == 200:
            return response.text
        # NB: Cambridge Digital Library returns inappropriate 500 status code for missing metadata files
        if response.status_code == 500:
            raise FileNotFoundAtUrl(f"Metadata not found at URL: {self.url} Please check the URL and try again.")
        else:
            response.raise_for_status()

    def get_iiif_image_url(self):
        """Returns the IIIF social media image of the page."""
        # Exercise 2 - fill in the implementation here
        pass


class NamedEntityDocument:
    """
    A spaCy document containing the named entities recognised in a text.
    """

    def __init__(self, text):
        self.text = text
        self._set_doc()

    def _set_doc(self):
        self._doc = nlp(self.clean_text(self.text))

    def get_doc(self):
        return self._doc

    @staticmethod
    def clean_text(text):
        """
        Clean the text of things that the spaCy models don't handle well.
        For example, Darwin's letters has many contractions.
        """
        clean_text = text.replace("& ", "and ").replace("&c", "etc").replace("   ", " ").strip()
        return clean_text

    def ner_viz_html(self):
        """Return a string of HTML with a visualisation of the named entities."""
        return displacy.render(self.get_doc(), style="ent", minify=True)
