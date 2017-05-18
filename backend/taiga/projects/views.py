from django.shortcuts import render
from .models import Project
from taiga.projects.issues.models import Issue
from taiga.users.models import User
from .forms import AddProjectForm
from taiga.projects.issues.forms import AddIssueToProjectForm
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def projects_list(request):
    args = {}
    plist = Project.objects.all()
    add_project_form = AddProjectForm
    args['title'] = "Projects"
    args['projects_list'] = plist
    args['add_project_form'] = add_project_form
    return render(request, "projects/projects_list.html", args)


def project_details(request, project_id):
    args = {}

    pdetails = Project.objects.values().get(id=project_id)
    args['project_details'] = pdetails

    pissues = Issue.objects.all().filter(project=project_id)
    args['issues'] = pissues

    users = User.objects.all()
    args['users'] = users

    add_issue_form = AddIssueToProjectForm
    args['add_issue_form'] = add_issue_form

    args['title'] = 'Project "' + pdetails['name'] + '"'

    return render(request, "projects/project_details.html", args)


def add_project(request):
    pass
