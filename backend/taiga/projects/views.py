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
from taiga.timelogs.models import Timelog
from taiga.timelogs.views import get_timelogs
from taiga.permissions import DEVELOPER_PERMISSIONS


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

    # args['project_details'] = Project.objects.values().get(id=project_id)
    args['project_details'] = Project.objects.get(id=project_id)
    args['issues'] = Issue.objects.all().filter(project=project_id)
    args['users'] = User.objects.all()
    args['add_issue_form'] = AddIssueToProjectForm
    args['title'] = 'Project "' + args['project_details'].name + '"'

    proj_mbr_roles = Membership.objects.filter(project=project_id)
    members = proj_mbr_roles.distinct('user')
    # roles = Role.objects.all()
    members_roles = {}
    for member in members:
        members_roles[member] = [mbr.role for mbr in proj_mbr_roles.filter(user_id=member.user.id)]

    args['members'] = members
    args['members_roles'] = members_roles

    timelogs = Timelog.objects.all().filter(issue__project__id=project_id)
    durations = [v['duration'] for v in list(timelogs.values())]

    args['total_time'] = sum(durations)

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


def user_project_perms(user_id, project_id):
    from django.core.exceptions import ObjectDoesNotExist
    user_perms = []
    try:
        roles = Membership.objects.filter(project_id=int(project_id), user_id=user_id)
    except ObjectDoesNotExist:
        return user_perms
    for role in roles:
        user_perms.extend(Role.objects.get(pk=role.role_id).permissions)
    return user_perms


def project_permission_required(perms, redir_page="/projects/"):
    def decor(func):
        def inner(request, project_id):
            required_perms = []
            if isinstance(perms, str):
                required_perms.append(perms)
            else:
                required_perms.extend(perms)
            user_perms = user_project_perms(request.user.id, project_id)
            for perm in required_perms:
                if perm not in user_perms:
                    return redirect(redir_page)
            return func(request, project_id)
        return inner
    return decor


# @project_permission_required(DEVELOPER_PERMISSIONS)
# @login_required()
def edit_project(request, project_id):
    args = dict()
    template = "projects/edit_project.html"

    project = Project.objects.get(pk=project_id)
    users = User.objects.all()
    proj_mbr_roles = Membership.objects.filter(project=project_id)
    members = proj_mbr_roles.distinct('user')
    roles = Role.objects.all()

    members_roles = {}
    for member in members:
        members_roles[member] = [mbr.role.id for mbr in proj_mbr_roles.filter(user_id=member.user.id)]

    args['project'] = project
    args['user'] = request.user
    args['user_perms'] = user_project_perms(request.user.id, project_id)
    args['users'] = users
    args['members'] = members
    args['members_roles'] = members_roles
    args['roles'] = roles
    args['editing'] = True   # for hide label "Edit projects" at the right top

    # if request.POST:
    #     args['test_data'] = []
    #     for user in users:
    #         member = 'member_' + str(user.id)
    #         args['test_data'] += [request.POST.getlist(member)]

    return render(request, template, args)


@csrf_protect
def add_project(request):
    pass
