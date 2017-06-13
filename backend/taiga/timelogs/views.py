import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from taiga import permissions
from .models import Timelog
from taiga.projects.models import Project
from .forms import TimelogForm
from taiga.projects.issues.models import Issue
from taiga.users.models import User
from taiga.projects.views import valid_id, send_err_msg, project_permission_required


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


# --- utils for view_timelogs --- #
def get_id(param, kwargs, req):
    try:
        id = kwargs[param]
    except KeyError:
        id = req.GET.get(param)
    if id:
        return int(id)


def get_project(project_id):
    return Project.objects.get(pk=project_id)


def get_project_issues(project_id):
    return Issue.objects.filter(project_id=project_id)


def get_distinct_users(timelogs):
    return User.objects.filter(pk__in=[timelog.user for timelog in timelogs.distinct('user')])


def get_timelog(timelogs, project_id=None, issue_id=None, user_id=None):
    if project_id:
        return timelogs.filter(issue__project__id=project_id)
    if issue_id:
        return timelogs.filter(issue__id=issue_id)
    if user_id:
        return timelogs.filter(user__id=user_id)


# ---------------------------------- #
# --------- View timelogs ---------- #
def view_timelogs(request, **kwargs):
    """
    Display timelogs
    """
    template = 'timelogs/timelogs_list.html'
    params = {}
    args = {
        'title': 'Timelogs',
        'timelog_form': TimelogForm,
        'issues': Issue.objects.all(),
        'users': User.objects.all(),
    }

    # initial timelogs query
    timelogs = Timelog.objects.all()

    # project_id
    params['project_id'] = get_id('project_id', kwargs, request)
    if params['project_id']:
        args['project'] = get_project(params['project_id'])
        # get timelogs of the project
        timelogs = get_timelog(timelogs, project_id=params['project_id'])
        # issues of the project only
        args['issues'] = get_project_issues(params['project_id'])
        # users who tracked at the project issues only
        args['users'] = get_distinct_users(timelogs)

    # issue_id
    params['issue_id'] = get_id('issue_id', kwargs, request)
    if params['issue_id']:
        # get issue's timelogs
        timelogs = get_timelog(timelogs, issue_id=params['issue_id'])
        # users who tracked at the issue only
        args['users'] = get_distinct_users(timelogs)

    # user_id
    params['user_id'] = get_id('user_id', kwargs, request)
    if params['user_id']:
        # get user's timelogs
        timelogs = get_timelog(timelogs, user_id=params['user_id'])
        # issues which the user tracked
        args['issues'] = args['issues'].filter(
            pk__in=[
                timelog.issue.id for timelog in Timelog.objects.filter(user_id=params['user_id']).distinct('issue')
        ])

    # get extra params
    params['date_from'] = request.GET.get('date_from')
    params['date_till'] = request.GET.get('date_till')
    params['order'] = request.GET.get('order')

    if params['date_from'] :
        timelogs = timelogs.filter(date__gte=params['date_from'] )
    if params['date_till']:
        timelogs = timelogs.filter(date__lte=params['date_till'])
    if params['order']:
        timelogs = timelogs.order_by(params['order'])

    # get total duration of all filtered timelogs
    duration = sum([v['duration'] for v in list(timelogs.values())])

    args['params'] = params
    args['total_duration'] = duration
    # args['timelogs'] = get_paginated_timelogs(request, timelogs.order_by('date'))
    args['timelogs'] = timelogs
    return render(request, template, args)


@project_permission_required('timelogs.add_timelog', '/timelogs/')
def add_timelog(request, issue_id):
    """
    Add a timelog
    """
    template = 'timelogs/timelog_details.html'

    args = {
        'timelog_form': TimelogForm,
        'issue_id': issue_id,
    }

    if request.POST:
        timelog_form = TimelogForm(request.POST)
        if timelog_form.is_valid():
            timelog_form.save()
            msg = 'Time log successfully added'
            messages.success(request, msg)
            return redirect('/issues/'+issue_id)
        else:
            send_err_msg(request, timelog_form)
            return render(request, template, args)

    return render(request, template, args)


@valid_id
@project_permission_required('timelogs.change_timelog', '/timelogs/')
def edit_timelog(request, timelog_id):
    """
    Edit timelog
    """
    template = 'timelogs/timelog_details.html'

    # get timelog info
    timelog = Timelog.objects.get(pk=timelog_id)

    args = {
        'timelog': timelog,
        'issue_id': timelog.issue.id,
        'timelog_form': TimelogForm(initial={
            'user': timelog.user,
            'date': timelog.date,
            'duration': timelog.duration,
        })
    }

    if request.POST:
        timelog_form = TimelogForm(request.POST)
        if timelog_form.is_valid():
            timelog_form = TimelogForm(request.POST, instance=timelog)
            timelog_form.save()
        else:
            send_err_msg(request, timelog_form)
            return render(request, template, args)

        msg = 'Timelog &#35;' + str(timelog.id) + ' successfully updated'
        messages.success(request, msg)

        return redirect('/timelogs/')

    return render(request, template, args)


@valid_id
@project_permission_required('timelogs.delete_timelog', '/timelogs/')
def delete_timelog(request, timelog_id):
    """
    Delete timelog
    """
    timelog = Timelog.objects.get(pk=timelog_id)
    timelog.delete()

    msg = 'Timelog &#35;' + timelog_id + ' successfully deleted'
    messages.success(request, msg)

    return redirect('/timelogs/')


# --------------------------------- #
# --- Random timelogs generator --- #
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