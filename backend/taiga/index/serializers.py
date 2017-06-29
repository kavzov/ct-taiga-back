from rest_framework import serializers
from taiga.projects.models import Project, Membership
# from taiga.users.serializers import RoleSerializer
from taiga.projects.issues.serializers import IssueShortSerializer


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = ('user', 'role')


class ProjectSerializer(serializers.ModelSerializer):
    memberships = MembershipSerializer(many=True, read_only=True)
    issues = IssueShortSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner', 'memberships', 'issues')

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance
