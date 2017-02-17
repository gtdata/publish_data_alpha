# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-15 13:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0005_dataset_is_harvested'),
    ]

    operations = [
        migrations.CreateModel(
            name='InspireDataset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bbox_east_long', models.CharField(blank=True, max_length=64, null=True)),
                ('bbox_west_long', models.CharField(blank=True, max_length=64, null=True)),
                ('bbox_north_lat', models.CharField(blank=True, max_length=64, null=True)),
                ('bbox_south_lat', models.CharField(blank=True, max_length=64, null=True)),
                ('coupled_resource', models.TextField(blank=True, null=True)),
                ('dataset_reference_date', models.TextField(blank=True, null=True)),
                ('frequency_of_update', models.CharField(blank=True, max_length=64, null=True)),
                ('guid', models.CharField(blank=True, max_length=128, null=True)),
                ('harvest_object_id', models.TextField(blank=True, null=True)),
                ('harvest_source_reference', models.TextField(blank=True, null=True)),
                ('import_source', models.TextField(blank=True, null=True)),
                ('metadata_date', models.CharField(blank=True, max_length=64, null=True)),
                ('metadata_language', models.CharField(blank=True, max_length=64, null=True)),
                ('provider', models.TextField(blank=True, null=True)),
                ('resource_type', models.CharField(blank=True, max_length=64, null=True)),
                ('responsible_party', models.TextField(blank=True, null=True)),
                ('spatial', models.TextField(blank=True, null=True)),
                ('spatial_data_service_type', models.CharField(blank=True, max_length=64, null=True)),
                ('spatial_reference_system', models.CharField(blank=True, max_length=128, null=True)),
                ('dataset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inspire', to='datasets.Dataset')),
            ],
        ),
    ]