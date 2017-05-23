from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")

        else:
            template = "index/login.html"
            return render(request, template, {'message': 'Something went wrong'})
    else:
        template = "index/login.html"
        return render(request, template, {})


def logout(request):
    pass