from django import forms
from .models import Project, Membership


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'owner']


class ProjectName(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']


class ProjectDescription(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['description']
        labels = {  }


class ProjectOwner(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['owner']


class ProjectMembers(forms.ModelForm):
    # members = forms.ModelChoiceField(queryset=Membership.objects.all(), empty_label=None)

    class Meta:
        model = Membership
        fields = ['id', 'user']
        labels = {
            'user': 'Members'
        }


