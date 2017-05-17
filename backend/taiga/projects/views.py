from django.shortcuts import render
from .models import Project
from taiga.projects.issues.models import Issue
from .forms import AddProjectForm
from taiga.projects.issues.forms import AddIssueForm
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def projects_list(request):
    projects_page_data = {}
    plist = Project.objects.all()
    add_project_form = AddProjectForm
    projects_page_data['title'] = "Projects list"
    projects_page_data['projects_list'] = plist
    projects_page_data['add_project_form'] = add_project_form
    return render(request, "projects/projects_list.html", projects_page_data)


def project_details(request, project_id):
    project_page_data = {}

    pdetails = Project.objects.values().get(id=project_id)
    project_page_data['project_details'] = pdetails

    pissues = Issue.objects.all().filter(project=project_id)
    project_page_data['issues'] = pissues

    add_issue_form = AddIssueForm
    project_page_data['add_issue_form'] = add_issue_form

    project_page_data['title'] = 'Project "' + pdetails['name'] + '"'

    return render(request, "projects/project_details.html", project_page_data)


def add_project(request):
    pass
