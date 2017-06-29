from rest_framework import serializers
from .models import Issue


class IssueShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'subject')


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'subject', 'description', 'assigned_to', 'project',
                  'users', 'status', 'priority', 'created_date', 'finished_date')