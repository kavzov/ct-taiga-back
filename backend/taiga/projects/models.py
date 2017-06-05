from django.db import models
from django.utils import timezone
from taiga.users.models import User


class Membership(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None, related_name="memberships")
    project = models.ForeignKey("Project", null=False, blank=False, related_name="memberships")
    role = models.ForeignKey("users.Role", null=False, blank=False, related_name="memberships")
    # is_admin = models.BooleanField(default=False, null=False, blank=False)


class Project(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)

    created_date = models.DateTimeField(null=False, blank=False, verbose_name="created date",
                                        default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False, verbose_name="modified date",
                                        default=timezone.now)
    owner = models.ForeignKey(User, null=True, blank=True, related_name="owned_projects", verbose_name="owner")
    members = models.ManyToManyField(User, related_name="projects", through="Membership", verbose_name="members",
                                     through_fields=("project", "user"))

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ["id"]


