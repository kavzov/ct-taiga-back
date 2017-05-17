from django.forms import ModelForm
from .models import Project

class AddProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']


