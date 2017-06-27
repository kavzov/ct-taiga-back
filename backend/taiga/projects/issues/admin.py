from django.contrib import admin
from .models import Issue, Priority, Status


admin.site.register(Issue)
admin.site.register(Priority)
admin.site.register(Status)
