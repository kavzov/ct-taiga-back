from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.db.models import Q
from django.http import response, HttpResponse, Http404
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
    template = 'index/test.html'

    return render(request, template, {})


from rest_framework import viewsets
from .serializers import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-modified_date')
    serializer_class = ProjectSerializer


class ProjectDetails(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProjectSerializer(snippet)
        return Response(serializer.data)
