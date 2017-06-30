from rest_framework import serializers
from .models import User, Role
from taiga.projects.issues.models import Issue
from taiga.projects.models import Project
from taiga.timelogs.models import Timelog
from taiga.projects.issues.serializers import IssueShortSerializer


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class ProjectShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')


class TimelogShortSerializer(serializers.ModelSerializer):
    issue = serializers.SerializerMethodField()

    class Meta:
        model = Timelog
        fields = ('id', 'issue', 'date', 'duration')

    def get_issue(self, obj):
        issues = Issue.objects.get(timelog_issue=obj)
        return IssueShortSerializer(issues).data


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'get_full_name')


class UserSerializer(serializers.ModelSerializer):
    assigned_issues = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()
    owned_projects = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    timelogs = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'issues', 'assigned_issues',
                  'owned_projects', 'projects', 'timelogs')

    def get_assigned_issues(self, obj):
        issues = Issue.objects.filter(assigned_to=obj)
        return IssueShortSerializer(issues, many=True).data

    def get_issues(self, obj):
        issues = Issue.objects.filter(users=obj)
        return IssueShortSerializer(issues, many=True).data

    def get_owned_projects(self, obj):
        projects = Project.objects.filter(owner=obj)
        return ProjectShortSerializer(projects, many=True).data

    def get_projects(self, obj):
        projects = Project.objects.filter(members=obj).distinct('name')
        return ProjectShortSerializer(projects, many=True).data

    def get_timelogs(self, obj):
        timelogs = Timelog.objects.filter(user=obj).order_by('date')
        return TimelogShortSerializer(timelogs, many=True).data
