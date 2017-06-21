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


# -------------------------------------- #

from .serializers import ProjectSerializer, MembershipSerializer
from rest_framework import generics


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all().order_by('-modified_date')
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# -------------------------------------- #

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class ProjectCountView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        projects = Project.objects.all()
        pr_serl = ProjectSerializer(projects, many=True)
        content = {'projects': pr_serl.data}
        return Response(content)

# -------------------------------------- #

from rest_framework.renderers import TemplateHTMLRenderer

class ProjectsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'projects/projects_list.html'

    def get(self, request):
        queryset = Project.objects.all()
        context = {
            'title': 'Projects list',
            'projects_list': queryset,
        }
        return Response(context)


# -------------------------------------- #


from django.shortcuts import get_object_or_404


class ProjectEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index/test.html'

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project)

        return Response({'serializer': serializer, 'project': project})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'project': project})
        serializer.save()
        return redirect('project-list')


# -------------------------------------- #


# from rest_framework import viewsets
# from .serializers import ProjectSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
#
#
# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all().order_by('-modified_date')
#     serializer_class = ProjectSerializer
#
#
# class ProjectDetails(APIView):
#     def get_object(self, pk):
#         try:
#             return Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         project = self.get_object(pk)
#         serializer = ProjectSerializer(project)
#         return Response(serializer.data)
