import serpy
from rest_framework import serializers
from taiga.mixins import DynamicFieldsMixin
# from taiga.projects.issues.serializers import IssueBaseInfoSerializer
from taiga.projects.issues.serializers import IssueSerializer
from taiga.users.serializers import RoleSerializer
from taiga.users.serializers import UserBaseSerializer
from .models import Project, Membership
from taiga.users.models import User, Role
from taiga.projects.issues.models import Issue
from taiga.timelogs.models import Timelog
from taiga.serializers import ProjectBaseSerializer
from taiga.serializers import IssueBaseSerializer
from taiga.serializers import UserBaseSerializer


class MemberSerializer(serpy.Serializer):
    # id = serpy.MethodField()
    user = serpy.MethodField()
    role = serpy.MethodField()

    # def get_id(self, obj):
    #     return obj.user.id                            # User ID inside single member dict block (if it is)

    def get_user(self, obj):
        return obj.user.get_full_name()
        # return UserBaseSerializer(obj.user).data      # Dict with user ID

    def get_role(self, obj):
        return obj.role.name
        # return RoleSerializer(obj.role).data          # Dict with role ID


class ProjectSerializer(ProjectBaseSerializer):
    description = serpy.Field()
    created_date = serpy.Field()
    owner = serpy.MethodField()
    issues = serpy.MethodField()
    members = serpy.MethodField()

    def get_owner(self, obj):
        return obj.owner.get_full_name()
        # return UserBaseSerializer(obj.owner).data     # Dict with user ID

    def get_issues(self, obj):
        from taiga.projects.issues.serializers import IssueBaseSerializer
        return IssueBaseSerializer(obj.issues.all(), many=True).data

    def get_members(self, obj):
        members = Membership.objects.filter(project=obj)
        return MemberSerializer(members, many=True).data


# class ProjectSerializer(serializers.ModelSerializer):
#     issues_info = IssueBaseInfoSerializer(many=True, read_only=True, required=False, source='issues')
#     members = serializers.SerializerMethodField(read_only=True)
#     # members = UserBaseInfoSerializer(many=True, required=False)
#     owner_info = UserBaseInfoSerializer(read_only=True, required=False, source='owner')
#
#     def get_members(self, obj):
#         memberships = Membership.objects.filter(project=obj).distinct('user')
#         return MemberSerializer(memberships, many=True).data
#
#     class Meta:
#         model = Project
#         fields = ('id', 'name', 'description', 'created_date', 'owner', 'owner_info', 'issues', 'issues_info', 'members')
#
#
# class ProjectBaseInfoSerializer(serializers.SerializerMethodField):
#     class Meta:
#         model = Project
#         fields = ('id', 'get_full_name')