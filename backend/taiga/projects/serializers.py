import serpy
from rest_framework import serializers
from taiga.mixins import DynamicFieldsMixin
from .models import Project
from .models import Membership
from taiga.serializers import ProjectBaseSerializer
from taiga.serializers import IssueBaseSerializer
from taiga.serializers import UserBaseSerializer


class MemberSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    userID = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    roleID = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = ('id', 'project', 'user', 'userID', 'role', 'roleID')

    def get_userID(self, obj):
        return obj.user.id                            # User ID inside single member dict block (if it is)

    def get_user(self, obj):
        return obj.user.get_full_name()
        # return UserBaseSerializer(obj.user).data      # Dict with user ID

    def get_role(self, obj):
        return obj.role.name
        # return RoleSerializer(obj.role).data          # Dict with role ID

    def get_roleID(self, obj):
        return obj.role.id


class ProjectSerializer(DynamicFieldsMixin, ProjectBaseSerializer):
    owner_info = serializers.SerializerMethodField()
    issues_info = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta(ProjectBaseSerializer.Meta):
        fields = ProjectBaseSerializer.Meta.fields + (
            'description', 'created_date', 'owner_info', 'issues_info', 'members', 'test_json'
        )

    def get_owner_info(self, obj):
        return obj.owner.get_full_name()
        # return UserBaseSerializer(obj.owner).data     # Dict with user ID

    def get_issues_info(self, obj):
        return IssueBaseSerializer(obj.issues.all(), many=True).data

    def get_members(self, obj):
        members = Membership.objects.filter(project=obj).distinct('user_id')
        return MemberSerializer(members, fields=(
            'user',
            # 'userID',
            'role',
            # 'roleID',
        ), many=True).data


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