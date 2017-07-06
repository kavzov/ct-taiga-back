import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from .models import User
from taiga.projects.issues.models import Issue
from taiga.timelogs.models import Timelog


def users_list(request):
    users = User.objects.all()
    args = {'users_list': users}

    return render(request, 'users/users_list.html', args)


def user_details(request, user_id):
    args = {}
    user = User.objects.get(id=user_id)

    q = Timelog.objects.filter(user=1).values('issue').distinct()
    issues = Issue.objects.filter(pk__in=q)

    args['title'] = 'User ' + user.username
    args['user_details'] = user
    args['id'] = user_id
    args['issues'] = issues

    return render(request, 'users/user_details.html', args)


# ---------------------------------------------------------------------------- #
# REST Framework ------------------------------------------------------------- #

from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, UserBaseSerializer
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import views, viewsets, mixins


class UserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserBaseSerializer


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # renderer_classes = (JSONRenderer,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def retrieve(self, request, pk):
    #     user = get_object_or_404(User, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

    def list(self, request):
        serializer = UserBaseSerializer(self.queryset, many=True)
        return Response(serializer.data)






