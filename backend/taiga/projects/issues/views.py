import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Issue
from .forms import AddIssueForm
from taiga.users.models import User
from taiga.timelogs.views import get_timelogs
from taiga.timelogs.models import Timelog
from taiga.projects.views import user_project_perms


def issues_list(request):
    args = {}
    iss_list = Issue.objects.all()
    add_issue_form = AddIssueForm
    args['title'] = "Issues"
    args['issues_list'] = iss_list
    args['add_issue_form'] = add_issue_form

    return render(request, "issues/issues_list.html", args)

from django.contrib.auth.decorators import permission_required, login_required
from taiga.permissions import DEVELOPER_PERMISSIONS, ADMIN_PERMISSIONS


def issue_details(request, issue_id):
    template = "issues/issue_details.html"
    args = {}

    # queryset of users who tracked at this issue
    users = User.objects.filter(
        pk__in=[
            timelog.user for timelog in Timelog.objects.filter(issue_id=issue_id).distinct('user')
        ]
    )

    # issue
    issue = Issue.objects.get(id=issue_id)

    # total time duration on this issue
    timelogs = Timelog.objects.all().filter(issue_id=issue_id)
    duration = sum([v['duration'] for v in list(timelogs.values())])

    # users and its durations
    users_durations = {}
    for user in users:
        user_timelogs = timelogs.filter(user=user)
        users_durations[user] =sum([v['duration'] for v in list(user_timelogs.values())])

    args['user_perms'] = user_project_perms(request.user.id, issue.project.id)
    args['title'] = 'Issue "' + issue.subject + '"'
    args['users'] = users
    args['issue_details'] = issue
    args['total_time'] = duration
    args['users_durations'] = users_durations

    return render(request, template, args)


def issue_timelogs(request, issue_id):
    format = request.GET.get('format')
    args = get_timelogs(request, issue_id=issue_id)

    if format == 'json':
        template = "timelogs/json_timelogs.html"
        args['jsondata'] = json.dumps(list(args['timelogs_list'].values('user_id', 'date', 'duration')), cls=DjangoJSONEncoder)
    else:
        template = "issues/issue_details.html"
        args['issue_details'] = Issue.objects.get(id=issue_id)

    return render(request, template, args)


@csrf_protect
def add_issue(request):
    pass
