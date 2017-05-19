import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from .models import User
from taiga.projects.issues.models import Issue
from taiga.timelogs.models import Timelog
from taiga.timelogs.views import get_timelogs


def users_list(request):
    users = User.objects.all()
    args = {'users_list': users}
    return render(request, 'users/users_list.html', args)


def user_details(request, user_id):
    args = {}
    user = User.objects.get(id=user_id)

    q = Timelog.objects.filter(user=1).values('issue').distinct()
    issues = Issue.objects.filter(pk__in=q)

    args['title'] = 'User ' + user.username
    args['user_details'] = user
    args['id'] = user_id
    args['issues'] = issues
    return render(request, 'users/user_details.html', args)


def user_timelogs(request, user_id):
    format = request.GET.get('format')
    args = get_timelogs(request, user_id=user_id)

    if format == 'json':
        template = "timelogs/json_timelogs.html"
        args['jsondata'] = json.dumps(list(args['timelogs_list'].values('issue_id', 'date', 'duration')), cls=DjangoJSONEncoder)
    else:
        template = "users/user_details.html"
        args['issue_details'] = User.objects.get(id=user_id)

    return render(request, template, args)
