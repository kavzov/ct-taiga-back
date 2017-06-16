from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Wiki

admin.site.register(Wiki, MarkdownxModelAdmin)
