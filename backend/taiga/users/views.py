from django.shortcuts import render
from django.http import HttpResponse
from .models import User


def users_list(request):
    """ show list of users """
    users = User.objects.all()
    args = {'users': users}
    return render(request, 'users_list.tmpl', args)


def user_details(request, user_id):
    args = {}
    user = User.objects.get(id=user_id)
    args['obj'] = user
    args['id'] = user_id
    args['name'] = user.username
    return render(request, 'user_details.tmpl', args)

