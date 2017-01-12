# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-11 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0004_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='countries',
        ),
        migrations.AddField(
            model_name='dataset',
            name='location',
            field=models.TextField(default=''),
        ),
    ]
