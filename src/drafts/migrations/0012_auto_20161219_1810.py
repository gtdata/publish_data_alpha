# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-19 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0011_dataset_organisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='frequency_weekly_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='frequency_weekly_start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
