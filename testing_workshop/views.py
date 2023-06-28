from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from testing_workshop.functions import DigitalLibraryPage, Letter

from .exceptions import FileNotFoundAtUrl
from .forms import NerTextForm

# from testing_workshop.functions import NamedEntityDocument


@csrf_exempt
def ner(request):
    """View function for retrieving the transcription of a Darwin letter from XML."""

    xml_title, iiif_image, viz_html = (None,) * 3

    # If POST submit the data
    if request.method == "POST":
        form = NerTextForm(request.POST)

        if form.is_valid():
            xml_url = form.cleaned_data["xml_url"]

            try:
                item = DigitalLibraryPage(xml_url)
                # iiif_image = item.get_iiif_image_url()  # Uncomment Exercise 2

                letter = Letter(item.get_metadata())
                xml_title = letter.get_title()
                # xml_transcription = letter.get_transcription()  # Uncomment Exercise 6

                # ner_doc = NamedEntityDocument(xml_transcription) # Uncomment Exercise 6
                # viz_html = ner_doc.ner_viz_html()  # Uncomment Exercise 6

            except FileNotFoundAtUrl as err:
                messages.error(request, str(err))

    # If GET or any other method display empty form
    else:
        form = NerTextForm()

    return render(
        request,
        "pages/ner.html",
        {"form": form, "xml_title": xml_title, "iiif_image": iiif_image, "viz_html": viz_html},
    )
