from django.shortcuts import render
from .models import User
from taiga.timelogs.models import Timelog


def users_list(request):
    users = User.objects.all()
    args = {'users_list': users}
    return render(request, 'users/users_list.html', args)


def user_details(request, user_id):
    args = {}
    user = User.objects.get(id=user_id)
    args['user_details'] = user
    args['id'] = user_id
    args['name'] = user.username
    return render(request, 'users/user_details.html', args)


def user_logs(request):
    pass