# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-22 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20161019_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='function',
            name='sendhex',
            field=models.CharField(default=(1, 2, 3), max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='function',
            name='prontohex',
            field=models.CharField(max_length=2000),
        ),
    ]
