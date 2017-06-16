from django import forms
from markdownx.fields import MarkdownxFormField


class WikiForm(forms.Form):
    title = forms.CharField(max_length=128, label='Title')
    text = MarkdownxFormField(label='Text')
