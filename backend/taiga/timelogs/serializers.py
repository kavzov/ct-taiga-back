from rest_framework import serializers
from taiga.mixins import DynamicFieldsMixin
from .models import Timelog


class TimelogSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Timelog
        fields = ('id', 'user', 'issue', 'date', 'duration', 'comment')
