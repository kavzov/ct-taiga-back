# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-26 13:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0013_auto_20170626_1139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issue',
            options={'ordering': ['created_date', 'subject'], 'verbose_name': 'issue', 'verbose_name_plural': 'issues'},
        ),
    ]
