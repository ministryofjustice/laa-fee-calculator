# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 18:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feetype',
            name='code',
            field=models.CharField(db_index=True, max_length=20),
        ),
    ]
