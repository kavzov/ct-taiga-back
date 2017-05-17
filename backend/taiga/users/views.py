from django.shortcuts import render
from .models import User
from taiga.timelogs.models import Timelog


def users_list(request):
    users = User.objects.all()
    args = {'users': users}
    return render(request, 'users/users_list.html', args)


def user_details(request, user_id):
    args = {}
    user = User.objects.get(id=user_id)
    args['obj'] = user
    args['id'] = user_id
    args['name'] = user.username
    return render(request, 'users/user_details.html', args)


# -------------------------------------------------------- #


def user_logs(request, user_id):
    """ Timelogs of a user with 'user_id' """

    def day_of_month(date):
        """ Day of month in format 'dd Month', e.g. '15 May' """
        return date.strftime("%d %B")

    user = User.objects.values('username').get(id=user_id)['username']
    # TODO validation of from_ and till_date
    from_date = request.GET.get('from')
    till_date = request.GET.get('till')

    rawlogs = Timelog.objects.\
        values('date', 'duration').\
        filter(user=user_id)

    if from_date:
        rawlogs = rawlogs.filter(date__gte=from_date)
    if till_date:
        rawlogs = rawlogs.filter(date__lte=till_date)

    logs = []
    total_duration = 0
    for log in rawlogs:
        d = dict()
        d['date'] = day_of_month(log['date'])
        total_duration += log['duration']
        d['duration'] = Timelog.decimal_str(log['duration'])
        logs.append(d)

    total_duration = Timelog.decimal_str(total_duration)

    args = {
        'username': user,
        'user_logs': logs,
        'total_duration': total_duration,
    }
    return render(request, 'users/user_logs.tmpl', args)