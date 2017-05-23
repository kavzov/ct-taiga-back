from django.contrib.auth import authenticate, login


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
        else:
            pass
            # Return an 'invalid login' error message.

    else:
        pass