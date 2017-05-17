from django.forms import ModelForm
from .models import Issue


class AddIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['subject', 'description', 'assigned_to']
        # project_id from url