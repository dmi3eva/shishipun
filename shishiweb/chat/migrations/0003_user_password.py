# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20171116_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.TextField(default=1234),
            preserve_default=False,
        ),
    ]
