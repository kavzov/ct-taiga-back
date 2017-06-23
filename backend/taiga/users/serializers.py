from rest_framework import serializers
from .models import User, Role
from taiga.index.serializers import ProjectSerializer
from taiga.projects.issues.serializers import IssueSerializer


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'permissions')


class UserSerializer(serializers.ModelSerializer):
    owned_projects = ProjectSerializer(many=True, read_only=True).data
    assigned_issues = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'get_full_name', 'owned_projects', 'assigned_issues')