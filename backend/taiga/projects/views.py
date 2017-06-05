import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Project, Membership
from .forms import ProjectForm
from taiga.projects.issues.models import Issue
from taiga.projects.issues.forms import AddIssueToProjectForm
from taiga.users.models import User, Role
from taiga.timelogs.models import Timelog
from taiga.timelogs.views import get_timelogs
from taiga.permissions import DEVELOPER_PERMISSIONS


def projects_list(request):
    args = {}
    plist = Project.objects.all()
    add_project_form = ProjectForm
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
        return []
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
def edit_project(request, project_id=0):
    template = "projects/edit_project.html"
    args = dict()

    users = User.objects.all()
    roles = Role.objects.all()
    args['users'] = users
    args['roles'] = roles
    args['user'] = request.user
    args['user_perms'] = user_project_perms(request.user.id, project_id)

    args['project_form'] = ProjectForm

    # Edit project
    if project_id:
        project = Project.objects.get(pk=project_id)
        proj_mbr_roles = Membership.objects.filter(project=project_id)
        members = [member.user.id for member in proj_mbr_roles.distinct('user')]

        members_roles = {}
        for member in members:
            members_roles[member] = [mbr.role.id for mbr in proj_mbr_roles.filter(user_id=member)]

        args['project'] = project
        args['members'] = members
        args['members_roles'] = members_roles
        args['editing'] = True   # for hide label "Edit projects" at the right top

        args['project_form'] = ProjectForm(initial={
            'name': project.name,
            'description': project.description,
            'owner': project.owner,
        })

        if request.POST:
            project_data = {}
            project_data['id'] = project_id
            project_data['name'] = request.POST.get('name')
            project_data['description'] = request.POST.get('description')
            project_data['owner'] = request.POST.get('owner')

            project_data['members'] = {}

            for user in users:
                label_name = 'member_' + str(user.id);
                roles_list = request.POST.getlist(label_name)

                # check member already in members list (member_in_<id> hidden field value)
                user_in_members_list = request.POST.get('member_in_' + str(user.id))
                if user_in_members_list:
                    # if user just added to members list => add him to 'members' list
                    if user.id not in members:
                        members.append(user.id)

                    # change member roles
                    try:
                        prev_mbr_roles = members_roles[user.id]
                    # if member is new
                    except KeyError:
                        prev_mbr_roles = []

                    now_mbr_roles = list(map(int, roles_list))

                    # deleted roles
                    for role in prev_mbr_roles:
                        if role not in now_mbr_roles:
                            # update db
                            Membership.objects.get(project_id=project_id, user_id=user.id, role_id=role).delete()

                    # added roles
                    for role in now_mbr_roles:
                        if role not in prev_mbr_roles:
                            # update db
                            Membership(project_id=project_id, user_id=user.id, role_id=role).save()

                    members_roles[user.id] = roles_list

                    project_data['members'][user.id] = members_roles[user.id]
                else:
                    # if user not in members list:
                    #   1. he have been deleted from the list
                    #   2. he haven't been added (KeyError & ValueError exceptions)
                    try:
                        members.remove(user.id)
                        members_roles.pop(user.id)
                        # delete from db all records where user at this project
                        Membership.objects.filter(project_id=project_id, user_id=user.id).delete()
                    except (KeyError, ValueError):
                        pass

            # args['test'] = membership_to_add

            # Update db project
            upd_proj = Project(
                id = project_data['id'],
                name = project_data['name'],
                description = project_data['description'],
                owner = User.objects.get(pk=project_data['owner'])
            )
            upd_proj.save()





    return render(request, template, args)


def add_project(request):
    pass
