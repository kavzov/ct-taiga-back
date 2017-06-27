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
    Check id (<project_id>, <issue_id>,...) from query string, whether it in db
    Redirect with error messages
    """
    def inner(request, *args, **kwargs):
        # apps list (in the singular)
        apps = [
            'project',
            'issue',
            'timelog',
            'wiki'
        ]

        def get_app_model_name(app):
            """ Model (e.g. 'project' -> Project) """
            return eval(app.capitalize())

        def get_app_id_label(app):
            """ app id label (e.g. 'project' -> 'project_id') """
            id_suffix = '_id'
            return app + id_suffix

        def get_app_redir_page(app):
            """ page for redirect (e.g. 'project' -> '/projects/') """
            if app == 'wiki':
                app = 'project'
            return '/{}s/'.format(app)

        def valid(app):
            """ redirect out with error message if id doesn't exist """
            app_id_label = get_app_id_label(app)
            app_id = kwargs.get(app_id_label, None)

            if app_id:
                app_model_name = get_app_model_name(app)
                try:
                    app_model_name.objects.get(pk=app_id)
                except ObjectDoesNotExist:
                    messages.error(request, 'Error: {} &#35; {} does not exist'.format(app, app_id))
                    return get_app_redir_page(app)

        for app in apps:
            err_redir = valid(app)
            if err_redir:
                return redirect(err_redir)

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


# -------------------------------------------------------------------------------------------------------------------- #
# Managing ----------------------------------------------------------------------------------------------------------- #

def get_managing_users(manager_id, project_id):
    """
    Returns users list of manager (user_id) at the project (project_id)
    """
    user = User.objects.get(pk=manager_id)
    for mng in user.managing:
        if mng['project'] == project_id:
            return mng['users']

def rm_managing(manager_id, project_id):
    """
    Remove dict with project_id from manager list of user_id
    """
    user = User.objects.get(pk=manager_id)
    for mng in user.managing:
        if mng['project'] == project_id:
            user.managing.remove(mng)
            user.save()
            break

def add_managing(manager_id, project_id, users):
    """
    Add managing for 'project_id' with 'users' (list) to 'manager_id'
    """
    pattern = "{{'project': {}, 'users': {}}}"
    user = User.objects.get(pk=manager_id)
    user.managing.append(pattern.format(project_id, users))
    user.save()

def add_user_to_managing(manager_id, project_id, user_id):
    """
    Add 'user_id' to existing managing
    """
    user = User.objects.get(pk=manager_id)
    for mng in user.managing:
        if mng['project'] == project_id:
            mng['users'].append(user_id)
            break

