from django.shortcuts import render
from .models import Timelog
from taiga.projects.issues.models import Issue
from taiga.users.models import User


def timelogs_list(request):
    issue_id = request.GET.get('issue')
    user_id = request.GET.get('user')
    from_date = request.GET.get('from')
    till_date = request.GET.get('till')
    order = request.GET.get('sort_by')

    timelogs_page_data = dict()
    timelogs_params = dict()
    timelogs = Timelog.objects.all().order_by('date')

    if issue_id:
        timelogs = timelogs.filter(issue__id=issue_id)
        timelogs_params['issue'] = Issue.objects.get(pk=issue_id)
    if user_id:
        timelogs = timelogs.filter(user__id=user_id)
        timelogs_params['user'] = User.objects.get(pk=user_id)
    if from_date:
        timelogs = timelogs.filter(date__gte=from_date)
    if till_date:
        timelogs = timelogs.filter(date__lte=till_date)
    if order:
        timelogs = timelogs.order_by(order)


    timelogs_page_data['timelogs_list'] = timelogs
    timelogs_page_data['timelogs_params'] = timelogs_params

    return render(request, "timelogs/timelogs_list.html", timelogs_page_data)


def timelog_details(request, timelog_id):
    pass


def add_timelog(request):
    pass


def edit_timelog(request, timelog_id):
    pass


def delete_timelog(request, timelog_id):
    pass
