from rest_framework import serializers
from taiga.mixins import DynamicFieldsMixin
from .models import Issue
import serpy
from taiga.serializers import ProjectBaseSerializer
from taiga.serializers import IssueBaseSerializer
from taiga.serializers import UserBaseSerializer


class IssueSerializer(IssueBaseSerializer):
    description = serpy.Field()
    project = serpy.MethodField()
    users = serpy.MethodField()

    def get_project(self, obj):
        # ----- Debug ----- #
        print('obj ----------------> ', obj.project)
        return ProjectBaseSerializer(obj.project).data

    def get_users(self, obj):
        return UserBaseSerializer(obj.users.all(), many=True).data











# class IssueBaseInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Issue
#         fields = ('id', 'subject')
#
#
# class IssueSerializer(serializers.ModelSerializer):
#     # users = UserBaseInfoSerializer(many=True)
#     class Meta:
#         model = Issue
#         fields = ('id', 'subject', 'description', 'assigned_to', 'project',
#                   'users', 'status', 'priority', 'created_date', 'finished_date')
