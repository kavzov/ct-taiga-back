import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from taiga import permissions
from .models import Timelog
from taiga.projects.models import Project
from .forms import TimelogForm
from taiga.projects.issues.models import Issue
from taiga.users.models import User


# --- Get timelogs --- #
def get_timelogs(request, **kwargs):
    """ Get timelogs from request and return args for template """
    params = dict()
    try:
        params['issue_id'] = kwargs['issue_id']
    except KeyError:
        params['issue_id'] = request.GET.get('issue_id')
    try:
        params['user_id'] = kwargs['user_id']
    except KeyError:
        params['user_id'] = request.GET.get('user_id')
    try:
        params['project_id'] = kwargs['project_id']
    except KeyError:
        params['project_id'] = request.GET.get('project_id')
    params['date_from'] = request.GET.get('date_from')
    params['date_till'] = request.GET.get('date_till')
    params['order'] = request.GET.get('sort_by')

    args = dict()
    timelogs = Timelog.objects.all().order_by('date')

    if params['project_id']:
        timelogs = timelogs.filter(issue__project__id=params['project_id'])
        params['project_name'] = Project.objects.values('name').get(pk=params['project_id'])['name']
    if params['issue_id']:
        timelogs = timelogs.filter(issue__id=params['issue_id'])
        params['issue_id'] = int(params['issue_id'])
    if params['user_id']:
        timelogs = timelogs.filter(user__id=params['user_id'])
        params['user_id'] = int(params['user_id'])
    if params['date_from'] :
        timelogs = timelogs.filter(date__gte=params['date_from'] )
    if params['date_till']:
        timelogs = timelogs.filter(date__lte=params['date_till'])
    if params['order']:
        timelogs = timelogs.order_by(params['order'])

    durations = [v['duration'] for v in list(timelogs.values())]

    args['title'] = 'Timelogs'
    args['total_duration'] = sum(durations)
    args['params'] = params
    args['timelogs_list'] = timelogs
    args['timelog_form'] = TimelogForm
    args['issues'] = Issue.objects.all()
    args['users'] = User.objects.all()

    return args
# --- Get timelogs --- #


def timelogs_list(request):
    format = request.GET.get('format')
    args = get_timelogs(request)

    if format == 'json':
        template = "timelogs/json_timelogs.html"
        args['jsondata'] = json.dumps(list(args['timelogs_list'].values('issue_id', 'user_id', 'date', 'duration')), cls=DjangoJSONEncoder)
    else:
        template = "timelogs/timelogs_list.html"

    return render(request, template, args)


def timelog_details(request, timelog_id):
    args = dict()
    timelog_details = Timelog.objects.get(pk=timelog_id)
    issues = Issue.objects.values()
    users = User.objects.all()

    args['timelog_form'] = TimelogForm
    args['timelog_details'] = timelog_details
    args['timelog_id'] = timelog_id
    args['issues'] = issues
    args['users'] = users
    template = "timelogs/timelog_details.html"

    return render(request, template, args)


def get_timelog_req_data(request):
    req = dict()
    issue_id = request.POST.get('issue_id')
    req['issue'] = Issue.objects.get(pk=issue_id)
    user_id = request.POST.get('user_id')
    req['user'] = User.objects.get(pk=user_id)
    req['date'] = request.POST.get("date")
    req['duration'] = request.POST.get("duration")

    return req


@permission_required(permissions.ADMIN_PERMISSIONS)
def edit_timelog(request, timelog_id):
    args = dict()
    if request.POST:
        req = get_timelog_req_data(request)
        timelog = Timelog(id=timelog_id, issue=req['issue'], user=req['user'], date=req['date'], duration=req['duration'])
        timelog.save()
        args['message'] = 'Timelog #{} successfully updated'.format(timelog_id)

    timelog_details = Timelog.objects.get(pk=timelog_id)
    issues = Issue.objects.values()
    users = User.objects.all()
    args['timelog_details'] = timelog_details
    args['timelog_id'] = timelog_id
    args['issues'] = issues
    args['users'] = users

    template = "timelogs/timelog_details.html"

    return render(request, template, args)


def add_timelog(request):
    args = dict()
    if request.POST:
        req = get_timelog_req_data(request)
        timelog = Timelog(issue=req['issue'], user=req['user'], date=req['date'], duration=req['duration'])
        timelog.save()
        args['message'] = 'Timelog successfully added'
    else:
        args['message'] = 'Add a timelog'
        args['add'] = True

    issues = Issue.objects.values()
    users = User.objects.all()
    args['issues'] = issues
    args['users'] = users

    template = "timelogs/timelog_details.html"

    return render(request, template, args)


def delete_timelog(request, timelog_id):
    pass
