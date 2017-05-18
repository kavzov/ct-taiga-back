from django.shortcuts import render
from .models import Timelog
from taiga.projects.models import Project
from .forms import TimelogForm
from taiga.projects.issues.models import Issue
from taiga.users.models import User


def timelogs_list(request):
    params = dict()
    params['issue_id'] = request.GET.get('issue_id')
    params['user_id'] = request.GET.get('user_id')
    params['project_id'] = request.GET.get('project_id')
    params['date_from'] = request.GET.get('date_from')
    params['date_till'] = request.GET.get('date_till')
    params['order'] = request.GET.get('sort_by')

    issue_id = request.GET.get('issue')
    user_id = request.GET.get('user')
    from_date = request.GET.get('date_from')
    till_date = request.GET.get('date_till')
    order = request.GET.get('sort_by')

    args = dict()
    timelogs = Timelog.objects.all().order_by('-date')

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

    return render(request, "timelogs/timelogs_list.html", args)


def timelog_details(request, timelog_id):
    pass


def add_timelog(request):
    pass


def edit_timelog(request, timelog_id):
    pass


def delete_timelog(request, timelog_id):
    pass
