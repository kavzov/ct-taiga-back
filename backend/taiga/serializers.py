from rest_framework import serializers
from taiga.users.models import User
from taiga.projects.models import Project
from taiga.projects.issues.models import Issue

# ---------------------------------------------------------------------------- #
# User ----------------------------------------------------------------------- #
class UserBaseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username')

    def get_name(self, obj):
        return obj.get_full_name()


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
