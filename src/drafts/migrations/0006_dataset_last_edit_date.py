# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-01 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0005_auto_20161130_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='last_edit_date',
            field=models.DateField(auto_now=True),
        ),
    ]
