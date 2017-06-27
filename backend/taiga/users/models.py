from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from taiga.permissions import PERMISSIONS


class User(User):
    managing = JSONField(default=[])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.get_full_name()


class Report(models.Model):
    user = models.ForeignKey(User, null=False, blank=False,
                             related_name='reports', verbose_name=_('user report'))
    date = models.DateTimeField(null=False, blank=False, auto_now_add=True,
                                verbose_name=_('date'))
    description = models.TextField(null=False, blank=False,
                                   verbose_name=_('description'))


class Role(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False,
                            verbose_name=_('role_name'))
    permissions = ArrayField(models.TextField(null=False, blank=False, choices=PERMISSIONS),
                             null=True, blank=True, default=[], verbose_name=_('permissions'))

    def __str__(self):
        return self.name


class Test(models.Model):
    user = models.IntegerField()
    mngr = JSONField(default=[])

    def get_managing_users(manager_id, project_id):
        """
        Returns users list of manager (user_id) at the project (project_id)
        """
        qs = Test.objects.filter(user=manager_id).filter(mngr__contains=[{'project': project_id}])
        for d in qs[0].mngr:
            if d['project'] == project_id:
                return d['users']

    def rm_managing(manager_id, project_id):
        """
        Remove dict with project_id from manager list of user_id
        """
        managings = Test.objects.get(pk=manager_id)
        for managing in managings:
            if managing['project'] == project_id:
                managings.remove(managing)
                return managings

    def add_managing(manager_id, project_id, users):
        pass

    def add_user_to_managing(manager_id, project_id, user_id):
        pass
