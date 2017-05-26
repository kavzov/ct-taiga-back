import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
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

    args['project_details'] = Project.objects.values().get(id=project_id)
    args['issues'] = Issue.objects.all().filter(project=project_id)
    args['users'] = User.objects.all()
    args['add_issue_form'] = AddIssueToProjectForm
    args['title'] = 'Project "' + args['project_details']['name'] + '"'

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


def project_permission_required(perms, redir_page="/projects/"):
    def decor(func):
        def inner(request, project_id):
            from django.core.exceptions import ObjectDoesNotExist
            required_perms = []
            if isinstance(perms, str):
                required_perms.append(perms)
            else:
                required_perms.extend(perms)
            try:
                # role = Membership.objects.get(project_id=int(project_id), user_id=request.user.id)
                roles = Membership.objects.all().filter(project_id=int(project_id), user_id=request.user.id)
            except ObjectDoesNotExist:
                return redirect(redir_page)
            user_perms = []
            for role in roles:
                user_perms.extend(Role.objects.get(pk=role.role_id).permissions)
            for perm in required_perms:
                if perm not in user_perms:
                    return redirect(redir_page)
            return func(request, project_id)
        return inner
    return decor


from taiga.permissions import DEVELOPER_PERMISSIONS
@csrf_protect
@project_permission_required(DEVELOPER_PERMISSIONS)
@login_required()
def edit_project(request, project_id):
    args = dict()
    template = "projects/edit_project.html"

    project = Project.objects.get(pk=project_id)
    users = User.objects.all()
    members = Membership.objects.filter(project=project_id)
    roles = Role.objects.all()

    # user_project_roles = [member.role.id for member in members.filter(user_id=)];

    args['project'] = project
    args['user'] = request.user
    args['users'] = users
    args['members'] = members
    args['roles'] = roles

    args['editing'] = True   # for hide label "Edit projects" at the right top

    return render(request, template, args)


@csrf_protect
def add_project(request):
    pass
