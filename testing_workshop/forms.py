from django import forms


class NerTextForm(forms.Form):
    xml_url = forms.URLField(label="URL", widget=forms.URLInput(attrs={"style": "width:100%;"}))
