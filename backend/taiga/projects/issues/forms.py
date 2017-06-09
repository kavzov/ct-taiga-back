from django import forms
from .models import Issue


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'subject', 'description', 'project', 'status', 'assigned_to'
        ]
        labels = {
            "assigned_to": "Assignee"
        }
