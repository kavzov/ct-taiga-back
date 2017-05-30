from django import forms
from taiga.projects.models import Project, Membership


class ProjectDetails(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'owner']
        labels = {
            'name': 'Name',
            'description': 'Descr',
            'owner': 'Owner'
        }


class ProjectMembers(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['id', 'user']
        labels = {
            'user': 'Member'
        }

