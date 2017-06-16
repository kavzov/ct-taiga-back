from django.db import models
from markdownx.models import MarkdownxField
from taiga.projects.models import Project
from taiga.users.models import User


class Wiki(models.Model):
    title = models.CharField(max_length = 128)
    content = MarkdownxField()
    project = models.ForeignKey(Project, null=False, blank=False, related_name='wiki_pages', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, related_name='owned_wiki_pages', verbose_name='owner')
    created_date = models.DateTimeField(null=False, blank=False, verbose_name='created_date', auto_now_add=True)
    modified_date = models.DateTimeField(null=True, blank=False, verbose_name='modified_date', auto_now=True)
    last_modifier = models.ForeignKey(User, null=True, blank=True, related_name='last_modified_wiki_pages',
                                      verbose_name='last modifier')
    # attachments = GenericRelation("attachments.Attachment")

    class Meta:
        verbose_name = 'wiki page'
        verbose_name_plural = 'wiki pages'
        ordering = ['project']

    def __str__(self):
        return self.title
