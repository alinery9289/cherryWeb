# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='mediafile',
            fields=[
                ('fileid', models.CharField(max_length=32, unique=True, serialize=False, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('authcode', models.CharField(max_length=32)),
                ('filesize', models.BigIntegerField()),
                ('location', models.CharField(max_length=200)),
                ('filetype', models.CharField(max_length=10, null=True, blank=True)),
                ('md5', models.CharField(max_length=45, null=True, blank=True)),
                ('uploadtime', models.DateTimeField()),
                ('encodeinfo', models.CharField(max_length=1200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='processlog',
            fields=[
                ('taskid', models.CharField(max_length=32, unique=True, serialize=False, primary_key=True)),
                ('fileid', models.CharField(max_length=32)),
                ('dealmethod', models.CharField(max_length=45)),
                ('controljson', models.CharField(max_length=1000)),
                ('dealstate', models.CharField(max_length=45)),
                ('afterfileid', models.CharField(max_length=32, null=True, blank=True)),
                ('dealtime', models.DateTimeField()),
                ('completetime', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('authcode', models.CharField(max_length=32, unique=True, serialize=False, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=45)),
                ('userid', models.CharField(unique=True, max_length=16)),
                ('password', models.CharField(max_length=32)),
                ('userstorage', models.BigIntegerField()),
                ('secretkey', models.CharField(max_length=45, unique=True, null=True, blank=True)),
                ('outdate', models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
