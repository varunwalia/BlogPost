# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-26 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Comments', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AddField(
            model_name='comments',
            name='parent',
            field=models.ForeignKey(blank='True', null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comments'),
        ),
    ]
