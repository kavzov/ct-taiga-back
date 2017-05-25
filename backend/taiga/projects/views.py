import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Project, Membership
from .forms import AddProjectForm
from taiga.projects.issues.models import Issue
from taiga.projects.issues.forms import AddIssueToProjectForm
from taiga.users.models import User, Role
from taiga.timelogs.views import get_timelogs


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


@csrf_protect
# @permission_required("projects.change_project")
@login_required()
def edit_project(request, project_id):
    # TODO
    # check permissions via query to db table 'projects_membership' using project_id and request.user.id
    # permission must be - "projects.change_project"
    # get role_id -> permissions_list -> if "projects.change_project" not in permissions_list -> redirect else do func
    # may be make decorator @project_permission_required
    args = dict()
    template = "projects/edit_project.html"

    project = Project.objects.get(pk=project_id)
    args['user'] = request.user
    args['project'] = project
    return render(request, template, args)


@csrf_protect
def add_project(request):
    pass
