from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ["id"]
