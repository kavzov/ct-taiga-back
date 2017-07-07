from rest_framework import serializers
from taiga.mixins import DynamicFieldsMixin
from taiga.users.models import User
from taiga.users.models import Role
from taiga.projects.models import Project
from taiga.projects.models import Membership
from taiga.projects.issues.models import Issue

# ---------------------------------------------------------------------------- #
# User ----------------------------------------------------------------------- #
class UserBaseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'name')

    def get_name(self, obj):
        return obj.get_full_name()


class RoleSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


# ---------------------------------------------------------------------------- #
# Issue ---------------------------------------------------------------------- #
class IssueBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'subject')

# ---------------------------------------------------------------------------- #
# Project -------------------------------------------------------------------- #
class ProjectBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')


class MemberSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = ('user', 'role', 'project')

    def get_role(self, obj):
        role = Role.objects.get(pk=obj.role_id)
        return RoleSerializer(role, fields=('name',)).data

    def get_project(self, obj):
        project = Project.objects.get(pk=obj.project_id)
        return ProjectBaseSerializer(project).data

