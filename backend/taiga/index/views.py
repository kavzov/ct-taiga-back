from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user


def auth_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/projects/')

        else:
            template = "index/login.html"
            return render(request, template, {'message': 'Something went wrong'})
    else:
        template = "index/login.html"
        return render(request, template, {})


def auth_logout(request):
    logout(request)
    return redirect("/login/")