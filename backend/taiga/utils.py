from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import render, redirect
from taiga.projects.models import Project, Membership
from taiga.projects.issues.models import Issue
from taiga.timelogs.models import Timelog
from taiga.users.models import User, Role
from taiga.wiki.models import Wiki


def valid_id(func):
    """
    Check whether issue, timelog, wiki, etc. are part of a project
    Redirect with error messages
    """
    def inner(request, *args, **kwargs):
        project_id = kwargs.get('project_id', None)
        issue_id = kwargs.get('issue_id', None)
        timelog_id = kwargs.get('timelog_id', None)
        wiki_id = kwargs.get('wiki_id', None)

        if project_id:
            try:
                Project.objects.get(pk=project_id)
            except ObjectDoesNotExist:
                messages.error(request, 'Error: project &#35;' + str(project_id) + ' does not exist')
                return redirect('/projects/')

        if issue_id:
            try:
                Issue.objects.get(pk=issue_id).project_id
            except ObjectDoesNotExist:
                messages.error(request, 'Error: issue &#35;' + str(issue_id) + ' does not exist')
                return redirect('/issues/')

        if timelog_id:
            try:
                Timelog.objects.get(pk=timelog_id).issue.project_id
            except ObjectDoesNotExist:
                messages.error(request, 'Error: timelog &#35;' + str(timelog_id) + ' does mot exist')
                return redirect('/timelogs/')

        if wiki_id:
            try:
                Wiki.objects.get(pk=wiki_id).project_id
            except ObjectDoesNotExist:
                messages.error(request, 'Error: wiki &#35;' + str(wiki_id) + ' does not exist')
                return redirect('/projects/')

        return func(request, *args, **kwargs)
    return inner


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
