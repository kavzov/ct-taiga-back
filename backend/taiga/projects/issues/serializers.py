from taiga.mixins import DynamicFieldsMixin
from taiga.serializers import IssueBaseSerializer


class IssueSerializer(DynamicFieldsMixin, IssueBaseSerializer):
    class Meta(IssueBaseSerializer.Meta):
        fields = IssueBaseSerializer.Meta.fields + (
            'description', 'assigned_to',  'project', 'users',
            'status', 'priority', 'created_date', 'finished_date'
        )
