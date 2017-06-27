from django.db import models
from django.utils.translation import ugettext_lazy as _
from taiga.projects.issues.models import Issue
from taiga.users.models import User


class Timelog(models.Model):
    issue = models.ForeignKey(Issue, null=False, blank=False, on_delete=models.DO_NOTHING,
                              related_name='timelog_issue', verbose_name=_('issue'))
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.DO_NOTHING,
                             related_name='timelog_user', verbose_name=_('user'))
    date = models.DateField(null=False, blank=False,
                            verbose_name=_('date'))
    duration = models.DecimalField(null=False, blank=False, max_digits=4, decimal_places=2,
                                   verbose_name=_('duration'))
    comment = models.TextField(null=True, blank=True,
                               verbose_name=_('timelog comment'))

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

