from django.forms import ModelForm
from .models import Issue


class AddIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['subject', 'description', 'project', 'status', 'assigned_to']


class AddIssueToProjectForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['subject', 'description', 'status', 'assigned_to']

