from rest_framework import serializers
from .models import Issue


class IssueShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'subject')


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class IssueSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'subject', 'description', 'assigned_to', 'project',
                  'users', 'status', 'priority', 'created_date', 'finished_date')

    # TODO make func like at http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
    # for dynamically fields setting and remove ...ShortSerializer classes

