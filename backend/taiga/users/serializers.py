from rest_framework import serializers
from taiga.mixins import DynamicFieldsMixin
from taiga.projects.models import Membership
from taiga.timelogs.models import Timelog
from taiga.timelogs.serializers import TimelogSerializer
from taiga.serializers import IssueBaseSerializer
from taiga.serializers import ProjectBaseSerializer
from taiga.serializers import MemberSerializer
from taiga.serializers import UserBaseSerializer


class UserSerializer(DynamicFieldsMixin, UserBaseSerializer):
    issues = IssueBaseSerializer(many=True)
    # TODO change related_name in model User from 'assigned_to' to 'assigned_issues'
    assigned_issues = IssueBaseSerializer(many=True)
    projects = serializers.SerializerMethodField()
    owned_projects = ProjectBaseSerializer(many=True)
    timelogs = serializers.SerializerMethodField()

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + (
            'username', 'issues', 'assigned_issues', 'owned_projects', 'projects', 'timelogs'
        )

    def get_timelogs(self, obj):
        timelogs = Timelog.objects.filter(user=obj).order_by('date')
        return TimelogSerializer(timelogs, fields=('issue', 'date', 'duration'), many=True).data

    def get_projects(self, obj):
        membership = Membership.objects.filter(user=obj).distinct('project')
        return MemberSerializer(membership, fields=('project', 'role'), many=True).data

