from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from taiga.permissions import PERMISSIONS
from taiga.projects.models import Project


class User(User):
    def __str__(self):
        return "{id}. {fname} {lname}".format(id=self.id, fname=self.first_name, lname=self.last_name)

    class Meta:
        ordering = ['id']


class Role(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="name")
    permissions = ArrayField(models.TextField(null=False, blank=False, choices=PERMISSIONS),
                             null=True, blank=True, default=[], verbose_name="permissions")
    project = models.ForeignKey(Project, null=True, blank=False, related_name="roles", verbose_name="project")



# class User(AbstractBaseUser):
#     username = models.CharField(max_length=50)
#     email = models.EmailField(max_length=255, unique=True)
#     is_admin = models.BooleanField(null=False, blank=False, default=False)
#
#     def __str__(self):
#         return "{id}. {name}".format(id=self.id, name=self.username)
#
#     class Meta:
#         verbose_name = "user"
#         verbose_name_plural = "users"
#         ordering = ["id"]
#
#     USERNAME_FIELD = "username"
