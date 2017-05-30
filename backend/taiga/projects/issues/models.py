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
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=16, choices=STATUSES, default='new')
    # created_date = models.DateTimeField(null=False, blank=False, verbose_name="created date", default=timezone.now)
    # modified_date = models.DateTimeField(null=False, blank=False, verbose_name="modified date")
    # finished_date = models.DateTimeField(null=True, blank=True, verbose_name="finished date")

    def __str__(self):
        return "{}".format(self.subject)

    class Meta:
        verbose_name = "issue"
        verbose_name_plural = "issues"
        ordering = ["id"]

