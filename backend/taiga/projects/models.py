from django.db import models
from django.utils import timezone
from taiga.users.models import User


class Masquerade(models.Model):
    project = models.ForeignKey('Project', related_name='masquerades', on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, related_name='user')
    masque = models.ForeignKey(User, default=None, related_name='masque')


class Membership(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None, related_name="memberships")
    project = models.ForeignKey("Project", null=False, blank=False, related_name="memberships",
                                on_delete=models.CASCADE)
    role = models.ForeignKey("users.Role", null=True, blank=False, related_name="memberships")


class Project(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)

    created_date = models.DateTimeField(null=False, blank=False, verbose_name="created date", auto_now_add=True)
    modified_date = models.DateTimeField(null=True, blank=False, verbose_name="modified date", auto_now=True)
    owner = models.ForeignKey(User, null=True, blank=True, related_name="owned_projects", verbose_name="owner")
    members = models.ManyToManyField(User, related_name="projects", through="Membership", verbose_name="members",
                                     through_fields=("project", "user"))
    masques = models.ManyToManyField(User, blank=True, through='Masquerade', through_fields=('project', 'user'),
                                     related_name='masque_projects', verbose_name='masques')

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ["id"]
