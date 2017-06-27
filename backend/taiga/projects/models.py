from django.db import models
from django.utils.translation import ugettext_lazy as _
from taiga.users.models import User


class Masquerade(models.Model):
    project = models.ForeignKey('Project', null=False, blank=False, on_delete=models.CASCADE,
                                related_name='masquerades')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='user')
    masque = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='masque')


class Membership(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None, related_name='memberships')
    project = models.ForeignKey("Project", null=False, blank=False, related_name='memberships',
                                on_delete=models.CASCADE)
    role = models.ForeignKey("users.Role", null=True, blank=False, related_name='memberships')


class Project(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False,
                            verbose_name=_('name'))
    description = models.TextField(null=False, blank=False,
                                   verbose_name=_('description'))
    created_date = models.DateTimeField(null=False, blank=False, auto_now_add=True,
                                        verbose_name=_('created date'))
    modified_date = models.DateTimeField(null=True, blank=False, auto_now=True,
                                         verbose_name=_('modified date'))
    owner = models.ForeignKey(User, null=True, blank=True, related_name='owned_projects',
                              verbose_name='owner')
    members = models.ManyToManyField(User, through='Membership', through_fields=('project', 'user'),
                                     related_name='projects', verbose_name=_('members'))
    masques = models.ManyToManyField(User, blank=True, through='Masquerade', through_fields=('project', 'user'),
                                     related_name='masque_projects', verbose_name=_('masques'))

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'
        ordering = ['name', 'id']

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Project {0}'.format(self.id)
