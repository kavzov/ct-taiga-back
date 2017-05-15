from django.db import models
from taiga.projects.issues.models import Issue
from taiga.users.models import User


class Timelog(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField()
    duration = models.DecimalField(max_digits=4, decimal_places=2)

    @classmethod
    def decimal_str(self, value):
        return str(value).rstrip('0').rstrip('.')

    def __str__(self):
        verbose = "{issue} - {date} - {user} - {duration}".format(
            issue=self.issue,
            date=self.date,
            user=self.user,
            duration=self.decimal_str(self.duration)
        )
        return verbose

