from django.db import models
from django.utils.translation import ugettext_lazy as _
from taiga.projects.models import Project
from taiga.users.models import User


class Issue(models.Model):
    subject = models.CharField(max_length=200, null=False, blank=False,
                               verbose_name=_('issue subject'))
    description = models.TextField(null=False, blank=True,
                                   verbose_name=_('description'))
    assigned_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,
                                    related_name='assigned_issues', verbose_name=_('assigned_to'))
    users = models.ManyToManyField(User, blank=True,
                                   related_name='issues', verbose_name=_('issue users'))
    project = models.ForeignKey(Project, null=False, blank=False, on_delete=models.CASCADE,
                                related_name='issues', verbose_name=_('project'))
    status = models.ForeignKey('issues.Status', null=True, blank=True,
                               related_name='issues', verbose_name=_('issue status'))
    priority = models.ForeignKey('issues.Priority', null=True, blank=True,
                                 related_name='issues', verbose_name=_('issue priority'))
    created_date = models.DateTimeField(null=False, blank=False, auto_now_add=True,
                                        verbose_name=_('created date'))
    modified_date = models.DateTimeField(null=True, blank=False, auto_now=True,
                                         verbose_name=_('modified date'))
    finished_date = models.DateTimeField(null=True, blank=True,
                                         verbose_name=_('finished date'))

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'issue'
        verbose_name_plural = 'issues'
        ordering = ['created_date', 'subject']


class Priority(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False,
                            verbose_name=_('name'))
    order = models.IntegerField(default=10, null=False, blank=False,
                                verbose_name=_('order'))

    class Meta:
        verbose_name = 'priority'
        verbose_name_plural = 'priorities'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False,
                            verbose_name=_('name'))
    order = models.IntegerField(default=10, null=False, blank=False,
                                verbose_name=_('order'))

    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'statuses'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
