# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cherryManage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='task',
            fields=[
                ('taskid', models.CharField(max_length=32, unique=True, serialize=False, primary_key=True)),
                ('fatherid', models.CharField(max_length=32, db_index=True)),
                ('afterfileid', models.CharField(max_length=32, null=True, blank=True)),
                ('dealmethod', models.CharField(max_length=45)),
                ('dealstate', models.CharField(max_length=45)),
                ('dealtime', models.DateTimeField()),
                ('completetime', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.RenameField(
            model_name='processlog',
            old_name='taskid',
            new_name='jobid',
        ),
        migrations.RemoveField(
            model_name='processlog',
            name='afterfileid',
        ),
        migrations.RemoveField(
            model_name='processlog',
            name='dealmethod',
        ),
    ]
