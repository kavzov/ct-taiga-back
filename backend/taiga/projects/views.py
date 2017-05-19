import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Project
from .forms import AddProjectForm
from taiga.projects.issues.models import Issue
from taiga.projects.issues.forms import AddIssueToProjectForm
from taiga.users.models import User
from taiga.timelogs.views import get_timelogs

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


def project_timelogs(request, project_id):
    format = request.GET.get('format')
    args = get_timelogs(request, project_id=project_id)

    if format == 'json':
        template = "timelogs/json_timelogs.html"
        args['jsondata'] = json.dumps(list(args['timelogs_list'].values('issue_id', 'user_id', 'date', 'duration')), cls=DjangoJSONEncoder)
    else:
        template = "projects/project_details.html"
        args['project_details'] = Project.objects.get(id=project_id)

    return render(request, template, args)


def add_project(request):
    pass
