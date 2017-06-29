from rest_framework import serializers
from taiga.projects.issues.serializers import IssueShortSerializer
from taiga.users.serializers import UserShortSerializer, RoleSerializer
from .models import Project, Membership
from taiga.users.models import User, Role
from taiga.projects.issues.models import Issue
from taiga.timelogs.models import Timelog


class MemberShortSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = ('user', 'role')

    def get_user(self, obj):
        user = User.objects.get(pk=obj.user)
        return UserShortSerializer(user).data

    def get_role(self, obj):
        role = Role.objects.get(pk=obj.role_id)
        return RoleSerializer(role).data



class ProjectSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'created_date', 'owner', 'issues', 'members')

    def get_issues(self, obj):
        issues = Issue.objects.filter(project=obj)
        return IssueShortSerializer(issues, many=True).data

    def get_members(self, obj):
        memberships = Membership.objects.filter(project=obj).distinct('user')
        members = [m.user for m in memberships]
        users = User.objects.filter(pk__in=members)
        return MemberShortSerializer(memberships, many=True).data

    def get_owner(self, obj):
        return UserShortSerializer(obj.owner).data
