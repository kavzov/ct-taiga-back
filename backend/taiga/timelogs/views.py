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
    timelogs_list = Timelog.objects.all().order_by('date')

    if params['project_id']:
        timelogs_list = timelogs_list.filter(issue__project__id=params['project_id'])
        params['project_name'] = Project.objects.values('name').get(pk=params['project_id'])['name']
    if params['issue_id']:
        timelogs_list = timelogs_list.filter(issue__id=params['issue_id'])
        params['issue_id'] = int(params['issue_id'])
    if params['user_id']:
        timelogs_list = timelogs_list.filter(user__id=params['user_id'])
        params['user_id'] = int(params['user_id'])
    if params['date_from'] :
        timelogs_list = timelogs_list.filter(date__gte=params['date_from'] )
    if params['date_till']:
        timelogs_list = timelogs_list.filter(date__lte=params['date_till'])
    if params['order']:
        timelogs_list = timelogs_list.order_by(params['order'])

    durations = [v['duration'] for v in list(timelogs_list.values())]

    args['title'] = 'Timelogs'
    args['total_duration'] = sum(durations)
    args['params'] = params
    args['timelogs_list'] = timelogs_list
    args['timelog_form'] = TimelogForm
    args['issues'] = Issue.objects.all()
    args['users'] = User.objects.all()

    return args
# --- Get timelogs --- #


def get_paginated_timelogs(request, query_list):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    records_on_page = 25

    paginator = Paginator(query_list, records_on_page)
    page = request.GET.get('page')
    try:
        timelogs = paginator.page(page)
    except PageNotAnInteger:
        timelogs = paginator.page(1)
    except EmptyPage:
        timelogs = paginator.page(paginator.num_pages)

    return timelogs


def timelogs_list(request):
    format = request.GET.get('format')
    args = get_timelogs(request)
    args['timelogs'] = get_paginated_timelogs(request, args['timelogs_list'])

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


@permission_required('timelogs.add_timelog')
def add_timelog(request):
    args = {}
    args['timelog_form'] = TimelogForm(
        initial={'user':2}
    )

    project_id = request.GET.get('project_id')
    if project_id:
        args['timelog_form'].fields['issue'].queryset = Issue.objects.filter(project_id=project_id)

    if request.POST:
        req = get_timelog_req_data(request)
        timelog = Timelog(issue=req['issue'], user=req['user'], date=req['date'], duration=req['duration'])
        timelog.save()
        args['message'] = 'Timelog successfully added'
    else:
        args['message'] = 'Add a timelog'
        args['add'] = True

    issues = Issue.objects.all()
    if project_id:
        issues = issues.filter(project_id=project_id)
    users = User.objects.all()
    args['issues'] = issues
    args['users'] = users

    template = "timelogs/timelog_details.html"

    return render(request, template, args)


@permission_required('timelogs.change_timelog')
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

@permission_required('timelogs.delete_timelog')
def delete_timelog(request, timelog_id):
    pass


# --------------------------------- #
# --- Generates random timelogs --- #
def generate(request):
    from random import randrange, choice
    def get_rand_duration():
        return "{}.{}".format(randrange(0,9), randrange(0,99,25))

    def get_rand_date():
        days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
        monthes = {'01':'31', '02':'28', '03':'31', '04':'30', '05':'31'}
        year = '2017'

        month = choice(list(monthes.keys()))
        day = choice(days)
        if day > monthes[month]:
            day = '28'
        date = "{}-{}-{}".format(year, month, day)
        return date

    def get_rand_user():
        # users_id = [v['id'] for v in User.objects.values('id')]
        users = User.objects.all()
        return choice(users)

    def get_rand_issue():
        issues = Issue.objects.all()
        return choice(issues)

    timelogs_count = 100
    # for t in range(1, timelogs_count):
    #     timelog = Timelog(issue=get_rand_issue(), user=get_rand_user(), date=get_rand_date(), duration=get_rand_duration())
    #     timelog.save()
        # print(timelog.duration)

    from django.http import HttpResponse
    return HttpResponse('Ok!')