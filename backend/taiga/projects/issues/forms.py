from django import forms
from .models import Issue


class AddIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'subject', 'description', 'project', 'status', 'assigned_to'
        ]
        labels = {
            "assigned_to": "Assignee"
        }


class AddIssueToProjectForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['subject', 'description', 'status', 'assigned_to']
        labels = {
            "assigned_to": "Assignee"
        }

