import serpy
from rest_framework import serializers
from taiga.mixins import DynamicFieldsMixin
from .models import User, Role
# from taiga.projects.serializers import ProjectBaseInfoSerializer
from taiga.projects.issues.models import Issue
from taiga.timelogs.models import Timelog
from taiga.timelogs.serializers import TimelogSerializer
# from taiga.projects.issues.serializers import IssueBaseInfoSerializer
from taiga.serializers import IssueBaseSerializer
from taiga.serializers import UserBaseSerializer


class RoleSerializer(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field()


class UserSerializer(UserBaseSerializer):
    issues = serpy.MethodField()

    def get_issues(self, obj):
        return IssueBaseSerializer(obj.issues.all(), many=True).data


















        # class UserSerializer(serializers.ModelSerializer):
        #     # issues = serializers.SerializerMethodField()
        #     issues = IssueBaseInfoSerializer(many=True)
        #     assigned_to = IssueBaseInfoSerializer(many=True)    # assigned issues TODO change 'related_name' in model 'user'
        #     projects = serializers.SerializerMethodField()
        #     # owned_projects = ProjectBaseInfoSerializer(many=True)
        #     timelogs = serializers.SerializerMethodField()
        #
        #     class Meta:
        #         model = User
        #         fields = ('id', 'username', 'first_name', 'last_name', 'issues', 'assigned_to',
        #                   'owned_projects', 'projects', 'timelogs')
        #
        #     def get_issues(self, obj):
        #         issues = Issue.objects.filter()
        #         return IssueBaseInfoSerializer()
        #
        #     def get_timelogs(self, obj):
        #         timelogs = Timelog.objects.filter(user=obj).order_by('date')
        #         return TimelogSerializer(timelogs, many=True).data
        #
        #     def get_projects(self, obj):
        #         pass
        #
        #
        # class UserBaseInfoSerializer(serializers.ModelSerializer):
        #     class Meta:
        #         model = User
        #         fields = ('id', 'get_full_name')