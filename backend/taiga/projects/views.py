import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Project, Membership
from .forms import ProjectForm
from taiga.projects.issues.models import Issue
from taiga.users.models import User, Role
from taiga.timelogs.models import Timelog
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

    args['project_details'] = Project.objects.get(id=project_id)
    args['issues'] = Issue.objects.all().filter(project=project_id)
    args['users'] = User.objects.all()
    args['title'] = 'Project "' + args['project_details'].name + '"'
    args['user_perms'] = user_project_perms(request.user.id, project_id)

    proj_mbr_roles = Membership.objects.filter(project=project_id)
    members = proj_mbr_roles.distinct('user')
    # roles = Role.objects.all()
    members_roles = {}
    for member in members:
        members_roles[member] = [mbr.role for mbr in proj_mbr_roles.filter(user_id=member.user.id).order_by('role_id')]

    args['members'] = members
    args['members_roles'] = members_roles

    timelogs = Timelog.objects.all().filter(issue__project__id=project_id)
    durations = [v['duration'] for v in list(timelogs.values())]

    args['total_time'] = sum(durations)

    return render(request, "projects/project_details.html", args)


def user_project_perms(user_id, project_id):
    # if Admin
    ADMIN_ID = 1
    MANAGER_PERMS_ID = 1
    if user_id == ADMIN_ID:
        return Role.objects.get(pk=MANAGER_PERMS_ID).permissions
    else:
        user_perms = []
        # if no roles at the project return []
        try:
            roles = Membership.objects.filter(project_id=int(project_id), user_id=user_id)
        except ObjectDoesNotExist:
            return []
        # else list of user permissions at the project
        for role in roles:
            # if not role_id (user at the project but hasn't roles)
            try:
                user_perms.extend(Role.objects.get(pk=role.role_id).permissions)
            except ObjectDoesNotExist:
                pass
        return user_perms


def valid_id(func):
    """
    Check whether issue or timelog at a project
    Redirect with error messages
    """
    def inner(request, *args, **kwargs):
        issue_id = kwargs.get('issue_id')
        timelog_id = kwargs.get('timelog_id')
        project_id = kwargs.get('project_id')

        if issue_id:
            try:
                Issue.objects.get(pk=issue_id).project_id
            except ObjectDoesNotExist:
                messages.error(request, 'Error: issue &#35;' + str(issue_id) + ' does NOT exist')
                return redirect('/issues/')

        if timelog_id:
            try:
                Timelog.objects.get(pk=timelog_id).issue.project_id
            except ObjectDoesNotExist:
                messages.error(request, 'Error: timelog &#35;' + str(timelog_id) + ' does NOT exist')
                return redirect('/timelogs/')

        if project_id:
            try:
                Project.objects.get(pk=project_id)
            except ObjectDoesNotExist:
                messages.error(request, 'Error: project &#35;' + str(project_id) + ' does NOT exist')
                return redirect('/projects/')

        return func(request, *args, **kwargs)
    return inner


def project_permission_required(perms, redir='/projects/'):
    def decor(func):
        def inner(request, *args, **kwargs):
            issue_id = kwargs.get('issue_id')
            timelog_id = kwargs.get('timelog_id')
            project_id = kwargs.get('project_id')

            if issue_id:
                project_id = Issue.objects.get(pk=issue_id).project_id
            if timelog_id:
                project_id = Timelog.objects.get(pk=timelog_id).issue.project_id

            # get user permissions
            user_perms = user_project_perms(request.user.id, project_id)

            # get required permissions from decorator
            required_perms = []
            # if it string
            if isinstance(perms, str):
                required_perms.append(perms)
            # list
            else:
                required_perms.extend(perms)

            # if at least one permission not in required permissions - redirect to 'redir_page'
            for perm in required_perms:
                if perm not in user_perms:
                    return redirect(redir)

            return func(request, *args, **kwargs)
        return inner
    return decor


def send_err_msg(req, form):
    err_msg_head = "Errors:"
    err_msg_text = form.errors.as_text()
    messages.error(req, err_msg_head)
    messages.error(req, err_msg_text)


@permission_required('projects.add_project')
def add_project(request):
    """
    Create new project
    """
    template = 'projects/edit_project.html'
    args = {
        'title': 'Add project',
        'users': User.objects.all(),
        'roles': Role.objects.all(),
        'project_form': ProjectForm,
        'editing': True,
    }

    roles = [str(role.id) for role in args['roles']]

    if request.POST:
        args['project_form'] = ProjectForm(request.POST)
        if args['project_form'].is_valid():
            p = args['project_form'].save()
            project_id = str(p.id)
        else:
            send_err_msg(request, args['project_form'])
            return render(request, template, args)

        for user in args['users']:
            # check member in members list (member_in_<id> hidden field value)
            user_in_members_list = request.POST.get('member_in_' + str(user.id))
            if user_in_members_list:
                label_name = 'member_' + str(user.id);
                roles_list = request.POST.getlist(label_name)

                # checked roles save in db
                for role in roles_list:
                    # validate roles
                    if role in roles:
                       Membership(
                            project_id=project_id,
                            user_id=user.id,
                            role_id=role
                       ).save()

        msg = 'Project &#35;' + project_id + \
              ': &laquo;' + request.POST.get('name') + \
              '&raquo; have successfully created'

        messages.success(request, msg)

        return redirect('/projects/')

#    args['test'] = [str(role.id) for role in args['roles']]
    return render(request, template, args)


@valid_id
@permission_required('projects.change_project')
def edit_project(request, project_id):
    """
    Edit project
    """
    template = 'projects/edit_project.html'

    # get project
    project = Project.objects.get(pk=project_id)

    # get all roles of all users at the project
    users_roles_at_project = Membership.objects.filter(project=project_id)

    # get list of users which are members (has roles) at the project
    members = [member.user.id for member in users_roles_at_project.distinct('user')]

    # assign roles by users
    members_roles = {}
    for member in members:
        # if member hasn't roles
        try:
            members_roles[member] = [mbr.role.id for mbr in users_roles_at_project.filter(user_id=member)]
        except AttributeError:
            members_roles[member] = []

    # args to template
    args = {
        'users': User.objects.all(),
        'roles': Role.objects.all(),
        'user_perms': user_project_perms(request.user.id, project_id),
        'editing': True,
        'project': project,
        'members': members,
        'members_roles': members_roles,
        'project_form': ProjectForm(initial={
            'name': project.name,
            'description': project.description,
            'owner': project.owner,
        }),
    }

    # submit form
    if request.POST:
        args['project_form'] = ProjectForm(request.POST)
        if args['project_form'].is_valid():
            args['project_form'] = ProjectForm(request.POST, instance=Project.objects.get(pk=project_id))
            args['project_form'].save()
        else:
            send_err_msg(request, args['project_form'])
            return render(request, template, args)

        # if members list are empty, set initial
        try:
            members
        except UnboundLocalError:
            members = []
            members_roles = {}

        # get added and removed members and roles
        for user in args['users']:
            # check every user either he is member (member_in_<id> hidden field value)
            user_in_members_list = request.POST.get('member_in_' + str(user.id))

            if user_in_members_list:
                # if user not in members list (just added) -> add him there
                if user.id not in members:
                    members.append(user.id)

                # get roles list of the user (using 'member_<id>' field name)
                roles_list = request.POST.getlist('member_' + str(user.id))

                # Get the difference between previous and new roles
                # 'prev_mbr_roles' - previous member roles (set [] if no roles yet)
                try:
                    prev_mbr_roles = members_roles[user.id]
                # no roles yet
                except KeyError:
                    prev_mbr_roles = []

                # 'now_mbr_roles' - new checked member roles
                now_mbr_roles = list(map(int, roles_list))

                # if now checked role not in prev checked list (=> it checked now), save it
                for role in now_mbr_roles:
                    if role not in prev_mbr_roles:
                        Membership(
                            project_id=project_id,
                            user_id=user.id,
                            role_id=role
                        ).save()

                # if prev checked role not in now checked list (=> it unchecked now), delete it
                for role in prev_mbr_roles:
                    if role not in now_mbr_roles:
                        # delete from db
                        Membership.objects.get(
                            project_id=project_id,
                            user_id=user.id,
                            role_id=role
                        ).delete()

                # update roles at user (add user and roles if it wasn't in the dict yet)
                members_roles[user.id] = roles_list

                # if member without roles (? it is possible ?)
                # (changed model Membership, set null=True by role field)
                if not roles_list:
                    Membership(
                        project_id=project_id,
                        user_id=user.id,
                        role_id=''
                    ).save()

            else:
                # if user not in members list:
                #   1. he have been deleted from it
                #   2. he haven't been added (KeyError & ValueError exceptions)
                try:
                    members.remove(user.id)
                    members_roles.pop(user.id)
                    # delete from db all records where user at this project
                    Membership.objects.filter(project_id=project_id, user_id=user.id).delete()
                except (KeyError, ValueError):
                    pass

        # send message of success project update
        msg = 'Project &#35;' + project_id + \
              ': &laquo;' + request.POST.get('name') + \
              '&raquo; have been successfully edited'
        messages.success(request, msg)

        return redirect('/projects/' + project_id)

    # args['test'] = project_id
    return render(request, template, args)


@valid_id
@permission_required('projects.delete_project')
def delete_project(request, project_id):
    """
    Delete project
    """
    # get project
    project = Project.objects.get(pk=project_id)

    # delete the project
    project.delete()

    # set successful message
    msg = 'The project &#35;' + project_id + ': &laquo;' + project.name + '&raquo; has been successfully deleted'

    # send the message
    messages.success(request, msg)

    # go to the Projects page
    return redirect('/projects/')
