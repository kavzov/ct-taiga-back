# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-19 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0005_auto_20170616_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wiki',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_date'),
        ),
    ]
