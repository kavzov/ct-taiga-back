import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Issue
from .forms import AddIssueForm
from taiga.users.models import User
from taiga.timelogs.views import get_timelogs


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


# @permission_required(ADMIN_PERMISSIONS)
def issue_details(request, issue_id):
    args = {}

    users = User.objects.all()
    iss_details = Issue.objects.get(id=issue_id)

    args['title'] = 'Issue "' + iss_details.subject + '"'
    args['users'] = users
    args['issue_details'] = iss_details
    template = "issues/issue_details.html"

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
