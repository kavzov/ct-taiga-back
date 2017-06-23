from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from taiga.permissions import PERMISSIONS


class User(User):
    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['id']


class Role(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name='role_name')
    permissions = ArrayField(models.TextField(null=False, blank=False, choices=PERMISSIONS),
                             null=True, blank=True, default=[], verbose_name='permissions')
    # project = models.ForeignKey(Project, null=True, blank=False, related_name="roles", verbose_name="project")

    def __str__(self):
        return self.name
