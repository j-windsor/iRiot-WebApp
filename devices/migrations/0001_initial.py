# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-05 16:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Room')),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function', models.CharField(max_length=30)),
                ('prontohex', models.CharField(max_length=1000)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Device')),
            ],
        ),
    ]