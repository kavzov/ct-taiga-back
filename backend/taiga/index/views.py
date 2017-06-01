from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.db.models import Q
from taiga.projects.models import Project, Membership
from taiga.users.models import User, Role
from .forms import ProjectDetails, ProjectMembers


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



def search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    users = User.objects.filter(Q(first_name__contains=search_text) | Q(last_name__contains=search_text) | Q(username__contains=search_text))
    args = {'search_users': users }
    template = "index/test.html"

    return render(request, template, args)


def test(request):
    template = "index/test.html"
    args = {}
    project_form = ProjectDetails
    member_form = ProjectMembers

    if request.POST:
        project_form = ProjectDetails(request.POST)
        member_form = ProjectMembers(request.POST)
        if project_form.is_valid() and member_form.is_valid():

            return render(request, template, {'text': 'OK ' + request.POST.get("name"), 'member': request.POST.get("user")})
    args['text'] = request.POST.get("name")
    args['project_form'] = project_form
    args['member_form'] = member_form
    args['users'] = User.objects.all()
    args['roles'] = Role.objects.all()

    return render(request, template, args)


def testformset(request):
    from django.forms import formset_factory

    ProjectFormSet = formset_factory(ProjectDetails)
    MemberFormSet = formset_factory(ProjectMembers)

    project_formset = ProjectFormSet(prefix='project')
    member_formset = MemberFormSet(prefix='member')

    template = "index/testformset.html"
    args = {}

    args['project_formset'] = project_formset
    args['member_formset'] = member_formset

    return render(request, template, args)
