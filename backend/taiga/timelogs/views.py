import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import JsonResponse
from taiga import permissions
from .models import Timelog
from taiga.projects.models import Project
from .forms import TimelogForm
from taiga.projects.issues.models import Issue
from taiga.users.models import User
from taiga.projects.views import valid_id, send_err_msg, user_project_perms, project_permission_required


# --- utils for view_timelogs --- #
def get_id(param, kwargs, req):
    """
    Get id of project, issue etc. by param from query string or get query
    """
    try:
        id = kwargs[param]
    except KeyError:
        id = req.GET.get(param)
    if id:
        return int(id)


def get_project(project_id):
    """
    Get project by project id
    """
    return Project.objects.get(pk=project_id)


def get_project_issues(project_id):
    """
    Get issues of project by project id
    """
    return Issue.objects.filter(project_id=project_id)


def get_distinct_users(timelogs):
    """
    Get distinct users of the timelog list
    """
    return User.objects.filter(pk__in=[timelog.user for timelog in timelogs.distinct('user')])


def get_timelogs(timelogs, project_id=None, issue_id=None, user_id=None):
    """
    Get timelogs of project or issue or user by its id
    """
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
    global project, issues, users, user_perms
    template = 'timelogs/timelogs_list.html'
    csvfilename = 'timelogs.csv'
    jsonfile = 'timelogs.json'
    title = 'Timelogs'

    # initial timelogs set
    timelogs = Timelog.objects.all()

    # project_id
    project_id = get_id('project_id', kwargs, request)
    # TODO remove 'if' after remove 'Tiemlogs' menu punct (no more need cause no output of all timelogs of all projects)
    if project_id:
        project = get_project(project_id)
        title += ' of &laquo;' + project.name + ' &raquo;'
        # get timelogs of the project
        timelogs = get_timelogs(timelogs, project_id=project_id)
        # issues of the project only
        issues = get_project_issues(project_id)
        # users who tracked at the project issues only
        users = get_distinct_users(timelogs)
        # authorized user perms at the project
        user_perms = user_project_perms(request.user.id, project_id)

    # filtered issue_id
    issue_id = get_id('issue_id', kwargs, request)
    if issue_id:
    # TODO get project_id, if called from issue details page
        # get issue's timelogs
        timelogs = get_timelogs(timelogs, issue_id=issue_id)
        # users who tracked at the issue only
        users = get_distinct_users(timelogs)

    # filtered user_id
    user_id = get_id('user_id', kwargs, request)
    if user_id:
        # get user's timelogs
        timelogs = get_timelogs(timelogs, user_id=user_id)
        # issues which the user tracked
        issues = issues.filter(
            pk__in=[
                timelog.issue.id for timelog in Timelog.objects.filter(user_id=user_id).distinct('issue')
        ])

    # extra filters
    date_from = request.GET.get('date_from')
    date_till = request.GET.get('date_till')
    order = request.GET.get('order')

    if date_from:
        timelogs = timelogs.filter(date__gte=date_from)
    if date_till:
        timelogs = timelogs.filter(date__lte=date_till)
    if order:
        timelogs = timelogs.order_by(order)

    if request.GET.get('format') == 'csv':
        # some_streaming_csv_view(request, csvfilename)
        data = export(timelogs, csvfilename, fields = ['issue', 'user', 'date', 'duration'])
        return HttpResponse(data)

    # total duration of filtered timelogs
    total_duration = sum([v['duration'] for v in list(timelogs.values())])

    if request.GET.get('format') == 'json':
        # data = [v for v in timelogs.values('issue', 'user', 'date', 'duration')]
        data = timelogs.values('issue', 'user', 'date', 'duration')
# TODO
        jsondata = JsonResponse(list(data), safe=False)
        response = HttpResponse(jsondata, content_type='text/json')
        # response['Content-Disposition'] = 'attachment; filename={}'.format(jsonfile)
        return response

    args = {
        'title': title,
        'timelog_form': TimelogForm,
        'project': project,
        'issues': issues,
        'issue_id': issue_id,
        'users': users,
        'user_id': user_id,
        'user_perms': user_perms,
        'date_from': date_from,
        'date_till': date_till,
        'order': order,
        'timelogs': timelogs,
        'total_duration': total_duration,
        'csvfile': csvfilename
    }

    return render(request, template, args)


import csv
from django.http import HttpResponse, StreamingHttpResponse


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def some_streaming_csv_view(request, csvfile):
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="{}".format(csvfile)'
    return response


def export(qs, filename, fields=None):
    model = qs.model
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    writer = csv.writer(response)
    # Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
    writer.writerow(headers)
    # Write data to CSV file
    for obj in qs:
        row = []
        for field in headers:
            if field in headers:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                row.append(val)
        writer.writerow(row)
    # Return CSV file to browser as download
    return response


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