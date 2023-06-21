from urllib.parse import urljoin

import pytest

from testing_workshop.functions import DIGITAL_LIBRARY_URL_PREFIX, METADATA_URL_PREFIX, NamedEntityDocument

# from testing_workshop.functions import (
#     DigitalLibraryPage,
#     Letter,
# )

# Exercise 3 - add two fixtures for Letter and DigitalLibraryPage here


@pytest.fixture
def ner_doc(transcription_text):
    return NamedEntityDocument(transcription_text)


@pytest.fixture
def page_url_valid():
    return urljoin(DIGITAL_LIBRARY_URL_PREFIX, "MS-DAR-00100-00001/1")


@pytest.fixture
def page_url_invalid():
    return urljoin(DIGITAL_LIBRARY_URL_PREFIX, "MS-DAR-00100-XXXXX/1")


@pytest.fixture
def metadata_url_valid():
    return urljoin(METADATA_URL_PREFIX, "MS-DAR-00100-00001")


@pytest.fixture
def metadata_url_invalid():
    return urljoin(METADATA_URL_PREFIX, "MS-DAR-00100-XXXXX")


@pytest.fixture
def letter_xml():
    return """
    <?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="DCP-LETT-111111">
    <teiHeader>
        <fileDesc><titleStmt>
                <title xml:id="main_title">Letter from  Hooker to Darwin</title>
            </titleStmt></fileDesc>
    </teiHeader>
    <text><body><div><div type="dcp-letter"><div type="letter">
        <head>Letter from  Hooker to Darwin</head>
        <div type="text">
            <opener></opener>
            <div type="transcription">
                <p>Many thanks indeed for your letter. It was most kind and I am immensely gratified.</p>
            </div>
        </div>
    </div></div></body></text>
</TEI>
    """


@pytest.fixture
def transcription_text():
    return """
    Charles Robert Darwin was born in Shrewsbury on 12 February 1809, at his family's home,
    before going to the well-regarded University of Edinburgh Medical School.
    """
