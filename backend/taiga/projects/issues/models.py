from django.db import models
from django.utils import timezone
from taiga.users.models import User
from taiga.projects.models import Project

class Issue(models.Model):
    STATUSES = (
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('resolved', 'Resolved'),
        ('feedback', 'Feedback'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    )
    subject = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    assigned_to = models.ForeignKey(User, related_name='assigned_issues', on_delete=models.DO_NOTHING)
#   users = models.ManyToManyField(User, related_name='issue_users')
    project = models.ForeignKey(Project, related_name='issues', on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=STATUSES, default='new')
    created_date = models.DateTimeField(null=False, blank=False, verbose_name="created date", auto_now_add=True)
    modified_date = models.DateTimeField(null=False, blank=False, verbose_name="modified date", auto_now=True)
    finished_date = models.DateTimeField(null=True, blank=True, verbose_name="finished date")

    def __str__(self):
        return "{}".format(self.subject)

    class Meta:
        verbose_name = "issue"
        verbose_name_plural = "issues"
        ordering = ["id"]

