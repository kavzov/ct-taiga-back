from django.db import models
from django.db.models import ForeignKey
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from markdownx.models import MarkdownxField
from taiga.projects.models import Project
from taiga.users.models import User


class Wiki(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False,
                             verbose_name=_('title'))
    content = MarkdownxField()
    parent = ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                        related_name='wiki_parents')
    project = models.ForeignKey(Project, null=False, blank=False, on_delete=models.CASCADE,
                                related_name='wiki_pages', verbose_name=_('project'))
    owner = models.ForeignKey(User, null=True, blank=True,
                              related_name='owned_wiki_pages', verbose_name='owner')
    created_date = models.DateTimeField(null=True, blank=True, auto_now_add=True,
                                        verbose_name='created_date')
    modified_date = models.DateTimeField(null=True, blank=False, auto_now=True,
                                         verbose_name='modified_date')
    last_modifier = models.ForeignKey(User, null=True, blank=True,
                                      related_name='last_modified_wiki_pages', verbose_name='last_modifier')
    # attachments = GenericRelation("attachments.Attachment")

    class Meta:
        verbose_name = 'wiki page'
        verbose_name_plural = 'wiki pages'
        ordering = ['project']
        permissions = (
            ('view_wiki', 'Can view wiki page'),
        )

    def __str__(self):
        return self.title


class WikiPermissions(models.Model):
    wiki = ForeignKey(Wiki, null=False, blank=False, on_delete=models.CASCADE,
                      related_name='wiki_permissions', verbose_name=_('wiki page'))
    user = ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE,
                      related_name='wiki_permissions', verbose_name=_('user'))
    permissions = ArrayField(models.TextField(null=False, blank=False), null=True, blank=True, default=[],
                             verbose_name='wiki_permissions')
