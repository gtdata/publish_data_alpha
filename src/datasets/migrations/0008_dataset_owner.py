# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-17 12:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datasets', '0007_remove_dataset_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_datasets', to=settings.AUTH_USER_MODEL),
        ),
    ]
